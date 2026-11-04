import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getHistory } from '../services/api';
import { Clock, Search, ArrowRight } from 'lucide-react';

export default function HistoryPage() {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    getHistory().then(setHistory).catch(console.error);
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center space-x-3 mb-8">
        <Clock className="w-8 h-8 text-indigo-600" />
        <h2 className="text-3xl font-bold text-slate-800">Search History</h2>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        {history.length === 0 ? (
          <div className="p-8 text-center text-slate-500">No recent searches.</div>
        ) : (
          <ul className="divide-y divide-slate-100">
            {history.map((item, i) => (
              <li key={i} className="hover:bg-slate-50 transition-colors">
                <Link to={`/search?q=${encodeURIComponent(item.query)}`} className="flex items-center justify-between p-6">
                  <div className="flex items-center space-x-4">
                    <div className="bg-slate-100 p-3 rounded-full text-slate-500">
                      <Search className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-lg text-indigo-900">{item.query}</h4>
                      <p className="text-sm text-slate-500">{new Date(item.timestamp).toLocaleString()}</p>
                    </div>
                  </div>
                  <ArrowRight className="w-5 h-5 text-slate-400" />
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
