from fastapi import FastAPI, Response, Depends

from app.utils import *
from app.database import SessionLocal, engine
from app.ORM.Client import Client
from app.ORM.Event import Event
from app.ORM.Schema import ClientCreateBase, EventBase, ClientReadBase

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/clients", response_model=List[ClientReadBase],
         summary="Получить всех клиентов из БД")
def get_all_clients(db: Session = Depends(get_db)):
    clients = find_all_from_table(db, Client, Client.event)

    return [ClientReadBase.model_validate(c) for c in clients]

@app.get("/events/{event_id}/clients/{inn}", response_model=ClientReadBase,
         summary="Получить клиента по ИНН и номеру мероприятия из БД")
def get_client_by_inn_and_event(inn: str, event_id: int, db: Session = Depends(get_db)):
    client = find_client_by_inn_and_event(db, inn, event_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    return ClientReadBase.model_validate(client)

@app.get("/events", response_model=List[EventBase],
         summary="Получить все мероприятия из БД")
def get_all_events(db: Session = Depends(get_db)):
    return find_all_from_table(db, Event)

@app.post("/clients", status_code=201,
          summary="Записать клиента в БД")
def create_client(client_in: ClientCreateBase, db: Session = Depends(get_db)):
    event = find_event_in_client_table(db, client_in)
    if not event:
        raise HTTPException(404, detail="Событие не найдено")

    client_exists = find_client_with_inn_on_event(db, client_in)
    if client_exists:
        raise HTTPException(status_code=400, detail="Этот клиент уже зарегистрирован на данном мероприятии")

    client = add_to_db(db, Client, client_in.model_dump())

    return {"id": client.id, "inn": client.inn}

@app.post("/events", status_code=201
          ,summary="Записать мероприятие в БД")
def create_event(event_in: EventBase, db: Session = Depends(get_db)):
    is_event_exists = find_event_in_table(db, event_in)
    if is_event_exists:
        raise HTTPException(400, detail="Событие с таким именем уже существует")

    event = add_to_db(db, Event, event_in.model_dump())

    return {"id": event.id, "name": event.name}

@app.delete("/clients", status_code=204,
            summary="Удалить всех клиентов из БД")
def delete_all_clients(db: Session = Depends(get_db)):
    delete_all_from_table(db, Client)

    return Response(status_code=204)

@app.delete("/events/{event_id}/clients/{inn}", status_code=204,
            summary="Удалить клиента из БД по инн и номеру мероприятия")
def delete_client_on_event(inn: str, event_id: int, db: Session = Depends(get_db)):
    delete_client_by_inn_and_event(db, inn, event_id)

    return Response(status_code=204)

@app.delete("/events", status_code=204,
            summary="Удалить все мероприятия из БД")
def delete_all_events(db: Session = Depends(get_db)):
    delete_all_from_table(db, Event)

    return Response(status_code=204)

@app.delete("/events/{event_id}", status_code=204,
            summary= "Удалить мероприятие по его номеру из БД")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    delete_event_by_id(db, event_id)

    return Response(status_code=204)
