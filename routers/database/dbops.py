from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models import Question, Listening

router = APIRouter()

class AnswerCheck(BaseModel):
    paragraph_id: Optional[str]
    question_id: str
    answer: str
    category: str
    question_type: Optional[str] = None

def get_table_class(category: str):
    if category == "Listening":
        return Listening
    elif category in ["Math", "Aptitude"]:
        return Question
    else:
        return None

@router.post("/check_answer/")
async def check_answer(request: AnswerCheck, db: Session = Depends(get_db)):
    table_class = get_table_class(request.category)
    
    if not table_class:
        raise HTTPException(status_code=400, detail="Invalid category")

    if request.category == "Listening":
        entry = db.query(table_class).filter(table_class.paragraph_id == request.paragraph_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Paragraph not found")
        
        question_number = request.question_id.split('-')[1]  # Assuming question_id format is 'Q001-1', 'Q001-2', etc.
        question_field = f"question{question_number}"
        answer_field = f"answer{question_number}"
        
        if hasattr(entry, question_field) and hasattr(entry, answer_field):
            correct_answer = getattr(entry, answer_field)
            is_correct = request.answer.lower() == correct_answer.lower()
            return {"correct": is_correct, "correct_answer": correct_answer}
        else:
            raise HTTPException(status_code=404, detail="Question not found in the given paragraph")
    else:
        entry = db.query(table_class).filter(
            (table_class.question_id == request.question_id) & 
            (table_class.question_type == request.question_type)
        ).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Question not found")
        
        is_correct = entry.answer.lower() == request.answer.lower()
        return {"correct": is_correct, "correct_answer": entry.answer}