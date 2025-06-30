from fastapi import FastAPI, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils import get_all_from_db
from app.database import SessionLocal, engine
from app.ORM.Client import Client
from app.ORM.Event import Event
from app.ORM.Schema import ClientBase, EventBase


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
    return get_all_from_db(db, Client)

@app.delete("/clients", status_code=204)
def delete_all_clients(db: Session = Depends(get_db)):
    try:
        db.query(Client).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {e}")

    return Response(status_code=204)

@app.get("/clients/{inn}", response_model=ClientBase)
def get_client_by_inn(inn: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.inn == inn).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client

@app.delete("/clients/{inn}", status_code=204)
def delete_client_by_inn(inn: str, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.inn == inn).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    db.delete(client)
    db.commit()
    return Response(status_code=204)

@app.post("/events", status_code=201)
def create_event(event_in: EventBase, db: Session = Depends(get_db)):
    existing = db.query(Event).filter(Event.name == event_in.name).first()
    if existing:
        raise HTTPException(400, detail="Событие с таким именем уже существует")

    event = Event(name=event_in.name)
    db.add(event)
    db.commit()
    db.refresh(event)

    return {"id": event.id, "name": event.name}

@app.get("/events", response_model=List[EventBase])
def get_all_events(db: Session = Depends(get_db)):
    return get_all_from_db(db, Event)