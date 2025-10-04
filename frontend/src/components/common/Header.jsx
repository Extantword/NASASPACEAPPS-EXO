import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Telescope, Menu, X } from 'lucide-react'
import { useState } from 'react'

const Header = () => {
  const location = useLocation()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const navigation = [
    { name: 'Home', href: '/', current: location.pathname === '/' },
    { name: 'Explorer', href: '/explorer', current: location.pathname === '/explorer' },
    { name: 'Visualizations', href: '/visualizations', current: location.pathname === '/visualizations' },
    { name: 'Machine Learning', href: '/ml', current: location.pathname === '/ml' },
    { name: 'Learn', href: '/learn', current: location.pathname === '/learn' },
  ]

  return (
    <header className="bg-black bg-opacity-50 backdrop-blur-md border-b border-white border-opacity-20">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Telescope className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold text-gradient">
                Exoplanet Explorer
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  item.current
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:text-white hover:bg-white hover:bg-opacity-10'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-300 hover:text-white p-2"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                    item.current
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:text-white hover:bg-white hover:bg-opacity-10'
                  }`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </nav>
    </header>
  )
}

export default Header