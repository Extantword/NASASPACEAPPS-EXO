"""
Tests for services
"""
import pytest
import asyncio
from app.services.nasa_service import nasa_service
from app.services.lightkurve_service import lightkurve_service


@pytest.mark.asyncio
async def test_nasa_service_get_missions():
    """Test NASA service missions"""
    missions = await nasa_service.get_missions()
    assert isinstance(missions, list)


@pytest.mark.asyncio
async def test_nasa_service_search_planets():
    """Test NASA service planet search"""
    result = await nasa_service.search_planets({"limit": 5})
    assert "planets" in result
    assert "total" in result
    assert isinstance(result["planets"], list)


@pytest.mark.asyncio
async def test_lightkurve_service_search():
    """Test lightkurve service search"""
    targets = await lightkurve_service.search_targets("TOI-100")
    assert isinstance(targets, list)


@pytest.mark.asyncio
async def test_lightkurve_service_download():
    """Test lightkurve service download"""
    lc_data = await lightkurve_service.download_lightcurve("TIC 123456789")
    assert "star_id" in lc_data
    assert "data" in lc_data
    assert "time" in lc_data["data"]
    assert "flux" in lc_data["data"]