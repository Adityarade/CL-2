import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Database, FileText, Activity } from 'lucide-react';
import { getStats } from '../services/api';

export default function HomePage() {
  const [stats, setStats] = useState({ papers: 0, genes: 0, diseases: 0, proteins: 0 });
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    getStats().then(setStats).catch(console.error);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <div className="space-y-16">
      <div className="text-center space-y-6 pt-12">
        <h1 className="text-5xl font-extrabold text-slate-900">
          Intelligent Biomedical Search &<br />Knowledge Discovery
        </h1>
        <p className="text-xl text-slate-600 max-w-3xl mx-auto">
          Search biomedical literature, discover biological entities, and explore relationships using modern information retrieval techniques.
        </p>
        
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mt-8 relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search genes, diseases, proteins, drugs or research topics..."
            className="w-full pl-12 pr-4 py-4 rounded-full border-2 border-indigo-100 shadow-lg text-lg focus:outline-none focus:border-indigo-500 transition-colors"
          />
          <Search className="absolute left-4 top-4 h-7 w-7 text-slate-400" />
          <button type="submit" className="absolute right-2 top-2 bottom-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 rounded-full font-medium transition-colors">
            Search
          </button>
        </form>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
        <StatCard icon={<FileText />} title="Research Papers" count={stats.papers} />
        <StatCard icon={<Database />} title="Genes Indexed" count={stats.genes} />
        <StatCard icon={<Activity />} title="Diseases" count={stats.diseases} />
        <StatCard icon={<Database />} title="Proteins" count={stats.proteins} />
      </div>

      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
        <h2 className="text-2xl font-bold mb-6 text-center text-slate-800">How BioIntel Works</h2>
        <div className="flex justify-between items-center text-sm md:text-base font-medium text-slate-600">
          <div className="text-center"><div className="w-16 h-16 mx-auto bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mb-2">1</div>User Query</div>
          <div className="flex-1 h-0.5 bg-slate-200 mx-4"></div>
          <div className="text-center"><div className="w-16 h-16 mx-auto bg-cyan-50 text-cyan-600 rounded-full flex items-center justify-center mb-2">2</div>Text Processing</div>
          <div className="flex-1 h-0.5 bg-slate-200 mx-4"></div>
          <div className="text-center"><div className="w-16 h-16 mx-auto bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mb-2">3</div>TF-IDF + BM25</div>
          <div className="flex-1 h-0.5 bg-slate-200 mx-4"></div>
          <div className="text-center"><div className="w-16 h-16 mx-auto bg-cyan-50 text-cyan-600 rounded-full flex items-center justify-center mb-2">4</div>Semantic Search</div>
          <div className="flex-1 h-0.5 bg-slate-200 mx-4"></div>
          <div className="text-center"><div className="w-16 h-16 mx-auto bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mb-2">5</div>Results</div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, count }: { icon: React.ReactNode, title: string, count: number }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 text-center">
      <div className="text-cyan-600 flex justify-center mb-4">{React.cloneElement(icon as React.ReactElement, { className: 'w-8 h-8' })}</div>
      <div className="text-3xl font-bold text-slate-800 mb-1">{count}</div>
      <div className="text-sm text-slate-500 font-medium">{title}</div>
    </div>
  );
}
