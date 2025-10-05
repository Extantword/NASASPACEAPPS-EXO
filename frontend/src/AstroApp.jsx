import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import ExplorerPage from './pages/ExplorerPage';
import MusicPage from './pages/MusicPage';
import ArtPage from './pages/ArtPage';
import LearnPage from './pages/LearnPage';
import AiBuilderPage from './pages/AiBuilderPage';
import InclusivePage from './pages/InclusivePage';
import './App.css';

// Componente para el campo de estrellas
function StarField() {
  useEffect(() => {
    const starsContainer = document.getElementById('starsContainer');
    if (starsContainer) {
      starsContainer.innerHTML = '';
      for (let i = 0; i < 200; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        starsContainer.appendChild(star);
      }
    }
  }, []);

  return <div className="stars" id="starsContainer"></div>;
}

// Barra de accesibilidad
function AccessibilityBar({ toggleNarrator, toggleContrast, toggleVibration, toggleSubtitles }) {
  return (
    <div className="accessibility-bar">
      <div className="access-btn" onClick={toggleNarrator} title="Narrador de voz">🔊</div>
      <div className="access-btn" onClick={toggleContrast} title="Alto contraste">◐</div>
      <div className="access-btn" onClick={toggleVibration} title="Vibraciones">📳</div>
      <div className="access-btn" onClick={toggleSubtitles} title="Subtítulos">💬</div>
    </div>
  );
}

// Página principal con navegación React Router
function HomePage() {
  const navigate = useNavigate();

  return (
    <>
      <header>
        <h1>🌌 AstroFeel</h1>
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
          <h3 className="module-title">Aprende con AstroFeel</h3>
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
}

// Componente principal de la aplicación
function App() {
  const [accessibleMode, setAccessibleMode] = useState(false);
  const location = useLocation();

  // Función para síntesis de voz
  const speak = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'es-ES';
      utterance.rate = 0.9;
      speechSynthesis.speak(utterance);
    }
  };

  // Funciones de accesibilidad
  const toggleNarrator = () => {
    speak('Narrador activado. Te guiaré por tu experiencia en AstroFeel.');
  };

  const toggleContrast = () => {
    document.body.style.filter = document.body.style.filter === 'contrast(1.5)' ? 'none' : 'contrast(1.5)';
  };

  const toggleVibration = () => {
    if (navigator.vibrate) {
      navigator.vibrate(200);
      alert('Vibraciones activadas');
    } else {
      alert('Tu dispositivo no soporta vibraciones');
    }
  };

  const toggleSubtitles = () => {
    alert('Subtítulos activados - En la versión completa verías subtítulos en tiempo real');
  };

  return (
    <>
      <StarField />
      <div className="container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/explorer" element={<ExplorerPage accessibleMode={accessibleMode} speak={speak} />} />
          <Route path="/music" element={<MusicPage accessibleMode={accessibleMode} speak={speak} />} />
          <Route path="/art" element={<ArtPage accessibleMode={accessibleMode} speak={speak} />} />
          <Route path="/learn" element={<LearnPage accessibleMode={accessibleMode} speak={speak} />} />
          <Route path="/ai" element={<AiBuilderPage accessibleMode={accessibleMode} speak={speak} />} />
          <Route path="/inclusive" element={<InclusivePage accessibleMode={accessibleMode} speak={speak} />} />
        </Routes>
      </div>
      <AccessibilityBar 
        toggleNarrator={toggleNarrator}
        toggleContrast={toggleContrast}
        toggleVibration={toggleVibration}
        toggleSubtitles={toggleSubtitles}
      />
    </>
  );
}

// Componente wrapper con Router
function AppWithRouter() {
  return (
    <Router>
      <App />
    </Router>
  );
}

export default AppWithRouter;