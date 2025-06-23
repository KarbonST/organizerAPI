from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from ORM.Client import Client
from ORM.Schema import ClientCreate

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clients", status_code=201)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):

    db_client = Client(**client_in.model_dump())
    db.add(db_client)
    try:
        db.commit()
        db.refresh(db_client)
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail="Ошибка при записи в БД: " + str(e))
    return {"id": db_client.id}
