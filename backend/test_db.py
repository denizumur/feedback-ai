import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(url)
    print("Bağlantı başarılı kanka! Borularda su var. ✅")
    conn.close()
except Exception as e:
    print(f"Hata devam ediyor: {e}")