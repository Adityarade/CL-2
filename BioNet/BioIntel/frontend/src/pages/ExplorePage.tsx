import React, { useState, useEffect } from 'react';
import { getEntities } from '../services/api';
import { Database, Activity, Beaker } from 'lucide-react';

export default function ExplorePage() {
  const [activeTab, setActiveTab] = useState<'genes' | 'diseases' | 'proteins'>('genes');
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getEntities(activeTab).then(res => {
      setData(res);
      setLoading(false);
    }).catch(console.error);
  }, [activeTab]);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex space-x-2 bg-white p-2 rounded-xl shadow-sm border border-slate-200">
        <TabButton active={activeTab === 'genes'} onClick={() => setActiveTab('genes')} icon={<Database className="w-4 h-4"/>} text="Genes" />
        <TabButton active={activeTab === 'diseases'} onClick={() => setActiveTab('diseases')} icon={<Activity className="w-4 h-4"/>} text="Diseases" />
        <TabButton active={activeTab === 'proteins'} onClick={() => setActiveTab('proteins')} icon={<Beaker className="w-4 h-4"/>} text="Proteins" />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-500">Loading entities...</div>
        ) : (
          <table className="w-full text-left">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 text-sm">
              <tr>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">Description</th>
                <th className="px-6 py-4 font-medium">Functions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {data.map((item, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="px-6 py-4 font-medium text-indigo-900">{item.name}</td>
                  <td className="px-6 py-4 text-sm text-slate-600">{item.description}</td>
                  <td className="px-6 py-4 text-sm text-slate-600">{item.functions || item.function || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function TabButton({ active, onClick, icon, text }: any) {
  return (
    <button
      onClick={onClick}
      className={`flex-1 flex items-center justify-center space-x-2 py-3 rounded-lg font-medium transition-colors ${
        active ? 'bg-indigo-50 text-indigo-700' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
      }`}
    >
      {icon}
      <span>{text}</span>
    </button>
  );
}
