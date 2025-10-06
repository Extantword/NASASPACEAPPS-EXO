import React, { useRef, useEffect } from 'react';

/**
 * Componente HydraCanvas - Renderiza visualizaciones de arte generativo con Hydra
 * 
 * Props:
 * - temperatura: Valor de temperatura que afecta los colores (rango: 3000-10000K)
 * - complejidad: Número de segmentos en el kaleidoscopio (rango: 2-12)
 * - velocidad: Velocidad de la animación (rango: 0.05-1.0)
 * - radio: Radio del planeta que afecta efectos especiales (rango: 0.5-5.0)
 */
const HydraCanvas = ({ temperatura, complejidad, velocidad, radio }) => {
  const canvasRef = useRef(null);
  const hydraRef = useRef(null);

  // Inicialización de Hydra (solo una vez)
  useEffect(() => {
    if (canvasRef.current && !hydraRef.current) {
      try {
        // Inicializar Hydra con el canvas específico
        hydraRef.current = new window.Hydra({ 
          canvas: canvasRef.current, 
          detectAudio: false,
          enableStreamCapture: false
        });
        
        console.log('Hydra inicializado correctamente');
      } catch (error) {
        console.error('Error inicializando Hydra:', error);
      }
    }

    // Cleanup al desmontar el componente
    return () => {
      if (hydraRef.current) {
        try {
          hydraRef.current.hush();
        } catch (error) {
          console.error('Error cerrando Hydra:', error);
        }
      }
    };
  }, []);

  // Actualización de la visualización cuando cambian las props
  useEffect(() => {
    if (!hydraRef.current) return;

    try {
      // Funciones para mapear temperatura a colores RGB
      // Implementamos una barra de calor desde azul frío (3000K) hasta rojo caliente (10000K)
      
      /**
       * Mapea un valor de un rango a otro
       * @param {number} value - Valor a mapear
       * @param {number} inMin - Mínimo del rango de entrada
       * @param {number} inMax - Máximo del rango de entrada
       * @param {number} outMin - Mínimo del rango de salida
       * @param {number} outMax - Máximo del rango de salida
       * @returns {number} Valor mapeado
       */
      const map = (value, inMin, inMax, outMin, outMax) => {
        return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
      };

      /**
       * Calcula el componente rojo basado en la temperatura
       * Temperaturas bajas = poco rojo, temperaturas altas = mucho rojo
       */
      const getRed = () => {
        if (temperatura <= 5000) {
          return map(temperatura, 3000, 5000, 0.1, 0.6); // Azul a naranja
        } else {
          return map(temperatura, 5000, 10000, 0.6, 1.0); // Naranja a rojo intenso
        }
      };

      /**
       * Calcula el componente verde basado en la temperatura
       * Máximo verde en temperaturas medias (como el sol)
       */
      const getGreen = () => {
        if (temperatura <= 6000) {
          return map(temperatura, 3000, 6000, 0.2, 0.8); // Incrementa hasta el máximo
        } else {
          return map(temperatura, 6000, 10000, 0.8, 0.3); // Decrece en temperaturas altas
        }
      };

      /**
       * Calcula el componente azul basado en la temperatura
       * Temperaturas bajas = mucho azul, temperaturas altas = poco azul
       */
      const getBlue = () => {
        if (temperatura <= 6000) {
          return map(temperatura, 3000, 6000, 1.0, 0.4); // Decrece desde azul intenso
        } else {
          return map(temperatura, 6000, 10000, 0.4, 0.1); // Muy poco azul en altas temperaturas
        }
      };

      // Generar la visualización fractal con Hydra
      // Usar las funciones globales de Hydra
      const { noise, kaleid, color, rotate, modulatePixelate, modulate, out, o0 } = window;

      // Crear el patrón base con ruido y efectos kaleidoscópicos
      let base = noise(10, velocidad)
        .kaleid(complejidad)
        .color(getRed(), getGreen(), getBlue())
        .rotate(0.009);

      // Aplicar efecto de pixelación si el radio es grande (planetas grandes)
      if (radio > 2.5) {
        base = base.modulatePixelate(noise(25, 0.5), 100);
      }

      // Aplicar modulación recursiva y renderizar
      base
        .modulate(o0, 0.5)
        .out(o0);

    } catch (error) {
      console.error('Error actualizando visualización Hydra:', error);
    }
  }, [temperatura, complejidad, velocidad, radio]);

  return (
    <div className="hydra-container">
      <canvas 
        ref={canvasRef}
        style={{
          width: '100%',
          height: '500px',
          borderRadius: '12px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
          border: '2px solid rgba(255, 255, 255, 0.1)'
        }}
      />
    </div>
  );
};

export default HydraCanvas;