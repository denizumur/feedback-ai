import React, { useEffect, useState } from 'react';
import { supabase } from './lib/supabaseClient';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { LayoutDashboard, MessageSquare, Star, TrendingUp, AlertCircle, CheckCircle2, XCircle, HelpCircle } from 'lucide-react';

function App() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  async function fetchReviews() {
    try {
      const { data, error } = await supabase.from('reviews').select('*');
      if (error) throw error;
      setReviews(data || []);
    } catch (err) {
      console.error("❌ Veri çekme hatası:", err.message);
    } finally {
      setLoading(false);
    }
  }

  // Grafik verilerini dinamik olarak hesapla
  const sentimentCounts = {
    POZITIF: reviews.filter(r => r.sentiment === 'POZITIF').length,
    NEGATIF: reviews.filter(r => r.sentiment === 'NEGATIF').length,
    NOTR: reviews.filter(r => r.sentiment === 'NOTR').length
  };

  const sentimentData = [
    { name: 'Pozitif', value: sentimentCounts.POZITIF },
    { name: 'Negatif', value: sentimentCounts.NEGATIF },
    { name: 'Nötr', value: sentimentCounts.NOTR },
  ];

  const COLORS = ['#22c55e', '#ef4444', '#f59e0b'];

  if (loading) return (
    <div className="flex h-screen items-center justify-center bg-gray-50 font-sans">
      <div className="flex flex-col items-center gap-4">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-600 border-opacity-25 border-t-blue-600"></div>
        <p className="text-gray-500 font-medium animate-pulse">Analizler Yükleniyor...</p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8 font-sans text-gray-900">
      <div className="max-w-7xl mx-auto">
        
        {/* Dashboard Üst Bilgi */}
        <header className="flex flex-col md:flex-row md:items-center justify-between mb-10 gap-4">
          <div>
            <h1 className="text-4xl font-black text-gray-900 tracking-tight">Feedback <span className="text-blue-600">AI</span></h1>
            <p className="text-gray-500 font-medium">Müşteri Deneyim Paneli • Cafe De Luca</p>
          </div>
          <div className="flex items-center gap-3 bg-white p-2 pr-4 rounded-2xl shadow-sm border border-gray-100">
            <div className="bg-blue-600 p-2 rounded-xl text-white">
              <LayoutDashboard size={20} />
            </div>
            <span className="font-bold text-gray-700">Deniz Umur / 2026</span>
          </div>
        </header>

        {/* İstatistik Özet Kartları */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <StatCard icon={<MessageSquare className="text-blue-600" />} label="Toplam Yorum" value={reviews.length} color="bg-blue-100/50" />
          <StatCard icon={<Star className="text-yellow-500" />} label="Genel Puan" value="4.2" color="bg-yellow-100/50" />
          <StatCard icon={<TrendingUp className="text-green-600" />} label="Memnuniyet" value={`%${reviews.length ? Math.round((sentimentCounts.POZITIF / reviews.length) * 100) : 0}`} color="bg-green-100/50" />
          <StatCard icon={<AlertCircle className="text-red-600" />} label="Kritik Uyarı" value="2" color="bg-red-100/50" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
          {/* Grafik Alanı (Uyarılar Giderildi) */}
          <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 lg:col-span-1 min-h-[400px]">
            <h2 className="text-xl font-bold mb-8 text-gray-800 flex items-center gap-2">
              <div className="w-1.5 h-6 bg-blue-600 rounded-full"></div>
              Duygu Analizi Dağılımı
            </h2>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%" debounce={100}>
                <PieChart>
                  <Pie data={sentimentData} cx="50%" cy="50%" innerRadius={70} outerRadius={90} paddingAngle={8} dataKey="value">
                    {sentimentData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="none" />)}
                  </Pie>
                  <Tooltip />
                  <Legend iconType="circle" verticalAlign="bottom" height={36}/>
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Gemini AI Rapor Alanı */}
          <div className="bg-indigo-900 p-10 rounded-3xl shadow-2xl lg:col-span-2 text-white relative overflow-hidden group">
            <div className="absolute -right-10 -bottom-10 opacity-10 group-hover:scale-110 transition-transform duration-700">
               <TrendingUp size={300} />
            </div>
            <div className="relative z-10">
              <div className="flex items-center gap-4 mb-6">
                <div className="bg-white/10 p-3 rounded-2xl backdrop-blur-md border border-white/20">
                  <div className="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse"></div>
                </div>
                <h2 className="text-2xl font-black tracking-wide">Gemini 2.5 AI Stratejik Rapor</h2>
              </div>
              <div className="space-y-6 text-indigo-100 text-lg leading-relaxed font-medium">
                <p className="bg-white/5 p-6 rounded-2xl border border-white/10 italic">
                  "Analiz sonuçlarına göre: İşletmeniz genelinde hizmet kalitesi (servis hızı ve personel ilgisi) %92 oranında pozitif puanlanıyor. Ancak fiyatlandırma politikası ve özellikle tatlı grubundaki (tiramisu) standart kaybı müşterilerin %15'inde olumsuz intiba bırakmış durumda."
                </p>
                <div className="flex flex-wrap gap-3">
                  <span className="bg-green-500/20 text-green-300 px-4 py-1.5 rounded-full text-sm font-bold border border-green-500/30">🎯 Personel Eğitimi Başarılı</span>
                  <span className="bg-red-500/20 text-red-300 px-4 py-1.5 rounded-full text-sm font-bold border border-red-500/30">⚠️ Fiyat Hassasiyeti Mevcut</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Yorum Listesi */}
        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-8 border-b border-gray-50 flex justify-between items-center bg-gray-50/30">
            <h2 className="text-2xl font-black text-gray-800">Canlı Müşteri Akışı</h2>
            <div className="text-xs font-bold px-4 py-2 bg-blue-50 text-blue-600 rounded-xl tracking-widest uppercase">Supabase Sync</div>
          </div>
          <div className="divide-y divide-gray-50">
            {reviews.map((r) => (
              <div key={r.id} className="p-8 hover:bg-blue-50/30 transition-all flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="flex-1">
                  <div className="flex items-center gap-4 mb-3">
                    <span className="text-lg font-bold text-gray-900">{r.author_name}</span>
                    <SentimentBadge type={r.sentiment} />
                  </div>
                  <p className="text-gray-600 leading-relaxed font-medium italic">"{r.content}"</p>
                </div>
                <div className="flex flex-col items-end gap-3 min-w-[120px]">
                  <div className="flex text-yellow-400 gap-0.5">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} size={16} fill={i < (r.rating || 0) ? "currentColor" : "none"} className={i < (r.rating || 0) ? "" : "text-gray-200"} />
                    ))}
                  </div>
                  <span className="text-[10px] font-black text-gray-400 bg-gray-100 px-3 py-1 rounded-lg uppercase tracking-widest">{r.category || 'GENEL'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// Alt Bileşenler
function StatCard({ icon, label, value, color }) {
  return (
    <div className="bg-white p-6 rounded-[2rem] shadow-sm border border-gray-100 flex items-center gap-6 hover:shadow-lg transition-all duration-300 border-b-4 border-b-transparent hover:border-b-blue-500">
      <div className={`p-5 ${color} rounded-[1.5rem]`}>{icon}</div>
      <div>
        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">{label}</p>
        <p className="text-3xl font-black text-gray-800 tracking-tighter">{value}</p>
      </div>
    </div>
  );
}

function SentimentBadge({ type }) {
  const config = {
    POZITIF: { icon: <CheckCircle2 size={14} />, text: 'Pozitif', style: 'bg-green-100 text-green-700 border-green-200' },
    NEGATIF: { icon: <XCircle size={14} />, text: 'Negatif', style: 'bg-red-100 text-red-700 border-red-200' },
    NOTR: { icon: <HelpCircle size={14} />, text: 'Nötr', style: 'bg-amber-100 text-amber-700 border-amber-200' },
  };
  const current = config[type] || config.NOTR;
  return (
    <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${current.style}`}>
      {current.icon} {current.text}
    </span>
  );
}

export default App;