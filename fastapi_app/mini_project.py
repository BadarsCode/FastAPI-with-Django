from fastapi import APIRouter 
from pydantic import BaseModel 


router = APIRouter() 

class Product(BaseModel):
    name: str 
    price: float 

products = []

@router.post('/add_product') 
def Add_product(product: Product):
    products.append(product.dict())
    return {
        'message': "Product Added",
        'data': product
    }

@router.get('/products')
def get_products():
    return products 