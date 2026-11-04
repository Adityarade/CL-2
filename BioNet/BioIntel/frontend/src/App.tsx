import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { BookOpen, Search, Home, Activity, BarChart2, Clock, Menu } from 'react-lucide';
import HomePage from './pages/HomePage';
import SearchPage from './pages/SearchPage';
import ExplorePage from './pages/ExplorePage';
import AnalyticsPage from './pages/AnalyticsPage';
import HistoryPage from './pages/HistoryPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <nav className="bg-indigo-900 text-white shadow-lg sticky top-0 z-50">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <Link to="/" className="flex items-center space-x-2">
                <Activity className="h-8 w-8 text-cyan-400" />
                <span className="text-xl font-bold tracking-wider">BioIntel</span>
              </Link>
              <div className="hidden md:flex space-x-8">
                <NavLink to="/" icon={<Home className="w-4 h-4" />} text="Home" />
                <NavLink to="/search" icon={<Search className="w-4 h-4" />} text="Search" />
                <NavLink to="/explore" icon={<BookOpen className="w-4 h-4" />} text="Explore" />
                <NavLink to="/analytics" icon={<BarChart2 className="w-4 h-4" />} text="Analytics" />
                <NavLink to="/history" icon={<Clock className="w-4 h-4" />} text="History" />
              </div>
            </div>
          </div>
        </nav>

        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/explore" element={<ExplorePage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
        
        <footer className="bg-slate-900 text-slate-400 py-6 text-center">
          <p>© 2026 BioIntel - Bioinformatics + Information Retrieval Laboratory</p>
        </footer>
      </div>
    </Router>
  );
}

function NavLink({ to, icon, text }: { to: string, icon: React.ReactNode, text: string }) {
  return (
    <Link to={to} className="flex items-center space-x-1 hover:text-cyan-300 transition-colors duration-200">
      {icon}
      <span>{text}</span>
    </Link>
  );
}

export default App;
