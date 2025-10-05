import React from 'react';
import { Link } from 'react-router-dom';

function MusicPage({ accessibleMode, speak }) {
  return (
    <div>
      <header>
        <h1>🎵 Música Espacial</h1>
        <p className="subtitle">Convierte datos astronómicos en experiencias sonoras</p>
        <Link to="/" style={{ color: '#00d4ff', textDecoration: 'none', marginTop: '10px', display: 'inline-block' }}>← Volver al inicio</Link>
      </header>

      <div className="page-container">
        <h2 style={{ color: '#00d4ff', marginBottom: '30px' }}>🌌 Sonificación del Cosmos</h2>
        
        <div className="feature-grid">
          <div className="feature-card">
            <span className="feature-icon">🎹</span>
            <h3>Compositor Cósmico</h3>
            <p>Transforma órbitas planetarias en melodías únicas. Cada exoplaneta tiene su propia firma musical.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🎼</span>
            <h3>Sinfonias Estelares</h3>
            <p>Crea composiciones completas basadas en sistemas planetarios enteros.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🎧</span>
            <h3>Experiencia Inmersiva</h3>
            <p>Audio espacial 3D que te coloca en el centro del cosmos.</p>
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '40px', padding: '40px', background: 'rgba(0, 212, 255, 0.1)', borderRadius: '20px' }}>
          <h3 style={{ color: '#00d4ff', marginBottom: '20px' }}>🎶 Próximamente</h3>
          <p style={{ fontSize: '1.1em', lineHeight: '1.6' }}>
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
    </div>
  );
}

export default MusicPage;