"""
NASA Exoplanet Archive service for fetching exoplanet data
"""
import asyncio
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from cachetools import TTLCache
from datetime import datetime, timedelta

# Import astroquery for real NASA data access
try:
    from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
    ASTROQUERY_AVAILABLE = True
except ImportError:
    ASTROQUERY_AVAILABLE = False
    logging.warning("astroquery not available, using mock data")

from app.config import settings

logger = logging.getLogger(__name__)


class NASAExoplanetService:
    """Service for interacting with NASA Exoplanet Archive"""
    
    def __init__(self):
        # Cache with 1 hour TTL
        self.cache = TTLCache(maxsize=100, ttl=3600)
        self.last_update = None
        
    async def _query_nasa_archive(self, table: str, columns: str = "*", where: str = None) -> pd.DataFrame:
        """Query NASA Exoplanet Archive using astroquery"""
        cache_key = f"{table}_{columns}_{where}"
        
        if cache_key in self.cache:
            logger.info("Returning cached NASA archive result")
            return self.cache[cache_key]
        
        if not ASTROQUERY_AVAILABLE:
            logger.warning("Astroquery not available, returning mock data")
            return await self._get_mock_data(table)
        
        try:
            loop = asyncio.get_event_loop()
            
            # Run astroquery in executor to avoid blocking
            if where:
                result = await loop.run_in_executor(
                    None,
                    lambda: NasaExoplanetArchive.query_criteria(
                        table=table,
                        select=columns,
                        where=where
                    )
                )
            else:
                result = await loop.run_in_executor(
                    None,
                    lambda: NasaExoplanetArchive.query_criteria(
                        table=table,
                        select=columns
                    )
                )
            
            # Convert to pandas DataFrame
            df = result.to_pandas()
            
            # Cache the result
            self.cache[cache_key] = df
            self.last_update = datetime.now()
            
            logger.info(f"Retrieved {len(df)} records from NASA Exoplanet Archive")
            return df
            
        except Exception as e:
            logger.error(f"Error querying NASA Exoplanet Archive: {str(e)}")
            # Fallback to mock data
            return await self._get_mock_data(table)
    
    async def get_missions(self) -> List[Dict[str, Any]]:
        """Get available missions/facilities from real NASA data"""
        try:
            # Query for discovery facilities
            df = await self._query_nasa_archive(
                table="ps",
                columns="disc_facility",
                where="disc_facility IS NOT NULL"
            )
            
            # Count planets per facility
            facility_counts = df['disc_facility'].value_counts()
            
            missions = []
            mission_info = {
                'Kepler': {
                    'description': 'NASA\'s first planet-hunting mission, operational 2009-2013',
                    'launch_date': '2009-03-07',
                    'active': False
                },
                'TESS': {
                    'description': 'Transiting Exoplanet Survey Satellite, launched 2018',
                    'launch_date': '2018-04-18',
                    'active': True
                },
                'K2': {
                    'description': 'Extended Kepler mission, operational 2014-2018',
                    'launch_date': '2014-05-30',
                    'active': False
                }
            }
            
            for facility, count in facility_counts.head(10).items():
                mission_name = self._map_facility_to_mission(facility)
                mission_data = mission_info.get(mission_name, {
                    'description': f'{facility} exoplanet survey',
                    'launch_date': None,
                    'active': False
                })
                
                missions.append({
                    'name': mission_name,
                    'facility': facility,
                    'total_objects': int(count),
                    'description': mission_data['description'],
                    'active': mission_data['active'],
                    'launch_date': mission_data['launch_date']
                })
            
            return missions
            
        except Exception as e:
            logger.error(f"Error getting missions: {str(e)}")
            return await self._get_mock_missions()
    
    async def search_planets(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Search for exoplanets with filters using real NASA data"""
        try:
            # Build WHERE clause for NASA archive query
            conditions = []
            
            # Basic filters
            conditions.append("pl_name IS NOT NULL")
            conditions.append("default_flag = 1")  # Get only default parameters
            
            if filters.get("mission"):
                facility = self._map_mission_to_facility(filters["mission"])
                if facility:
                    conditions.append(f"disc_facility LIKE '%{facility}%'")
            
            if filters.get("min_period"):
                conditions.append(f"pl_orbper >= {filters['min_period']}")
            
            if filters.get("max_period"):
                conditions.append(f"pl_orbper <= {filters['max_period']}")
            
            if filters.get("min_radius"):
                conditions.append(f"pl_rade >= {filters['min_radius']}")
            
            if filters.get("max_radius"):
                conditions.append(f"pl_rade <= {filters['max_radius']}")
            
            where_clause = " AND ".join(conditions)
            
            # Query NASA archive
            df = await self._query_nasa_archive(
                table="ps",
                columns="pl_name,hostname,pl_orbper,pl_rade,pl_masse,pl_eqt,discoverymethod,disc_year,disc_facility,st_rad,st_mass,st_teff",
                where=where_clause
            )
            
            # Apply limit and offset
            limit = min(filters.get("limit", 50), 500)
            offset = filters.get("offset", 0)
            
            total_count = len(df)
            df_page = df.iloc[offset:offset+limit]
            
            planets = []
            for _, row in df_page.iterrows():
                planet = {
                    "id": str(hash(str(row['pl_name']))) if pd.notna(row['pl_name']) else "",
                    "name": str(row['pl_name']) if pd.notna(row['pl_name']) else "",
                    "host_star": str(row['hostname']) if pd.notna(row['hostname']) else "",
                    "disposition": "CONFIRMED",
                    "period": float(row['pl_orbper']) if pd.notna(row['pl_orbper']) else None,
                    "radius": float(row['pl_rade']) if pd.notna(row['pl_rade']) else None,
                    "mass": float(row['pl_masse']) if pd.notna(row['pl_masse']) else None,
                    "temperature": float(row['pl_eqt']) if pd.notna(row['pl_eqt']) else None,
                    "discovery_method": str(row['discoverymethod']) if pd.notna(row['discoverymethod']) else None,
                    "discovery_year": int(row['disc_year']) if pd.notna(row['disc_year']) else None,
                    "mission": self._map_facility_to_mission(row['disc_facility']) if pd.notna(row['disc_facility']) else ""
                }
                planets.append(planet)
            
            return {
                "planets": planets,
                "total": total_count,
                "page": (offset // limit) + 1,
                "per_page": limit
            }
            
        except Exception as e:
            logger.error(f"Error searching planets: {str(e)}")
            return await self._get_mock_planets(filters)
    
    async def get_planet_statistics(self) -> Dict[str, Any]:
        """Get comprehensive planet statistics from real NASA data"""
        try:
            df = await self._query_nasa_archive(
                table="ps",
                columns="pl_name,discoverymethod,disc_year,disc_facility",
                where="default_flag = 1 AND pl_name IS NOT NULL"
            )
            
            total = len(df)
            
            # By mission/facility
            by_mission = {}
            for facility in df['disc_facility'].dropna():
                mission = self._map_facility_to_mission(facility)
                by_mission[mission] = by_mission.get(mission, 0) + 1
            
            # By discovery method
            by_method = df['discoverymethod'].value_counts().head(10).to_dict()
            
            # By discovery year
            by_year = df['disc_year'].dropna().value_counts().sort_index().to_dict()
            by_year = {str(int(k)): int(v) for k, v in by_year.items()}
            
            return {
                "total": total,
                "by_mission": by_mission,
                "by_method": by_method,
                "by_year": by_year,
                "last_updated": self.last_update.isoformat() if self.last_update else None
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {
                "total": 0,
                "by_mission": {},
                "by_method": {},
                "by_year": {},
                "error": str(e)
            }
    
    def _map_facility_to_mission(self, facility: str) -> str:
        """Map facility name to mission name"""
        if not facility:
            return "Unknown"
            
        facility_lower = str(facility).lower()
        if "kepler" in facility_lower:
            return "Kepler"
        elif "tess" in facility_lower:
            return "TESS"
        elif "k2" in facility_lower:
            return "K2"
        elif "corot" in facility_lower:
            return "CoRoT"
        elif "hat" in facility_lower:
            return "HAT"
        elif "wasp" in facility_lower:
            return "WASP"
        elif "kelt" in facility_lower:
            return "KELT"
        else:
            return facility[:20]  # Truncate long facility names
    
    def _map_mission_to_facility(self, mission: str) -> Optional[str]:
        """Map mission name to facility name for queries"""
        mission_mapping = {
            "kepler": "Kepler",
            "tess": "TESS",
            "k2": "K2",
            "corot": "CoRoT"
        }
        return mission_mapping.get(mission.lower())
    
    async def _get_mock_data(self, table: str) -> pd.DataFrame:
        """Fallback mock data when astroquery is not available"""
        if table == "ps":
            # Create mock exoplanet data
            mock_data = []
            for i in range(100):
                mock_data.append({
                    'pl_name': f'Mock Planet {i+1}',
                    'hostname': f'Mock Star {i+1}',
                    'disc_facility': ['Kepler', 'TESS', 'K2'][i % 3],
                    'pl_orbper': np.random.lognormal(1, 1),
                    'pl_rade': np.random.lognormal(0, 0.5),
                    'pl_masse': np.random.lognormal(0, 0.8),
                    'pl_eqt': np.random.normal(500, 200),
                    'discoverymethod': 'Transit',
                    'disc_year': np.random.randint(2009, 2024),
                    'st_rad': np.random.normal(1, 0.3),
                    'st_mass': np.random.normal(1, 0.2),
                    'st_teff': np.random.normal(5800, 500)
                })
            return pd.DataFrame(mock_data)
        return pd.DataFrame()
    
    async def _get_mock_missions(self) -> List[Dict[str, Any]]:
        """Mock missions data"""
        return [
            {
                'name': 'Kepler',
                'facility': 'Kepler',
                'total_objects': 2600,
                'description': 'NASA\'s first planet-hunting mission',
                'active': False,
                'launch_date': '2009-03-07'
            },
            {
                'name': 'TESS',
                'facility': 'TESS',
                'total_objects': 7000,
                'description': 'Transiting Exoplanet Survey Satellite',
                'active': True,
                'launch_date': '2018-04-18'
            }
        ]
    
    async def _get_mock_planets(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Mock planets search result"""
        mock_planets = []
        limit = filters.get("limit", 50)
        
        for i in range(limit):
            mock_planets.append({
                "id": f"mock_{i}",
                "name": f"Mock Planet {i+1}",
                "host_star": f"Mock Star {i+1}",
                "disposition": "CONFIRMED",
                "period": np.random.lognormal(1, 1),
                "radius": np.random.lognormal(0, 0.5),
                "mass": np.random.lognormal(0, 0.8),
                "temperature": np.random.normal(500, 200),
                "discovery_method": "Transit",
                "discovery_year": np.random.randint(2009, 2024),
                "mission": ["Kepler", "TESS", "K2"][i % 3]
            })
        
        return {
            "planets": mock_planets,
            "total": limit,
            "page": 1,
            "per_page": limit
        }


# Global service instance
nasa_service = NASAExoplanetService()