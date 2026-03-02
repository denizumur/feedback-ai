# 🚀 Feedback-AI: Akıllı İşletme Analiz Sistemi

Bu proje, Google Haritalar üzerindeki işletme yorumlarını otomatik olarak çeken, **Gemini 2.5 Flash-Lite** yapay zekası ile analiz eden ve sonuçları **Supabase** üzerinde depolayan uçtan uca bir veri işleme hattıdır.

## 🧠 Özellikler
* **📍 Akıllı Veri Çekme:** SerpApi kullanarak Google Haritalar'dan canlı yorum verisi toplama.
* **🤖 AI Analizi:** Gemini 2.5 Flash-Lite ile yorumların duygu (Sentiment), kategori (Fiyat, Lezzet, Servis vb.) ve özet analizlerini yapma.
* **⚡ Hızlı Depolama:** Analiz edilen verilerin anlık olarak Supabase PostgreSQL veritabanına işlenmesi.
* **🛡️ Kota Dostu:** Ücretsiz API limitlerini aşmamak için geliştirilmiş "Rate Limit" korumalı döngü mekanizması.

## 🛠️ Teknoloji Yığını
* **Dil:** Python 3.x
* **AI:** Google Gemini 2.5 Flash-Lite API
* **DB:** Supabase (PostgreSQL)
* **Scraper:** SerpApi (Google Maps Engine)

## 🚀 Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/denizumur/feedback-ai.git](https://github.com/denizumur/feedback-ai.git)
## 2. Gerekli kütüphaneleri yükleyin:

pip install -r requirements.txt


## 3. .env dosyanızı oluşturun (Asla paylaşmayın!):

SUPABASE_URL=your_url
SUPABASE_KEY=your_key
SERPAPI_KEY=your_key
GEMINI_API_KEY=your_key
## 4.Sistemi çalıştırın:

python run_full_process.py