import React from 'react'
import { Github, ExternalLink } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-gray-900 border-t border-gray-800">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Project Info */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Exoplanet Explorer</h3>
            <p className="text-gray-400 text-sm">
              NASA Space Apps Challenge 2024 project for exploring and analyzing exoplanets 
              discovered by Kepler, TESS, and K2 missions.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a 
                  href="https://exoplanetarchive.ipac.caltech.edu/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white text-sm flex items-center space-x-1"
                >
                  <ExternalLink className="h-3 w-3" />
                  <span>NASA Exoplanet Archive</span>
                </a>
              </li>
              <li>
                <a 
                  href="https://mast.stsci.edu/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white text-sm flex items-center space-x-1"
                >
                  <ExternalLink className="h-3 w-3" />
                  <span>MAST Archive</span>
                </a>
              </li>
              <li>
                <a 
                  href="https://docs.lightkurve.org/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white text-sm flex items-center space-x-1"
                >
                  <ExternalLink className="h-3 w-3" />
                  <span>Lightkurve Documentation</span>
                </a>
              </li>
            </ul>
          </div>

          {/* Team */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Team</h3>
            <div className="flex items-center space-x-4">
              <a 
                href="https://github.com/your-team/exoplanet-explorer" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-white"
              >
                <Github className="h-6 w-6" />
              </a>
            </div>
            <p className="text-gray-500 text-xs mt-4">
              Built with ❤️ for NASA Space Apps Challenge 2024
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-4">
          <p className="text-center text-gray-500 text-xs">
            Data courtesy of NASA/IPAC.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer