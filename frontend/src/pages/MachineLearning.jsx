import React, { useState, useEffect } from 'react'
import { Brain, Zap, Target, TrendingUp } from 'lucide-react'
import Loading from '../components/common/Loading'
import api from '../api/endpoints'

const MachineLearning = () => {
  const [models, setModels] = useState([])
  const [selectedModel, setSelectedModel] = useState('random_forest')
  const [features, setFeatures] = useState({
    period: '',
    radius: '',
    mass: '',
    temperature: '',
    stellar_radius: '',
    stellar_mass: ''
  })
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [featureImportance, setFeatureImportance] = useState(null)
  const [modelMetrics, setModelMetrics] = useState(null)

  useEffect(() => {
    loadModels()
    loadFeatureImportance()
    loadModelMetrics()
  }, [selectedModel])

  const loadModels = async () => {
    try {
      const response = await api.ml.getModels()
      setModels(response.data.models || [])
    } catch (err) {
      console.error('Error loading models:', err)
    }
  }

  const loadFeatureImportance = async () => {
    try {
      const response = await api.ml.getFeatureImportance(selectedModel)
      setFeatureImportance(response.data)
    } catch (err) {
      console.error('Error loading feature importance:', err)
    }
  }

  const loadModelMetrics = async () => {
    try {
      const response = await api.ml.getMetrics(selectedModel)
      setModelMetrics(response.data)
    } catch (err) {
      console.error('Error loading model metrics:', err)
    }
  }

  const handleFeatureChange = (featureName, value) => {
    setFeatures(prev => ({
      ...prev,
      [featureName]: value
    }))
  }

  const handlePredict = async (e) => {
    e.preventDefault()
    
    // Validate features
    const numericFeatures = {}
    let hasValidFeatures = false
    
    for (const [key, value] of Object.entries(features)) {
      if (value && !isNaN(parseFloat(value))) {
        numericFeatures[key] = parseFloat(value)
        hasValidFeatures = true
      }
    }
    
    if (!hasValidFeatures) {
      setError('Please provide at least one valid numeric feature')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await api.ml.classify(numericFeatures, selectedModel)
      setPrediction(response.data)
    } catch (err) {
      setError('Failed to classify candidate. Please try again.')
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  const loadExampleData = () => {
    setFeatures({
      period: '3.14',
      radius: '1.2',
      mass: '1.1',
      temperature: '288',
      stellar_radius: '1.0',
      stellar_mass: '1.0'
    })
  }

  const clearForm = () => {
    setFeatures({
      period: '',
      radius: '',
      mass: '',
      temperature: '',
      stellar_radius: '',
      stellar_mass: ''
    })
    setPrediction(null)
    setError(null)
  }

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-4">
            Machine Learning Classification
          </h1>
          <p className="text-gray-300">
            AI-powered exoplanet validation and classification
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Classification Panel */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="flex items-center mb-6">
                <Brain className="h-6 w-6 text-blue-400 mr-2" />
                <h2 className="text-xl font-semibold text-white">Exoplanet Classification</h2>
              </div>

              {/* Model Selection */}
              <div className="mb-6">
                <label className="block text-white text-sm font-medium mb-2">
                  ML Model
                </label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="w-full px-4 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {models.map((model) => (
                    <option key={model.name} value={model.name}>
                      {model.description} (Accuracy: {(model.accuracy * 100).toFixed(1)}%)
                    </option>
                  ))}
                </select>
              </div>

              {/* Feature Input Form */}
              <form onSubmit={handlePredict} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Orbital Period (days)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={features.period}
                      onChange={(e) => handleFeatureChange('period', e.target.value)}
                      className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 3.14"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Planet Radius (Earth radii)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={features.radius}
                      onChange={(e) => handleFeatureChange('radius', e.target.value)}
                      className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 1.2"
                    />
                  </div>

                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Planet Mass (Earth masses)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={features.mass}
                      onChange={(e) => handleFeatureChange('mass', e.target.value)}
                      className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 1.1"
                    />
                  </div>

                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Equilibrium Temperature (K)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={features.temperature}
                      onChange={(e) => handleFeatureChange('temperature', e.target.value)}
                      className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 288"
                    />
                  </div>

                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Stellar Radius (Solar radii)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={features.stellar_radius}
                      onChange={(e) => handleFeatureChange('stellar_radius', e.target.value)}
                      className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 1.0"
                    />
                  </div>

                  <div>
                    <label className="block text-white text-sm font-medium mb-2">
                      Stellar Mass (Solar masses)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={features.stellar_mass}
                      onChange={(e) => handleFeatureChange('stellar_mass', e.target.value)}
                      className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., 1.0"
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4">
                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary flex items-center"
                  >
                    <Zap className="h-4 w-4 mr-2" />
                    {loading ? 'Classifying...' : 'Classify'}
                  </button>
                  <button
                    type="button"
                    onClick={loadExampleData}
                    className="btn-secondary"
                  >
                    Load Example
                  </button>
                  <button
                    type="button"
                    onClick={clearForm}
                    className="btn-secondary"
                  >
                    Clear
                  </button>
                </div>
              </form>

              {/* Error Display */}
              {error && (
                <div className="mt-4 bg-red-900 bg-opacity-50 border border-red-500 rounded-lg p-4 text-red-200">
                  {error}
                </div>
              )}

              {/* Prediction Results */}
              {prediction && (
                <div className="mt-6 p-4 bg-white bg-opacity-5 rounded-lg">
                  <h3 className="text-lg font-semibold text-white mb-4">Classification Result</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-white mb-1">
                        {prediction.prediction}
                      </div>
                      <div className="text-sm text-gray-400">Prediction</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-400 mb-1">
                        {(prediction.confidence * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-400">Confidence</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-400 mb-1">
                        {selectedModel.replace('_', ' ').toUpperCase()}
                      </div>
                      <div className="text-sm text-gray-400">Model Used</div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">Class Probabilities</h4>
                    <div className="space-y-2">
                      {Object.entries(prediction.probabilities).map(([className, probability]) => (
                        <div key={className} className="flex justify-between items-center">
                          <span className="text-gray-400">{className.replace('_', ' ')}</span>
                          <div className="flex items-center">
                            <div className="w-20 bg-gray-700 rounded-full h-2 mr-2">
                              <div 
                                className="bg-blue-500 h-2 rounded-full" 
                                style={{ width: `${probability * 100}%` }}
                              ></div>
                            </div>
                            <span className="text-white text-sm w-12">
                              {(probability * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Model Information Sidebar */}
          <div className="space-y-6">
            {/* Feature Importance */}
            {featureImportance && (
              <div className="card">
                <div className="flex items-center mb-4">
                  <Target className="h-5 w-5 text-blue-400 mr-2" />
                  <h3 className="text-lg font-semibold text-white">Feature Importance</h3>
                </div>
                <div className="space-y-3">
                  {featureImportance.sorted_features.slice(0, 6).map(([feature, importance]) => (
                    <div key={feature} className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">{feature.replace('_', ' ')}</span>
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-700 rounded-full h-2 mr-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full" 
                            style={{ width: `${importance * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-white text-xs w-8">
                          {(importance * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Model Performance */}
            {modelMetrics && (
              <div className="card">
                <div className="flex items-center mb-4">
                  <TrendingUp className="h-5 w-5 text-blue-400 mr-2" />
                  <h3 className="text-lg font-semibold text-white">Model Performance</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Accuracy</span>
                    <span className="text-white font-semibold">
                      {(modelMetrics.metrics.accuracy * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Precision</span>
                    <span className="text-white font-semibold">
                      {(modelMetrics.metrics.precision * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Recall</span>
                    <span className="text-white font-semibold">
                      {(modelMetrics.metrics.recall * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">F1 Score</span>
                    <span className="text-white font-semibold">
                      {(modelMetrics.metrics.f1_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Model Info */}
            <div className="card">
              <h3 className="text-lg font-semibold text-white mb-4">About ML Classification</h3>
              <div className="text-sm text-gray-300 space-y-2">
                <p>
                  Our machine learning models are trained on confirmed exoplanet data 
                  to classify candidates as:
                </p>
                <ul className="list-disc list-inside space-y-1 text-xs">
                  <li><strong>CONFIRMED</strong> - High confidence exoplanet</li>
                  <li><strong>CANDIDATE</strong> - Needs further validation</li>
                  <li><strong>FALSE_POSITIVE</strong> - Likely not a planet</li>
                </ul>
                <p className="text-xs">
                  Features include orbital period, planet radius/mass, stellar properties, 
                  and transit characteristics.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MachineLearning