from services.scraper import ReviewScraper
from database import DatabaseManager
from services.analysis import AIAnalyzer
from services.local_nlp import LocalNLP
import time

# Başlatıcılar
scraper = ReviewScraper()
db = DatabaseManager()
ai = AIAnalyzer()
local_model = LocalNLP()

mekan = "Cafe De Luca, İzmit"
print(f"🚀 {mekan} için hibrit analiz süreci başlatılıyor...\n")

# 1. Google Haritalar'dan Yorumları Çek
yorumlar = scraper.fetch_reviews(mekan)

if yorumlar:
    print(f"✅ {len(yorumlar)} adet yorum başarıyla çekildi.")
    
    # 2. Yerel NLP ile Hızlı Duygu Analizi (Sıfır Kota Kullanımı)
    print("🧠 Yerel NLP modeli (BERTürk) duygu analizi yapıyor...")
    for r in yorumlar:
        metin = r.get("snippet", "")
        if metin:
            yerel_analiz = local_model.analyze(metin)
            # Analiz sonuçlarını yorum objesine ekle
            r['sentiment'] = yerel_analiz['sentiment']
            r['category'] = "ANALIZ_EDILIYOR" # Gemini toplu raporunda belirlenecek
            r['summary'] = "Genel raporda belirtildi."
            
    # 3. Veritabanına Analizli Verileri Kaydet
    # (Not: database.py içinde save_reviews_batch kullandığını varsayıyorum)
    print("💾 Analiz sonuçları Supabase'e işleniyor...")
    db.save_reviews_batch(yorumlar)

    # 4. KRİTİK: Gemini ile Tek Seferde "Yönetici Raporu"
    # Artık her yorum için ayrı gitmiyoruz, hepsini tek pakette yolluyoruz.
    print("\n📊 Gemini 2.5 Flash-Lite ile stratejik rapor hazırlanıyor...")
    rapor = ai.generate_executive_report(yorumlar)
    
    print("\n" + "═" * 60)
    print("       📋 İŞLETME YÖNETİCİ RAPORU (Gemini 2.5 AI)")
    print("═" * 60)
    print(rapor)
    print("═" * 60)

else:
    print("❌ Yorumlar çekilemedi, süreç durduruldu.")