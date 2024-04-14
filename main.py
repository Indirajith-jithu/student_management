from enum import Enum
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import uvicorn 

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/Test_stundent"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define enums for gender and department
class Gender(str, Enum):
    male = "male"
    female = "female"

class Department(str, Enum):
    computer_science = "Computer Science"
    mathematics = "Mathematics"
    physics = "Physics"
    biology = "Biology"
    history = "History"

# Define input and output models
class StudentBase(BaseModel):
    name: str
    age: int
    gender: Gender
    department: Department

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True

# Define the Student model
class DBStudent(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(SQLEnum(Gender))
    department = Column(SQLEnum(Department))

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = DBStudent(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/", response_model=List[Student])
def read_all_students(db: Session = Depends(get_db)):
    return db.query(DBStudent).all()

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(DBStudent).filter(DBStudent.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}




if  __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)