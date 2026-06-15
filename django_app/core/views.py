from django.shortcuts import render
import requests 
from django.http import JsonResponse 
# Create your views here.

def home(request):
    response = requests.get("http://127.0.0.1:8001/ai")
    data = response.json() 
    return JsonResponse({
        "message": "Hello From Django!",
        "fastapi_response": data
    })

