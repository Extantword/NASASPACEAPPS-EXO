import React from 'react'
import { BookOpen, Star, Telescope, Globe, Zap, Target } from 'lucide-react'

const Learn = () => {
  const concepts = [
    {
      icon: <Globe className="h-8 w-8" />,
      title: "What is an Exoplanet?",
      description: "An exoplanet is a planet that orbits a star outside our solar system. These distant worlds come in many sizes and compositions.",
      details: [
        "Also called 'extrasolar planets'",
        "First confirmed in 1995",
        "Over 5,000 confirmed to date",
        "Many more candidates await confirmation"
      ]
    },
    {
      icon: <Target className="h-8 w-8" />,
      title: "Detection Methods",
      description: "Scientists use various techniques to discover exoplanets, each with unique advantages and limitations.",
      details: [
        "Transit photometry - measures star dimming",
        "Radial velocity - detects stellar wobble",
        "Direct imaging - photographs the planet",
        "Gravitational microlensing - uses gravity as lens"
      ]
    },
    {
      icon: <Telescope className="h-8 w-8" />,
      title: "NASA Missions",
      description: "Space telescopes have revolutionized exoplanet discovery with unprecedented precision and scope.",
      details: [
        "Kepler (2009-2013) - First dedicated planet hunter",
        "K2 (2014-2018) - Extended Kepler mission",
        "TESS (2018-present) - All-sky survey",
        "James Webb - Atmospheric analysis"
      ]
    },
    {
      icon: <Zap className="h-8 w-8" />,
      title: "Light Curves",
      description: "Light curves show how a star's brightness changes over time, revealing transiting planets.",
      details: [
        "Periodic dips indicate planet transits",
        "Depth reveals planet size",
        "Duration shows orbital distance",
        "Shape provides atmospheric clues"
      ]
    }
  ]

  const glossary = [
    {
      term: "Transit",
      definition: "When a planet passes in front of its host star, causing a temporary dimming of the star's light."
    },
    {
      term: "Habitable Zone",
      definition: "The region around a star where liquid water could exist on a planet's surface."
    },
    {
      term: "Hot Jupiter",
      definition: "A gas giant planet that orbits very close to its host star, completing an orbit in days."
    },
    {
      term: "Super-Earth",
      definition: "A planet larger than Earth but smaller than Neptune, typically 1.25 to 2 Earth radii."
    },
    {
      term: "Orbital Period",
      definition: "The time it takes for a planet to complete one orbit around its host star."
    },
    {
      term: "Radial Velocity",
      definition: "The speed at which a star moves toward or away from Earth due to gravitational pull from orbiting planets."
    },
    {
      term: "Light Curve",
      definition: "A graph showing how the brightness of a star changes over time."
    },
    {
      term: "False Positive",
      definition: "A detection that initially appears to be a planet but is later determined to be caused by other phenomena."
    }
  ]

  const missionDetails = [
    {
      name: "Kepler Space Telescope",
      period: "2009-2013",
      discoveries: "2,600+ confirmed planets",
      method: "Transit photometry",
      achievement: "Proved Earth-sized planets are common"
    },
    {
      name: "K2 Mission",
      period: "2014-2018", 
      discoveries: "500+ confirmed planets",
      method: "Transit photometry",
      achievement: "Expanded search to different star fields"
    },
    {
      name: "TESS",
      period: "2018-Present",
      discoveries: "7,000+ candidates",
      method: "All-sky transit survey",
      achievement: "Surveys entire sky for nearby exoplanets"
    }
  ]

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-white mb-4">
            Learn About Exoplanets
          </h1>
          <p className="text-gray-300 max-w-2xl mx-auto">
            Discover the fascinating world of planets beyond our solar system and the 
            cutting-edge science behind their detection and characterization.
          </p>
        </div>

        {/* Key Concepts */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">Key Concepts</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {concepts.map((concept, index) => (
              <div key={index} className="card">
                <div className="flex items-start space-x-4">
                  <div className="text-blue-400 mt-1">
                    {concept.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {concept.title}
                    </h3>
                    <p className="text-gray-300 text-sm mb-3">
                      {concept.description}
                    </p>
                    <ul className="space-y-1">
                      {concept.details.map((detail, i) => (
                        <li key={i} className="text-gray-400 text-xs flex items-start">
                          <span className="text-blue-400 mr-2">•</span>
                          {detail}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* NASA Missions */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-8 text-center">NASA Exoplanet Missions</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {missionDetails.map((mission, index) => (
              <div key={index} className="card text-center">
                <div className="mb-4">
                  <Star className="h-12 w-12 text-blue-400 mx-auto mb-2" />
                  <h3 className="text-lg font-semibold text-white">
                    {mission.name}
                  </h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Period:</span>
                    <span className="text-white">{mission.period}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Discoveries:</span>
                    <span className="text-white">{mission.discoveries}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Method:</span>
                    <span className="text-white">{mission.method}</span>
                  </div>
                </div>
                <div className="mt-3 p-2 bg-white bg-opacity-5 rounded">
                  <p className="text-gray-300 text-xs">
                    {mission.achievement}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Interactive Demo */}
        <section className="mb-12">
          <div className="card">
            <h2 className="text-2xl font-bold text-white mb-6">Understanding Transit Photometry</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">How It Works</h3>
                <div className="space-y-3 text-sm text-gray-300">
                  <div className="flex items-start">
                    <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 mt-0.5">1</span>
                    <p>A planet orbits between its star and Earth</p>
                  </div>
                  <div className="flex items-start">
                    <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 mt-0.5">2</span>
                    <p>During transit, the planet blocks a small amount of starlight</p>
                  </div>
                  <div className="flex items-start">
                    <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 mt-0.5">3</span>
                    <p>We detect this as a periodic dimming in the light curve</p>
                  </div>
                  <div className="flex items-start">
                    <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs mr-3 mt-0.5">4</span>
                    <p>The depth and duration reveal planet properties</p>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <div className="bg-white bg-opacity-5 rounded-lg p-6">
                  <div className="relative">
                    <div className="w-16 h-16 bg-yellow-400 rounded-full mx-auto mb-4 flex items-center justify-center">
                      <Star className="h-8 w-8 text-yellow-900" />
                    </div>
                    <div className="w-4 h-4 bg-blue-500 rounded-full absolute top-6 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
                    <p className="text-gray-300 text-sm">Planet Transit Event</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Glossary */}
        <section>
          <h2 className="text-2xl font-bold text-white mb-8 text-center">Glossary</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {glossary.map((item, index) => (
              <div key={index} className="card">
                <h3 className="text-lg font-semibold text-white mb-2">
                  {item.term}
                </h3>
                <p className="text-gray-300 text-sm">
                  {item.definition}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Resources */}
        <section className="mt-12">
          <div className="card text-center">
            <h2 className="text-2xl font-bold text-white mb-6">Additional Resources</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <a 
                href="https://exoplanets.nasa.gov/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn-secondary flex items-center justify-center"
              >
                <BookOpen className="h-4 w-4 mr-2" />
                NASA Exoplanets
              </a>
              <a 
                href="https://exoplanetarchive.ipac.caltech.edu/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn-secondary flex items-center justify-center"
              >
                <Telescope className="h-4 w-4 mr-2" />
                Exoplanet Archive
              </a>
              <a 
                href="https://tess.mit.edu/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="btn-secondary flex items-center justify-center"
              >
                <Star className="h-4 w-4 mr-2" />
                TESS Mission
              </a>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default Learn