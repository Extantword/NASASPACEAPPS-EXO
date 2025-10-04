# Exoplanet Explorer 

An interactive web application for exploring and analyzing exoplanet data from NASA missions. Built for the **2025 NASA Space Apps Challenge**.

## Features

- **Exoplanet Search & Discovery**: Browse thousands of confirmed exoplanets from Kepler, TESS, and K2 missions
- **Interactive Visualizations**: Analyze light curves, correlations, and statistical distributions
- **Machine Learning Classification**: AI-powered exoplanet validation and candidate classification
- **Educational Content**: Learn about exoplanet science and detection methods
- **Real-time Data**: Integration with NASA Exoplanet Archive and MAST

## Architecture

### Backend (Python)
- **FastAPI** - Modern, fast web framework
- **Lightkurve** - Light curve analysis
- **Astroquery** - NASA data access
- **Scikit-learn** - Machine learning
- **Pandas/NumPy** - Data processing

### Frontend (React)
- **React 18** - Modern UI framework
- **Vite** - Fast development and building
- **Recharts** - Interactive data visualization
- **React Router** - Client-side routing
- **Axios** - API communication

## Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Extantword/NASASPACEAPPS-EXO.git
cd NASASPACEAPPS-EXO/exoplanet-explorer
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start the backend server
python app/main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Home Page**: Overview of the project and quick statistics
2. **Explorer**: Search and filter exoplanets and stars
3. **Visualizations**: View light curves and analyze correlations
4. **Machine Learning**: Classify exoplanet candidates using AI
5. **Learn**: Educational content about exoplanet science

## API Endpoints

### Missions
- `GET /api/v1/missions` - List all missions
- `GET /api/v1/missions/{name}` - Get mission details

### Stars
- `GET /api/v1/stars/search` - Search for stars
- `GET /api/v1/stars/{id}` - Get star details

### Planets
- `GET /api/v1/planets` - List exoplanets with filters
- `GET /api/v1/planets/{id}` - Get planet details
- `GET /api/v1/planets/stats/overview` - Get statistics

### Light Curves
- `GET /api/v1/lightcurves/{star_id}` - Get light curve data
- `GET /api/v1/lightcurves/{star_id}/download` - Download as CSV
- `GET /api/v1/lightcurves/{star_id}/metadata` - Get metadata

### Machine Learning
- `POST /api/v1/ml/classify` - Classify exoplanet candidate
- `GET /api/v1/ml/models` - List available models
- `GET /api/v1/ml/feature_importance` - Get feature importance
- `GET /api/v1/ml/metrics/{model}` - Get model performance

## Development

### Backend Development
```bash
cd backend

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# API documentation
# Visit http://localhost:8000/docs for Swagger UI
# Visit http://localhost:8000/redoc for ReDoc
```

### Frontend Development
```bash
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Data Sources

- **NASA Exoplanet Archive**: Confirmed exoplanet data
- **MAST Archive**: Light curve data from Kepler, K2, and TESS
- **Lightkurve**: Python library for light curve analysis

## Machine Learning

The ML models are trained to classify exoplanet candidates into:
- **CONFIRMED**: High-confidence exoplanets
- **CANDIDATE**: Requires further validation
- **FALSE_POSITIVE**: Likely not a planet

Features used include:
- Orbital period
- Planet radius and mass
- Stellar properties
- Transit characteristics

## Configuration

### Backend Configuration (`.env`)
```bash
API_HOST=localhost
API_PORT=8000
DEBUG=True
NASA_EXOPLANET_API_URL=https://exoplanetarchive.ipac.caltech.edu/TAP/sync
MAST_API_URL=https://mast.stsci.edu/api/v0.1
CORS_ORIGINS=["http://localhost:5173"]
```

### Frontend Configuration (`.env`)
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Exoplanet Explorer
VITE_APP_VERSION=1.0.0
```

## Deployment

### Using Docker (Recommended)
```bash
# Build and run with docker-compose
docker-compose up --build
```

### Manual Deployment
1. Build frontend: `npm run build`
2. Serve frontend files with nginx/apache
3. Run backend with gunicorn: `gunicorn app.main:app`
4. Configure reverse proxy for API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request


## NASA Space Apps Challenge

This project was created for the **2025 NASA Space Apps Challenge** under the challenge:
**"A World Away: Hunting for Exoplanets with AI"**

### Team
- **Project Name**: EXO
- **Team**: EXO
- **Repository**: [GitHub](https://github.com/Extantword/NASASPACEAPPS-EXO)

## 🔗 Links

- **Live Demo**: 
- **API Documentation**: `http://localhost:8000/docs`
- **NASA Exoplanet Archive**: https://exoplanetarchive.ipac.caltech.edu/
- **TESS Mission**: https://tess.mit.edu/
- **Lightkurve Documentation**: https://docs.lightkurve.org/


