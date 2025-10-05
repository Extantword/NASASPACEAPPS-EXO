import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';

const exoplanets = [
  { name: 'Kepler-452b', color: '#4CAF50', temp: 265, size: 1.6, sound: 'C' },
  { name: 'TRAPPIST-1e', color: '#2196F3', temp: 246, size: 0.92, sound: 'E' },
  { name: 'Proxima b', color: '#FF5722', temp: 234, size: 1.3, sound: 'G' },
  { name: 'HD 209458b', color: '#FFC107', temp: 1130, size: 1.38, sound: 'A' },
  { name: 'GJ 1214b', color: '#9C27B0', temp: 393, size: 2.68, sound: 'D' },
  { name: '55 Cancri e', color: '#E91E63', temp: 2700, size: 2.0, sound: 'F' }
];

function ExplorerPage({ accessibleMode, speak }) {
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const canvasRef = useRef(null);
  const soundWaveRef = useRef(null);

  useEffect(() => {
    // Generar barras de onda de sonido
    const soundWave = soundWaveRef.current;
    if (soundWave) {
      soundWave.innerHTML = '';
      for (let i = 0; i < 50; i++) {
        const bar = document.createElement('div');
        bar.className = 'wave-bar';
        bar.style.left = (i * 2) + '%';
        bar.style.animationDelay = (i * 0.05) + 's';
        soundWave.appendChild(bar);
      }
    }
  }, []);

  const createParticleExplosion = (color) => {
    for (let i = 0; i < 50; i++) {
      const particle = document.createElement('div');
      particle.style.position = 'fixed';
      particle.style.width = Math.random() * 10 + 5 + 'px';
      particle.style.height = particle.style.width;
      particle.style.background = color;
      particle.style.borderRadius = '50%';
      particle.style.left = '50%';
      particle.style.top = '50%';
      particle.style.pointerEvents = 'none';
      particle.style.zIndex = '9999';
      particle.style.boxShadow = `0 0 20px ${color}`;
      
      const angle = (Math.PI * 2 * i) / 50;
      const velocity = Math.random() * 300 + 200;
      const tx = Math.cos(angle) * velocity;
      const ty = Math.sin(angle) * velocity;
      
      document.body.appendChild(particle);
      
      particle.animate([
        { transform: 'translate(-50%, -50%) scale(1)', opacity: 1 },
        { transform: `translate(calc(-50% + ${tx}px), calc(-50% + ${ty}px)) scale(0)`, opacity: 0 }
      ], {
        duration: 1500,
        easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      }).onfinish = () => particle.remove();
    }
  };

  const createRippleEffect = (color) => {
    for (let i = 0; i < 3; i++) {
      setTimeout(() => {
        const ripple = document.createElement('div');
        ripple.style.position = 'fixed';
        ripple.style.left = '50%';
        ripple.style.top = '50%';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.width = '100px';
        ripple.style.height = '100px';
        ripple.style.border = `3px solid ${color}`;
        ripple.style.borderRadius = '50%';
        ripple.style.pointerEvents = 'none';
        ripple.style.zIndex = '9998';
        
        document.body.appendChild(ripple);
        
        ripple.animate([
          { width: '100px', height: '100px', opacity: 1 },
          { width: '2000px', height: '2000px', opacity: 0 }
        ], {
          duration: 2000,
          easing: 'ease-out'
        }).onfinish = () => ripple.remove();
      }, i * 300);
    }
  };

  const playSoundEffect = (planet) => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const notes = { C: 261.63, D: 293.66, E: 329.63, F: 349.23, G: 392.00, A: 440.00 };
    
    // Crear múltiples osciladores para un sonido más rico
    for (let i = 0; i < 3; i++) {
      setTimeout(() => {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.frequency.setValueAtTime(notes[planet.sound] * (1 + i * 0.5), audioContext.currentTime);
        oscillator.type = i === 0 ? 'sine' : 'triangle';
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1.5);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 1.5);
      }, i * 200);
    }
  };

  const selectPlanet = (planet) => {
    setSelectedPlanet(planet);
    
    // Cambiar el color de fondo con animación
    document.body.style.transition = 'all 1.5s ease';
    document.body.style.background = `radial-gradient(circle at center, ${planet.color}33 0%, #0a0e27 40%, #1a1042 70%, #2d1b69 100%)`;
    
    // Crear partículas explosivas
    createParticleExplosion(planet.color);
    
    // Reproducir sonido automáticamente
    playSoundEffect(planet);
    
    // Hacer vibrar si está disponible
    if (navigator.vibrate) {
      navigator.vibrate([100, 50, 100, 50, 200]);
    }
    
    // Animación de pulso en todas las estrellas
    document.querySelectorAll('.star').forEach(star => {
      star.style.background = planet.color;
      star.style.boxShadow = `0 0 10px ${planet.color}`;
    });
    
    // Crear anillos expansivos
    createRippleEffect(planet.color);
    
    // Cambiar color de las barras de sonido
    document.querySelectorAll('.wave-bar').forEach(bar => {
      bar.style.background = `linear-gradient(to top, ${planet.color}, ${planet.color}99)`;
    });
    
    if (accessibleMode) {
      speak(`Has seleccionado ${planet.name}. Temperatura ${planet.temp} Kelvin. Tamaño ${planet.size} veces la Tierra.`);
    }
  };

  const playSound = () => {
    if (!selectedPlanet) {
      alert('Primero selecciona un exoplaneta');
      return;
    }
    
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    const notes = { C: 261.63, D: 293.66, E: 329.63, F: 349.23, G: 392.00, A: 440.00 };
    oscillator.frequency.setValueAtTime(notes[selectedPlanet.sound], audioContext.currentTime);
    oscillator.type = 'sine';
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 2);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 2);
    
    if (accessibleMode && navigator.vibrate) {
      navigator.vibrate([200, 100, 200]);
    }
  };

  const generateArt = () => {
    if (!selectedPlanet) {
      alert('Primero selecciona un exoplaneta');
      return;
    }
    
    setIsModalOpen(true);
    setTimeout(() => {
      drawGenerativeArt();
    }, 100);
  };

  const drawGenerativeArt = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Limpiar canvas
    ctx.fillStyle = '#0a0e27';
    ctx.fillRect(0, 0, width, height);
    
    const planet = selectedPlanet;
    const centerX = width / 2;
    const centerY = height / 2;
    
    // Estilo basado en temperatura
    const isHot = planet.temp > 500;
    const patternCount = Math.floor(planet.size * 30);
    
    // Fondo de galaxia
    for (let i = 0; i < 200; i++) {
      const x = Math.random() * width;
      const y = Math.random() * height;
      const size = Math.random() * 2;
      ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.8})`;
      ctx.beginPath();
      ctx.arc(x, y, size, 0, Math.PI * 2);
      ctx.fill();
    }
    
    // Patrón principal basado en los datos del planeta
    if (isHot) {
      // Patrón de energía caótica para planetas calientes
      for (let i = 0; i < patternCount; i++) {
        const angle = (Math.PI * 2 * i) / patternCount;
        const radius = 50 + Math.sin(i * 0.5) * 100 + (planet.temp / 20);
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, 30);
        gradient.addColorStop(0, planet.color + 'ff');
        gradient.addColorStop(0.5, planet.color + '88');
        gradient.addColorStop(1, planet.color + '00');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, 20 + Math.random() * 10, 0, Math.PI * 2);
        ctx.fill();
        
        // Líneas de energía
        ctx.strokeStyle = planet.color + '44';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
    } else {
      // Patrón de ondas suaves para planetas fríos
      for (let ring = 0; ring < 10; ring++) {
        ctx.strokeStyle = planet.color + Math.floor(255 - ring * 20).toString(16);
        ctx.lineWidth = 3;
        
        ctx.beginPath();
        for (let angle = 0; angle < Math.PI * 2; angle += 0.1) {
          const waveOffset = Math.sin(angle * (planet.size * 5) + ring) * 20;
          const radius = 50 + ring * 25 + waveOffset;
          const x = centerX + Math.cos(angle) * radius;
          const y = centerY + Math.sin(angle) * radius;
          
          if (angle === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.closePath();
        ctx.stroke();
      }
    }
    
    // Planeta central
    const planetGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 60);
    planetGradient.addColorStop(0, planet.color + 'ff');
    planetGradient.addColorStop(0.7, planet.color + 'cc');
    planetGradient.addColorStop(1, planet.color + '00');
    
    ctx.fillStyle = planetGradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 60, 0, Math.PI * 2);
    ctx.fill();
    
    // Detalles fractales
    for (let i = 0; i < 50; i++) {
      const angle = Math.random() * Math.PI * 2;
      const distance = Math.random() * 200 + 80;
      const x = centerX + Math.cos(angle) * distance;
      const y = centerY + Math.sin(angle) * distance;
      
      ctx.fillStyle = planet.color + '66';
      ctx.beginPath();
      
      // Formas basadas en la nota musical
      const sides = { C: 3, D: 4, E: 5, F: 6, G: 7, A: 8 }[planet.sound];
      const size = Math.random() * 10 + 5;
      
      for (let j = 0; j < sides; j++) {
        const vertexAngle = (Math.PI * 2 * j) / sides;
        const vx = x + Math.cos(vertexAngle) * size;
        const vy = y + Math.sin(vertexAngle) * size;
        if (j === 0) ctx.moveTo(vx, vy);
        else ctx.lineTo(vx, vy);
      }
      ctx.closePath();
      ctx.fill();
    }
    
    // Partículas orbitales
    for (let i = 0; i < 100; i++) {
      const angle = (Math.PI * 2 * i) / 100;
      const orbitRadius = 150 + Math.sin(i * 0.3) * 50;
      const x = centerX + Math.cos(angle) * orbitRadius;
      const y = centerY + Math.sin(angle) * orbitRadius;
      
      ctx.fillStyle = planet.color + 'aa';
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, Math.PI * 2);
      ctx.fill();
    }
    
    // Texto de datos
    ctx.fillStyle = planet.color;
    ctx.font = 'bold 16px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`${planet.name.toUpperCase()}`, centerX, 30);
    
    ctx.font = '12px monospace';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.fillText(`TEMP: ${planet.temp}K | SIZE: ${planet.size}x | NOTE: ${planet.sound}`, centerX, height - 20);
  };

  const regenerateArt = () => {
    drawGenerativeArt();
    if (navigator.vibrate) {
      navigator.vibrate(50);
    }
  };

  const downloadArt = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const link = document.createElement('a');
    link.download = `astrofeel-${selectedPlanet.name}-${Date.now()}.png`;
    link.href = canvas.toDataURL();
    link.click();
    
    if (accessibleMode) {
      speak('Arte descargado exitosamente');
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">🪐 Explorador de Exoplanetas</h1>
        <p className="page-description">Descubre mundos distantes a través de datos reales</p>
        <Link to="/" className="back-button">← Volver al inicio</Link>
      </div>

      <div className="interactive-demo">
        <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#06b6d4' }}>
          🌟 Demo Interactiva: Explorador de Exoplanetas
        </h2>

        <div className="exoplanet-viewer">
          {exoplanets.map((planet, index) => (
            <div key={index} style={{ textAlign: 'center' }}>
              <div 
                className="planet"
                style={{
                  background: `radial-gradient(circle at 30% 30%, ${planet.color}, ${planet.color}dd)`,
                  color: planet.color
                }}
                onClick={() => selectPlanet(planet)}
              />
              <div className="planet-info">
                <strong>{planet.name}</strong><br />{planet.temp}K
              </div>
            </div>
          ))}
        </div>

        <div className="sound-wave" ref={soundWaveRef}></div>

        <div className="demo-controls">
          <button className="control-button" onClick={playSound}>🎵 Reproducir Sonido Cósmico</button>
          <button className="control-button" onClick={generateArt}>🎨 Generar Arte</button>
        </div>

        <div id="planetDescription" style={{ textAlign: 'center', marginTop: '20px', minHeight: '60px', fontSize: '1.1em', lineHeight: '1.6' }}>
          {selectedPlanet && (
            <span>
              <span style={{ color: selectedPlanet.color, fontSize: '1.3em' }}>✨ {selectedPlanet.name}</span><br /><br />
              Temperatura: {selectedPlanet.temp}K | Tamaño: {selectedPlanet.size}x Tierra | Nota musical: {selectedPlanet.sound}<br /><br />
              Este exoplaneta emite una frecuencia única que puedes escuchar y sentir.
            </span>
          )}
        </div>
      </div>

      {/* Modal de Arte Generativo */}
      {isModalOpen && selectedPlanet && (
        <div className="modal" style={{ display: 'flex' }}>
          <div className="modal-content">
            <span className="close-modal" onClick={closeModal}>&times;</span>
            <h2 style={{ color: selectedPlanet.color, marginBottom: '20px' }}>
              🎨 Arte Generativo: {selectedPlanet.name}
            </h2>
            <canvas 
              ref={canvasRef} 
              width="500" 
              height="500" 
              style={{ borderRadius: '15px', boxShadow: `0 0 30px ${selectedPlanet.color}88` }}
            />
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center' }}>
              <button className="control-button" onClick={regenerateArt} style={{ padding: '10px 20px' }}>🔄 Regenerar</button>
              <button className="control-button" onClick={downloadArt} style={{ padding: '10px 20px' }}>💾 Descargar</button>
            </div>
            <p style={{ marginTop: '15px', textAlign: 'center', color: 'rgba(255,255,255,0.7)' }}>
              Basado en: Temp {selectedPlanet.temp}K | Tamaño {selectedPlanet.size}x | Nota {selectedPlanet.sound}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default ExplorerPage;