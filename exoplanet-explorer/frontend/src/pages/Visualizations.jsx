import React, { useState, useEffect } from 'react'
import { BarChart, LineChart, Activity, Download } from 'lucide-react'
import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter } from 'recharts'
import Loading from '../components/common/Loading'
import api from '../api/endpoints'

const Visualizations = () => {
  const [lightCurveData, setLightCurveData] = useState(null)
  const [selectedStar, setSelectedStar] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [planetStats, setPlanetStats] = useState(null)

  useEffect(() => {
    loadPlanetStats()
  }, [])

  const loadPlanetStats = async () => {
    try {
      const response = await api.planets.getStats()
      setPlanetStats(response.data)
    } catch (err) {
      console.error('Error loading planet stats:', err)
    }
  }

  const loadLightCurve = async (starId) => {
    if (!starId.trim()) return

    setLoading(true)
    setError(null)

    try {
      const response = await api.lightCurves.get(starId, 'TESS')
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
    loadLightCurve(selectedStar)
  }

  // Mock data for planet correlations
  const planetCorrelationData = [
    { period: 1.2, radius: 0.8, name: 'TOI-100b' },
    { period: 3.5, radius: 1.2, name: 'TOI-101b' },
    { period: 8.1, radius: 2.1, name: 'TOI-102b' },
    { period: 15.7, radius: 3.2, name: 'TOI-103b' },
    { period: 25.3, radius: 1.8, name: 'TOI-104b' },
    { period: 42.1, radius: 4.1, name: 'TOI-105b' },
    { period: 67.2, radius: 2.8, name: 'TOI-106b' },
    { period: 95.5, radius: 5.2, name: 'TOI-107b' },
  ]

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-4">
            Data Visualizations
          </h1>
          <p className="text-gray-300">
            Interactive charts and analysis tools for exoplanet data
          </p>
        </div>

        {/* Light Curve Section */}
        <div className="card mb-8">
          <div className="flex items-center mb-6">
            <Activity className="h-6 w-6 text-blue-400 mr-2" />
            <h2 className="text-xl font-semibold text-white">Light Curve Analysis</h2>
          </div>

          {/* Search Form */}
          <form onSubmit={handleSearch} className="mb-6">
            <div className="flex gap-4">
              <input
                type="text"
                value={selectedStar}
                onChange={(e) => setSelectedStar(e.target.value)}
                placeholder="Enter star ID (e.g., TIC 123456789, TOI-100)"
                className="flex-1 px-4 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="submit"
                className="btn-primary flex items-center"
                disabled={loading}
              >
                <Activity className="h-4 w-4 mr-2" />
                Load Light Curve
              </button>
            </div>
          </form>

          {/* Loading State */}
          {loading && <Loading message="Loading light curve data..." />}

          {/* Error State */}
          {error && (
            <div className="bg-red-900 bg-opacity-50 border border-red-500 rounded-lg p-4 text-red-200 text-center">
              {error}
            </div>
          )}

          {/* Light Curve Chart */}
          {lightCurveData && !loading && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-white">
                    {lightCurveData.star_name}
                  </h3>
                  <p className="text-gray-300 text-sm">
                    Mission: {lightCurveData.mission} | Data Points: {lightCurveData.chartData.length}
                  </p>
                </div>
                <button className="btn-secondary flex items-center text-sm">
                  <Download className="h-4 w-4 mr-2" />
                  Download CSV
                </button>
              </div>

              <div className="bg-white bg-opacity-5 rounded-lg p-4">
                <ResponsiveContainer width="100%" height={400}>
                  <RechartsLineChart data={lightCurveData.chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis 
                      dataKey="time" 
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.2)',
                        borderRadius: '8px',
                        color: 'white'
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="flux" 
                      stroke="#3B82F6" 
                      strokeWidth={1}
                      dot={false}
                    />
                  </RechartsLineChart>
                </ResponsiveContainer>
              </div>

              {/* Metadata */}
              <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-lg font-semibold text-white">
                    {lightCurveData.metadata.duration_days?.toFixed(1) || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-400">Duration (days)</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-white">
                    {lightCurveData.metadata.mean_flux?.toFixed(4) || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-400">Mean Flux</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-white">
                    {lightCurveData.metadata.std_flux?.toFixed(6) || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-400">Std Dev</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-white">
                    {lightCurveData.data.cadence || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-400">Cadence</div>
                </div>
              </div>
            </div>
          )}

          {!lightCurveData && !loading && !error && (
            <div className="text-center py-12">
              <Activity className="h-16 w-16 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">Enter a star identifier to load light curve data</p>
            </div>
          )}
        </div>

        {/* Planet Correlations */}
        <div className="card mb-8">
          <div className="flex items-center mb-6">
            <BarChart className="h-6 w-6 text-blue-400 mr-2" />
            <h2 className="text-xl font-semibold text-white">Planet Correlations</h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Period vs Radius Scatter Plot */}
            <div>
              <h3 className="text-lg font-medium text-white mb-4">
                Orbital Period vs Planet Radius
              </h3>
              <div className="bg-white bg-opacity-5 rounded-lg p-4">
                <ResponsiveContainer width="100%" height={300}>
                  <ScatterChart data={planetCorrelationData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis 
                      dataKey="period" 
                      name="Period (days)"
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <YAxis 
                      dataKey="radius" 
                      name="Radius (Earth radii)"
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <Tooltip 
                      cursor={{ strokeDasharray: '3 3' }}
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.2)',
                        borderRadius: '8px',
                        color: 'white'
                      }}
                    />
                    <Scatter 
                      dataKey="radius" 
                      fill="#3B82F6"
                    />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Discovery Statistics */}
            <div>
              <h3 className="text-lg font-medium text-white mb-4">
                Discovery Statistics
              </h3>
              {planetStats ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">By Mission</h4>
                    <div className="space-y-2">
                      {Object.entries(planetStats.by_mission || {}).map(([mission, count]) => (
                        <div key={mission} className="flex justify-between items-center">
                          <span className="text-gray-400">{mission}</span>
                          <span className="text-white font-semibold">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium text-gray-300 mb-2">Discovery Methods</h4>
                    <div className="space-y-2">
                      {Object.entries(planetStats.by_method || {}).slice(0, 5).map(([method, count]) => (
                        <div key={method} className="flex justify-between items-center">
                          <span className="text-gray-400 text-sm truncate">{method}</span>
                          <span className="text-white font-semibold">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <Loading message="Loading statistics..." />
              )}
            </div>
          </div>
        </div>

        {/* Quick Analysis Tools */}
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-6">Quick Analysis Tools</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="btn-secondary flex items-center justify-center p-4">
              <LineChart className="h-5 w-5 mr-2" />
              Period Analysis
            </button>
            <button className="btn-secondary flex items-center justify-center p-4">
              <BarChart className="h-5 w-5 mr-2" />
              Size Distribution
            </button>
            <button className="btn-secondary flex items-center justify-center p-4">
              <Activity className="h-5 w-5 mr-2" />
              Transit Detection
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Visualizations