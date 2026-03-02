from database import supabase
import uuid

def seed_data():
    # 1. İşletme Ekle
    biz_data = {
        "name": "Lezzet Durağı",
        "maps_url": "https://goo.gl/maps/test",
        "category": "Restoran",
        "is_active": True
    }
    
    # Supabase'e veriyi gönder ve dönen ID'yi al
    biz_response = supabase.table("businesses").insert(biz_data).execute()
    business_id = biz_response.data[0]['id']
    
    print(f"İşletme eklendi, ID: {business_id}")

    # 2. Yorumları Ekle
    reviews = [
        {
            "business_id": business_id,
            "author_name": "Deniz Can",
            "rating": 1,
            "content": "Çok kötü servis, yemekler buz gibiydi!",
            "external_id": str(uuid.uuid4())
        },
        {
            "business_id": business_id,
            "author_name": "Aslı Demir",
            "rating": 5,
            "content": "Her şey mükemmeldi, teşekkürler!",
            "external_id": str(uuid.uuid4())
        }
    ]

    supabase.table("reviews").insert(reviews).execute()
    print("Yorumlar başarıyla eklendi kanka! ✅")

if __name__ == "__main__":
    seed_data()