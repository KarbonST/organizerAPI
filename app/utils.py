from typing import Type, Any, List, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.ORM.Client import Client
from app.ORM.Event import Event
from app.ORM.Schema import ClientBase, EventBase


def get_all_from_table(db: Session, model: Type[Any]) -> List[Any]:
    return db.query(model).all()

def delete_all_from_table(db: Session, model: Type[Any]) -> int:
    try:
        deleted = db.query(model).delete(synchronize_session=False)
        db.commit()
        return deleted
    except Exception as e:
        db.rollback()
        # Пробрасываем HTTPException, чтобы маршрут отдал корректный 500
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {e}")

def is_event_in_db(db: Session, client_in: ClientBase):
    ev = db.query(Event).get(client_in.event_id)
    if not ev:
        raise HTTPException(404, detail="Событие не найдено")

def is_client_with_inn_on_event(db: Session, client_in: ClientBase):
    exists = (db.query(Client).filter(Client.inn == client_in.inn, Client.event_id == client_in.event_id).first())
    if exists:
        raise HTTPException(status_code=400, detail="Этот клиент уже зарегистрирован на данном мероприятии")

def is_event_already_in_table(db: Session, event_in: EventBase):
    existing = db.query(Event).filter(Event.name == event_in.name).first()
    if existing:
        raise HTTPException(400, detail="Событие с таким именем уже существует")

def add_to_db(db: Session, model: Type[Any], data: Dict[str, Any]):
    obj = model(**data)
    db.add(obj)

    try:
        db.commit()
        db.refresh(obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=f"Ошибка при записи в БД: {e}")

    return obj