from fastapi import FastAPI 
from mini_project import router as product_router 
from day2.day2 import router as student_router

import models 
from database import engine
from database import sessionLocal 
from sqlalchemy.orm import Session 
from fastapi import Depends 

from schemas import UserCreate, UserResponse 
import models 


models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

# app.include_router(student_router)
# app.include_router(product_router)
@app.get("/")
def home():
    return {"message": "FastAPI is running!"} 

@app.get("/ai")
def ai_response():
    return {"message": "This message is from the AI endpoint!"}

# @app.get("/user/{user_id}") 
# def get_user(user_id: int):
#     return {
#         "user_id": user_id
#         }

@app.get('/search')
def search(name: str):
    return {
        "search": name
    }


@app.get('/item') 
def product(name: str, price: float):
    return { 
        'name': name,
        'price': price
    }


@app.post('/add') 
def add():
    return {
        'message': "Data Added"
    }

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field 

class Student(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(gt=18, lt=26) 

    
@app.post('/student') 
def create_student(student: Student): 
    return {
        'name': student.name, 
        'age': student.age
    }

from typing import Optional 

@app.get('/profile') 
def user_profile(name: Optional[str] = None):
    return {
        'name': name or "Guest"
    }



# Database connection and session management
def get_db(): 
    db = sessionLocal()

    try: 
        yield db 
    finally: 
        db.close()


@app.post('/user', response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)):

    new_user = models.User(
        name=user.name, 
        email=user.email
    )
    db.add(new_user) 
    db.commit() 
    db.refresh(new_user)
    return new_user 


@app.get('/users', response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all() 
    return users 

@app.get('/user/{id}', response_model=UserResponse) 
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 
    if not user: 
        raise HTTPException(status_code=404, detail = 'User Not Found')

    return user 


@app.put('/user/{id}', response_model = UserResponse) 
def update_user(
    id: int,
    user: UserCreate, 
    db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.id == id).first() 
    if not db_user: 
        raise HTTPException(status_code=404, detail = 'User Not Found') 
    
    db_user.name = user.name 
    db_user.email = user.email 
    db.commit() 
    return {
        'message': "User Updated Successfully"
    }

@app.delete('/user/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 
    if not user: 
        raise HTTPException(status_code=404, detail = 'User Not Found') 
    
    db.delete(user)
    db.commit()

    return {
        'message': "user Deleted Successfully"
    }
