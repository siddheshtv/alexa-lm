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
    question_id1: str
    question1: str
    option_a1: str
    option_b1: str
    option_c1: str
    answer1: str
    question_id2: str
    question2: str
    option_a2: str
    option_b2: str
    option_c2: str
    answer2: str
    question_id3: str
    question3: str
    option_a3: str
    option_b3: str
    option_c3: str
    answer3: str
    question_id4: str
    question4: str
    option_a4: str
    option_b4: str
    option_c4: str
    answer4: str
    question_id5: str
    question5: str
    option_a5: str
    option_b5: str
    option_c5: str
    answer5: str

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
        question_id1=paragraph.question_id1,
        question1=paragraph.question1,
        option_a1=paragraph.option_a1,
        option_b1=paragraph.option_b1,
        option_c1=paragraph.option_c1,
        answer1=paragraph.answer1,
        question_id2=paragraph.question_id2,
        question2=paragraph.question2,
        option_a2=paragraph.option_a2,
        option_b2=paragraph.option_b2,
        option_c2=paragraph.option_c2,
        answer2=paragraph.answer2,
        question_id3=paragraph.question_id3,
        question3=paragraph.question3,
        option_a3=paragraph.option_a3,
        option_b3=paragraph.option_b3,
        option_c3=paragraph.option_c3,
        answer3=paragraph.answer3,
        question_id4=paragraph.question_id4,
        question4=paragraph.question4,
        option_a4=paragraph.option_a4,
        option_b4=paragraph.option_b4,
        option_c4=paragraph.option_c4,
        answer4=paragraph.answer4,
        question_id5=paragraph.question_id5,
        question5=paragraph.question5,
        option_a5=paragraph.option_a5,
        option_b5=paragraph.option_b5,
        option_c5=paragraph.option_c5,
        answer5=paragraph.answer5
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
    
    print(f"Querying with level: {level}, question_type: {question_type}, age_range: {age_range}")

    
    questions = db.query(Question).filter(
        Question.level == level,
        Question.question_type == question_type,
        Question.age_range == age_range
    ).order_by(func.random()).limit(5).all()
    print(f"Number of questions retrieved: {len(questions)}")
    
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