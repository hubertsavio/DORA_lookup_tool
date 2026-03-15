import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import SearchPage from './pages/SearchPage'
import DocumentDetailPage from './pages/DocumentDetailPage'
import AboutPage from './pages/AboutPage'

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/document/:id" element={<DocumentDetailPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

// Made with Bob
