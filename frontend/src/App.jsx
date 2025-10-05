import React, { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import ExplorerPage from './pages/ExplorerPage'
import MusicPage from './pages/MusicPage'
import ArtPage from './pages/ArtPage'
import LearnPage from './pages/LearnPage'
import AiBuilderPage from './pages/AiBuilderPage'
import InclusivePage from './pages/InclusivePage'
import './index.css'

// Componente para exoplanetas flotantes de fondo
function FloatingPlanets() {
  useEffect(() => {
    const floatingPlanetsContainer = document.getElementById('floatingPlanets');
    if (floatingPlanetsContainer) {
      floatingPlanetsContainer.innerHTML = '';
      const planetColors = [
        'linear-gradient(135deg, #7c3aed, #ec4899)',
        'linear-gradient(135deg, #06b6d4, #7c3aed)',
        'linear-gradient(135deg, #ec4899, #f59e0b)',
        'linear-gradient(135deg, #10b981, #06b6d4)',
        'linear-gradient(135deg, #f59e0b, #ec4899)'
      ];

      for (let i = 0; i < 15; i++) {
        const planet = document.createElement('div');
        planet.className = 'exoplanet';
        const size = Math.random() * 200 + 50;
        planet.style.width = size + 'px';
        planet.style.height = size + 'px';
        planet.style.left = Math.random() * 100 + '%';
        planet.style.top = Math.random() * 100 + '%';
        planet.style.background = planetColors[Math.floor(Math.random() * planetColors.length)];
        planet.style.animationDelay = Math.random() * 20 + 's';
        planet.style.animationDuration = (Math.random() * 15 + 15) + 's';
        planet.style.opacity = Math.random() * 0.3 + 0.1;
        floatingPlanetsContainer.appendChild(planet);
      }
    }
  }, []);

  return <div className="floating-planets" id="floatingPlanets"></div>;
}

// Componente para el campo de estrellas
function StarField() {
  useEffect(() => {
    const starsContainer = document.getElementById('starsContainer');
    if (starsContainer) {
      starsContainer.innerHTML = '';
      for (let i = 0; i < 400; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 3 + 1;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        star.style.animationDuration = (Math.random() * 2 + 2) + 's';
        starsContainer.appendChild(star);
      }
    }
  }, []);

  return <div className="stars" id="starsContainer"></div>;
}

// Componente de navegación
function Navigation() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <nav>
      <div className="nav-container">
        <div className="logo">
          <img src="/logo.png" alt="ExoFeel Logo" className="logo-icon" />
          ExoFeel
        </div>
        <ul className="nav-links">
          <li><a href="#" onClick={(e) => { e.preventDefault(); navigate('/'); }}>Inicio</a></li>
          <li><a href="#" onClick={(e) => { e.preventDefault(); navigate('/explorer'); }}>Explorador</a></li>
          <li><a href="#" onClick={(e) => { e.preventDefault(); navigate('/music'); }}>Música</a></li>
          <li><a href="#" onClick={(e) => { e.preventDefault(); navigate('/art'); }}>Arte</a></li>
          <li><a href="#" onClick={(e) => { e.preventDefault(); navigate('/learn'); }}>Foro</a></li>
          <li><a href="#" onClick={(e) => { e.preventDefault(); navigate('/ai'); }}>IA</a></li>
        </ul>
      </div>
    </nav>
  );
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

function App() {
  const [accessibleMode, setAccessibleMode] = useState(false);

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
    speak('Narrador activado. Te guiaré por tu experiencia en ExoFeel.');
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
      <FloatingPlanets />
      <StarField />
      <Navigation />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
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
  )
}

export default App