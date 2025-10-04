import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Download, Filter, Layers, Maximize2 } from 'lucide-react';

const ExoplanetVisualization = ({ 
  planets = [], 
  className = "",
  title = "Exoplanet Properties"
}) => {
  const [filteredData, setFilteredData] = useState([]);
  const [xAxis, setXAxis] = useState('pl_orbper');
  const [yAxis, setYAxis] = useState('pl_rade');
  const [colorBy, setColorBy] = useState('discoverymethod');
  const [filters, setFilters] = useState({
    mission: 'all',
    year: 'all',
    method: 'all'
  });
  const [showFilters, setShowFilters] = useState(false);
  
  const axisOptions = [
    { value: 'pl_orbper', label: 'Orbital Period (days)', scale: 'log' },
    { value: 'pl_rade', label: 'Planet Radius (Earth radii)', scale: 'log' },
    { value: 'pl_masse', label: 'Planet Mass (Earth masses)', scale: 'log' },
    { value: 'pl_eqt', label: 'Equilibrium Temperature (K)', scale: 'linear' },
    { value: 'st_rad', label: 'Stellar Radius (Solar radii)', scale: 'linear' },
    { value: 'st_mass', label: 'Stellar Mass (Solar masses)', scale: 'linear' },
    { value: 'st_teff', label: 'Stellar Temperature (K)', scale: 'linear' },
    { value: 'disc_year', label: 'Discovery Year', scale: 'linear' }
  ];

  const colorOptions = [
    { value: 'discoverymethod', label: 'Discovery Method' },
    { value: 'disc_facility', label: 'Discovery Facility' },
    { value: 'disc_year', label: 'Discovery Year' },
    { value: 'planet_type', label: 'Planet Type' }
  ];

  // Color schemes for different categories
  const colorSchemes = {
    discoverymethod: {
      'Transit': '#3b82f6',
      'Radial Velocity': '#ef4444', 
      'Microlensing': '#10b981',
      'Direct Imaging': '#f59e0b',
      'Astrometry': '#8b5cf6',
      'Other': '#6b7280'
    },
    disc_facility: {
      'Kepler': '#3b82f6',
      'TESS': '#ef4444',
      'K2': '#10b981',
      'CoRoT': '#f59e0b',
      'WASP': '#8b5cf6',
      'HAT': '#ec4899',
      'Other': '#6b7280'
    },
    planet_type: {
      'Rocky': '#a78bfa',
      'Super Earth': '#34d399',
      'Neptune': '#60a5fa',
      'Gas Giant': '#f472b6',
      'Other': '#6b7280'
    }
  };

  useEffect(() => {
    if (planets && planets.length > 0) {
      processData();
    }
  }, [planets, filters, xAxis, yAxis, colorBy]);

  const processData = () => {
    let data = planets.map(planet => ({
      ...planet,
      // Categorize planets by type based on radius
      planet_type: categorizePlanet(planet.pl_rade),
      // Clean facility names
      disc_facility: cleanFacilityName(planet.disc_facility)
    }));

    // Apply filters
    if (filters.mission !== 'all') {
      data = data.filter(p => p.disc_facility?.toLowerCase().includes(filters.mission.toLowerCase()));
    }
    if (filters.year !== 'all') {
      const year = parseInt(filters.year);
      data = data.filter(p => p.disc_year >= year);
    }
    if (filters.method !== 'all') {
      data = data.filter(p => p.discoverymethod === filters.method);
    }

    // Filter out invalid data points
    data = data.filter(p => 
      p[xAxis] != null && 
      p[yAxis] != null && 
      !isNaN(p[xAxis]) && 
      !isNaN(p[yAxis]) &&
      p[xAxis] > 0 && 
      p[yAxis] > 0
    );

    setFilteredData(data);
  };

  const categorizePlanet = (radius) => {
    if (!radius || isNaN(radius)) return 'Other';
    if (radius < 1.5) return 'Rocky';
    if (radius < 2.5) return 'Super Earth';
    if (radius < 6) return 'Neptune';
    return 'Gas Giant';
  };

  const cleanFacilityName = (facility) => {
    if (!facility) return 'Other';
    if (facility.toLowerCase().includes('kepler')) return 'Kepler';
    if (facility.toLowerCase().includes('tess')) return 'TESS';
    if (facility.toLowerCase().includes('k2')) return 'K2';
    if (facility.toLowerCase().includes('corot')) return 'CoRoT';
    if (facility.toLowerCase().includes('wasp')) return 'WASP';
    if (facility.toLowerCase().includes('hat')) return 'HAT';
    return 'Other';
  };

  const getColor = (dataPoint) => {
    const colorValue = dataPoint[colorBy];
    const scheme = colorSchemes[colorBy];
    
    if (colorBy === 'disc_year' && colorValue) {
      // Color gradient for years
      const minYear = 1995;
      const maxYear = 2024;
      const normalized = (colorValue - minYear) / (maxYear - minYear);
      const hue = 240 - (normalized * 120); // Blue to red
      return `hsl(${hue}, 70%, 50%)`;
    }
    
    return scheme?.[colorValue] || '#6b7280';
  };

  const formatAxisLabel = (value, axis) => {
    const option = axisOptions.find(opt => opt.value === axis);
    if (option?.scale === 'log' && value > 0) {
      if (value >= 1000) return (value / 1000).toFixed(1) + 'k';
      if (value >= 1) return value.toFixed(1);
      return value.toFixed(2);
    }
    return value.toFixed(1);
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const xOption = axisOptions.find(opt => opt.value === xAxis);
      const yOption = axisOptions.find(opt => opt.value === yAxis);
      
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg max-w-xs">
          <p className="font-semibold text-gray-900 mb-2">{data.pl_name || 'Unknown Planet'}</p>
          <p className="text-sm text-gray-600 mb-1">
            Host: {data.hostname || 'Unknown'}
          </p>
          <div className="space-y-1 text-sm">
            <p>
              <span className="font-medium">{xOption?.label}:</span> {data[xAxis]?.toFixed(3)}
            </p>
            <p>
              <span className="font-medium">{yOption?.label}:</span> {data[yAxis]?.toFixed(3)}
            </p>
            <p>
              <span className="font-medium">Discovery:</span> {data.discoverymethod} ({data.disc_year})
            </p>
            <p>
              <span className="font-medium">Facility:</span> {data.disc_facility}
            </p>
            {data.planet_type && (
              <p>
                <span className="font-medium">Type:</span> {data.planet_type}
              </p>
            )}
          </div>
        </div>
      );
    }
    return null;
  };

  const exportData = () => {
    const csvContent = [
      // Header
      ['Planet Name', 'Host Star', xAxis, yAxis, colorBy, 'Discovery Year', 'Discovery Method'].join(','),
      // Data rows
      ...filteredData.map(d => [
        d.pl_name || '',
        d.hostname || '',
        d[xAxis] || '',
        d[yAxis] || '',
        d[colorBy] || '',
        d.disc_year || '',
        d.discoverymethod || ''
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = `exoplanets_${xAxis}_vs_${yAxis}.csv`;
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
  };

  // Get unique values for filter dropdowns
  const uniqueMissions = [...new Set(planets.map(p => cleanFacilityName(p.disc_facility)))].filter(Boolean);
  const uniqueMethods = [...new Set(planets.map(p => p.discoverymethod))].filter(Boolean);
  const uniqueYears = [...new Set(planets.map(p => p.disc_year))].filter(Boolean).sort((a, b) => b - a);

  return (
    <div className={`bg-white rounded-lg shadow-lg ${className}`}>
      {/* Header with controls */}
      <div className="flex flex-wrap items-center justify-between p-4 border-b border-gray-200 gap-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-600">
            Showing {filteredData.length.toLocaleString()} of {planets.length.toLocaleString()} exoplanets
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center px-3 py-2 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200"
          >
            <Filter size={16} className="mr-1" />
            Filters
          </button>
          
          <button
            onClick={exportData}
            className="flex items-center px-3 py-2 text-sm bg-green-100 text-green-700 rounded-lg hover:bg-green-200"
          >
            <Download size={16} className="mr-1" />
            Export
          </button>
        </div>
      </div>

      {/* Axis and color controls */}
      <div className="p-4 bg-gray-50 border-b border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">X-Axis</label>
            <select
              value={xAxis}
              onChange={(e) => setXAxis(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            >
              {axisOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Y-Axis</label>
            <select
              value={yAxis}
              onChange={(e) => setYAxis(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            >
              {axisOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Color By</label>
            <select
              value={colorBy}
              onChange={(e) => setColorBy(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            >
              {colorOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Filters panel */}
      {showFilters && (
        <div className="p-4 bg-blue-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Mission/Facility</label>
              <select
                value={filters.mission}
                onChange={(e) => setFilters({...filters, mission: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Missions</option>
                {uniqueMissions.map(mission => (
                  <option key={mission} value={mission}>{mission}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Discovery Method</label>
              <select
                value={filters.method}
                onChange={(e) => setFilters({...filters, method: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Methods</option>
                {uniqueMethods.map(method => (
                  <option key={method} value={method}>{method}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Discovery Year (from)</label>
              <select
                value={filters.year}
                onChange={(e) => setFilters({...filters, year: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Years</option>
                {uniqueYears.slice(0, 10).map(year => (
                  <option key={year} value={year}>{year}+</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="p-4">
        <ResponsiveContainer width="100%" height={500}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 60, left: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              type="number"
              dataKey={xAxis}
              scale={axisOptions.find(opt => opt.value === xAxis)?.scale || 'linear'}
              domain={['dataMin', 'dataMax']}
              tickFormatter={(value) => formatAxisLabel(value, xAxis)}
              label={{ 
                value: axisOptions.find(opt => opt.value === xAxis)?.label, 
                position: 'insideBottom', 
                offset: -40 
              }}
            />
            <YAxis
              type="number"
              dataKey={yAxis}
              scale={axisOptions.find(opt => opt.value === yAxis)?.scale || 'linear'}
              domain={['dataMin', 'dataMax']}
              tickFormatter={(value) => formatAxisLabel(value, yAxis)}
              label={{ 
                value: axisOptions.find(opt => opt.value === yAxis)?.label, 
                angle: -90, 
                position: 'insideLeft' 
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Scatter data={filteredData}>
              {filteredData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getColor(entry)} fillOpacity={0.7} />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex flex-wrap gap-4">
          {colorBy !== 'disc_year' && colorSchemes[colorBy] && Object.entries(colorSchemes[colorBy]).map(([key, color]) => (
            <div key={key} className="flex items-center">
              <div 
                className="w-3 h-3 rounded-full mr-2" 
                style={{ backgroundColor: color }}
              />
              <span className="text-sm text-gray-700">{key}</span>
            </div>
          ))}
          {colorBy === 'disc_year' && (
            <div className="flex items-center">
              <div className="w-20 h-3 bg-gradient-to-r from-blue-500 to-red-500 rounded mr-2" />
              <span className="text-sm text-gray-700">1995 → 2024</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ExoplanetVisualization;