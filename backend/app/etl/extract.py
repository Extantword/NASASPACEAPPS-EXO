"""
Data extraction module for downloading datasets from NASA archives
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime
import aiofiles
import json

try:
    from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
    import lightkurve as lk
    ASTRO_LIBS_AVAILABLE = True
except ImportError:
    ASTRO_LIBS_AVAILABLE = False

from app.config import settings

logger = logging.getLogger(__name__)


class DataExtractor:
    """Extract data from NASA archives and MAST"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Create mission-specific directories
        for mission in ["kepler", "tess", "k2"]:
            (self.raw_dir / mission).mkdir(exist_ok=True)
    
    async def extract_exoplanet_catalog(self, force_refresh: bool = False) -> str:
        """Extract complete exoplanet catalog from NASA Exoplanet Archive"""
        catalog_file = self.processed_dir / "exoplanets_catalog.csv"
        metadata_file = self.processed_dir / "catalog_metadata.json"
        
        # Check if we need to refresh
        if not force_refresh and catalog_file.exists():
            # Check if file is less than 24 hours old
            file_age = datetime.now().timestamp() - catalog_file.stat().st_mtime
            if file_age < 86400:  # 24 hours
                logger.info("Using existing catalog (less than 24h old)")
                return str(catalog_file)
        
        logger.info("Downloading complete exoplanet catalog...")
        
        if not ASTRO_LIBS_AVAILABLE:
            logger.warning("Astroquery not available, creating mock catalog")
            await self._create_mock_catalog(catalog_file, metadata_file)
            return str(catalog_file)
        
        try:
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            
            # Download confirmed planets table
            planets_df = await loop.run_in_executor(
                None,
                lambda: NasaExoplanetArchive.query_criteria(
                    table="ps",
                    select="*",
                    where="default_flag = 1"
                ).to_pandas()
            )
            
            # Save to CSV
            async with aiofiles.open(catalog_file, 'w') as f:
                await f.write(planets_df.to_csv(index=False))
            
            # Create metadata
            metadata = {
                "download_date": datetime.now().isoformat(),
                "total_planets": len(planets_df),
                "source": "NASA Exoplanet Archive",
                "table": "ps (Planetary Systems)",
                "columns": list(planets_df.columns),
                "file_size_mb": catalog_file.stat().st_size / (1024 * 1024)
            }
            
            async with aiofiles.open(metadata_file, 'w') as f:
                await f.write(json.dumps(metadata, indent=2))
            
            logger.info(f"Downloaded {len(planets_df)} confirmed exoplanets")
            return str(catalog_file)
            
        except Exception as e:
            logger.error(f"Error downloading catalog: {str(e)}")
            # Create mock catalog as fallback
            await self._create_mock_catalog(catalog_file, metadata_file)
            return str(catalog_file)
    
    async def extract_popular_lightcurves(self, targets: List[str], mission: str = "TESS") -> Dict[str, str]:
        """Extract light curves for popular targets"""
        mission_dir = self.raw_dir / mission.lower()
        results = {}
        
        logger.info(f"Downloading light curves for {len(targets)} targets from {mission}")
        
        if not ASTRO_LIBS_AVAILABLE:
            logger.warning("Lightkurve not available, creating mock light curves")
            for target in targets:
                mock_file = await self._create_mock_lightcurve(target, mission, mission_dir)
                results[target] = mock_file
            return results
        
        # Download light curves concurrently (but limited)
        semaphore = asyncio.Semaphore(3)  # Limit concurrent downloads
        
        async def download_single(target: str):
            async with semaphore:
                try:
                    loop = asyncio.get_event_loop()
                    
                    # Search and download
                    search_result = await loop.run_in_executor(
                        None,
                        lambda: lk.search_lightcurve(target, mission=mission.upper())
                    )
                    
                    if len(search_result) > 0:
                        lc_collection = await loop.run_in_executor(
                            None,
                            lambda: search_result.download_all(quality_bitmask='hardest')
                        )
                        
                        if len(lc_collection) > 0:
                            lc = await loop.run_in_executor(
                                None,
                                lambda: lc_collection.stitch().remove_nans()
                            )
                            
                            # Save as FITS and CSV
                            target_clean = target.replace(" ", "_").replace("-", "_")
                            fits_file = mission_dir / f"{target_clean}_lightcurve.fits"
                            csv_file = mission_dir / f"{target_clean}_lightcurve.csv"
                            
                            # Save FITS
                            await loop.run_in_executor(None, lambda: lc.to_fits(fits_file))
                            
                            # Save CSV
                            lc_data = {
                                'time': lc.time.value,
                                'flux': lc.flux.value,
                                'flux_err': lc.flux_err.value if hasattr(lc, 'flux_err') else None
                            }
                            df = pd.DataFrame(lc_data)
                            await loop.run_in_executor(None, lambda: df.to_csv(csv_file, index=False))
                            
                            results[target] = str(csv_file)
                            logger.info(f"Downloaded light curve for {target}")
                            return
                
                except Exception as e:
                    logger.error(f"Error downloading {target}: {str(e)}")
                
                # Fallback to mock data
                mock_file = await self._create_mock_lightcurve(target, mission, mission_dir)
                results[target] = mock_file
        
        # Execute downloads
        await asyncio.gather(*[download_single(target) for target in targets])
        
        logger.info(f"Completed downloading {len(results)} light curves")
        return results
    
    async def extract_mission_summary(self, mission: str) -> str:
        """Extract summary statistics for a specific mission"""
        summary_file = self.processed_dir / f"{mission.lower()}_summary.json"
        
        logger.info(f"Extracting summary for {mission} mission")
        
        try:
            # Get mission-specific data
            if not ASTRO_LIBS_AVAILABLE:
                summary = await self._create_mock_mission_summary(mission)
            else:
                loop = asyncio.get_event_loop()
                
                # Query for mission-specific planets
                mission_df = await loop.run_in_executor(
                    None,
                    lambda: NasaExoplanetArchive.query_criteria(
                        table="ps",
                        select="pl_name,hostname,pl_orbper,pl_rade,discoverymethod,disc_year",
                        where=f"disc_facility LIKE '%{mission}%' AND default_flag = 1"
                    ).to_pandas()
                )
                
                summary = {
                    "mission": mission,
                    "total_planets": len(mission_df),
                    "discovery_years": mission_df['disc_year'].dropna().value_counts().to_dict(),
                    "discovery_methods": mission_df['discoverymethod'].value_counts().to_dict(),
                    "period_stats": {
                        "min": float(mission_df['pl_orbper'].min()) if not mission_df['pl_orbper'].isna().all() else None,
                        "max": float(mission_df['pl_orbper'].max()) if not mission_df['pl_orbper'].isna().all() else None,
                        "median": float(mission_df['pl_orbper'].median()) if not mission_df['pl_orbper'].isna().all() else None
                    },
                    "radius_stats": {
                        "min": float(mission_df['pl_rade'].min()) if not mission_df['pl_rade'].isna().all() else None,
                        "max": float(mission_df['pl_rade'].max()) if not mission_df['pl_rade'].isna().all() else None,
                        "median": float(mission_df['pl_rade'].median()) if not mission_df['pl_rade'].isna().all() else None
                    },
                    "updated": datetime.now().isoformat()
                }
            
            # Save summary
            async with aiofiles.open(summary_file, 'w') as f:
                await f.write(json.dumps(summary, indent=2))
            
            logger.info(f"Created summary for {mission}: {summary['total_planets']} planets")
            return str(summary_file)
            
        except Exception as e:
            logger.error(f"Error creating {mission} summary: {str(e)}")
            # Create mock summary
            summary = await self._create_mock_mission_summary(mission)
            async with aiofiles.open(summary_file, 'w') as f:
                await f.write(json.dumps(summary, indent=2))
            return str(summary_file)
    
    async def _create_mock_catalog(self, catalog_file: Path, metadata_file: Path):
        """Create mock exoplanet catalog for development"""
        import numpy as np
        
        # Generate mock data
        n_planets = 1000
        mock_data = []
        
        missions = ["Kepler", "TESS", "K2", "CoRoT", "WASP", "HAT"]
        methods = ["Transit", "Radial Velocity", "Microlensing", "Direct Imaging"]
        
        for i in range(n_planets):
            mock_data.append({
                'pl_name': f'Mock Planet {i+1:04d}',
                'hostname': f'Mock Star {i+1:04d}',
                'disc_facility': np.random.choice(missions),
                'discoverymethod': np.random.choice(methods),
                'disc_year': np.random.randint(1995, 2024),
                'pl_orbper': np.random.lognormal(1, 1.5),
                'pl_rade': np.random.lognormal(0, 0.8),
                'pl_masse': np.random.lognormal(0, 1.2),
                'pl_eqt': np.random.normal(500, 300),
                'st_rad': np.random.normal(1, 0.4),
                'st_mass': np.random.normal(1, 0.3),
                'st_teff': np.random.normal(5800, 800)
            })
        
        df = pd.DataFrame(mock_data)
        
        # Save catalog
        df.to_csv(catalog_file, index=False)
        
        # Save metadata
        metadata = {
            "download_date": datetime.now().isoformat(),
            "total_planets": len(df),
            "source": "Mock Data (Development)",
            "table": "mock_ps",
            "columns": list(df.columns),
            "file_size_mb": catalog_file.stat().st_size / (1024 * 1024)
        }
        
        async with aiofiles.open(metadata_file, 'w') as f:
            await f.write(json.dumps(metadata, indent=2))
    
    async def _create_mock_lightcurve(self, target: str, mission: str, mission_dir: Path) -> str:
        """Create mock light curve file"""
        import numpy as np
        
        # Generate realistic mock light curve
        np.random.seed(hash(target) % 2**32)
        
        if mission.upper() == "TESS":
            n_points = 2000
            duration = 27.0
        elif mission.upper() == "KEPLER":
            n_points = 4000
            duration = 90.0
        else:
            n_points = 1500
            duration = 30.0
        
        time = np.linspace(0, duration, n_points)
        flux = np.ones(n_points)
        
        # Add stellar variability and noise
        flux += np.random.normal(0, 0.001, n_points)
        
        # Add transit if target looks like a planet host
        if "TOI" in target or "KOI" in target or np.random.random() < 0.3:
            period = 2 + np.random.exponential(5)
            depth = 0.001 + np.random.exponential(0.005)
            duration_hours = 2 + np.random.exponential(4)
            
            for transit_time in np.arange(period/2, duration, period):
                transit_mask = np.abs(time - transit_time) < duration_hours/24
                flux[transit_mask] -= depth
        
        # Create DataFrame
        df = pd.DataFrame({
            'time': time,
            'flux': flux,
            'flux_err': np.full(n_points, 0.001)
        })
        
        # Save file
        target_clean = target.replace(" ", "_").replace("-", "_")
        csv_file = mission_dir / f"{target_clean}_lightcurve.csv"
        df.to_csv(csv_file, index=False)
        
        return str(csv_file)
    
    async def _create_mock_mission_summary(self, mission: str) -> Dict[str, Any]:
        """Create mock mission summary"""
        import numpy as np
        
        mission_stats = {
            "Kepler": {"total": 2600, "years": range(2009, 2014)},
            "TESS": {"total": 7000, "years": range(2018, 2024)},
            "K2": {"total": 500, "years": range(2014, 2019)}
        }
        
        stats = mission_stats.get(mission, {"total": 1000, "years": range(2009, 2024)})
        
        return {
            "mission": mission,
            "total_planets": stats["total"],
            "discovery_years": {str(year): np.random.randint(50, 500) for year in stats["years"]},
            "discovery_methods": {
                "Transit": int(stats["total"] * 0.8),
                "Radial Velocity": int(stats["total"] * 0.15),
                "Other": int(stats["total"] * 0.05)
            },
            "period_stats": {
                "min": 0.5,
                "max": 500.0,
                "median": 10.0
            },
            "radius_stats": {
                "min": 0.3,
                "max": 20.0,
                "median": 2.0
            },
            "updated": datetime.now().isoformat(),
            "mock_data": True
        }


# Global extractor instance
data_extractor = DataExtractor()