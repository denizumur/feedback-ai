from sqlalchemy.orm import Session
from . import models

def save_reviews_to_db(db: Session, business_id: str, reviews_data: list):
    for item in reviews_data:
        # Daha önce kaydedilmiş mi kontrol et (external_id ile)
        db_review = db.query(models.Review).filter(models.Review.external_id == item['external_id']).first()
        
        if not db_review:
            new_review = models.Review(
                business_id=business_id,
                author_name=item['author_name'],
                rating=item['rating'],
                content=item['content'],
                external_id=item['external_id'],
                publish_date=item['publish_date']
            )
            db.add(new_review)
    
    db.commit()
    return {"status": "success", "message": f"{len(reviews_data)} yorum işlendi."}