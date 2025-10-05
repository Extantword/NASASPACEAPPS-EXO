import React from 'react';
import { Link } from 'react-router-dom';

function LearnPage({ accessibleMode, speak }) {
  return (
    <div>
      <header>
        <h1>🧠 Aprende con AstroFeel</h1>
        <p className="subtitle">Educación interactiva sobre astronomía e IA</p>
        <Link to="/" style={{ color: '#00d4ff', textDecoration: 'none', marginTop: '10px', display: 'inline-block' }}>← Volver al inicio</Link>
      </header>

      <div className="page-container">
        <h2 style={{ color: '#00d4ff', marginBottom: '30px' }}>🎓 Academia AstroFeel</h2>
        
        <div className="feature-grid">
          <div className="feature-card">
            <span className="feature-icon">📚</span>
            <h3>Cursos Interactivos</h3>
            <p>Aprende astronomía, física e inteligencia artificial de forma práctica y visual.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🏆</span>
            <h3>Misiones y Logros</h3>
            <p>Completa desafíos educativos y desbloquea nuevos contenidos del universo.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">👥</span>
            <h3>Aprendizaje Colaborativo</h3>
            <p>Conecta con otros exploradores cósmicos y aprende en comunidad.</p>
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '40px', padding: '40px', background: 'rgba(76, 175, 80, 0.1)', borderRadius: '20px' }}>
          <h3 style={{ color: '#4CAF50', marginBottom: '20px' }}>📜 Contenido Educativo</h3>
          <p style={{ fontSize: '1.1em', lineHeight: '1.6' }}>
            Próximamente estarán disponibles lecciones sobre:
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginTop: '30px' }}>
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
    </div>
  );
}

export default LearnPage;