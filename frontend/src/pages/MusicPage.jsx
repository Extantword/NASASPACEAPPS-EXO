import React from 'react';
import { Link } from 'react-router-dom';

function MusicPage({ accessibleMode, speak }) {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">🎵 Música Espacial</h1>
        <p className="page-description">Convierte datos astronómicos en experiencias sonoras</p>
        <Link to="/" className="back-button">← Volver al inicio</Link>
      </div>

      <h2 style={{ color: '#06b6d4', marginBottom: '30px', textAlign: 'center' }}>🌌 Sonificación del Cosmos</h2>
      
      <div className="feature-grid">
        <div className="feature-card">
          <span className="feature-icon">🎹</span>
          <h3 className="feature-title">Compositor Cósmico</h3>
          <p className="feature-description">Transforma órbitas planetarias en melodías únicas. Cada exoplaneta tiene su propia firma musical.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">🎼</span>
          <h3 className="feature-title">Sinfonias Estelares</h3>
          <p className="feature-description">Crea composiciones completas basadas en sistemas planetarios enteros.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">🎧</span>
          <h3 className="feature-title">Experiencia Inmersiva</h3>
          <p className="feature-description">Audio espacial 3D que te coloca en el centro del cosmos.</p>
        </div>
      </div>
      
      <div className="interactive-demo">
        <h3 style={{ color: '#06b6d4', marginBottom: '20px', textAlign: 'center' }}>🎶 Próximamente</h3>
        <p style={{ fontSize: '1.1em', lineHeight: '1.6', textAlign: 'center', marginBottom: '20px' }}>
          Aquí estará el generador de música basado en exoplanetas. <br/>
          Cada planeta tendrá su propia sonificación basada en sus propiedades físicas:
        </p>
        <ul style={{ textAlign: 'left', maxWidth: '500px', margin: '20px auto', lineHeight: '1.8' }}>
          <li>Temperatura → Tono</li>
          <li>Tamaño → Volumen</li>
          <li>Distancia orbital → Ritmo</li>
          <li>Composición atmosférica → Timbre</li>
        </ul>
      </div>
    </div>
  );
}

export default MusicPage;