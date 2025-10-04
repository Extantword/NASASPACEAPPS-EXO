"""
API routes for planets
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional

from app.models.schemas import PlanetResponse, PlanetFilter
from app.services.nasa_service import nasa_service

router = APIRouter()


@router.get("/", response_model=PlanetResponse)
async def get_planets(
    mission: Optional[str] = Query(None, description="Mission filter"),
    disposition: Optional[str] = Query(None, description="Planet disposition"),
    min_period: Optional[float] = Query(None, ge=0, description="Minimum orbital period (days)"),
    max_period: Optional[float] = Query(None, ge=0, description="Maximum orbital period (days)"),
    min_radius: Optional[float] = Query(None, ge=0, description="Minimum planet radius (Earth radii)"),
    max_radius: Optional[float] = Query(None, ge=0, description="Maximum planet radius (Earth radii)"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Result offset for pagination")
):
    """Get list of exoplanets with optional filters"""
    try:
        filters = {
            "mission": mission,
            "disposition": disposition,
            "min_period": min_period,
            "max_period": max_period,
            "min_radius": min_radius,
            "max_radius": max_radius,
            "limit": limit,
            "offset": offset
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = await nasa_service.search_planets(filters)
        
        return PlanetResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching planets: {str(e)}")


@router.get("/{planet_id}")
async def get_planet_details(planet_id: str):
    """Get details for a specific planet"""
    try:
        # Search for planet by ID/name
        filters = {"limit": 1000}  # Large limit to search through all
        result = await nasa_service.search_planets(filters)
        
        # Find planet by ID or name
        for planet in result["planets"]:
            if planet["id"] == planet_id or planet["name"].lower() == planet_id.lower():
                return {
                    **planet,
                    "system_info": {
                        "host_star": planet["host_star"],
                        "star_properties": {
                            "mass": None,  # Would need additional query
                            "radius": None,
                            "temperature": None
                        }
                    },
                    "discovery_info": {
                        "method": planet["discovery_method"],
                        "year": planet["discovery_year"],
                        "mission": planet["mission"]
                    }
                }
        
        raise HTTPException(status_code=404, detail=f"Planet '{planet_id}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching planet details: {str(e)}")


@router.get("/stats/overview")
async def get_planet_statistics():
    """Get overview statistics of exoplanets"""
    try:
        # Get all planets (with reasonable limit)
        result = await nasa_service.search_planets({"limit": 5000})
        planets = result["planets"]
        
        if not planets:
            return {"total": 0, "by_mission": {}, "by_method": {}, "by_year": {}}
        
        # Calculate statistics
        total = len(planets)
        
        # By mission
        by_mission = {}
        for planet in planets:
            mission = planet.get("mission", "Unknown")
            by_mission[mission] = by_mission.get(mission, 0) + 1
        
        # By discovery method
        by_method = {}
        for planet in planets:
            method = planet.get("discovery_method", "Unknown")
            by_method[method] = by_method.get(method, 0) + 1
        
        # By discovery year
        by_year = {}
        for planet in planets:
            year = planet.get("discovery_year")
            if year:
                by_year[str(year)] = by_year.get(str(year), 0) + 1
        
        return {
            "total": total,
            "by_mission": by_mission,
            "by_method": by_method,
            "by_year": dict(sorted(by_year.items()))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating statistics: {str(e)}")