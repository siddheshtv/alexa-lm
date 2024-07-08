from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.sql import func
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
    
class ListeningResponse(BaseModel):
    paragraph_id: str
    paragraph: str
    question_id_1: str
    question_1: str
    question_id_2: str
    question_2: str
    question_id_3: str
    question_3: str
    question_id_4: str
    question_4: str
    question_id_5: str
    question_5: str

class ListeningRequest(BaseModel):
    pass

@router.post("/get_listening_paragraph/", response_model=ListeningResponse)
async def get_listening_paragraph(request: ListeningRequest, db: Session = Depends(get_db)):
    paragraph = db.query(Listening).order_by(func.random()).first()
    
    if not paragraph:
        raise HTTPException(status_code=404, detail="No listening paragraphs found")
    
    return ListeningResponse(
        paragraph_id=paragraph.paragraph_id,
        paragraph=paragraph.paragraph,
        question_id_1=f"Q{paragraph.paragraph_id}-1",
        question_1=paragraph.question1,
        question_id_2=f"Q{paragraph.paragraph_id}-2",
        question_2=paragraph.question2,
        question_id_3=f"Q{paragraph.paragraph_id}-3",
        question_3=paragraph.question3,
        question_id_4=f"Q{paragraph.paragraph_id}-4",
        question_4=paragraph.question4,
        question_id_5=f"Q{paragraph.paragraph_id}-5",
        question_5=paragraph.question5
    )

# @router.post("/check_answer/")
# async def check_answer(request: AnswerCheck, db: Session = Depends(get_db)):
#     table_class = get_table_class(request.category)
    
#     if not table_class:
#         raise HTTPException(status_code=400, detail="Invalid category")

#     if request.category == "Listening":
#         entry = db.query(table_class).filter(table_class.paragraph_id == request.paragraph_id).first()
#         if not entry:
#             raise HTTPException(status_code=404, detail="Paragraph not found")
        
#         question_number = request.question_id.split('-')[1]  # Assuming question_id format is 'Q001-1', 'Q001-2', etc.
#         question_field = f"question{question_number}"
#         answer_field = f"answer{question_number}"
        
#         if hasattr(entry, question_field) and hasattr(entry, answer_field):
#             correct_answer = getattr(entry, answer_field)
#             is_correct = request.answer.lower() == correct_answer.lower()
#             return {"correct": is_correct, "correct_answer": correct_answer}
#         else:
#             raise HTTPException(status_code=404, detail="Question not found in the given paragraph")
#     else:
#         entry = db.query(table_class).filter(
#             (table_class.question_id == request.question_id) & 
#             (table_class.question_type == request.question_type)
#         ).first()
#         if not entry:
#             raise HTTPException(status_code=404, detail="Question not found")
        
#         is_correct = entry.answer.lower() == request.answer.lower()
#         return {"correct": is_correct, "correct_answer": entry.answer}


@router.post("/check_answer/")
async def check_answer(
    paragraph_id: Optional[str] = Form(None),
    question_id: str = Form(...),
    answer: str = Form(...),
    category: str = Form(...),
    question_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    table_class = get_table_class(category)
    
    if not table_class:
        raise HTTPException(status_code=400, detail="Invalid category")

    if category == "Listening":
        entry = db.query(table_class).filter(table_class.paragraph_id == paragraph_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Paragraph not found")
        
        question_number = question_id.split('-')[1]
        question_field = f"question{question_number}"
        answer_field = f"answer{question_number}"
        
        if hasattr(entry, question_field) and hasattr(entry, answer_field):
            correct_answer = getattr(entry, answer_field)
            is_correct = answer.lower() == correct_answer.lower()
            return {"correct": is_correct, "correct_answer": correct_answer}
        else:
            raise HTTPException(status_code=404, detail="Question not found in the given paragraph")
    else:
        entry = db.query(table_class).filter(
            (table_class.question_id == question_id) & 
            (table_class.question_type == question_type)
        ).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Question not found")
        
        is_correct = entry.answer.lower() == answer.lower()
        return {"correct": is_correct, "correct_answer": entry.answer}