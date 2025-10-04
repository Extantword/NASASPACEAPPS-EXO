"""
Startup script that pre-downloads popular datasets when the server starts
"""
import asyncio
import logging
from typing import List
from pathlib import Path

from app.etl.extract import data_extractor
from app.config import settings

logger = logging.getLogger(__name__)


class DataStartupService:
    """Service to pre-load popular datasets at startup"""
    
    def __init__(self):
        self.startup_complete = False
        self.popular_targets = [
            # Famous exoplanets for TESS
            "TOI-715 b",
            "TOI-849 b", 
            "WASP-96 b",
            "HD 209458 b",
            "TRAPPIST-1",
            "Kepler-442 b",
            "K2-18 b",
            "55 Cancri e",
            "GJ 1214 b",
            "HAT-P-7 b",
            
            # Famous Kepler targets
            "Kepler-186 f",
            "Kepler-452 b", 
            "Kepler-22 b",
            "Kepler-62 f",
            "Kepler-438 b",
            "Kepler-1649 c",
            "KOI-5715.01",
            "KIC 8462852",  # Tabby's Star
            "Kepler-16 b",
            "Kepler-90 h"
        ]
    
    async def initialize_data(self) -> bool:
        """Initialize popular datasets at startup"""
        try:
            logger.info("Starting data initialization...")
            
            # Start tasks concurrently
            tasks = [
                self._download_exoplanet_catalog(),
                self._download_popular_lightcurves(),
                self._create_mission_summaries()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check for any failures
            failed_tasks = [r for r in results if isinstance(r, Exception)]
            if failed_tasks:
                logger.warning(f"Some initialization tasks failed: {failed_tasks}")
            
            # Mark as complete even if some tasks failed
            self.startup_complete = True
            logger.info("Data initialization completed")
            
            return len(failed_tasks) == 0
            
        except Exception as e:
            logger.error(f"Critical error during data initialization: {str(e)}")
            self.startup_complete = True  # Don't block startup
            return False
    
    async def _download_exoplanet_catalog(self):
        """Download the main exoplanet catalog"""
        try:
            catalog_path = await data_extractor.extract_exoplanet_catalog(force_refresh=False)
            logger.info(f"Exoplanet catalog ready: {catalog_path}")
            return catalog_path
        except Exception as e:
            logger.error(f"Failed to download exoplanet catalog: {str(e)}")
            raise
    
    async def _download_popular_lightcurves(self):
        """Download light curves for popular targets"""
        try:
            # Split targets between missions
            tess_targets = [t for t in self.popular_targets if any(x in t for x in ["TOI", "WASP", "HD", "TRAPPIST", "GJ", "HAT"])]
            kepler_targets = [t for t in self.popular_targets if any(x in t for x in ["Kepler", "KOI", "KIC"])]
            
            # Download TESS light curves
            if tess_targets:
                tess_results = await data_extractor.extract_popular_lightcurves(
                    targets=tess_targets[:10],  # Limit to avoid long startup
                    mission="TESS"
                )
                logger.info(f"Downloaded {len(tess_results)} TESS light curves")
            
            # Download Kepler light curves  
            if kepler_targets:
                kepler_results = await data_extractor.extract_popular_lightcurves(
                    targets=kepler_targets[:10],  # Limit to avoid long startup
                    mission="Kepler"
                )
                logger.info(f"Downloaded {len(kepler_results)} Kepler light curves")
            
        except Exception as e:
            logger.error(f"Failed to download popular light curves: {str(e)}")
            raise
    
    async def _create_mission_summaries(self):
        """Create summaries for each mission"""
        try:
            missions = ["Kepler", "TESS", "K2"]
            
            tasks = [
                data_extractor.extract_mission_summary(mission) 
                for mission in missions
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful = [r for r in results if not isinstance(r, Exception)]
            logger.info(f"Created {len(successful)} mission summaries")
            
        except Exception as e:
            logger.error(f"Failed to create mission summaries: {str(e)}")
            raise
    
    def is_ready(self) -> bool:
        """Check if data initialization is complete"""
        return self.startup_complete
    
    async def get_initialization_status(self) -> dict:
        """Get detailed status of data initialization"""
        data_dir = Path("data")
        
        status = {
            "startup_complete": self.startup_complete,
            "catalog_exists": (data_dir / "processed" / "exoplanets_catalog.csv").exists(),
            "tess_lightcurves": len(list((data_dir / "raw" / "tess").glob("*.csv"))) if (data_dir / "raw" / "tess").exists() else 0,
            "kepler_lightcurves": len(list((data_dir / "raw" / "kepler").glob("*.csv"))) if (data_dir / "raw" / "kepler").exists() else 0,
            "mission_summaries": len(list((data_dir / "processed").glob("*_summary.json"))) if (data_dir / "processed").exists() else 0
        }
        
        return status
    
    async def force_refresh_all(self) -> bool:
        """Force refresh all cached data"""
        try:
            logger.info("Force refreshing all cached data...")
            
            # Clear startup flag to allow re-initialization
            self.startup_complete = False
            
            # Re-download with force refresh
            catalog_path = await data_extractor.extract_exoplanet_catalog(force_refresh=True)
            
            # Re-download popular light curves
            await self._download_popular_lightcurves()
            
            # Recreate mission summaries
            await self._create_mission_summaries()
            
            self.startup_complete = True
            logger.info("Force refresh completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Force refresh failed: {str(e)}")
            self.startup_complete = True
            return False


# Global startup service instance
startup_service = DataStartupService()


async def initialize_startup_data():
    """Convenience function to initialize data at startup"""
    return await startup_service.initialize_data()


async def get_data_status():
    """Convenience function to get data status"""
    return await startup_service.get_initialization_status()