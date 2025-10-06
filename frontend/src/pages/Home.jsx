// PROBLEMA: Home.jsx tenía código duplicado y corrupto que impedía el renderizado correcto
// SOLUCIÓN: Componente limpio que se integra perfectamente con el diseño de AstroApp

import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <>
      <header>
        <h1>🌌 ExoFeel</h1>
        <p className="subtitle">Exploración Multisensorial del Universo con IA</p>
        <p style={{ marginTop: '15px', color: 'rgba(255,255,255,0.7)' }}>
          Experimenta el cosmos a través de todos tus sentidos
        </p>
      </header>

      <div className="galaxy-grid">
        <div className="module-card" onClick={() => navigate('/explorer')}>
          <span className="module-icon">🪐</span>
          <h3 className="module-title">Explorador de Exoplanetas</h3>
          <p className="module-description">
            Visualiza planetas descubiertos en un mapa 3D interactivo. Cada planeta cuenta su propia historia a través de colores, sonidos y datos científicos.
          </p>
        </div>

        <div className="module-card" onClick={() => navigate('/music')}>
          <span className="module-icon">🎵</span>
          <h3 className="module-title">Música Espacial</h3>
          <p className="module-description">
            Convierte datos astronómicos en experiencias sonoras únicas. La IA transforma órbitas y temperaturas en melodías cósmicas.
          </p>
        </div>

        <div className="module-card" onClick={() => navigate('/art')}>
          <span className="module-icon">🎨</span>
          <h3 className="module-title">Arte Generativo</h3>
          <p className="module-description">
            Crea visualizaciones artísticas basadas en datos reales de exoplanetas. Comparte tus creaciones en la galería colaborativa.
          </p>
        </div>

        <div className="module-card" onClick={() => navigate('/learn')}>
          <span className="module-icon">🧠</span>
          <h3 className="module-title">Foro</h3>
          <p className="module-description">
            Lecciones interactivas sobre astronomía e IA. Completa misiones educativas y desbloquea nuevos descubrimientos.
          </p>
        </div>

        <div className="module-card" onClick={() => navigate('/ai')}>
          <span className="module-icon">🤖</span>
          <h3 className="module-title">Crea tu IA</h3>
          <p className="module-description">
            Diseña tus propios modelos de IA para analizar datos espaciales. Sin código, 100% visual e intuitivo.
          </p>
        </div>

        <div className="module-card" onClick={() => navigate('/inclusive')}>
          <span className="module-icon">♿</span>
          <h3 className="module-title">Experiencia Inclusiva</h3>
          <p className="module-description">
            Modo accesible total con narración, vibraciones hápticas y adaptación sensorial para todos los usuarios.
          </p>
        </div>
      </div>
    </>
  );
};

export default Home;