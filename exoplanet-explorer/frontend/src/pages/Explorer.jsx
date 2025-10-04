import React, { useState, useEffect } from 'react'
import { Search, Filter, Star, Planet } from 'lucide-react'
import Loading from '../components/common/Loading'
import api from '../api/endpoints'

const Explorer = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMission, setSelectedMission] = useState('')
  const [planets, setPlanets] = useState([])
  const [stars, setStars] = useState([])
  const [missions, setMissions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('planets')
  const [filters, setFilters] = useState({
    minPeriod: '',
    maxPeriod: '',
    minRadius: '',
    maxRadius: ''
  })

  // Load missions on component mount
  useEffect(() => {
    loadMissions()
  }, [])

  // Load planets when filters change
  useEffect(() => {
    if (activeTab === 'planets') {
      loadPlanets()
    }
  }, [selectedMission, filters, activeTab])

  const loadMissions = async () => {
    try {
      const response = await api.missions.getAll()
      setMissions(response.data)
    } catch (err) {
      console.error('Error loading missions:', err)
    }
  }

  const loadPlanets = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const filterParams = {
        mission: selectedMission || undefined,
        min_period: filters.minPeriod || undefined,
        max_period: filters.maxPeriod || undefined,
        min_radius: filters.minRadius || undefined,
        max_radius: filters.maxRadius || undefined,
        limit: 50
      }
      
      // Remove undefined values
      Object.keys(filterParams).forEach(key => 
        filterParams[key] === undefined && delete filterParams[key]
      )
      
      const response = await api.planets.getAll(filterParams)
      setPlanets(response.data.planets || [])
    } catch (err) {
      setError('Failed to load planets. Please try again.')
      setPlanets([])
    } finally {
      setLoading(false)
    }
  }

  const searchStars = async () => {
    if (!searchQuery.trim()) return
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await api.stars.search(searchQuery, selectedMission, 20)
      setStars(response.data || [])
    } catch (err) {
      setError('Failed to search stars. Please try again.')
      setStars([])
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    if (activeTab === 'stars') {
      searchStars()
    }
  }

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }))
  }

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-4">
            Exoplanet Explorer
          </h1>
          <p className="text-gray-300">
            Search and explore exoplanets and their host stars from NASA missions
          </p>
        </div>

        {/* Controls */}
        <div className="card mb-8">
          {/* Tab Navigation */}
          <div className="flex space-x-4 mb-6">
            <button
              onClick={() => setActiveTab('planets')}
              className={`px-4 py-2 rounded-lg flex items-center ${
                activeTab === 'planets'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white bg-opacity-10 text-gray-300 hover:text-white'
              }`}
            >
              <Planet className="h-4 w-4 mr-2" />
              Planets
            </button>
            <button
              onClick={() => setActiveTab('stars')}
              className={`px-4 py-2 rounded-lg flex items-center ${
                activeTab === 'stars'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white bg-opacity-10 text-gray-300 hover:text-white'
              }`}
            >
              <Star className="h-4 w-4 mr-2" />
              Stars
            </button>
          </div>

          {/* Search Bar (for stars) */}
          {activeTab === 'stars' && (
            <form onSubmit={handleSearch} className="mb-6">
              <div className="flex gap-4">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search by TIC, KIC, KOI, or star name..."
                  className="flex-1 px-4 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  type="submit"
                  className="btn-primary flex items-center"
                >
                  <Search className="h-4 w-4 mr-2" />
                  Search
                </button>
              </div>
            </form>
          )}

          {/* Mission Filter */}
          <div className="mb-6">
            <label className="block text-white text-sm font-medium mb-2">
              Mission
            </label>
            <select
              value={selectedMission}
              onChange={(e) => setSelectedMission(e.target.value)}
              className="w-full px-4 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Missions</option>
              {missions.map((mission) => (
                <option key={mission.name} value={mission.name.toLowerCase()}>
                  {mission.name}
                </option>
              ))}
            </select>
          </div>

          {/* Planet Filters */}
          {activeTab === 'planets' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-white text-sm font-medium mb-2">
                  Min Period (days)
                </label>
                <input
                  type="number"
                  value={filters.minPeriod}
                  onChange={(e) => handleFilterChange('minPeriod', e.target.value)}
                  className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0"
                />
              </div>
              <div>
                <label className="block text-white text-sm font-medium mb-2">
                  Max Period (days)
                </label>
                <input
                  type="number"
                  value={filters.maxPeriod}
                  onChange={(e) => handleFilterChange('maxPeriod', e.target.value)}
                  className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="∞"
                />
              </div>
              <div>
                <label className="block text-white text-sm font-medium mb-2">
                  Min Radius (Earth radii)
                </label>
                <input
                  type="number"
                  value={filters.minRadius}
                  onChange={(e) => handleFilterChange('minRadius', e.target.value)}
                  className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="0"
                />
              </div>
              <div>
                <label className="block text-white text-sm font-medium mb-2">
                  Max Radius (Earth radii)
                </label>
                <input
                  type="number"
                  value={filters.maxRadius}
                  onChange={(e) => handleFilterChange('maxRadius', e.target.value)}
                  className="w-full px-3 py-2 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="∞"
                />
              </div>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && <Loading message={`Loading ${activeTab}...`} />}

        {/* Error State */}
        {error && (
          <div className="card bg-red-900 bg-opacity-50 border-red-500 text-center">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* Results */}
        {!loading && !error && (
          <div>
            {activeTab === 'planets' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-white">
                    Exoplanets ({planets.length})
                  </h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {planets.map((planet) => (
                    <div key={planet.id} className="card">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="text-lg font-semibold text-white truncate">
                          {planet.name}
                        </h3>
                        <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded">
                          {planet.mission}
                        </span>
                      </div>
                      <p className="text-gray-300 text-sm mb-3">
                        Host Star: {planet.host_star}
                      </p>
                      <div className="space-y-2 text-sm">
                        {planet.period && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Period:</span>
                            <span className="text-white">{planet.period.toFixed(2)} days</span>
                          </div>
                        )}
                        {planet.radius && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Radius:</span>
                            <span className="text-white">{planet.radius.toFixed(2)} R⊕</span>
                          </div>
                        )}
                        {planet.mass && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Mass:</span>
                            <span className="text-white">{planet.mass.toFixed(2)} M⊕</span>
                          </div>
                        )}
                        {planet.discovery_year && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Discovered:</span>
                            <span className="text-white">{planet.discovery_year}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
                {planets.length === 0 && (
                  <div className="text-center py-12">
                    <Planet className="h-16 w-16 text-gray-500 mx-auto mb-4" />
                    <p className="text-gray-400">No planets found with current filters</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'stars' && (
              <div>
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-white">
                    Stars ({stars.length})
                  </h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {stars.map((star) => (
                    <div key={star.id} className="card">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="text-lg font-semibold text-white truncate">
                          {star.name}
                        </h3>
                        <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded">
                          {star.mission}
                        </span>
                      </div>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">ID:</span>
                          <span className="text-white font-mono text-xs">{star.id}</span>
                        </div>
                        {star.ra && star.dec && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Coordinates:</span>
                            <span className="text-white text-xs">
                              {star.ra.toFixed(4)}, {star.dec.toFixed(4)}
                            </span>
                          </div>
                        )}
                        {star.magnitude && (
                          <div className="flex justify-between">
                            <span className="text-gray-400">Magnitude:</span>
                            <span className="text-white">{star.magnitude.toFixed(2)}</span>
                          </div>
                        )}
                        <div className="flex justify-between">
                          <span className="text-gray-400">Light Curve:</span>
                          <span className={`text-xs px-2 py-1 rounded ${
                            star.has_lightcurve 
                              ? 'bg-green-600 text-white' 
                              : 'bg-gray-600 text-gray-300'
                          }`}>
                            {star.has_lightcurve ? 'Available' : 'Not Available'}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                {stars.length === 0 && !searchQuery && (
                  <div className="text-center py-12">
                    <Star className="h-16 w-16 text-gray-500 mx-auto mb-4" />
                    <p className="text-gray-400">Enter a search query to find stars</p>
                  </div>
                )}
                {stars.length === 0 && searchQuery && (
                  <div className="text-center py-12">
                    <Star className="h-16 w-16 text-gray-500 mx-auto mb-4" />
                    <p className="text-gray-400">No stars found for "{searchQuery}"</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Explorer