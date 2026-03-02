from pydantic import BaseModel
from typing import List, Optional

class BusinessCreate(BaseModel):
    name: str
    maps_url: str
    category: Optional[str] = None

class AnalysisResponse(BaseModel):
    sentiment_score: float
    category_tags: List[str]
    is_critical: bool
    ai_reply_suggestion: str

    class Config:
        from_attributes = True