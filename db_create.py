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
    question_id1 = Column(String(10), nullable=False)
    question1 = Column(Text, nullable=False)
    option_a1 = Column(Text, nullable=False)
    option_b1 = Column(Text, nullable=False)
    option_c1 = Column(Text, nullable=False)
    answer1 = Column(String(10), nullable=False)
    question_id2 = Column(String(10), nullable=False)
    question2 = Column(Text, nullable=False)
    option_a2 = Column(Text, nullable=False)
    option_b2 = Column(Text, nullable=False)
    option_c2 = Column(Text, nullable=False)
    answer2 = Column(String(10), nullable=False)
    question_id3 = Column(String(10), nullable=False)
    question3 = Column(Text, nullable=False)
    option_a3 = Column(Text, nullable=False)
    option_b3 = Column(Text, nullable=False)
    option_c3 = Column(Text, nullable=False)
    answer3 = Column(String(10), nullable=False)
    question_id4 = Column(String(10), nullable=False)
    question4 = Column(Text, nullable=False)
    option_a4 = Column(Text, nullable=False)
    option_b4 = Column(Text, nullable=False)
    option_c4 = Column(Text, nullable=False)
    answer4 = Column(String(10), nullable=False)
    question_id5 = Column(String(10), nullable=False)
    question5 = Column(Text, nullable=False)
    option_a5 = Column(Text, nullable=False)
    option_b5 = Column(Text, nullable=False)
    option_c5 = Column(Text, nullable=False)
    answer5 = Column(String(10), nullable=False)

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
                question_id1=row['question_id1'],
                question1=row['question1'],
                option_a1=row['option_a1'],
                option_b1=row['option_b1'],
                option_c1=row['option_c1'],
                answer1=row['answer1'],
                question_id2=row['question_id2'],
                question2=row['question2'],
                option_a2=row['option_a2'],
                option_b2=row['option_b2'],
                option_c2=row['option_c2'],
                answer2=row['answer2'],
                question_id3=row['question_id3'],
                question3=row['question3'],
                option_a3=row['option_a3'],
                option_b3=row['option_b3'],
                option_c3=row['option_c3'],
                answer3=row['answer3'],
                question_id4=row['question_id4'],
                question4=row['question4'],
                option_a4=row['option_a4'],
                option_b4=row['option_b4'],
                option_c4=row['option_c4'],
                answer4=row['answer4'],
                question_id5=row['question_id5'],
                question5=row['question5'],
                option_a5=row['option_a5'],
                option_b5=row['option_b5'],
                option_c5=row['option_c5'],
                answer5=row['answer5']
            )
            session.add(listening)
    session.commit()

insert_questions_data()
insert_listening_data()
session.close()
print("Database populated successfully.")