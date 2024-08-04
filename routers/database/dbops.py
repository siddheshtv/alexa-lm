from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
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

class FeedbackResponse(BaseModel):
    feedback: int

@router.post("/calculate_feedback/", response_model=FeedbackResponse)
async def calculate_feedback(
    answer1: bool = Form(...),
    answer2: bool = Form(...),
    answer3: bool = Form(...)
):
    answers = [answer1, answer2, answer3]
    correct_count = sum(answers)

    if correct_count == 3:
        feedback = 3
    elif correct_count == 2:
        feedback = 2
    elif correct_count == 1:
        feedback = 1
    else:
        feedback = 0

    return FeedbackResponse(feedback=feedback)

class QuestionResponse(BaseModel):
    question_id_1: Optional[str] = None
    question_1: Optional[str] = None
    question_type_1: Optional[str] = None
    age_range_1: Optional[str] = None
    answer_1: Optional[str] = None
    level_1: Optional[str] = None

    question_id_2: Optional[str] = None
    question_2: Optional[str] = None
    question_type_2: Optional[str] = None
    age_range_2: Optional[str] = None
    answer_2: Optional[str] = None
    level_2: Optional[str] = None

    question_id_3: Optional[str] = None
    question_3: Optional[str] = None
    question_type_3: Optional[str] = None
    age_range_3: Optional[str] = None
    answer_3: Optional[str] = None
    level_3: Optional[str] = None

    question_id_4: Optional[str] = None
    question_4: Optional[str] = None
    question_type_4: Optional[str] = None
    age_range_4: Optional[str] = None
    answer_4: Optional[str] = None
    level_4: Optional[str] = None

    question_id_5: Optional[str] = None
    question_5: Optional[str] = None
    question_type_5: Optional[str] = None
    age_range_5: Optional[str] = None
    answer_5: Optional[str] = None
    level_5: Optional[str] = None

@router.post("/get_questions/", response_model=QuestionResponse)
async def get_questions(
    question_type: str = Form(...),
    age_range: str = Form(...),
    feedback: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    if feedback is not None:
        if feedback >= 4 :
            level = "hard"
        elif feedback <= 2:
            level = "easy"
        else:
            level = "medium"
    else:
        level = "easy"
    
    if question_type not in ["math", "aptitude"]:
        raise HTTPException(status_code=400, detail="Invalid question type. Must be 'math' or 'aptitude'")
    
    questions = db.query(Question).filter(
        Question.level == level,
        Question.question_type == question_type,
        Question.age_range == age_range
    ).order_by(func.random()).limit(5).all()
    
    response = QuestionResponse()
    for i, q in enumerate(questions, 1):
        setattr(response, f"question_id_{i}", str(q.question_id))
        setattr(response, f"question_{i}", q.question)
        setattr(response, f"question_type_{i}", q.question_type)
        setattr(response, f"age_range_{i}", q.age_range)
        setattr(response, f"answer_{i}", q.answer)
        setattr(response, f"level_{i}", q.level)
    
    return response


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