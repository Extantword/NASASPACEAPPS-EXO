"""
Lightkurve service for downloading and processing light curves
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd
from cachetools import TTLCache
from datetime import datetime

# Import lightkurve for real data access
try:
    import lightkurve as lk
    LIGHTKURVE_AVAILABLE = True
except ImportError:
    LIGHTKURVE_AVAILABLE = False
    logging.warning("lightkurve not available, using mock data")

logger = logging.getLogger(__name__)


class LightkurveService:
    """Service for downloading and processing light curves using lightkurve"""
    
    def __init__(self):
        # Cache with 2 hour TTL for light curve data
        self.cache = TTLCache(maxsize=50, ttl=7200)
        self.target_cache = TTLCache(maxsize=200, ttl=3600)
    
    async def search_targets(self, query: str, mission: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for targets (stars) in MAST archive using real lightkurve"""
        cache_key = f"search_{query}_{mission}"
        
        if cache_key in self.target_cache:
            logger.info("Returning cached target search")
            return self.target_cache[cache_key]
        
        if not LIGHTKURVE_AVAILABLE:
            logger.warning("Lightkurve not available, returning mock data")
            return self._get_mock_targets(query, mission)
        
        try:
            # Run lightkurve search in thread to avoid blocking
            loop = asyncio.get_event_loop()
            search_result = await loop.run_in_executor(
                None, 
                self._search_targets_sync, 
                query, mission
            )
            
            targets = []
            if search_result is not None and len(search_result) > 0:
                for i, result in enumerate(search_result[:20]):  # Limit to 20 results
                    try:
                        # Extract target information
                        target_name = getattr(result, 'target_name', f'Target_{i}')
                        mission_name = getattr(result, 'mission', mission or 'Unknown')
                        
                        # Get coordinates if available
                        ra = getattr(result, 'ra', None)
                        dec = getattr(result, 'dec', None)
                        
                        # Try to get magnitude
                        magnitude = None
                        if hasattr(result, 'tmag'):
                            magnitude = float(result.tmag) if result.tmag else None
                        elif hasattr(result, 'kepmag'):
                            magnitude = float(result.kepmag) if result.kepmag else None
                        
                        target_info = {
                            "id": str(target_name),
                            "name": str(target_name),
                            "ra": float(ra) if ra is not None else None,
                            "dec": float(dec) if dec is not None else None,
                            "magnitude": magnitude,
                            "mission": str(mission_name).upper(),
                            "has_lightcurve": True
                        }
                        targets.append(target_info)
                        
                    except Exception as e:
                        logger.warning(f"Error processing target {i}: {str(e)}")
                        continue
            
            # Cache the results
            self.target_cache[cache_key] = targets
            
            logger.info(f"Found {len(targets)} targets for query: {query}")
            return targets
            
        except Exception as e:
            logger.error(f"Error searching targets: {str(e)}")
            # Return mock data as fallback
            return self._get_mock_targets(query, mission)
    
    async def download_lightcurve(self, target_id: str, mission: str = "TESS", 
                                 normalize: bool = True, remove_outliers: bool = True) -> Dict[str, Any]:
        """Download and process light curve data for a target using real lightkurve"""
        cache_key = f"lc_{target_id}_{mission}_{normalize}_{remove_outliers}"
        
        if cache_key in self.cache:
            logger.info("Returning cached light curve")
            return self.cache[cache_key]
        
        if not LIGHTKURVE_AVAILABLE:
            logger.warning("Lightkurve not available, returning mock data")
            return self._get_mock_lightcurve(target_id, mission)
        
        try:
            # Run lightkurve download in thread
            loop = asyncio.get_event_loop()
            lightcurve_data = await loop.run_in_executor(
                None,
                self._download_lightcurve_sync,
                target_id, mission, normalize, remove_outliers
            )
            
            if lightcurve_data is not None:
                # Cache the result
                self.cache[cache_key] = lightcurve_data
                logger.info(f"Downloaded light curve for {target_id}")
                return lightcurve_data
            else:
                # Return mock data if no real data available
                return self._get_mock_lightcurve(target_id, mission)
                
        except Exception as e:
            logger.error(f"Error downloading light curve for {target_id}: {str(e)}")
            # Return mock data for development
            return self._get_mock_lightcurve(target_id, mission)
    
    async def get_lightcurve_metadata(self, target_id: str, mission: str = "TESS") -> Dict[str, Any]:
        """Get comprehensive metadata for a light curve"""
        try:
            lc_data = await self.download_lightcurve(target_id, mission, normalize=False, remove_outliers=False)
            
            if not lc_data or 'data' not in lc_data:
                return {"error": "No light curve data available"}
            
            time_data = lc_data['data']['time']
            flux_data = lc_data['data']['flux']
            
            # Calculate advanced statistics
            metadata = {
                "target_id": target_id,
                "mission": mission,
                "total_points": len(time_data),
                "observation_span_days": max(time_data) - min(time_data) if time_data else 0,
                "cadence": lc_data['data'].get('cadence', 'unknown'),
                "flux_statistics": {
                    "mean": float(np.mean(flux_data)) if flux_data else None,
                    "median": float(np.median(flux_data)) if flux_data else None,
                    "std": float(np.std(flux_data)) if flux_data else None,
                    "min": float(np.min(flux_data)) if flux_data else None,
                    "max": float(np.max(flux_data)) if flux_data else None,
                },
                "time_statistics": {
                    "start": min(time_data) if time_data else None,
                    "end": max(time_data) if time_data else None,
                    "gaps": self._detect_time_gaps(time_data),
                },
                "quality_flags": {
                    "has_quality_flags": lc_data['data'].get('quality') is not None,
                    "flagged_points": 0  # Would calculate from quality array
                }
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error getting metadata for {target_id}: {str(e)}")
            return {"error": str(e)}
    
    def _search_targets_sync(self, query: str, mission: Optional[str] = None):
        """Synchronous target search using lightkurve"""
        try:
            import lightkurve as lk
            
            # Determine mission for search
            search_mission = mission.upper() if mission else "TESS"
            
            # Try different search methods based on query format
            search_result = None
            
            # Try as target pixel file first (more comprehensive)
            try:
                search_result = lk.search_targetpixelfile(query, mission=search_mission)
            except:
                pass
            
            # If no results, try as light curve
            if search_result is None or len(search_result) == 0:
                try:
                    search_result = lk.search_lightcurve(query, mission=search_mission)
                except:
                    pass
            
            # If still no results, try with all missions
            if search_result is None or len(search_result) == 0:
                try:
                    search_result = lk.search_lightcurve(query)
                except:
                    pass
            
            return search_result
            
        except Exception as e:
            logger.error(f"Sync search error: {str(e)}")
            return None
    
    def _download_lightcurve_sync(self, target_id: str, mission: str, 
                                 normalize: bool, remove_outliers: bool) -> Optional[Dict[str, Any]]:
        """Synchronous light curve download and processing"""
        try:
            import lightkurve as lk
            
            # Search for light curves
            search_result = lk.search_lightcurve(target_id, mission=mission.upper())
            
            if len(search_result) == 0:
                logger.warning(f"No light curves found for {target_id} in {mission}")
                return None
            
            # Download all available light curves
            lc_collection = search_result.download_all(quality_bitmask='hardest')
            
            if len(lc_collection) == 0:
                logger.warning(f"Failed to download light curves for {target_id}")
                return None
            
            # Stitch together multiple quarters/sectors
            lc = lc_collection.stitch()
            
            # Apply processing options
            if remove_outliers:
                lc = lc.remove_outliers(sigma=3)
            
            # Remove NaN values
            lc = lc.remove_nans()
            
            if normalize:
                lc = lc.normalize()
            
            # Extract data
            time = lc.time.value
            flux = lc.flux.value
            flux_err = lc.flux_err.value if hasattr(lc, 'flux_err') and lc.flux_err is not None else None
            quality = lc.quality.value if hasattr(lc, 'quality') and lc.quality is not None else None
            
            # Determine cadence
            if len(time) > 1:
                median_cadence = np.median(np.diff(time))
                cadence = "short" if median_cadence < 0.1 else "long"  # < 0.1 days = short cadence
            else:
                cadence = "unknown"
            
            # Build result
            result = {
                "star_id": str(target_id),
                "star_name": str(getattr(lc, 'label', target_id)),
                "mission": mission.upper(),
                "data": {
                    "time": time.tolist(),
                    "flux": flux.tolist(),
                    "flux_err": flux_err.tolist() if flux_err is not None else None,
                    "quality": quality.tolist() if quality is not None else None,
                    "cadence": cadence
                },
                "metadata": {
                    "length": len(time),
                    "duration_days": float(time.max() - time.min()) if len(time) > 0 else 0,
                    "mean_flux": float(np.mean(flux)),
                    "std_flux": float(np.std(flux)),
                    "sectors": getattr(lc, 'sector', None),
                    "campaign": getattr(lc, 'campaign', None),
                    "quarter": getattr(lc, 'quarter', None),
                    "processed": {
                        "normalized": normalize,
                        "outliers_removed": remove_outliers
                    }
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Sync download error: {str(e)}")
            return None
    
    def _detect_time_gaps(self, time_data: List[float]) -> int:
        """Detect significant gaps in time series data"""
        if len(time_data) < 2:
            return 0
        
        time_array = np.array(time_data)
        diffs = np.diff(time_array)
        median_diff = np.median(diffs)
        
        # Count gaps larger than 5x the median cadence
        significant_gaps = np.sum(diffs > 5 * median_diff)
        return int(significant_gaps)
    
    def _get_mock_targets(self, query: str, mission: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate mock target data for development"""
        mock_targets = []
        mission = mission or "TESS"
        
        # Generate based on query
        if "TOI" in query.upper():
            base_id = query.replace("TOI-", "").replace("TOI ", "")
            try:
                toi_num = int(base_id.split()[0]) if base_id else 100
            except:
                toi_num = 100
                
            mock_targets.append({
                "id": f"TIC {123456789 + toi_num}",
                "name": f"TOI-{toi_num}",
                "ra": 45.0 + toi_num * 0.01,
                "dec": -30.0 + toi_num * 0.01,
                "magnitude": 10.5 + (toi_num % 5) * 0.2,
                "mission": mission,
                "has_lightcurve": True
            })
        else:
            # Generate multiple mock results
            for i in range(5):
                mock_targets.append({
                    "id": f"TIC {123456789 + i}",
                    "name": f"Mock-{query}-{i+1}",
                    "ra": 45.0 + i * 0.1,
                    "dec": -30.0 + i * 0.1,
                    "magnitude": 10.5 + i * 0.2,
                    "mission": mission,
                    "has_lightcurve": True
                })
        
        return mock_targets
    
    def _get_mock_lightcurve(self, target_id: str, mission: str) -> Dict[str, Any]:
        """Generate mock light curve data with realistic transit features"""
        # Use target_id as seed for reproducible mock data
        np.random.seed(hash(target_id) % 2**32)
        
        # Parameters based on mission
        if mission.upper() == "TESS":
            n_points = 2000  # TESS 2-minute cadence for ~27 days
            duration_days = 27.0
            cadence = "short"
        elif mission.upper() == "KEPLER":
            n_points = 4000  # Kepler long cadence for ~90 days
            duration_days = 90.0
            cadence = "long"
        else:
            n_points = 1500
            duration_days = 30.0
            cadence = "short"
        
        time = np.linspace(0, duration_days, n_points)
        
        # Base stellar flux with realistic noise
        flux = np.ones(n_points)
        
        # Add stellar variability (red noise)
        variability_amplitude = 0.001 + (hash(target_id) % 100) / 50000
        variability_timescale = 2.0 + (hash(target_id) % 10)
        for i in range(1, 5):
            flux += variability_amplitude * np.sin(2 * np.pi * time / (variability_timescale * i)) / i
        
        # Add white noise
        noise_level = 0.0005 + (hash(target_id) % 50) / 100000
        flux += np.random.normal(0, noise_level, n_points)
        
        # Add periodic transit signal if this looks like a planet host
        if "TOI" in target_id or "KOI" in target_id or hash(target_id) % 3 == 0:
            period = 2.0 + (hash(target_id) % 20)  # 2-22 day period
            transit_depth = 0.002 + (hash(target_id) % 100) / 100000  # 0.2-1% depth
            transit_duration = 0.1 + (hash(target_id) % 50) / 1000  # Transit duration in days
            
            # Add multiple transits
            for transit_time in np.arange(period/2, duration_days, period):
                transit_mask = np.abs(time - transit_time) < transit_duration/2
                flux[transit_mask] -= transit_depth
        
        # Generate quality flags (10% flagged)
        quality = np.zeros(n_points, dtype=int)
        flagged_indices = np.random.choice(n_points, size=int(0.1 * n_points), replace=False)
        quality[flagged_indices] = 1
        
        # Generate flux errors
        flux_err = np.full(n_points, noise_level)
        
        return {
            "star_id": target_id,
            "star_name": f"Mock Star {target_id}",
            "mission": mission.upper(),
            "data": {
                "time": time.tolist(),
                "flux": flux.tolist(),
                "flux_err": flux_err.tolist(),
                "quality": quality.tolist(),
                "cadence": cadence
            },
            "metadata": {
                "length": n_points,
                "duration_days": duration_days,
                "mean_flux": float(np.mean(flux)),
                "std_flux": float(np.std(flux)),
                "mock_data": True,
                "noise_level": noise_level,
                "has_transits": "TOI" in target_id or "KOI" in target_id or hash(target_id) % 3 == 0,
                "processed": {
                    "normalized": True,
                    "outliers_removed": True
                }
            }
        }


# Global service instance
lightkurve_service = LightkurveService()