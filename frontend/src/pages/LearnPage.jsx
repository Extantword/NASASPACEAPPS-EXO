import React from 'react';
import { Link } from 'react-router-dom';

function LearnPage({ accessibleMode, speak }) {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">🧠 Aprende con ExoFeel</h1>
        <p className="page-description">Educación interactiva sobre astronomía e IA</p>
        <Link to="/" className="back-button">← Volver al inicio</Link>
      </div>

      <h2 style={{ color: '#06b6d4', marginBottom: '30px', textAlign: 'center' }}>🎓 Academia ExoFeel</h2>
      
      <div className="feature-grid">
        <div className="feature-card">
          <span className="feature-icon">📚</span>
          <h3 className="feature-title">Cursos Interactivos</h3>
          <p className="feature-description">Aprende astronomía, física e inteligencia artificial de forma práctica y visual.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">🏆</span>
          <h3 className="feature-title">Misiones y Logros</h3>
          <p className="feature-description">Completa desafíos educativos y desbloquea nuevos contenidos del universo.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">👥</span>
          <h3 className="feature-title">Aprendizaje Colaborativo</h3>
          <p className="feature-description">Conecta con otros exploradores cósmicos y aprende en comunidad.</p>
        </div>
      </div>
      
      <div className="interactive-demo">
        <h3 style={{ color: '#4CAF50', marginBottom: '20px', textAlign: 'center' }}>📜 Contenido Educativo</h3>
        <p style={{ fontSize: '1.1em', lineHeight: '1.6', textAlign: 'center', marginBottom: '30px' }}>
          Próximamente estarán disponibles lecciones sobre:
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
          <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
            <h4>🌌 Astronomía Básica</h4>
            <p>Sistemas estelares, exoplanetas, galaxias</p>
          </div>
          <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
            <h4>🤖 IA y Machine Learning</h4>
            <p>Algoritmos, redes neuronales, análisis de datos</p>
          </div>
          <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
            <h4>🔭 Métodos de Detección</h4>
            <p>Transit, velocidad radial, microlentes</p>
          </div>
          <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
            <h4>🎯 Habitabilidad</h4>
            <p>Zona habitable, atmósferas, biosignaturas</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LearnPage;