import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Header from './components/common/Header'
import Footer from './components/common/Footer'
import ErrorBoundary from './components/common/ErrorBoundary'
import Home from './pages/Home'
import Explorer from './pages/Explorer'
import Visualizations from './pages/Visualizations'
import MachineLearning from './pages/MachineLearning'
import Learn from './pages/Learn'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <ErrorBoundary>
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/explorer" element={<Explorer />} />
            <Route path="/visualizations" element={<Visualizations />} />
            <Route path="/ml" element={<MachineLearning />} />
            <Route path="/learn" element={<Learn />} />
          </Routes>
        </main>
        <Footer />
      </ErrorBoundary>
    </div>
  )
}

export default App