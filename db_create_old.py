from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import csv

Base = declarative_base()

class Question(Base):
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key=True)
    question_id = Column(String(10), unique=True, nullable=False)
    question = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)
    age_range = Column(String(10), nullable=False)
    answer = Column(Text, nullable=False)
    level = Column(String(10), nullable=False)

class Listening(Base):
    __tablename__ = 'Listening'
    id = Column(Integer, primary_key=True)
    paragraph_id = Column(String(10), unique=True, nullable=False)
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

load_dotenv()

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f'{DATABASE_PREFIX}://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def insert_questions_data():
    with open('questions.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            question = Question(
                question_id=row['question_id'],
                question=row['question'],
                question_type=row['question_type'],
                age_range=row['age_range'],
                answer=row['answer'],
                level=row['level']
            )
            session.add(question)
    session.commit()

def insert_listening_data():
    with open('questionsp.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            listening = Listening(
                paragraph_id=row['paragraph_id'],
                paragraph=row['paragraph'],
                question1=row['question1'],
                answer1=row['answer1'],
                question2=row['question2'],
                answer2=row['answer2'],
                question3=row['question3'],
                answer3=row['answer3'],
                question4=row['question4'],
                answer4=row['answer4'],
                question5=row['question5'],
                answer5=row['answer5']
            )
            session.add(listening)
    session.commit()

insert_questions_data()
insert_listening_data()

session.close()

print("Database populated successfully.")