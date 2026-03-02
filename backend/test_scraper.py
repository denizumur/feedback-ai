from services.scraper import ReviewScraper
from database import DatabaseManager # Dosyan ana dizinde olduğu için böyle çağırdık

# 1. Hazırlık
scraper = ReviewScraper()
db = DatabaseManager()
mekan = "Cafe De Luca, İzmit"

# 2. Veri Çekme
print(f"📡 {mekan} için canlı veriler toplanıyor...")
yorumlar = scraper.fetch_reviews(mekan)

# 3. Veritabanına Yazma
if yorumlar:
    db.save_reviews_batch(yorumlar)
    print("\n🔥 İŞLEM TAMAM! Şimdi Supabase Dashboard'una gir ve 'reviews' tablosuna bak!")
else:
    print("⚠️ Kaydedilecek veri bulunamadı.")