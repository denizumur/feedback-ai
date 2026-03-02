import os
import json
from google import genai
from dotenv import load_dotenv

# .env yüklemesi
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
env_path = os.path.join(parent_dir, ".env")
load_dotenv(dotenv_path=env_path)

class AIAnalyzer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY .env dosyasında bulunamadı!")
            
        # Gemini 2.5 Flash-Lite (2026 versiyonu) için Client kurulumu
        self.client = genai.Client(api_key=api_key)

    def generate_executive_report(self, all_reviews):
        """
        Tüm yorumları tek bir devasa blok olarak analiz eder. 
        Maliyeti düşürür, stratejik derinliği artırır.
        """
        review_text = ""
        for i, r in enumerate(all_reviews):
            content = r.get('content', r.get('snippet', ''))
            if content:
                review_text += f"Müşteri Yorumu {i+1}: {content}\n"

        if not review_text:
            return "Analiz edilecek geçerli yorum bulunamadı."

        # Sert ve net prompt: Gemini'nin 'yardım teklif etmesini' engeller.
        prompt = f"""
        ROL: Sen profesyonel bir restoran danışmanısın.
        GÖREV: Aşağıdaki yorumları analiz et ve doğrudan işletme sahibine yönelik bir rapor hazırla.
        
        VERİLER (Müşteri Geri Bildirimleri):
        {review_text}
        
        RAPOR FORMATI (SADECE BU BAŞLIKLARI KULLAN):
        1. **Genel Durum**: Müşteri memnuniyetinin özeti.
        2. **Güçlü Yönler**: İşletmenin parladığı noktalar.
        3. **Zayıf Yönler**: Acil düzeltilmesi gereken 2 kritik hata.
        4. **Eylem Planı**: Ciro artıracak 1 somut tavsiye.

        NOT: Giriş cümlesi kurma, 'hazırlayabilirim' deme. Doğrudan rapora başla.
        """
        
        try:
            print(f"🧠 {len(all_reviews)} yorum için stratejik rapor oluşturuluyor...")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"❌ Rapor Hatası: {e}")
            return "Rapor oluşturma aşamasında bir teknik aksaklık yaşandı."

    def analyze_all_reviews_at_once(self, reviews_list):
        """
        JSON tabanlı toplu analiz. Frontend grafikleri için ana veri kaynağı.
        """
        formatted_reviews = ""
        for i, r in enumerate(reviews_list):
            formatted_reviews += f"ID {i+1}: {r.get('snippet', r.get('content', ''))}\n"

        prompt = f"""
        GÖREV: Aşağıdaki yorumları analiz et ve sonucu SADECE JSON formatında döndür.
        YORUMLAR:
        {formatted_reviews}

        İSTEDİĞİM JSON ŞEMASI:
        {{
            "analyses": [
                {{"id": 1, "sentiment": "POZITIF/NEGATIF/NOTR", "category": "FIYAT/LEZZET/SERVIS/ORTAM/DIGER"}},
                ...
            ],
            "executive_summary": "Kısa genel özet"
        }}
        
        DİKKAT: JSON dışında hiçbir metin yazma.
        """

        try:
            print(f"🚀 Toplu JSON analizi başlatıldı ({len(reviews_list)} yorum)...")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=prompt
            )
            
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            print(f"❌ Toplu Analiz Hatası: {e}")
            return None