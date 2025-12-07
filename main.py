from fastapi import FastAPI, HTTPException, Depends

from database import SessionLocal

app = FastAPI(title="crm API")

def get_db():
    """определяем БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/operators/", response_model=OperatorResp, status_code=201)
def create_operator(

