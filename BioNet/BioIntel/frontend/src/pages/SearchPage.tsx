import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { searchPapers } from '../services/api';
import { Search, ChevronDown, ChevronUp, FileText, User } from 'lucide-react';

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const q = searchParams.get('q') || '';
  
  const [query, setQuery] = useState(q);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [entityType, setEntityType] = useState('All');
  const [ranking, setRanking] = useState('Hybrid');

  const performSearch = async (searchQuery: string, type: string, rank: string) => {
    if (!searchQuery) return;
    setLoading(true);
    try {
      const data = await searchPapers(searchQuery, type, rank);
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (q) {
      performSearch(q, entityType, ranking);
    }
  }, [q, entityType, ranking]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      setSearchParams({ q: query });
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="relative flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search..."
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-slate-300 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            />
            <Search className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
          </div>
          <button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 rounded-lg font-medium">
            Search
          </button>
        </form>

        <div className="flex gap-6 mt-6 pt-6 border-t border-slate-100">
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-slate-700">Entity Type:</label>
            <select value={entityType} onChange={(e) => setEntityType(e.target.value)} className="text-sm border border-slate-300 rounded-md p-1.5 focus:outline-none">
              <option>All</option>
              <option>Gene</option>
              <option>Disease</option>
              <option>Protein</option>
              <option>Drug</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-slate-700">Ranking Method:</label>
            <select value={ranking} onChange={(e) => setRanking(e.target.value)} className="text-sm border border-slate-300 rounded-md p-1.5 focus:outline-none">
              <option>Hybrid</option>
              <option>TF-IDF</option>
              <option>BM25</option>
              <option>Semantic</option>
            </select>
          </div>
        </div>
      </div>

      <div>
        {loading ? (
          <div className="text-center py-12 text-slate-500">Searching biomedical indices...</div>
        ) : q && results.length === 0 ? (
          <div className="text-center py-12 text-slate-500">No results found for "{q}"</div>
        ) : (
          <div className="space-y-4">
            {results.length > 0 && <div className="text-sm text-slate-500">{results.length} results found</div>}
            {results.map((res, i) => (
              <ResultCard key={i} result={res} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function ResultCard({ result }: { result: any }) {
  const [expanded, setExpanded] = useState(false);
  const { paper } = result;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-bold text-indigo-900 mb-2">{paper.title}</h3>
          <span className="bg-emerald-100 text-emerald-800 text-xs font-semibold px-2.5 py-0.5 rounded ml-2 whitespace-nowrap">
            Score: {(result.score * 100).toFixed(1)}%
          </span>
        </div>
        
        <p className="text-slate-600 text-sm mb-4 line-clamp-2">{paper.abstract}</p>
        
        <div className="flex items-center text-xs text-slate-500 space-x-4 mb-4">
          <span className="flex items-center"><User className="w-3 h-3 mr-1"/> {paper.authors}</span>
          <span className="flex items-center"><FileText className="w-3 h-3 mr-1"/> {paper.journal} ({paper.year})</span>
        </div>
        
        {result.matched_entities.length > 0 && (
          <div className="flex gap-2 mb-4">
            {result.matched_entities.map((e: string, i: number) => (
              <span key={i} className="px-2 py-1 bg-cyan-50 text-cyan-700 text-xs font-medium rounded border border-cyan-100">
                {e}
              </span>
            ))}
          </div>
        )}
        
        <div className="flex gap-3">
          <button onClick={() => setExpanded(!expanded)} className="text-sm font-medium text-indigo-600 flex items-center hover:text-indigo-800">
            {expanded ? <ChevronUp className="w-4 h-4 mr-1" /> : <ChevronDown className="w-4 h-4 mr-1" />}
            Why this result?
          </button>
        </div>
      </div>
      
      {expanded && (
        <div className="bg-slate-50 p-6 border-t border-slate-200 text-sm">
          <h4 className="font-semibold text-slate-700 mb-3">Relevance Breakdown</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="bg-white p-3 rounded border border-slate-200 text-center">
              <div className="text-xs text-slate-500">TF-IDF</div>
              <div className="font-mono text-indigo-700">{result.tf_idf_score.toFixed(4)}</div>
            </div>
            <div className="bg-white p-3 rounded border border-slate-200 text-center">
              <div className="text-xs text-slate-500">BM25</div>
              <div className="font-mono text-indigo-700">{result.bm25_score.toFixed(4)}</div>
            </div>
            <div className="bg-white p-3 rounded border border-slate-200 text-center">
              <div className="text-xs text-slate-500">Semantic Sim</div>
              <div className="font-mono text-indigo-700">{result.semantic_score.toFixed(4)}</div>
            </div>
            <div className="bg-white p-3 rounded border border-slate-200 text-center bg-indigo-50 border-indigo-100">
              <div className="text-xs text-indigo-500 font-bold">Final Score</div>
              <div className="font-mono text-indigo-900 font-bold">{result.score.toFixed(4)}</div>
            </div>
          </div>
          
          <div className="mb-2">
            <span className="font-medium text-slate-700">Matched Query Terms: </span>
            <span className="text-slate-600">{result.matched_terms.join(', ') || 'Semantic match only'}</span>
          </div>
          
          <div>
            <span className="font-medium text-slate-700">Matched Biological Entities: </span>
            <span className="text-slate-600">{result.matched_entities.join(', ') || 'None directly matched'}</span>
          </div>
        </div>
      )}
    </div>
  );
}
