import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

class ReviewScraper:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")

    def fetch_reviews(self, business_name, limit=5):
        print(f"🔍 Haritalarda '{business_name}' aranıyor...")
        
        # ADIM 1: Mekanı Bul (Burada place_id çekmek daha sağlamdır)
        search_params = {
            "engine": "google_maps",
            "q": business_name,
            "type": "search",
            "api_key": self.api_key
        }
        
        search = GoogleSearch(search_params)
        results = search.get_dict()
        
        # En garanti ID 'data_id'dir
        data_id = None
        if "place_results" in results:
            data_id = results["place_results"].get("data_id")
        elif "local_results" in results and len(results["local_results"]) > 0:
            data_id = results["local_results"][0].get("data_id")
            
        if not data_id:
            print(f"❌ '{business_name}' için ID bulunamadı.")
            return []
            
        print(f"✅ ID Yakalandı: {data_id}. Yorumlar çekiliyor...")

        # ADIM 2: Yorumları Çek (Motoru google_maps_reviews olarak netleştirelim)
        review_params = {
            "engine": "google_maps_reviews",
            "data_id": data_id,
            "api_key": self.api_key,
            "hl": "tr"
        }
        
        review_search = GoogleSearch(review_params)
        res = review_search.get_dict()
        
        # HATA AYIKLAMA: Eğer boş dönüyorsa res içindeki anahtarları kontrol et
        reviews = res.get("reviews", [])
        
        # Bazı durumlarda SerpApi veriyi farklı bir anahtarda gönderebilir
        if not reviews and "user_reviews" in res:
            reviews = res.get("user_reviews", [])

        return reviews