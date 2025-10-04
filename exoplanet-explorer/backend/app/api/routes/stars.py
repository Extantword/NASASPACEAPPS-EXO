"""
API routes for stars
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.schemas import StarInfo, StarSearch
from app.services.lightkurve_service import lightkurve_service

router = APIRouter()


@router.get("/search", response_model=List[StarInfo])
async def search_stars(
    query: str = Query(..., description="Search query (TIC, KIC, KOI, or star name)"),
    mission: Optional[str] = Query(None, description="Mission filter (kepler, tess, k2)"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results")
):
    """Search for stars/targets"""
    try:
        targets = await lightkurve_service.search_targets(query, mission)
        
        # Convert to StarInfo models
        star_list = []
        for target in targets[:limit]:
            star_info = StarInfo(
                id=target["id"],
                name=target["name"],
                ra=target.get("ra"),
                dec=target.get("dec"),
                magnitude=target.get("magnitude"),
                mission=target["mission"],
                has_lightcurve=target["has_lightcurve"]
            )
            star_list.append(star_info)
        
        return star_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching stars: {str(e)}")


@router.get("/{star_id}")
async def get_star_details(star_id: str):
    """Get details for a specific star"""
    try:
        # For now, search for the star to get its details
        targets = await lightkurve_service.search_targets(star_id)
        
        if not targets:
            raise HTTPException(status_code=404, detail=f"Star '{star_id}' not found")
        
        # Return the first match
        target = targets[0]
        return {
            "id": target["id"],
            "name": target["name"],
            "ra": target.get("ra"),
            "dec": target.get("dec"),
            "magnitude": target.get("magnitude"),
            "mission": target["mission"],
            "has_lightcurve": target["has_lightcurve"],
            "coordinates": {
                "ra": target.get("ra"),
                "dec": target.get("dec")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching star details: {str(e)}")