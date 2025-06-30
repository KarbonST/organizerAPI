from fastapi import FastAPI, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils import get_all_from_table, delete_all_from_table, is_event_in_db, is_client_with_inn_on_event
from app.utils import is_event_already_in_table, add_to_db
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
    is_event_in_db(db, client_in)
    is_client_with_inn_on_event(db, client_in)

    client = add_to_db(db, Client, client_in.model_dump())

    return {"id": client.id, "inn": client.inn}

@app.get("/clients", response_model=List[ClientBase])
def get_all_clients(db: Session = Depends(get_db)):
    return get_all_from_table(db, Client)

@app.delete("/clients", status_code=204)
def delete_all_clients(db: Session = Depends(get_db)):
    delete_all_from_table(db, Client)
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
    is_event_already_in_table(db, event_in)

    event = add_to_db(db, Event, event_in.model_dump())

    return {"id": event.id, "name": event.name}

@app.get("/events", response_model=List[EventBase])
def get_all_events(db: Session = Depends(get_db)):
    return get_all_from_table(db, Event)

@app.delete("/events", status_code=204)
def delete_all_events(db: Session = Depends(get_db)):
    delete_all_from_table(db, Event)
    return Response(status_code=204)

@app.delete("/events/{id}", status_code=204)
