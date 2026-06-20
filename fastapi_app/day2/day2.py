from fastapi import APIRouter 
from pydantic import BaseModel, Field 
from typing import Optional 

router = APIRouter() 


class Student(BaseModel): 
    name : str = Field(min_length=3, max_length=50) 
    age : int = Field(gt=18, lt=26) 


@router.get('/students', tags=['Students'])
def students():
    return {
        'message': 'Students'
    }

@router.post('/student', tags=['Students'])
def create_student(student: Student):
    return {
        'name': student.name, 
        'age': student.age,
        'message': 'Students'
    }


class User(BaseModel):
    name: str 
    email: Optional[str] = None


@router.post('/user')
def create_user(user: User):
    return {
        'name': user.name,
        'email': user.email
    }

class UserResponse(BaseModel):
    name: str 
    email: Optional[str] = None

@router.get('/user', response_model= UserResponse)
def get_user():
    return {
        'name': 'subhan',
        'password': 'secret',
        'email': "subhan@gmail.com"
    }

import time
from fastapi import status 
class BlogPost(BaseModel):
    title: str 
    content: str 
    created_at: float = Field(default_factory=lambda: time.time())
@router.post('/blog', status_code = status.HTTP_201_CREATED)
def create_blog(blog: BlogPost):
    return {
        'title': blog.title,
        'content': blog.content, 
        'created_at': blog.created_at 
    }



from fastapi import HTTPException

students = {
    1: 'subhan',
    2: 'azhar',
}

@router.get('/student/{id}')
def get_student(id: int):
    
    if id not in students:
        raise HTTPException(
            status_code = 404,
            detail = "student not found"
        )
    return {
        'student': students[id]
    }


from fastapi import Query 

@router.get('/search')
def search(name: str = Query(min_length=3)):
    return {
        'name': name
    }

# Numeric validation 
@router.get('/item')
def numeric(price: int = Query(gt=0)):
    return {
        'Price': price
    }


# path Validation 
from fastapi import Path

@router.get('/product/{product_id}')
def product( product_id: int = Path(gt=0)):
    return {
        'product_id': product_id
    }


@router.get('/users', tags=['Users'])
def users():
    return {
        'message': 'Users'
    }