from transformers import pipeline

class LocalNLP:
    def __init__(self):
        # Türkçe duygu analizi için önceden eğitilmiş model
        # İlk çalıştırmada modeli indirecek, sonra hep çevrimdışı çalışacak
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis", 
            model="savasy/bert-base-turkish-sentiment-cased"
        )

    def analyze(self, text):
        try:
            # Yerel modelden sonucu al
            result = self.sentiment_pipeline(text)[0]
            
            # Etiketleri daha anlaşılır yapalım
            label = "POZITIF" if result['label'] == 'positive' else "NEGATIF"
            if result['score'] < 0.6: label = "NOTR"
            
            return {
                "sentiment": label,
                "confidence": round(result['score'], 2)
            }
        except Exception as e:
            print(f"❌ Yerel NLP Hatası: {e}")
            return {"sentiment": "Bilinmiyor", "confidence": 0}