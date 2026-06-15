from fastapi import FastAPI 

app = FastAPI() 
@app.get("/")
def home():
    return {"message": "FastAPI is running!"} 

@app.get("/ai")
def ai_response():
    return {"message": "This message is from the AI endpoint!"}
