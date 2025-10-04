"""
API routes for missions
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import MissionInfo
from app.services.nasa_service import nasa_service

router = APIRouter()


@router.get("/", response_model=List[MissionInfo])
async def get_missions():
    """Get list of available missions"""
    try:
        missions = await nasa_service.get_missions()
        
        # Convert to MissionInfo models
        mission_list = []
        for mission in missions:
            mission_info = MissionInfo(
                name=mission["name"],
                description=mission["description"],
                active=mission["active"],
                launch_date=mission.get("launch_date"),
                total_objects=mission["total_objects"]
            )
            mission_list.append(mission_info)
        
        return mission_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching missions: {str(e)}")


@router.get("/{mission_name}")
async def get_mission_details(mission_name: str):
    """Get details for a specific mission"""
    try:
        missions = await nasa_service.get_missions()
        
        for mission in missions:
            if mission["name"].lower() == mission_name.lower():
                return mission
        
        raise HTTPException(status_code=404, detail=f"Mission '{mission_name}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching mission details: {str(e)}")