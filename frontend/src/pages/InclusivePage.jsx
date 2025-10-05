import React from 'react';
import { Link } from 'react-router-dom';

function InclusivePage({ accessibleMode, speak }) {
  return (
    <div>
      <header>
        <h1>♿ Experiencia Inclusiva</h1>
        <p className="subtitle">Accesibilidad total para todos los usuarios</p>
        <Link to="/" style={{ color: '#00d4ff', textDecoration: 'none', marginTop: '10px', display: 'inline-block' }}>← Volver al inicio</Link>
      </header>

      <div className="page-container">
        <h2 style={{ color: '#00d4ff', marginBottom: '30px' }}>🌌 Cosmos Accesible</h2>
        
        <div className="feature-grid">
          <div className="feature-card">
            <span className="feature-icon">🔊</span>
            <h3>Narración de Voz</h3>
            <p>Sistema completo de síntesis de voz que describe todas las interacciones y contenidos.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">📳</span>
            <h3>Feedback Háptico</h3>
            <p>Vibraciones sincronizadas que traducen experiencias visuales en sensaciones táctiles.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">◐</span>
            <h3>Alto Contraste</h3>
            <p>Modos visuales optimizados para diferentes tipos de visión y preferencias.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">💬</span>
            <h3>Subtítulos Dinámicos</h3>
            <p>Transcripción en tiempo real de todos los contenidos auditivos.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">⌨️</span>
            <h3>Navegación por Teclado</h3>
            <p>Control completo usando solo el teclado con atajos intuitivos.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🌍</span>
            <h3>Multiidioma</h3>
            <p>Interfaz disponible en múltiples idiomas con localización cultural.</p>
          </div>
        </div>
        
        <div style={{ marginTop: '40px', padding: '40px', background: 'rgba(156, 39, 176, 0.1)', borderRadius: '20px' }}>
          <h3 style={{ color: '#9C27B0', marginBottom: '20px', textAlign: 'center' }}>🌱 Principios de Diseño Inclusivo</h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginTop: '30px' }}>
            <div>
              <h4 style={{ color: '#00d4ff', marginBottom: '15px' }}>📋 Perceptible</h4>
              <ul style={{ lineHeight: '1.8', paddingLeft: '20px' }}>
                <li>Múltiples canales sensoriales</li>
                <li>Información adaptable</li>
                <li>Contrastes ajustables</li>
                <li>Tamaños de texto escalables</li>
              </ul>
            </div>
            
            <div>
              <h4 style={{ color: '#4CAF50', marginBottom: '15px' }}>🕹️ Operable</h4>
              <ul style={{ lineHeight: '1.8', paddingLeft: '20px' }}>
                <li>Múltiples métodos de entrada</li>
                <li>Controles de tiempo ajustables</li>
                <li>Navegación consistente</li>
                <li>Evitar contenido que cause convulsiones</li>
              </ul>
            </div>
            
            <div>
              <h4 style={{ color: '#FF9800', marginBottom: '15px' }}>🧠 Comprensible</h4>
              <ul style={{ lineHeight: '1.8', paddingLeft: '20px' }}>
                <li>Lenguaje claro y simple</li>
                <li>Funcionalidad predecible</li>
                <li>Asistencia para errores</li>
                <li>Contexto y ayuda disponibles</li>
              </ul>
            </div>
            
            <div>
              <h4 style={{ color: '#F44336', marginBottom: '15px' }}>🔌 Robusto</h4>
              <ul style={{ lineHeight: '1.8', paddingLeft: '20px' }}>
                <li>Compatible con tecnologías asistivas</li>
                <li>Funciona en diferentes dispositivos</li>
                <li>Actualizable y mantenible</li>
                <li>Estándares web accesibles</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '40px', padding: '30px', background: 'rgba(255,255,255,0.05)', borderRadius: '20px' }}>
          <h3 style={{ color: '#00d4ff', marginBottom: '15px' }}>🚀 Tecnologías Implementadas</h3>
          <p style={{ fontSize: '1.1em', lineHeight: '1.6', marginBottom: '20px' }}>
            AstroFeel utiliza las últimas tecnologías para garantizar una experiencia verdaderamente inclusiva:
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '15px' }}>
            <span style={{ padding: '8px 16px', background: 'rgba(0, 212, 255, 0.2)', borderRadius: '20px' }}>ARIA Standards</span>
            <span style={{ padding: '8px 16px', background: 'rgba(123, 47, 247, 0.2)', borderRadius: '20px' }}>Web Speech API</span>
            <span style={{ padding: '8px 16px', background: 'rgba(76, 175, 80, 0.2)', borderRadius: '20px' }}>Vibration API</span>
            <span style={{ padding: '8px 16px', background: 'rgba(255, 193, 7, 0.2)', borderRadius: '20px' }}>High Contrast</span>
            <span style={{ padding: '8px 16px', background: 'rgba(156, 39, 176, 0.2)', borderRadius: '20px' }}>Keyboard Navigation</span>
            <span style={{ padding: '8px 16px', background: 'rgba(233, 30, 99, 0.2)', borderRadius: '20px' }}>Screen Readers</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InclusivePage;