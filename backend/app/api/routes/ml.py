"""
API routes for machine learning
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.schemas import MLClassificationRequest, MLClassificationResponse

router = APIRouter()


@router.post("/classify", response_model=MLClassificationResponse)
async def classify_candidate(request: MLClassificationRequest):
    """Classify exoplanet candidate using ML model"""
    try:
        # Mock ML classification for now
        # In a real implementation, this would load a trained model
        
        features = request.features
        model_type = request.model_type
        
        # Mock classification logic
        confidence_score = 0.75 + (hash(str(features)) % 100) / 400  # Random confidence 0.75-1.0
        
        # Simple rule-based mock classification
        period = features.get("period", 0)
        radius = features.get("radius", 0)
        
        if period > 300 or radius > 10:
            prediction = "FALSE_POSITIVE"
            confidence = max(0.6, confidence_score - 0.1)
        elif 1 < period < 50 and 0.5 < radius < 4:
            prediction = "CONFIRMED"
            confidence = confidence_score
        else:
            prediction = "CANDIDATE"
            confidence = confidence_score - 0.2
        
        probabilities = {
            "CONFIRMED": confidence if prediction == "CONFIRMED" else (1 - confidence) / 2,
            "CANDIDATE": confidence if prediction == "CANDIDATE" else (1 - confidence) / 2,
            "FALSE_POSITIVE": confidence if prediction == "FALSE_POSITIVE" else (1 - confidence) / 2
        }
        
        # Normalize probabilities
        total_prob = sum(probabilities.values())
        if total_prob > 0:
            probabilities = {k: v / total_prob for k, v in probabilities.items()}
        
        return MLClassificationResponse(
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in ML classification: {str(e)}")


@router.get("/models")
async def get_available_models():
    """Get list of available ML models"""
    return {
        "models": [
            {
                "name": "random_forest",
                "description": "Random Forest classifier for exoplanet validation",
                "features": ["period", "radius", "mass", "temperature", "stellar_radius", "stellar_mass"],
                "accuracy": 0.89,
                "trained_samples": 10000
            },
            {
                "name": "neural_network",
                "description": "Deep neural network for exoplanet classification",
                "features": ["period", "radius", "mass", "temperature", "stellar_radius", "stellar_mass", "transit_depth"],
                "accuracy": 0.92,
                "trained_samples": 15000
            }
        ]
    }


@router.post("/predict_batch")
async def predict_batch(candidates: list[Dict[str, Any]]):
    """Batch prediction for multiple candidates"""
    try:
        results = []
        
        for i, candidate in enumerate(candidates[:100]):  # Limit to 100 candidates
            # Create request for each candidate
            request = MLClassificationRequest(
                features=candidate.get("features", {}),
                model_type=candidate.get("model_type", "random_forest")
            )
            
            # Get prediction
            result = await classify_candidate(request)
            
            results.append({
                "index": i,
                "candidate_id": candidate.get("id", f"candidate_{i}"),
                "prediction": result.prediction,
                "confidence": result.confidence,
                "probabilities": result.probabilities
            })
        
        return {
            "total_processed": len(results),
            "results": results,
            "summary": {
                "confirmed": len([r for r in results if r["prediction"] == "CONFIRMED"]),
                "candidates": len([r for r in results if r["prediction"] == "CANDIDATE"]),
                "false_positives": len([r for r in results if r["prediction"] == "FALSE_POSITIVE"])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch prediction: {str(e)}")


@router.get("/feature_importance")
async def get_feature_importance(model_type: str = "random_forest"):
    """Get feature importance for a specific model"""
    try:
        # Mock feature importance data
        mock_importance = {
            "random_forest": {
                "period": 0.25,
                "radius": 0.22,
                "transit_depth": 0.18,
                "stellar_radius": 0.15,
                "temperature": 0.12,
                "stellar_mass": 0.08
            },
            "neural_network": {
                "transit_depth": 0.28,
                "period": 0.23,
                "radius": 0.20,
                "stellar_radius": 0.12,
                "temperature": 0.10,
                "stellar_mass": 0.07
            }
        }
        
        importance = mock_importance.get(model_type, mock_importance["random_forest"])
        
        return {
            "model_type": model_type,
            "feature_importance": importance,
            "sorted_features": sorted(importance.items(), key=lambda x: x[1], reverse=True)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feature importance: {str(e)}")


@router.get("/metrics/{model_type}")
async def get_model_metrics(model_type: str):
    """Get performance metrics for a specific model"""
    try:
        # Mock model metrics
        mock_metrics = {
            "random_forest": {
                "accuracy": 0.89,
                "precision": 0.87,
                "recall": 0.91,
                "f1_score": 0.89,
                "confusion_matrix": [
                    [850, 50, 100],   # True CONFIRMED
                    [60, 820, 120],   # True CANDIDATE  
                    [90, 130, 780]    # True FALSE_POSITIVE
                ],
                "classes": ["CONFIRMED", "CANDIDATE", "FALSE_POSITIVE"]
            },
            "neural_network": {
                "accuracy": 0.92,
                "precision": 0.90,
                "recall": 0.94,
                "f1_score": 0.92,
                "confusion_matrix": [
                    [920, 40, 40],    # True CONFIRMED
                    [50, 880, 70],    # True CANDIDATE
                    [60, 80, 860]     # True FALSE_POSITIVE
                ],
                "classes": ["CONFIRMED", "CANDIDATE", "FALSE_POSITIVE"]
            }
        }
        
        metrics = mock_metrics.get(model_type)
        if not metrics:
            raise HTTPException(status_code=404, detail=f"Model '{model_type}' not found")
        
        return {
            "model_type": model_type,
            "metrics": metrics,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model metrics: {str(e)}")