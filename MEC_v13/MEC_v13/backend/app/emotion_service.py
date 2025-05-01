# backend/services/emotion_service.py

from sqlalchemy.orm import Session
from backend.models import EmotionHistory

def get_emotion_history_by_user_id(db: Session, user_id: int):
    return db.query(EmotionHistory).filter(EmotionHistory.user_id == user_id).all()

def add_emotion_to_history(db: Session, user_id: int, emotion: str, intensity: float, confidence: float):
    db_emotion = EmotionHistory(
        user_id=user_id, 
        emotion=emotion, 
        intensity=intensity, 
        confidence=confidence
    )
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion
