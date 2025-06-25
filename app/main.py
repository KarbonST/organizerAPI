from fastapi import FastAPI, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine
from app.ORM.Client import Client
from app.ORM.Schema import ClientBase

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clients", status_code=201)
def create_client(client_in: ClientBase, db: Session = Depends(get_db)):

    db_client = Client(**client_in.model_dump())
    db.add(db_client)
    try:
        db.commit()
        db.refresh(db_client)
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail="Ошибка при записи в БД: " + str(e))
    return {"id": db_client.id}

@app.get("/clients", response_model=List[ClientBase])
def get_all_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients

@app.delete("/clients", status_code=204)
def delete_all_clients(db: Session = Depends(get_db)):

    try:
        db.query(Client).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {e}")

    return Response(status_code=204)
