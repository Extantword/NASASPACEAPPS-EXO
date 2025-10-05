import React from 'react';
import { Link } from 'react-router-dom';

function AiBuilderPage({ accessibleMode, speak }) {
  return (
    <div>
      <header>
        <h1>🤖 Crea tu IA</h1>
        <p className="subtitle">Constructor de IA visual sin código</p>
        <Link to="/" style={{ color: '#00d4ff', textDecoration: 'none', marginTop: '10px', display: 'inline-block' }}>← Volver al inicio</Link>
      </header>

      <div className="page-container">
        <h2 style={{ color: '#00d4ff', marginBottom: '30px' }}>🔧 Laboratorio de IA</h2>
        
        <div className="feature-grid">
          <div className="feature-card">
            <span className="feature-icon">🧩</span>
            <h3>Constructor Visual</h3>
            <p>Arrastra y suelta bloques para crear modelos de IA sin escribir código.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">📊</span>
            <h3>Análisis de Datos</h3>
            <p>Procesa grandes conjuntos de datos astronómicos con algoritmos inteligentes.</p>
          </div>
          
          <div className="feature-card">
            <span className="feature-icon">🔍</span>
            <h3>Detección de Patrones</h3>
            <p>Entrena modelos para identificar exoplanetas y fenómenos cósmicos.</p>
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '40px', padding: '40px', background: 'rgba(255, 193, 7, 0.1)', borderRadius: '20px' }}>
          <h3 style={{ color: '#FFC107', marginBottom: '20px' }}>🚀 Plataforma en Construcción</h3>
          <p style={{ fontSize: '1.1em', lineHeight: '1.6' }}>
            Estamos desarrollando una plataforma revolucionaria donde podrás:
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '30px' }}>
            <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
              <h4>📋 Plantillas Predefinidas</h4>
              <p>Modelos pre-configurados para clasificación de exoplanetas, detección de tránsitos y análisis espectral</p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
              <h4>🧠 Redes Neuronales</h4>
              <p>Constructor visual de arquitecturas CNN, RNN y Transformer para datos astronómicos</p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
              <h4>📈 Visualización en Tiempo Real</h4>
              <p>Ve cómo tu IA aprende y mejora con métricas interactivas y gráficos dinámicos</p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255,255,255,0.05)', borderRadius: '10px' }}>
              <h4>🌐 Colaboración Global</h4>
              <p>Comparte tus modelos con la comunidad y colabora en proyectos de investigación</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AiBuilderPage;