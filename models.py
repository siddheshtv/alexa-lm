from sqlalchemy import Column, Integer, Text, String, MetaData
from database import Base

metadata = MetaData()

class Question(Base):
    __tablename__ = 'Questions'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String(10), unique=True, nullable=False, index=True)
    question = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)
    age_range = Column(String(10), nullable=False)
    answer = Column(Text, nullable=False)
    level = Column(String(10), nullable=False)

class Listening(Base):
    __tablename__ = 'Listening'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    paragraph_id = Column(String(10), unique=True, nullable=False, index=True)
    paragraph = Column(Text, nullable=False)
    question1 = Column(Text, nullable=False)
    answer1 = Column(Text, nullable=False)
    question2 = Column(Text, nullable=False)
    answer2 = Column(Text, nullable=False)
    question3 = Column(Text, nullable=False)
    answer3 = Column(Text, nullable=False)
    question4 = Column(Text, nullable=False)
    answer4 = Column(Text, nullable=False)
    question5 = Column(Text, nullable=False)
    answer5 = Column(Text, nullable=False)