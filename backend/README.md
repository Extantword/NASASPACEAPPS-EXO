# Backend - Exoplanet Explorer API

Backend API for the Exoplanet Explorer project built with FastAPI.

## Features

- NASA Exoplanet Archive integration
- Light curve data from MAST
- Machine learning classification
- Interactive data visualization support
- Comprehensive API documentation

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment:
```bash
cp .env.example .env
```

4. Run the server:
```bash
python app/main.py
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
app/
├── api/           # API routes and endpoints
├── services/      # Business logic and external API integration
├── models/        # Data models and schemas
├── utils/         # Utility functions
└── etl/          # Data extraction, transformation, loading
```

## Testing

```bash
pytest tests/
```