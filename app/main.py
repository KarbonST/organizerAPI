from fastapi import FastAPI, Response, Depends
from rich.jupyter import display
from sqlalchemy import func

from app.utils import *
from app.database import SessionLocal, engine
from app.ORM.Clients import Clients
from app.ORM.Events import Events
from app.ORM.Schema import ClientCreateBase, EventCreateBase, ClientReadBase, EventReadModel

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
    clients = find_all_from_table(db, Clients, Clients.event)
    return [ClientReadBase.model_validate(c) for c in clients]

@app.get("/events/id_inn/{event_id}/clients/{inn}", response_model=ClientReadBase,
         summary="Получить клиента по ИНН и id мероприятия из БД")
def get_client_by_inn_and_event_id(inn: str, event_id: int, db: Session = Depends(get_db)):
    client = find_client_by_inn_and_event_id(db, inn, event_id)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    return ClientReadBase.model_validate(client)

@app.get("/events/number_inn/{event_number}/clients/{inn}", response_model=ClientReadBase,
         summary="Получить клиента по ИНН и номеру мероприятия из БД")
def get_client_by_inn_and_event_number(inn: str, event_number: int, db: Session = Depends(get_db)):
    client = find_client_by_inn_and_event_number(db, inn, event_number)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    return ClientReadBase.model_validate(client)

@app.get("/events", response_model=List[EventReadModel],
         summary="Получить все мероприятия из БД")
def get_all_events(db: Session = Depends(get_db)):
    return find_all_from_table(db, Events)

@app.post("/clients", status_code=201,
          summary="Записать клиента в БД")
def create_client(client_in: ClientCreateBase, db: Session = Depends(get_db)):
    event = find_event_by_number(db, client_in.event_number)
    if not event:
        raise HTTPException(404, detail="Событие не найдено")

    client_exists = find_client_with_inn_on_event(db, client_in)
    if client_exists:
        raise HTTPException(status_code=400, detail="Этот клиент уже зарегистрирован на данном мероприятии")

    client = client_in.model_dump()
    client.pop("event_number")
    client["event_id"] = event.id

    is_created = add_to_db(db, Clients, client)
    if not is_created:
        raise HTTPException(400, detail=f"Ошибка при записи в БД клиента")

    return {f"Клиент с ИНН: {client_in.inn} успешно зарегистрирован на мероприятии {event.name}"}

@app.post("/events", status_code=201
          ,summary="Записать мероприятие в БД")
def create_event(event_in: EventCreateBase, db: Session = Depends(get_db)):
    is_event_exists = find_event_in_table(db, event_in)
    if is_event_exists:
        raise HTTPException(400, detail="Событие с таким именем уже существует")

    max_number = db.query(func.coalesce(func.max(Events.event_number), 0)).scalar()
    event_data = event_in.model_dump()
    event_data["event_number"] = max_number + 1

    is_created = add_to_db(db, Events, event_data)
    if not is_created:
        raise HTTPException(400, detail=f"Ошибка при записи в БД мероприятия")

    return {f"Мероприятие {event_in.name} успешно добавлено"}

@app.delete("/clients", status_code=200,
            summary="Удалить всех клиентов из БД")
def delete_all_clients(db: Session = Depends(get_db)):
    is_deleted = delete_all_from_table(db, Clients)
    if not is_deleted:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении всех клиентов")
    return {"Все клиенты успешно удалены"}

@app.delete("/events/id_inn/{event_id}/clients/{inn}", status_code=200,
            summary="Удалить клиента из БД по его инн и id мероприятия")
def delete_client_on_event_by_id(inn: str, event_id: int, db: Session = Depends(get_db)):
    event = find_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Удаляемый клиент с инн {inn} не найден")

    is_deleted = delete_client_by_inn_and_event_id(db, inn, event_id)
    if not is_deleted:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении клиента по инн: {inn}")
    return {f"Клиент с ИНН: {inn} успешно удален с мероприятия {event.name}"}

@app.delete("/events/number_inn/{event_number}/clients/{inn}", status_code=200,
            summary="Удалить клиента из БД по его инн и номеру мероприятия")
def delete_client_on_event_by_number(inn: str, event_number: int, db: Session = Depends(get_db)):
    event = find_event_by_number(db, event_number)
    if not event:
        raise HTTPException(status_code=404, detail=f"Удаляемый клиент с инн {inn} не найден")

    is_deleted = delete_client_by_inn_and_event_number(db, inn, event_number)
    if not is_deleted:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении клиента по инн: {inn}")
    return {f"Клиент с ИНН: {inn} успешно удален с мероприятия {event.name}"}

@app.delete("/events", status_code=200,
            summary="Удалить все мероприятия из БД")
def delete_all_events(db: Session = Depends(get_db)):
    is_deleted = delete_all_from_table(db, Events)
    if not is_deleted:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении всех мероприятий")
    return {"Все мероприятия и связанные с ними клиенты успешно удалены"}

@app.delete("/events/id/{event_id}", status_code=200,
            summary= "Удалить мероприятие по его id из БД")
def delete_event_by_his_id(event_id: int, db: Session = Depends(get_db)):
    event = find_event_by_id(db, event_id)
    if not event:
        raise HTTPException(404, detail= "Искомого мероприятия не существует")

    removed_event_number = event.event_number

    is_deleted = delete_event_by_id(db, event_id)
    if not is_deleted:
        raise HTTPException(404, detail="Ошибка при удалении мероприятия")

    update_event_numbers(db, removed_event_number)

    return {f"Мероприятие {event.name} и связанные с ним клиенты успешно удалены"}

@app.delete("/events/event_number/{event_number}", status_code=200,
            summary="Удалить мероприятие по его номеру из БД")
def delete_event_by_his_event_number(event_number: int, db: Session = Depends(get_db)):
    event = find_event_by_number(db, event_number)
    if not event:
        raise HTTPException(404, detail="Искомого мероприятия не существует")

    removed_event_number = event_number

    is_deleted = delete_event_by_number(db, event_number)
    if not is_deleted:
        raise HTTPException(404, detail="Ошибка при удалении мероприятия")

    update_event_numbers(db, removed_event_number)

    return {f"Мероприятие {event.name} и связанные с ним клиенты успешно удалены"}


@app.delete("/events/name/{event_name}", status_code=200,
            summary="Удалить мероприятие по его наименованию из БД")
def delete_event_by_his_name(event_name: str, db: Session = Depends(get_db)):
    event = find_event_by_name(db, event_name)
    if not event:
        raise HTTPException(404,  detail= "Искомого мероприятия не существует")

    removed_event_number = event.event_number

    is_deleted = delete_event_by_name(db, event_name)
    if not is_deleted:
        raise HTTPException(404, detail= "Ошибка при удалении мероприятия")

    update_event_numbers(db, removed_event_number)

    return {f"Мероприятие {event_name} и связанные с ним клиенты успешно удалены"}