from fastapi import FastAPI 
from mini_project import router as product_router 


app = FastAPI() 

app.include_router(product_router)
@app.get("/")
def home():
    return {"message": "FastAPI is running!"} 

@app.get("/ai")
def ai_response():
    return {"message": "This message is from the AI endpoint!"}

@app.get("/user/{user_id}") 
def get_user(user_id: int):
    return {
        "user_id": user_id
        }

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
from pydantic import BaseModel 

class Student(BaseModel):
    name: str 
    age: int 

    
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