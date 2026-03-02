import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine

load_dotenv()
db_url = os.getenv("DATABASE_URL")

print(f"Bağlanmaya çalışılan URL: {db_url}") # Şifreni gizli tut ama formatı kontrol et

try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        print("✅ BAĞLANTI BAŞARILI! Supabase ile el sıkıştık.")
except Exception as e:
    print(f"❌ HATA: {e}")