from typing import Type, Any, List, Dict

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.ORM.Clients import Clients
from app.ORM.Events import Events
from app.ORM.Schema import ClientCreateBase, EventBase, ClientReadBase


def find_all_from_table(db: Session, model: Type[Any], *relations_to_load: Any) -> List[Any]:
    query = db.query(model)
    for rel in relations_to_load:
        query = query.options(joinedload(rel))
    return query.all()

def find_client_by_inn_and_event(db: Session, inn: str, event_id: int):
    return db.query(Clients).filter(Clients.inn == inn, Clients.event_id == event_id).first()

def find_event_in_client_table(db: Session, client_in: ClientCreateBase):
    return db.query(Events).filter(Events.id == client_in.event_id).first()

def find_client_with_inn_on_event(db: Session, client_in: ClientCreateBase):
    return db.query(Clients).filter(Clients.inn == client_in.inn, Clients.event_id == client_in.event_id).first()

def find_event_in_table(db: Session, event_in: EventBase):
    return db.query(Events).filter(Events.name == event_in.name).first()

def find_event_by_id(db: Session, event_id: int):
    event = db.query(Events).filter(Events.id == event_id).first()
    return event.name if event else None

def delete_all_from_table(db: Session, model: Type[Any]) -> bool:
    try:
        db.query(model).delete(synchronize_session=False)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False

def delete_client_by_inn_and_event(db: Session, inn: str, event_id: int) -> bool:
    client = find_client_by_inn_and_event(db, inn, event_id)
    try:
        db.delete(client)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return False
    return True

def delete_event_by_id(db:Session, event_id: int):
    deleted = db.query(Events).filter(Events.id == event_id).delete()
    db.commit()
    return bool(deleted)

def add_to_db(db: Session, model: Type[Any], data: Dict[str, Any]) -> bool:
    obj = model(**data)
    db.add(obj)

    try:
        db.commit()
        db.refresh(obj)
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
