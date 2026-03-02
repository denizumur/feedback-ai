import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # .env dosyasından bilgileri çekiyoruz
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def save_reviews_batch(self, reviews):
        """
        Yerel NLP'den gelen analizleri ve ham yorum verilerini 
        topluca Supabase'e basar. Hibrit mimari için ana metot budur.
        """
        processed_data = []
        
        for r in reviews:
            # Rating'i integer yapma garantisi
            try:
                rating_int = int(float(r.get("rating", 0)))
            except:
                rating_int = 0

            # Yerel NLP'den gelen sentiment'i al, yoksa 'Bilinmiyor' yaz
            processed_data.append({
                "author_name": r.get("user", {}).get("name"),
                "content": r.get("snippet", ""),
                "rating": rating_int,
                "external_id": r.get("review_id"),
                "sentiment": r.get("sentiment", "Bilinmiyor"),
                "category": r.get("category", "DIGER"),
                "summary": r.get("summary", "Yerel analiz tamamlandı.")
            })

        try:
            # .upsert() ile mükerrer kayıtları önlüyoruz
            result = self.supabase.table("reviews").upsert(
                processed_data, 
                on_conflict="external_id"
            ).execute()
            
            print(f"✅ {len(processed_data)} yorum başarıyla Supabase'e işlendi.")
            return result
        except Exception as e:
            print(f"❌ Supabase Toplu Kayıt Hatası: {e}")
            return None

    def save_reviews_with_analysis(self, reviews, ai_analyzer):
        """
        NOT: Bu eski metodun, eğer her yorumu tek tek Gemini'ye 
        göndermek istersen (kota harcayarak) diye yedek olarak duruyor.
        """
        # ... (Senin paylaştığın time.sleep(7) içeren kod bloğu burada durabilir)
        pass