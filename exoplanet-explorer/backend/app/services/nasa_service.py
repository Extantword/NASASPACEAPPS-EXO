"""
NASA Exoplanet Archive service for fetching exoplanet data
"""
import httpx
import pandas as pd
import asyncio
from typing import Dict, List, Optional, Any
import logging
from urllib.parse import quote

from app.config import settings

logger = logging.getLogger(__name__)


class NASAExoplanetService:
    """Service for interacting with NASA Exoplanet Archive"""
    
    def __init__(self):
        self.base_url = settings.nasa_exoplanet_api_url
        self.cache = {}
        
    async def _make_request(self, query: str) -> pd.DataFrame:
        """Make async request to NASA Exoplanet Archive"""
        cache_key = f"nasa_{hash(query)}"
        
        if cache_key in self.cache:
            logger.info("Returning cached result")
            return self.cache[cache_key]
        
        params = {
            "query": query,
            "format": "csv"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                # Convert CSV response to DataFrame
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                
                # Cache the result
                self.cache[cache_key] = df
                logger.info(f"Retrieved {len(df)} records from NASA Exoplanet Archive")
                
                return df
                
        except Exception as e:
            logger.error(f"Error fetching data from NASA API: {str(e)}")
            raise
    
    async def get_missions(self) -> List[Dict[str, Any]]:
        """Get available missions/facilities"""
        query = """
        SELECT DISTINCT disc_facility, count(*) as total_planets
        FROM ps 
        WHERE disc_facility IS NOT NULL
        GROUP BY disc_facility
        ORDER BY total_planets DESC
        """
        
        try:
            df = await self._make_request(query)
            missions = []
            
            for _, row in df.iterrows():
                facility = row['disc_facility']
                # Map facility names to common mission names
                mission_name = self._map_facility_to_mission(facility)
                if mission_name:
                    missions.append({
                        "name": mission_name,
                        "facility": facility,
                        "total_objects": int(row['total_planets']),
                        "description": self._get_mission_description(mission_name),
                        "active": mission_name in ["TESS"],
                        "launch_date": self._get_mission_launch_date(mission_name)
                    })
            
            return missions
            
        except Exception as e:
            logger.error(f"Error getting missions: {str(e)}")
            return []
    
    async def search_planets(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Search for exoplanets with filters"""
        conditions = ["pl_name IS NOT NULL"]
        
        if filters.get("mission"):
            mission_facility = self._map_mission_to_facility(filters["mission"])
            if mission_facility:
                conditions.append(f"disc_facility = '{mission_facility}'")
        
        if filters.get("disposition"):
            conditions.append(f"pl_rade IS NOT NULL")  # Basic filter for confirmed planets
        
        if filters.get("min_period"):
            conditions.append(f"pl_orbper >= {filters['min_period']}")
        
        if filters.get("max_period"):
            conditions.append(f"pl_orbper <= {filters['max_period']}")
        
        if filters.get("min_radius"):
            conditions.append(f"pl_rade >= {filters['min_radius']}")
        
        if filters.get("max_radius"):
            conditions.append(f"pl_rade <= {filters['max_radius']}")
        
        where_clause = " AND ".join(conditions)
        limit = min(filters.get("limit", 50), 500)
        offset = filters.get("offset", 0)
        
        query = f"""
        SELECT pl_name, hostname, pl_orbper, pl_rade, pl_masse, 
               pl_eqt, discoverymethod, disc_year, disc_facility,
               st_rad, st_mass, st_teff
        FROM ps 
        WHERE {where_clause}
        ORDER BY disc_year DESC
        LIMIT {limit} OFFSET {offset}
        """
        
        try:
            df = await self._make_request(query)
            
            planets = []
            for _, row in df.iterrows():
                planet = {
                    "id": str(hash(row['pl_name'])) if pd.notna(row['pl_name']) else "",
                    "name": row['pl_name'] if pd.notna(row['pl_name']) else "",
                    "host_star": row['hostname'] if pd.notna(row['hostname']) else "",
                    "disposition": "CONFIRMED",  # NASA archive contains confirmed planets
                    "period": float(row['pl_orbper']) if pd.notna(row['pl_orbper']) else None,
                    "radius": float(row['pl_rade']) if pd.notna(row['pl_rade']) else None,
                    "mass": float(row['pl_masse']) if pd.notna(row['pl_masse']) else None,
                    "temperature": float(row['pl_eqt']) if pd.notna(row['pl_eqt']) else None,
                    "discovery_method": row['discoverymethod'] if pd.notna(row['discoverymethod']) else None,
                    "discovery_year": int(row['disc_year']) if pd.notna(row['disc_year']) else None,
                    "mission": self._map_facility_to_mission(row['disc_facility']) if pd.notna(row['disc_facility']) else ""
                }
                planets.append(planet)
            
            # Get total count for pagination
            count_query = f"""
            SELECT COUNT(*) as total
            FROM ps 
            WHERE {where_clause}
            """
            
            count_df = await self._make_request(count_query)
            total = int(count_df.iloc[0]['total']) if not count_df.empty else len(planets)
            
            return {
                "planets": planets,
                "total": total,
                "page": (offset // limit) + 1,
                "per_page": limit
            }
            
        except Exception as e:
            logger.error(f"Error searching planets: {str(e)}")
            return {"planets": [], "total": 0, "page": 1, "per_page": limit}
    
    def _map_facility_to_mission(self, facility: str) -> Optional[str]:
        """Map facility name to mission name"""
        if not facility:
            return None
            
        facility_lower = facility.lower()
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
        return facility
    
    def _map_mission_to_facility(self, mission: str) -> Optional[str]:
        """Map mission name to facility name"""
        mission_mapping = {
            "kepler": "Kepler",
            "tess": "TESS",
            "k2": "K2"
        }
        return mission_mapping.get(mission.lower())
    
    def _get_mission_description(self, mission: str) -> str:
        """Get mission description"""
        descriptions = {
            "Kepler": "NASA's first planet-hunting mission, operational 2009-2013",
            "TESS": "Transiting Exoplanet Survey Satellite, launched 2018",
            "K2": "Extended Kepler mission, operational 2014-2018",
            "CoRoT": "French space telescope, operational 2006-2014",
            "HAT": "Ground-based Hungarian Automated Telescope network"
        }
        return descriptions.get(mission, f"{mission} exoplanet survey")
    
    def _get_mission_launch_date(self, mission: str) -> Optional[str]:
        """Get mission launch date"""
        launch_dates = {
            "Kepler": "2009-03-07",
            "TESS": "2018-04-18",
            "K2": "2014-05-30",
            "CoRoT": "2006-12-27"
        }
        return launch_dates.get(mission)


# Global service instance
nasa_service = NASAExoplanetService()