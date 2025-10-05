import React from 'react';
import { Link } from 'react-router-dom';

function ArtPage({ accessibleMode, speak }) {
  return (
    <div>
      <header>
        <h1>🎨 Arte Generativo</h1>
        <p className="subtitle">Visualizaciones artísticas basadas en datos reales</p>
        <Link to="/" style={{ color: '#00d4ff', textDecoration: 'none', marginTop: '10px', display: 'inline-block' }}>← Volver al inicio</Link>
      </header>

      <div className="page-container">
        <h2 style={{ color: '#00d4ff', marginBottom: '30px' }}>🌌 Galería Cósmica</h2>
        
        <div className="feature-grid">
          <div className="feature-card">
            <span className="feature-icon">🌨️</span>
            <h3>Patrones Fractales</h3>
            <p>Algoritmos que interpretan datos de exoplanetas como arte abstracto único.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🌈</span>
            <h3>Paletas Cósmicas</h3>
            <p>Colores generados desde temperaturas, composiciones y espectros reales.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🔄</span>
            <h3>Arte Evolutivo</h3>
            <p>Las obras cambian dinámicamente con nuevos descubrimientos astronómicos.</p>
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '40px', padding: '40px', background: 'rgba(123, 47, 247, 0.1)', borderRadius: '20px' }}>
          <h3 style={{ color: '#7b2ff7', marginBottom: '20px' }}>🖼️ Galería en Desarrollo</h3>
          <p style={{ fontSize: '1.1em', lineHeight: '1.6' }}>
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
    </div>
  );
}

export default ArtPage;