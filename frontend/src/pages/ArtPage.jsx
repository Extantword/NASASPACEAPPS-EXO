import React from 'react';
import { Link } from 'react-router-dom';

function ArtPage({ accessibleMode, speak }) {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">🎨 Arte Generativo</h1>
        <p className="page-description">Visualizaciones artísticas basadas en datos reales</p>
        <Link to="/" className="back-button">← Volver al inicio</Link>
      </div>

      <h2 style={{ color: '#06b6d4', marginBottom: '30px', textAlign: 'center' }}>🌌 Galería Cósmica</h2>
      
      <div className="feature-grid">
        <div className="feature-card">
          <span className="feature-icon">🌨️</span>
          <h3 className="feature-title">Patrones Fractales</h3>
          <p className="feature-description">Algoritmos que interpretan datos de exoplanetas como arte abstracto único.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">🌈</span>
          <h3 className="feature-title">Paletas Cósmicas</h3>
          <p className="feature-description">Colores generados desde temperaturas, composiciones y espectros reales.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">🔄</span>
          <h3 className="feature-title">Arte Evolutivo</h3>
          <p className="feature-description">Las obras cambian dinámicamente con nuevos descubrimientos astronómicos.</p>
        </div>
      </div>
      
      <div className="interactive-demo">
        <h3 style={{ color: '#7c3aed', marginBottom: '20px', textAlign: 'center' }}>🖼️ Galería en Desarrollo</h3>
        <p style={{ fontSize: '1.1em', lineHeight: '1.6', textAlign: 'center', marginBottom: '20px' }}>
          Aquí se mostrará la galería de arte generativo colaborativa. <br/>
          Los usuarios podrán:
        </p>
        <ul style={{ textAlign: 'left', maxWidth: '500px', margin: '20px auto', lineHeight: '1.8' }}>
          <li>Crear arte único basado en datos de exoplanetas</li>
          <li>Compartir sus creaciones con la comunidad</li>
          <li>Colaborar en obras colectivas</li>
          <li>Descargar e imprimir sus diseños</li>
          <li>Participar en desafíos artísticos temáticos</li>
        </ul>
      </div>
    </div>
  );
}

export default ArtPage;