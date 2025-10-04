import React from 'react'
import { Link } from 'react-router-dom'
import { Rocket, Search, BarChart, Brain, BookOpen, Star, Planet } from 'lucide-react'

const Home = () => {
  const features = [
    {
      icon: <Search className="h-8 w-8" />,
      title: "Explore Exoplanets",
      description: "Search and discover thousands of confirmed exoplanets from NASA missions",
      link: "/explorer"
    },
    {
      icon: <BarChart className="h-8 w-8" />,
      title: "Data Visualization",
      description: "Interactive charts and light curve analysis tools",
      link: "/visualizations"
    },
    {
      icon: <Brain className="h-8 w-8" />,
      title: "Machine Learning",
      description: "AI-powered exoplanet classification and validation",
      link: "/ml"
    },
    {
      icon: <BookOpen className="h-8 w-8" />,
      title: "Learn & Discover",
      description: "Educational content about exoplanets and space exploration",
      link: "/learn"
    }
  ]

  const stats = [
    { label: "Confirmed Exoplanets", value: "5,000+", icon: <Planet className="h-6 w-6" /> },
    { label: "Host Stars", value: "3,700+", icon: <Star className="h-6 w-6" /> },
    { label: "NASA Missions", value: "3", icon: <Rocket className="h-6 w-6" /> },
    { label: "Discovery Methods", value: "10+", icon: <Search className="h-6 w-6" /> },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Explore the{' '}
            <span className="text-gradient">
              Universe
            </span>{' '}
            of Exoplanets
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Discover, analyze, and visualize exoplanet data from NASA's Kepler, TESS, and K2 missions. 
            Powered by machine learning and interactive visualizations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/explorer" className="btn-primary inline-flex items-center">
              <Search className="h-5 w-5 mr-2" />
              Start Exploring
            </Link>
            <Link to="/learn" className="btn-secondary inline-flex items-center">
              <BookOpen className="h-5 w-5 mr-2" />
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <div key={index} className="card text-center">
                <div className="text-blue-400 mb-2 flex justify-center">
                  {stat.icon}
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-300">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              Powerful Tools for Exoplanet Research
            </h2>
            <p className="text-gray-300 max-w-2xl mx-auto">
              From data exploration to machine learning, our platform provides comprehensive tools 
              for analyzing exoplanet discoveries.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Link key={index} to={feature.link} className="group">
                <div className="card h-full text-center group-hover:scale-105 transition-transform">
                  <div className="text-blue-400 mb-4 flex justify-center">
                    {feature.icon}
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-300 text-sm">
                    {feature.description}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="card">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
              <div>
                <h2 className="text-3xl font-bold text-white mb-4">
                  Data from NASA Space Missions
                </h2>
                <p className="text-gray-300 mb-6">
                  Our platform integrates data from multiple NASA missions including Kepler, TESS, and K2, 
                  providing access to light curves, planetary parameters, and discovery information for 
                  thousands of confirmed exoplanets.
                </p>
                <div className="space-y-3">
                  <div className="flex items-center text-sm">
                    <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                    <span className="text-gray-300">Kepler Mission (2009-2013)</span>
                  </div>
                  <div className="flex items-center text-sm">
                    <div className="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
                    <span className="text-gray-300">K2 Extended Mission (2014-2018)</span>
                  </div>
                  <div className="flex items-center text-sm">
                    <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                    <span className="text-gray-300">TESS Mission (2018-Present)</span>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <div className="relative inline-block">
                  <div className="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <Rocket className="h-16 w-16 text-white" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-yellow-500 rounded-full animate-pulse"></div>
                  <div className="absolute -bottom-2 -left-2 w-6 h-6 bg-green-500 rounded-full animate-pulse"></div>
                </div>
                <p className="text-gray-300 text-sm">
                  Real-time data from active missions
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home