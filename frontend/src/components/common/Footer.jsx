import React from 'react'
import { Github, ExternalLink } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-black bg-opacity-50 backdrop-blur-md border-t border-white border-opacity-20 mt-auto">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Project Info */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Exoplanet Explorer</h3>
            <p className="text-gray-300 text-sm">
              An interactive tool for exploring and analyzing exoplanet data from NASA missions. 
              Built for the NASA Space Apps Challenge 2024.
            </p>
          </div>

          {/* Data Sources */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Data Sources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a 
                  href="https://exoplanetarchive.ipac.caltech.edu/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-blue-400 flex items-center"
                >
                  NASA Exoplanet Archive
                  <ExternalLink className="h-3 w-3 ml-1" />
                </a>
              </li>
              <li>
                <a 
                  href="https://mast.stsci.edu/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-blue-400 flex items-center"
                >
                  MAST Archive
                  <ExternalLink className="h-3 w-3 ml-1" />
                </a>
              </li>
              <li>
                <a 
                  href="https://docs.lightkurve.org/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-blue-400 flex items-center"
                >
                  Lightkurve
                  <ExternalLink className="h-3 w-3 ml-1" />
                </a>
              </li>
            </ul>
          </div>

          {/* Team & Links */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Team & Code</h3>
            <div className="space-y-2 text-sm">
              <p className="text-gray-300">
                Built with ❤️ for NASA Space Apps Challenge
              </p>
              <a 
                href="https://github.com/Extantword/NASASPACEAPPS-EXO" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-gray-300 hover:text-blue-400 flex items-center"
              >
                <Github className="h-4 w-4 mr-2" />
                View on GitHub
              </a>
              <p className="text-gray-400 text-xs mt-4">
                &copy; 2024 Exoplanet Explorer Team. Open source project.
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer