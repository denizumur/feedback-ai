from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, database
from .services.scraper import ReviewScraper

# Uygulama başladığında veritabanı tablolarını otomatik oluşturur 
# (Eğer Supabase'de manuel oluşturduysan bu satır zarar vermez, kontrol eder geçer)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FeedBackAI API", description="Müşteri yorumlarını analiz eden AI asistanı")

# Veritabanı Bağlantısı (Dependency)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "online", "message": "FeedBackAI Backend is running"}

@app.post("/sync-reviews/{business_id}")
def sync_reviews(business_id: str, db: Session = Depends(get_db)):
    # 1. İşletmeyi veritabanında bul
    business = db.query(models.Business).filter(models.Business.id == business_id).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="İşletme bulunamadı kanka!")

    try:
        # 2. Scraper'ı çalıştır (İşletmenin kayıtlı maps_url'ini kullanır)
        scraper = ReviewScraper(business.maps_url)
        reviews_data = scraper.fetch_reviews()
        
        # 3. Çekilen yorumları DB'ye kaydet
        result = crud.save_reviews_to_db(db, business_id, reviews_data)
        
        return {
            "status": "success",
            "business_name": business.name,
            "processed_reviews": len(reviews_data),
            "details": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Veri çekme sırasında hata oluştu: {str(e)}")

# Yeni bir işletme eklemek için hızlı bir endpoint (Test amaçlı)
@app.post("/businesses/")
def create_business(name: str, maps_url: str, db: Session = Depends(get_db)):
    new_biz = models.Business(name=name, maps_url=maps_url)
    db.add(new_biz)
    db.commit()
    db.refresh(new_biz)
    return new_biz