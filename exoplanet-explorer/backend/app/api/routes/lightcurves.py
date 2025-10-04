"""
API routes for light curves
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.schemas import LightCurveResponse
from app.services.lightkurve_service import lightkurve_service

router = APIRouter()


@router.get("/{star_id}", response_model=LightCurveResponse)
async def get_lightcurve(
    star_id: str,
    mission: Optional[str] = Query("TESS", description="Mission (TESS, Kepler, K2)"),
    normalize: bool = Query(True, description="Whether to normalize the flux"),
    remove_outliers: bool = Query(True, description="Whether to remove outliers")
):
    """Get light curve data for a star"""
    try:
        lightcurve_data = await lightkurve_service.download_lightcurve(star_id, mission)
        
        if not lightcurve_data:
            raise HTTPException(status_code=404, detail=f"No light curve data found for star '{star_id}'")
        
        # Apply additional processing if requested
        if not normalize or not remove_outliers:
            # For now, return the processed data as is
            # In a full implementation, you'd apply these filters here
            pass
        
        return LightCurveResponse(**lightcurve_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching light curve: {str(e)}")


@router.get("/{star_id}/download")
async def download_lightcurve_csv(
    star_id: str,
    mission: Optional[str] = Query("TESS", description="Mission (TESS, Kepler, K2)")
):
    """Download light curve data as CSV"""
    try:
        from fastapi.responses import StreamingResponse
        import io
        import csv
        
        lightcurve_data = await lightkurve_service.download_lightcurve(star_id, mission)
        
        if not lightcurve_data:
            raise HTTPException(status_code=404, detail=f"No light curve data found for star '{star_id}'")
        
        # Create CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        headers = ["time", "flux"]
        if lightcurve_data["data"].get("flux_err"):
            headers.append("flux_err")
        writer.writerow(headers)
        
        # Write data
        time_data = lightcurve_data["data"]["time"]
        flux_data = lightcurve_data["data"]["flux"]
        flux_err_data = lightcurve_data["data"].get("flux_err")
        
        for i in range(len(time_data)):
            row = [time_data[i], flux_data[i]]
            if flux_err_data:
                row.append(flux_err_data[i])
            writer.writerow(row)
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={star_id}_lightcurve.csv"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading light curve: {str(e)}")


@router.get("/{star_id}/metadata")
async def get_lightcurve_metadata(
    star_id: str,
    mission: Optional[str] = Query("TESS", description="Mission (TESS, Kepler, K2)")
):
    """Get light curve metadata"""
    try:
        lightcurve_data = await lightkurve_service.download_lightcurve(star_id, mission)
        
        if not lightcurve_data:
            raise HTTPException(status_code=404, detail=f"No light curve data found for star '{star_id}'")
        
        return {
            "star_id": lightcurve_data["star_id"],
            "star_name": lightcurve_data["star_name"],
            "mission": lightcurve_data["mission"],
            "metadata": lightcurve_data["metadata"],
            "data_info": {
                "total_points": len(lightcurve_data["data"]["time"]),
                "cadence": lightcurve_data["data"]["cadence"],
                "time_range": {
                    "start": min(lightcurve_data["data"]["time"]) if lightcurve_data["data"]["time"] else None,
                    "end": max(lightcurve_data["data"]["time"]) if lightcurve_data["data"]["time"] else None
                },
                "flux_range": {
                    "min": min(lightcurve_data["data"]["flux"]) if lightcurve_data["data"]["flux"] else None,
                    "max": max(lightcurve_data["data"]["flux"]) if lightcurve_data["data"]["flux"] else None
                }
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching light curve metadata: {str(e)}")