import React, { useState, useEffect } from 'react'
import { BarChart, Activity, Download, Search, TrendingUp, Globe } from 'lucide-react'
import Loading from '../components/common/Loading'
import { LightCurveChart, ExoplanetVisualization } from '../components/visualizations'
import api from '../api/endpoints'

const Visualizations = () => {
  const [lightCurveData, setLightCurveData] = useState(null)
  const [planetsData, setPlanetsData] = useState([])
  const [selectedTarget, setSelectedTarget] = useState('')
  const [selectedMission, setSelectedMission] = useState('TESS')
  const [loading, setLoading] = useState(false)
  const [planetsLoading, setPlanetsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [planetStats, setPlanetStats] = useState(null)
  const [activeTab, setActiveTab] = useState('lightcurves')

  useEffect(() => {
    loadPlanetStats()
    loadPlanetsData()
  }, [])

  const loadPlanetStats = async () => {
    try {
      const response = await api.planets.getStats()
      setPlanetStats(response.data)
    } catch (err) {
      console.error('Error loading planet stats:', err)
    }
  }

  const loadPlanetsData = async () => {
    setPlanetsLoading(true)
    try {
      const response = await api.planets.search('', { limit: 2000 })
      setPlanetsData(response.data.planets)
    } catch (err) {
      console.error('Error loading planets data:', err)
    } finally {
      setPlanetsLoading(false)
    }
  }

  const loadLightCurve = async (target) => {
    if (!target.trim()) return

    setLoading(true)
    setError(null)

    try {
      const response = await api.lightCurves.get(target, selectedMission)
      const data = response.data

      // Convert to chart-friendly format
      const chartData = data.data.time.map((time, index) => ({
        time: time,
        flux: data.data.flux[index],
        flux_err: data.data.flux_err ? data.data.flux_err[index] : null
      }))

      setLightCurveData({
        ...data,
        chartData: chartData
      })
    } catch (err) {
      setError('Failed to load light curve data. Please try again.')
      setLightCurveData(null)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    loadLightCurve(selectedTarget)
  }

  const popularTargets = [
    'TOI-715 b', 'WASP-96 b', 'HD 209458 b', 'TRAPPIST-1', 'Kepler-442 b',
    'K2-18 b', '55 Cancri e', 'Kepler-186 f', 'Kepler-452 b', 'KIC 8462852'
  ]

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-4">
            Interactive Data Visualizations
          </h1>
          <p className="text-gray-300">
            Advanced charts and analysis tools powered by real NASA data
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-lg mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab('lightcurves')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'lightcurves'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Activity className="inline-block w-4 h-4 mr-2" />
                Light Curves
              </button>
              <button
                onClick={() => setActiveTab('correlations')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'correlations'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <TrendingUp className="inline-block w-4 h-4 mr-2" />
                Planet Properties
              </button>
              <button
                onClick={() => setActiveTab('statistics')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'statistics'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <BarChart className="inline-block w-4 h-4 mr-2" />
                Mission Statistics
              </button>
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'lightcurves' && (
          <div className="space-y-8">
            {/* Light Curve Search */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Light Curve Explorer
              </h2>
              
              <form onSubmit={handleSearch} className="mb-6">
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Target Name
                    </label>
                    <input
                      type="text"
                      value={selectedTarget}
                      onChange={(e) => setSelectedTarget(e.target.value)}
                      placeholder="e.g., TOI-715 b, WASP-96 b, Kepler-442 b"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  
                  <div className="sm:w-48">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Mission
                    </label>
                    <select
                      value={selectedMission}
                      onChange={(e) => setSelectedMission(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="TESS">TESS</option>
                      <option value="Kepler">Kepler</option>
                      <option value="K2">K2</option>
                    </select>
                  </div>
                  
                  <button
                    type="submit"
                    disabled={loading || !selectedTarget.trim()}
                    className="sm:mt-7 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                  >
                    <Search className="w-4 h-4 mr-2" />
                    {loading ? 'Loading...' : 'Search'}
                  </button>
                </div>
              </form>

              {/* Popular targets */}
              <div className="mb-6">
                <p className="text-sm text-gray-600 mb-2">Popular targets:</p>
                <div className="flex flex-wrap gap-2">
                  {popularTargets.map(target => (
                    <button
                      key={target}
                      onClick={() => {
                        setSelectedTarget(target)
                        loadLightCurve(target)
                      }}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200"
                    >
                      {target}
                    </button>
                  ))}
                </div>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-600">{error}</p>
                </div>
              )}
            </div>

            {/* Light Curve Chart */}
            {lightCurveData && (
              <LightCurveChart
                data={lightCurveData.chartData}
                title={`Light Curve: ${lightCurveData.target_name || selectedTarget}`}
                target={lightCurveData.target_name || selectedTarget}
                mission={selectedMission}
                className="mb-8"
              />
            )}

            {loading && (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <Loading />
              </div>
            )}
          </div>
        )}

        {activeTab === 'correlations' && (
          <div className="space-y-8">
            {planetsLoading ? (
              <div className="bg-white rounded-lg shadow-lg p-8">
                <Loading />
              </div>
            ) : (
              <ExoplanetVisualization
                planets={planetsData}
                title="Exoplanet Properties Explorer"
                className="mb-8"
              />
            )}
          </div>
        )}

        {activeTab === 'statistics' && (
          <div className="space-y-8">
            {/* Mission Statistics */}
            {planetStats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center">
                    <Globe className="h-8 w-8 text-blue-500 mr-3" />
                    <div>
                      <p className="text-gray-600 text-sm">Confirmed Exoplanets</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {planetStats.total_confirmed?.toLocaleString() || 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center">
                    <Activity className="h-8 w-8 text-green-500 mr-3" />
                    <div>
                      <p className="text-gray-600 text-sm">TESS Discoveries</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {planetStats.by_mission?.TESS?.toLocaleString() || 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center">
                    <TrendingUp className="h-8 w-8 text-purple-500 mr-3" />
                    <div>
                      <p className="text-gray-600 text-sm">Kepler Legacy</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {planetStats.by_mission?.Kepler?.toLocaleString() || 'N/A'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Discovery Timeline */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Exoplanet Discovery Timeline
              </h3>
              <div className="text-center py-8 text-gray-500">
                Discovery timeline visualization coming soon...
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Visualizations