"""
FastAPI main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import asyncio

from app.config import settings
from app.api.routes import missions, stars, planets, lightcurves, ml, websockets
from app.websockets import router as websocket_chat_router
from app.etl.startup import initialize_startup_data

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Exoplanet Explorer API",
    description="NASA Space Apps Challenge - Exoplanet data analysis and visualization API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(missions.router, prefix="/api/v1/missions", tags=["missions"])
app.include_router(stars.router, prefix="/api/v1/stars", tags=["stars"])
app.include_router(planets.router, prefix="/api/v1/planets", tags=["planets"])
app.include_router(lightcurves.router, prefix="/api/v1/lightcurves", tags=["lightcurves"])
app.include_router(ml.router, prefix="/api/v1/ml", tags=["machine-learning"])
app.include_router(websockets.router, prefix="/api/v1/ws", tags=["websockets"])

# Include WebSocket chat router
app.include_router(websocket_chat_router.router, prefix="/api/v1", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    """Initialize data when the server starts"""
    logger.info("🚀 Starting Exoplanet Explorer API...")
    
    # Start data initialization in background
    asyncio.create_task(initialize_startup_data_background())


async def initialize_startup_data_background():
    """Initialize data in background to avoid blocking startup"""
    try:
        logger.info("📡 Initializing NASA datasets...")
        success = await initialize_startup_data()
        if success:
            logger.info("✅ NASA datasets initialized successfully")
        else:
            logger.warning("⚠️ Some datasets failed to initialize (using fallback data)")
    except Exception as e:
        logger.error(f"❌ Data initialization failed: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Exoplanet Explorer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "exoplanet-explorer-api"}


@app.get("/api/v1/data/status")
async def data_status():
    """Get data initialization status"""
    from app.etl.startup import get_data_status
    return await get_data_status()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )