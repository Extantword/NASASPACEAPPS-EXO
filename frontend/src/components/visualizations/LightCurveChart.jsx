import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Brush, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Download, Settings, ZoomIn, ZoomOut, RotateCcw, Maximize2 } from 'lucide-react';

const LightCurveChart = ({ 
  data = [], 
  title = "Light Curve", 
  target = "", 
  mission = "",
  onExport,
  className = "" 
}) => {
  const [processedData, setProcessedData] = useState([]);
  const [originalData, setOriginalData] = useState([]);
  const [isNormalized, setIsNormalized] = useState(false);
  const [isDetrended, setIsDetrended] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [outlierThreshold, setOutlierThreshold] = useState(3);
  const [showSettings, setShowSettings] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [transitMarkers, setTransitMarkers] = useState([]);
  
  const chartRef = useRef(null);
  const containerRef = useRef(null);

  // Initialize data when props change
  useEffect(() => {
    if (data && data.length > 0) {
      setOriginalData(data);
      setProcessedData(data);
      detectTransits(data);
    }
  }, [data]);

  // Process data when settings change
  useEffect(() => {
    if (originalData.length > 0) {
      let processed = [...originalData];
      
      if (isNormalized) {
        processed = normalizeData(processed);
      }
      
      if (isDetrended) {
        processed = detrendData(processed);
      }
      
      setProcessedData(processed);
    }
  }, [originalData, isNormalized, isDetrended, outlierThreshold]);

  const normalizeData = (data) => {
    const fluxValues = data.map(d => d.flux).filter(f => f != null && !isNaN(f));
    const median = fluxValues.sort((a, b) => a - b)[Math.floor(fluxValues.length / 2)];
    
    return data.map(point => ({
      ...point,
      flux: point.flux / median,
      flux_err: point.flux_err ? point.flux_err / median : null
    }));
  };

  const detrendData = (data) => {
    if (data.length < 10) return data;
    
    // Simple linear detrending
    const n = data.length;
    const timeValues = data.map(d => d.time);
    const fluxValues = data.map(d => d.flux);
    
    // Calculate linear trend
    const sumX = timeValues.reduce((a, b) => a + b, 0);
    const sumY = fluxValues.reduce((a, b) => a + b, 0);
    const sumXY = timeValues.reduce((sum, x, i) => sum + x * fluxValues[i], 0);
    const sumXX = timeValues.reduce((sum, x) => sum + x * x, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    // Remove trend
    return data.map(point => ({
      ...point,
      flux: point.flux - (slope * point.time + intercept) + 1.0
    }));
  };

  const detectTransits = (data) => {
    if (data.length < 100) return;
    
    const fluxValues = data.map(d => d.flux).filter(f => f != null && !isNaN(f));
    const median = fluxValues.sort((a, b) => a - b)[Math.floor(fluxValues.length / 2)];
    const mad = fluxValues.map(f => Math.abs(f - median)).sort((a, b) => a - b)[Math.floor(fluxValues.length / 2)];
    const threshold = median - 3 * mad;
    
    const transits = [];
    let inTransit = false;
    let transitStart = null;
    
    data.forEach((point, i) => {
      if (point.flux < threshold && !inTransit) {
        inTransit = true;
        transitStart = point.time;
      } else if (point.flux >= threshold && inTransit) {
        inTransit = false;
        if (transitStart !== null) {
          transits.push({
            start: transitStart,
            end: point.time,
            depth: median - Math.min(...data.slice(Math.max(0, i-10), i+10).map(p => p.flux))
          });
        }
      }
    });
    
    setTransitMarkers(transits);
  };

  const handleExportData = () => {
    const csvContent = [
      'time,flux,flux_err',
      ...processedData.map(d => `${d.time},${d.flux},${d.flux_err || ''}`)
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.download = `${target}_lightcurve_${mission}_processed.csv`;
    link.href = url;
    link.click();
    
    URL.revokeObjectURL(url);
  };

  const resetView = () => {
    setZoomLevel(1);
    setIsNormalized(false);
    setIsDetrended(false);
    setProcessedData(originalData);
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium">{`Time: ${label?.toFixed(4)} days`}</p>
          <p className="text-blue-600">{`Flux: ${data.flux?.toFixed(6)}`}</p>
          {data.flux_err && (
            <p className="text-gray-500 text-sm">{`Error: ±${data.flux_err?.toFixed(6)}`}</p>
          )}
          {transitMarkers.some(t => t.start <= label && label <= t.end) && (
            <p className="text-red-600 text-sm font-medium">Transit Event</p>
          )}
        </div>
      );
    }
    return null;
  };

  if (!processedData || processedData.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
        <div className="text-center py-8">
          <div className="text-gray-400 text-lg">No light curve data available</div>
          <div className="text-gray-500 text-sm mt-2">
            Try searching for a different target or check the data source
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      className={`bg-white rounded-lg shadow-lg ${isFullscreen ? 'fixed inset-0 z-50 p-4' : className}`}
    >
      {/* Header with controls */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {target && (
            <p className="text-sm text-gray-600">
              Target: {target} {mission && `(${mission})`}
            </p>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          {/* Processing controls */}
          <div className="flex items-center space-x-2 mr-4">
            <label className="flex items-center text-sm">
              <input
                type="checkbox"
                checked={isNormalized}
                onChange={(e) => setIsNormalized(e.target.checked)}
                className="mr-1"
              />
              Normalize
            </label>
            <label className="flex items-center text-sm">
              <input
                type="checkbox"
                checked={isDetrended}
                onChange={(e) => setIsDetrended(e.target.checked)}
                className="mr-1"
              />
              Detrend
            </label>
          </div>
          
          {/* Action buttons */}
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
            title="Settings"
          >
            <Settings size={18} />
          </button>
          
          <button
            onClick={resetView}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
            title="Reset view"
          >
            <RotateCcw size={18} />
          </button>
          
          {/* Export dropdown */}
          <div className="relative group">
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded">
              <Download size={18} />
            </button>
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
              <button
                onClick={handleExportData}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Export data (CSV)
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Settings panel */}
      {showSettings && (
        <div className="p-4 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Outlier Threshold (σ)
              </label>
              <input
                type="range"
                min="1"
                max="5"
                step="0.5"
                value={outlierThreshold}
                onChange={(e) => setOutlierThreshold(parseFloat(e.target.value))}
                className="w-full"
              />
              <span className="text-xs text-gray-500">{outlierThreshold}σ</span>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Data Points
              </label>
              <span className="text-sm text-gray-600">{processedData.length.toLocaleString()}</span>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Detected Transits
              </label>
              <span className="text-sm text-gray-600">{transitMarkers.length}</span>
            </div>
          </div>
        </div>
      )}

      {/* Chart */}
      <div ref={chartRef} className="p-4">
        <ResponsiveContainer width="100%" height={isFullscreen ? 600 : 400}>
          <LineChart data={processedData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="time" 
              type="number"
              scale="linear"
              domain={['dataMin', 'dataMax']}
              tickFormatter={(value) => value.toFixed(2)}
              label={{ value: 'Time (days)', position: 'insideBottom', offset: -10 }}
            />
            <YAxis 
              tickFormatter={(value) => value.toFixed(4)}
              label={{ value: isNormalized ? 'Normalized Flux' : 'Relative Flux', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Brush 
              dataKey="time" 
              height={60}
              stroke="#3b82f6"
              fill="#eff6ff"
            />
            
            {/* Transit markers */}
            {transitMarkers.map((transit, i) => (
              <ReferenceLine
                key={i}
                x={transit.start}
                stroke="#ef4444"
                strokeDasharray="2 2"
                strokeWidth={1}
              />
            ))}
            
            <Line
              type="monotone"
              dataKey="flux"
              stroke="#3b82f6"
              strokeWidth={1}
              dot={false}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Transit summary */}
      {transitMarkers.length > 0 && (
        <div className="p-4 bg-blue-50 border-t border-gray-200">
          <h4 className="text-sm font-medium text-blue-900 mb-2">
            Detected Transit Events ({transitMarkers.length})
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 text-xs">
            {transitMarkers.slice(0, 6).map((transit, i) => (
              <div key={i} className="bg-white p-2 rounded">
                <div>Start: {transit.start.toFixed(3)} days</div>
                <div>Duration: {(transit.end - transit.start).toFixed(3)} days</div>
                <div>Depth: {(transit.depth * 1e6).toFixed(0)} ppm</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default LightCurveChart;