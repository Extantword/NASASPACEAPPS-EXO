"""
Pydantic schemas for API request/response models
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class MissionInfo(BaseModel):
    """Mission information model"""
    name: str = Field(..., description="Mission name (e.g., Kepler, TESS, K2)")
    description: str = Field(..., description="Mission description")
    active: bool = Field(..., description="Whether the mission is currently active")
    launch_date: Optional[str] = Field(None, description="Mission launch date")
    total_objects: int = Field(0, description="Total number of objects observed")


class StarSearch(BaseModel):
    """Star search request model"""
    query: str = Field(..., description="Search query (TIC, KIC, KOI, or star name)")
    mission: Optional[str] = Field(None, description="Mission filter (kepler, tess, k2)")
    limit: int = Field(20, ge=1, le=100, description="Maximum number of results")


class StarInfo(BaseModel):
    """Star information model"""
    id: str = Field(..., description="Star identifier")
    name: str = Field(..., description="Star name")
    ra: Optional[float] = Field(None, description="Right ascension")
    dec: Optional[float] = Field(None, description="Declination")
    magnitude: Optional[float] = Field(None, description="Visual magnitude")
    mission: str = Field(..., description="Observing mission")
    has_lightcurve: bool = Field(False, description="Whether lightcurve data is available")


class LightCurveData(BaseModel):
    """Light curve data model"""
    time: List[float] = Field(..., description="Time values")
    flux: List[float] = Field(..., description="Flux values")
    flux_err: Optional[List[float]] = Field(None, description="Flux error values")
    quality: Optional[List[int]] = Field(None, description="Quality flags")
    cadence: str = Field(..., description="Data cadence (short/long)")


class LightCurveResponse(BaseModel):
    """Light curve response model"""
    star_id: str = Field(..., description="Star identifier")
    star_name: str = Field(..., description="Star name")
    mission: str = Field(..., description="Mission name")
    data: LightCurveData = Field(..., description="Light curve data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class PlanetFilter(BaseModel):
    """Planet search filter model"""
    mission: Optional[str] = Field(None, description="Mission filter")
    disposition: Optional[str] = Field(None, description="Planet disposition (CONFIRMED, CANDIDATE, FALSE POSITIVE)")
    min_period: Optional[float] = Field(None, ge=0, description="Minimum orbital period (days)")
    max_period: Optional[float] = Field(None, ge=0, description="Maximum orbital period (days)")
    min_radius: Optional[float] = Field(None, ge=0, description="Minimum planet radius (Earth radii)")
    max_radius: Optional[float] = Field(None, ge=0, description="Maximum planet radius (Earth radii)")
    limit: int = Field(50, ge=1, le=500, description="Maximum number of results")
    offset: int = Field(0, ge=0, description="Result offset for pagination")


class PlanetInfo(BaseModel):
    """Planet information model"""
    id: str = Field(..., description="Planet identifier")
    name: str = Field(..., description="Planet name")
    host_star: str = Field(..., description="Host star name")
    disposition: str = Field(..., description="Planet disposition")
    period: Optional[float] = Field(None, description="Orbital period (days)")
    radius: Optional[float] = Field(None, description="Planet radius (Earth radii)")
    mass: Optional[float] = Field(None, description="Planet mass (Earth masses)")
    temperature: Optional[float] = Field(None, description="Equilibrium temperature (K)")
    discovery_method: Optional[str] = Field(None, description="Discovery method")
    discovery_year: Optional[int] = Field(None, description="Discovery year")
    mission: str = Field(..., description="Discovery mission")


class PlanetResponse(BaseModel):
    """Planet search response model"""
    planets: List[PlanetInfo] = Field(..., description="List of planets")
    total: int = Field(..., description="Total number of results")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Results per page")


class MLClassificationRequest(BaseModel):
    """ML classification request model"""
    features: Dict[str, float] = Field(..., description="Feature values for classification")
    model_type: str = Field("random_forest", description="Model type to use")


class MLClassificationResponse(BaseModel):
    """ML classification response model"""
    prediction: str = Field(..., description="Predicted class")
    confidence: float = Field(..., description="Prediction confidence")
    probabilities: Dict[str, float] = Field(..., description="Class probabilities")


class VisualizationRequest(BaseModel):
    """Visualization request model"""
    chart_type: str = Field(..., description="Type of chart to generate")
    x_axis: str = Field(..., description="X-axis parameter")
    y_axis: str = Field(..., description="Y-axis parameter")
    filters: Optional[Dict[str, Any]] = Field(None, description="Data filters")


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error description")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")