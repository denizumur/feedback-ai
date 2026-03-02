🚀 Feedback-AI Pro: Akıllı İşletme Analiz & Görselleştirme Sistemi
Bu proje; Google Haritalar üzerindeki işletme yorumlarını çeken, hibrit bir yapay zeka mimarisi (Yerel NLP + LLM) ile analiz eden ve sonuçları modern bir React Dashboard üzerinde görselleştiren uçtan uca bir sistemdir.

🧠 Özellikler
📍 Akıllı Veri Çekme: Google Haritalar'dan canlı yorum verisi toplama.

🤖 Hibrit AI Analizi: * Yerel NLP (BERTürk): Duygu analizi işlemleri yerel model ile yapılarak API maliyeti sıfırlanır.

Gemini 2.5 Flash-Lite: İşletme sahibi için stratejik "Yönetici Özeti" toplu paket (Batch Processing) halinde oluşturulur.

📊 Dinamik Dashboard: Recharts ve Tailwind CSS kullanılarak hazırlanan, verileri gerçek zamanlı görselleştiren modern arayüz.

⚡ Hızlı Depolama: Analiz edilen verilerin anlık olarak Supabase PostgreSQL veritabanına işlenmesi.

🛡️ Kota Dostu: API maliyetini %90 oranında düşüren "Toplu İşleme" (Batching) stratejisi.

🛠️ Kullanılan Teknolojiler
Backend: Python 3.x, Gemini 2.5 Flash-Lite API, BERTürk (Local NLP).

Frontend: React (Vite), Tailwind CSS, Recharts, Lucide Icons.

Veritabanı: Supabase (PostgreSQL).

🚀 Kurulum ve Kullanım
1. Backend Kurulumu
Bash
cd backend
pip install -r requirements.txt
python run_full_process.py
2. Frontend Kurulumu
Bash
cd frontend
npm install
npm run dev
