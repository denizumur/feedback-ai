from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class Business(Base):
    __tablename__ = "businesses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))
    name = Column(String, nullable=False)
    maps_url = Column(Text, nullable=False)
    category = Column(String)
    is_active = Column(Boolean, default=True)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"))
    author_name = Column(String)
    rating = Column(Integer)
    content = Column(Text)
    external_id = Column(String, unique=True)
    publish_date = Column(DateTime)

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), ForeignKey("reviews.id"))
    sentiment_score = Column(Float)
    category_tags = Column(JSON) # ["hijyen", "hız"] şeklinde saklanacak
    is_critical = Column(Boolean, default=False)
    ai_reply_suggestion = Column(Text)