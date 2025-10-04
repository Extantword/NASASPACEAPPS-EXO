"""
Lightkurve service for downloading and processing light curves
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class LightkurveService:
    """Service for downloading and processing light curves using lightkurve"""
    
    def __init__(self):
        self.cache = {}
    
    async def search_targets(self, query: str, mission: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for targets (stars) in MAST archive"""
        try:
            # Import lightkurve in async context
            import lightkurve as lk
            
            # Run lightkurve search in thread to avoid blocking
            loop = asyncio.get_event_loop()
            search_result = await loop.run_in_executor(
                None, 
                self._search_targets_sync, 
                query, mission
            )
            
            targets = []
            if search_result is not None and len(search_result) > 0:
                for i, target in enumerate(search_result[:20]):  # Limit to 20 results
                    target_info = {
                        "id": str(getattr(target, 'target_name', f'target_{i}')),
                        "name": str(getattr(target, 'target_name', 'Unknown')),
                        "ra": float(getattr(target, 'ra', 0.0)),
                        "dec": float(getattr(target, 'dec', 0.0)),
                        "magnitude": float(getattr(target, 'kmag', 0.0)) if hasattr(target, 'kmag') else None,
                        "mission": str(getattr(target, 'mission', mission or 'Unknown')),
                        "has_lightcurve": True
                    }
                    targets.append(target_info)
            
            logger.info(f"Found {len(targets)} targets for query: {query}")
            return targets
            
        except Exception as e:
            logger.error(f"Error searching targets: {str(e)}")
            # Return mock data for development
            return self._get_mock_targets(query, mission)
    
    async def download_lightcurve(self, target_id: str, mission: str = "TESS") -> Dict[str, Any]:
        """Download light curve data for a target"""
        cache_key = f"lc_{target_id}_{mission}"
        
        if cache_key in self.cache:
            logger.info("Returning cached light curve")
            return self.cache[cache_key]
        
        try:
            # Import lightkurve in async context
            import lightkurve as lk
            
            # Run lightkurve download in thread
            loop = asyncio.get_event_loop()
            lightcurve = await loop.run_in_executor(
                None,
                self._download_lightcurve_sync,
                target_id, mission
            )
            
            if lightcurve is not None:
                # Process and normalize the light curve
                processed_lc = self._process_lightcurve(lightcurve)
                
                # Cache the result
                self.cache[cache_key] = processed_lc
                logger.info(f"Downloaded light curve for {target_id}")
                
                return processed_lc
            else:
                # Return mock data if no real data available
                return self._get_mock_lightcurve(target_id, mission)
                
        except Exception as e:
            logger.error(f"Error downloading light curve for {target_id}: {str(e)}")
            # Return mock data for development
            return self._get_mock_lightcurve(target_id, mission)
    
    def _search_targets_sync(self, query: str, mission: Optional[str] = None):
        """Synchronous target search"""
        try:
            import lightkurve as lk
            
            # Determine mission for search
            search_mission = mission or "TESS"
            
            # Search for targets
            search_result = lk.search_targetpixelfile(
                query, 
                mission=search_mission.upper()
            )
            
            return search_result
            
        except Exception as e:
            logger.error(f"Sync search error: {str(e)}")
            return None
    
    def _download_lightcurve_sync(self, target_id: str, mission: str):
        """Synchronous light curve download"""
        try:
            import lightkurve as lk
            
            # Search for light curves
            search_result = lk.search_lightcurve(
                target_id,
                mission=mission.upper()
            )
            
            if len(search_result) > 0:
                # Download the first available light curve
                lc_collection = search_result.download_all()
                if len(lc_collection) > 0:
                    # Stitch together multiple quarters/sectors
                    lc = lc_collection.stitch()
                    return lc
            
            return None
            
        except Exception as e:
            logger.error(f"Sync download error: {str(e)}")
            return None
    
    def _process_lightcurve(self, lightcurve) -> Dict[str, Any]:
        """Process and clean light curve data"""
        try:
            # Remove NaN values and outliers
            lc_clean = lightcurve.remove_nans().remove_outliers(sigma=3)
            
            # Normalize flux
            lc_normalized = lc_clean.normalize()
            
            # Convert to arrays
            time = lc_normalized.time.value.tolist()
            flux = lc_normalized.flux.value.tolist()
            flux_err = lc_normalized.flux_err.value.tolist() if hasattr(lc_normalized, 'flux_err') else None
            
            return {
                "star_id": str(getattr(lightcurve, 'targetid', 'unknown')),
                "star_name": str(getattr(lightcurve, 'label', 'Unknown Star')),
                "mission": str(getattr(lightcurve, 'mission', 'Unknown')),
                "data": {
                    "time": time,
                    "flux": flux,
                    "flux_err": flux_err,
                    "quality": None,
                    "cadence": "short" if len(time) > 10000 else "long"
                },
                "metadata": {
                    "length": len(time),
                    "duration_days": max(time) - min(time) if time else 0,
                    "mean_flux": float(np.mean(flux)) if flux else 0,
                    "std_flux": float(np.std(flux)) if flux else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing light curve: {str(e)}")
            return self._get_mock_lightcurve("unknown", "Unknown")
    
    def _get_mock_targets(self, query: str, mission: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate mock target data for development"""
        mock_targets = [
            {
                "id": f"TIC {123456789 + i}",
                "name": f"TOI-{100 + i}",
                "ra": 45.0 + i * 0.1,
                "dec": -30.0 + i * 0.1,
                "magnitude": 10.5 + i * 0.2,
                "mission": mission or "TESS",
                "has_lightcurve": True
            }
            for i in range(5)
        ]
        
        # Filter by query if specific
        if query.lower() not in ["", "*"]:
            mock_targets = [t for t in mock_targets if query.lower() in t["name"].lower()]
        
        return mock_targets
    
    def _get_mock_lightcurve(self, target_id: str, mission: str) -> Dict[str, Any]:
        """Generate mock light curve data for development"""
        # Generate synthetic light curve with transit-like features
        np.random.seed(hash(target_id) % 2**32)
        
        n_points = 1000
        time = np.linspace(0, 30, n_points)  # 30 days
        
        # Base stellar flux with noise
        flux = np.ones(n_points) + np.random.normal(0, 0.001, n_points)
        
        # Add periodic transit signal
        period = 3.0 + (hash(target_id) % 10)  # Random period between 3-13 days
        transit_depth = 0.005 + (hash(target_id) % 100) / 100000  # Random depth
        
        for i, t in enumerate(time):
            phase = (t % period) / period
            if 0.48 < phase < 0.52:  # Transit window
                flux[i] -= transit_depth
        
        return {
            "star_id": target_id,
            "star_name": f"Mock Star {target_id}",
            "mission": mission,
            "data": {
                "time": time.tolist(),
                "flux": flux.tolist(),
                "flux_err": (np.ones(n_points) * 0.001).tolist(),
                "quality": None,
                "cadence": "short"
            },
            "metadata": {
                "length": n_points,
                "duration_days": 30.0,
                "mean_flux": float(np.mean(flux)),
                "std_flux": float(np.std(flux)),
                "mock_data": True,
                "period": period,
                "transit_depth": transit_depth
            }
        }


# Global service instance
lightkurve_service = LightkurveService()