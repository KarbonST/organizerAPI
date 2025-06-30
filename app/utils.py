from typing import Type, Any, List, Dict

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.ORM.Client import Client
from app.ORM.Event import Event
from app.ORM.Schema import ClientCreateBase, EventBase, ClientReadBase


def find_all_from_table(db: Session, model: Type[Any], *relations_to_load: Any) -> List[Any]:
    query = db.query(model)
    for rel in relations_to_load:
        query = query.options(joinedload(rel))
    return query.all()

def find_client_by_inn_and_event(db: Session, inn: str, event_id: int):
    return db.query(Client).filter(Client.inn == inn, Client.event_id == event_id)


def find_event_in_client_table(db: Session, client_in: ClientCreateBase):
    return db.query(Event).get(client_in.event_id)

def delete_all_from_table(db: Session, model: Type[Any]) -> int:
    try:
        deleted = db.query(model).delete(synchronize_session=False)
        db.commit()
        return deleted
    except Exception as e:
        db.rollback()
        # Пробрасываем HTTPException, чтобы маршрут отдал корректный 500
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {e}")

def delete_client_by_inn_and_event(db: Session, inn: str, event_id: int):
    client = find_client_by_inn_and_event(db, inn, event_id)

    try:
        db.delete(client)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {e}")

def delete_event_by_id(db:Session, event_id: int):
    pass

def find_client_with_inn_on_event(db: Session, client_in: ClientCreateBase):
    return db.query(Client).filter(Client.inn == client_in.inn, Client.event_id == client_in.event_id).first()

def find_event_in_table(db: Session, event_in: EventBase):
    return db.query(Event).filter(Event.name == event_in.name).first()

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