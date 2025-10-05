import React from 'react';
import { Link } from 'react-router-dom';

function AiBuilderPage({ accessibleMode, speak }) {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">🤖 Crea tu IA</h1>
        <p className="page-description">Constructor de IA visual sin código</p>
        <Link to="/" className="back-button">← Volver al inicio</Link>
      </div>

      <h2 style={{ color: '#06b6d4', marginBottom: '30px', textAlign: 'center' }}>🔧 Laboratorio de IA</h2>
      
      <div className="feature-grid">
        <div className="feature-card">
          <span className="feature-icon">🧩</span>
          <h3 className="feature-title">Constructor Visual</h3>
          <p className="feature-description">Arrastra y suelta bloques para crear modelos de IA sin escribir código.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">📊</span>
          <h3 className="feature-title">Análisis de Datos</h3>
          <p className="feature-description">Procesa grandes conjuntos de datos astronómicos con algoritmos inteligentes.</p>
        </div>
        
        <div className="feature-card">
          <span className="feature-icon">🔍</span>
          <h3 className="feature-title">Detección de Patrones</h3>
          <p className="feature-description">Entrena modelos para identificar exoplanetas y fenómenos cósmicos.</p>
        </div>
      </div>
      
      <div className="interactive-demo">
        <h3 style={{ color: '#FFC107', marginBottom: '20px', textAlign: 'center' }}>🚀 Plataforma en Construcción</h3>
        <p style={{ fontSize: '1.1em', lineHeight: '1.6', textAlign: 'center', marginBottom: '30px' }}>
          Estamos desarrollando una plataforma revolucionaria donde podrás:
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
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
  );
}

export default AiBuilderPage;