import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import HydraCanvas from '../components/HydraCanvas';

/**
 * ArtPage - Laboratorio de Arte Generativo
 * 
 * Permite a los usuarios crear visualizaciones artísticas en tiempo real
 * manipulando parámetros que simmulan propiedades de exoplanetas
 */
function ArtPage({ accessibleMode, speak }) {
  // Estados para controlar los parámetros de la visualización Hydra
  // Valores iniciales basados en un exoplaneta típico
  const [temperatura, setTemperatura] = useState(8000);  // Temperatura estelar en Kelvin
  const [complejidad, setComplejidad] = useState(5);     // Complejidad del patrón fractal
  const [velocidad, setVelocidad] = useState(0.2);       // Velocidad de animación
  const [radio, setRadio] = useState(2.6);               // Radio del planeta en radios terrestres

  /**
   * Maneja el cambio de valores en los sliders
   * También proporciona feedback de accesibilidad cuando está habilitado
   */
  const handleSliderChange = (setter, value, paramName) => {
    setter(parseFloat(value));
    
    // Feedback de accesibilidad
    if (accessibleMode && speak) {
      speak(`${paramName} ajustado a ${value}`);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">🎨 Laboratorio de Arte Generativo</h1>
        <p className="page-description">
          Crea arte único basado en propiedades de exoplanetas. 
          Ajusta los controles para explorar diferentes visualizaciones cósmicas.
        </p>
        <Link to="/" className="back-button">← Volver al inicio</Link>
      </div>

      {/* Canvas de Hydra - Visualización principal */}
      <div className="art-canvas-section" style={{ marginBottom: '40px' }}>
        <h2 style={{ 
          color: '#06b6d4', 
          marginBottom: '20px', 
          textAlign: 'center',
          fontSize: '1.5em'
        }}>
          🌌 Tu Obra Cósmica
        </h2>
        
        <HydraCanvas 
          temperatura={temperatura}
          complejidad={complejidad}
          velocidad={velocidad}
          radio={radio}
        />
      </div>

      {/* Sección de Controles Interactivos */}
      <div className="controls-section">
        <h3 style={{ 
          color: '#7c3aed', 
          marginBottom: '30px', 
          textAlign: 'center',
          fontSize: '1.3em'
        }}>
          �️ Controles de Parámetros Planetarios
        </h3>
        
        <div className="controls-grid" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '25px',
          maxWidth: '1000px',
          margin: '0 auto'
        }}>
          
          {/* Control de Temperatura */}
          <div className="control-item" style={{
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '20px',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '10px', 
              fontWeight: 'bold',
              color: '#f97316'
            }}>
              🌡️ Temperatura Estelar: {temperatura.toLocaleString()} K
            </label>
            <input
              type="range"
              min="3000"
              max="10000"
              step="100"
              value={temperatura}
              onChange={(e) => handleSliderChange(setTemperatura, e.target.value, 'Temperatura')}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                background: 'linear-gradient(to right, #3b82f6, #f59e0b, #dc2626)',
                outline: 'none',
                cursor: 'pointer'
              }}
              aria-label="Control de temperatura estelar"
            />
            <div style={{ fontSize: '0.9em', color: '#94a3b8', marginTop: '5px' }}>
              Rango: 3,000K (frío/azul) - 10,000K (caliente/rojo)
            </div>
          </div>

          {/* Control de Complejidad */}
          <div className="control-item" style={{
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '20px',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '10px', 
              fontWeight: 'bold',
              color: '#8b5cf6'
            }}>
              🔮 Complejidad del Patrón: {complejidad}
            </label>
            <input
              type="range"
              min="2"
              max="12"
              step="1"
              value={complejidad}
              onChange={(e) => handleSliderChange(setComplejidad, e.target.value, 'Complejidad')}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                background: 'linear-gradient(to right, #06b6d4, #8b5cf6)',
                outline: 'none',
                cursor: 'pointer'
              }}
              aria-label="Control de complejidad del patrón"
            />
            <div style={{ fontSize: '0.9em', color: '#94a3b8', marginTop: '5px' }}>
              Segmentos del kaleidoscopio: 2 (simple) - 12 (complejo)
            </div>
          </div>

          {/* Control de Velocidad */}
          <div className="control-item" style={{
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '20px',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '10px', 
              fontWeight: 'bold',
              color: '#10b981'
            }}>
              ⚡ Velocidad de Animación: {velocidad.toFixed(2)}
            </label>
            <input
              type="range"
              min="0.05"
              max="1.0"
              step="0.05"
              value={velocidad}
              onChange={(e) => handleSliderChange(setVelocidad, e.target.value, 'Velocidad')}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                background: 'linear-gradient(to right, #1f2937, #10b981)',
                outline: 'none',
                cursor: 'pointer'
              }}
              aria-label="Control de velocidad de animación"
            />
            <div style={{ fontSize: '0.9em', color: '#94a3b8', marginTop: '5px' }}>
              Velocidad orbital: 0.05 (lento) - 1.0 (rápido)
            </div>
          </div>

          {/* Control de Radio */}
          <div className="control-item" style={{
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '20px',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '10px', 
              fontWeight: 'bold',
              color: '#f472b6'
            }}>
              🪐 Radio Planetario: {radio.toFixed(1)} R⊕
            </label>
            <input
              type="range"
              min="0.5"
              max="5.0"
              step="0.1"
              value={radio}
              onChange={(e) => handleSliderChange(setRadio, e.target.value, 'Radio')}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                background: 'linear-gradient(to right, #6366f1, #f472b6)',
                outline: 'none',
                cursor: 'pointer'
              }}
              aria-label="Control de radio planetario"
            />
            <div style={{ fontSize: '0.9em', color: '#94a3b8', marginTop: '5px' }}>
              Tamaño: 0.5 (pequeño) - 5.0 (gigante) radios terrestres
            </div>
          </div>
        </div>
      </div>

      {/* Información sobre la visualización */}
      <div className="info-section" style={{ 
        marginTop: '40px', 
        padding: '25px',
        background: 'rgba(255, 255, 255, 0.03)',
        borderRadius: '12px',
        border: '1px solid rgba(255, 255, 255, 0.1)'
      }}>
        <h4 style={{ color: '#06b6d4', marginBottom: '15px' }}>
          📊 Cómo Funciona Esta Visualización
        </h4>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '20px',
          fontSize: '0.95em',
          lineHeight: '1.6'
        }}>
          <div>
            <strong style={{ color: '#f97316' }}>🌡️ Temperatura:</strong><br/>
            Controla los colores de la visualización simulando la temperatura de la estrella anfitriona.
          </div>
          <div>
            <strong style={{ color: '#8b5cf6' }}>🔮 Complejidad:</strong><br/>
            Determina la cantidad de segmentos en el patrón kaleidoscópico, simulando la complejidad del sistema.
          </div>
          <div>
            <strong style={{ color: '#10b981' }}>⚡ Velocidad:</strong><br/>
            Controla la rapidez de la animación, representando la velocidad orbital del planeta.
          </div>
          <div>
            <strong style={{ color: '#f472b6' }}>🪐 Radio:</strong><br/>
            Afecta los efectos especiales. Planetas grandes (&gt;2.5 R⊕) activan efectos de pixelación.
          </div>
        </div>
      </div>
    </div>
  );
}

export default ArtPage;