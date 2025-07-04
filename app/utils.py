from typing import Type, Any, List, Dict

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.ORM.Clients import Clients
from app.ORM.Events import Events
from app.ORM.Schema import ClientCreateBase, EventCreateBase


def find_all_from_table(db: Session, model: Type[Any], *relations_to_load: Any) -> List[Any]:
    query = db.query(model)
    for rel in relations_to_load:
        query = query.options(joinedload(rel))
    return query.all()

def find_client_by_inn_and_event_id(db: Session, inn: str, event_id: int):
    return db.query(Clients).filter(Clients.inn == inn, Clients.event_id == event_id).first()

def find_client_by_inn_and_event_number(db: Session, inn: str, event_number: int):
    return db.query(Clients).join(Events,Clients.event_id == Events.id).filter(Clients.inn == inn, Events.event_number == event_number).first()

def find_event_in_client_table_by_id(db: Session, client_in: ClientCreateBase):
    return db.query(Events).filter(Events.id == client_in.event_id).first()

def find_event_by_name(db: Session, event_name: str):
    return db.query(Events).filter(Events.name == event_name).first()

def find_client_with_inn_on_event(db: Session, client_in: ClientCreateBase):
    event = find_event_by_number(db, client_in.event_number)
    if not event:
        return None
    return db.query(Clients).filter(Clients.inn == client_in.inn, Clients.event_id == event.id).first()

def find_event_in_table(db: Session, event_in: EventCreateBase):
    return db.query(Events).filter(Events.name == event_in.name).first()

def find_event_by_id(db: Session, event_id: int):
    return db.query(Events).filter(Events.id == event_id).first()

def find_event_by_number(db: Session, event_number: int):
    return db.query(Events).filter(Events.event_number == event_number).first()

def delete_all_from_table(db: Session, model: Type[Any]) -> bool:
    try:
        db.query(model).delete(synchronize_session=False)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False

def delete_client_by_inn_and_event_id(db: Session, inn: str, event_id: int) -> bool:
    client = find_client_by_inn_and_event_id(db, inn, event_id)
    try:
        db.delete(client)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return False
    return True

def delete_client_by_inn_and_event_number(db: Session, inn: str, event_number: int) -> bool:
    client = find_client_by_inn_and_event_number(db, inn, event_number)
    try:
        db.delete(client)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return False
    return True

def delete_event_by_id(db:Session, event_id: int):
    event = find_event_by_id(db, event_id)
    if not event:
        return False

    db.delete(event)
    db.commit()
    return True

def delete_event_by_number(db:Session, event_number: int):
    event = find_event_by_number(db, event_number)
    if not event:
        return False

    db.delete(event)
    db.commit()
    return True

def delete_event_by_name(db:Session, event_name: str) -> bool:
    event = find_event_by_name(db, event_name)
    if not event:
        return False

    db.delete(event)
    db.commit()
    return True

def update_event_numbers(db: Session, removed_event_number: int):
    db.query(Events) \
      .filter(Events.event_number > removed_event_number) \
      .update(
         {Events.event_number: Events.event_number - 1},
         synchronize_session="fetch"
      )
    db.commit()

def add_to_db(db: Session, model: Type[Any], data: Dict[str, Any]) -> bool:
    obj = model(**data)
    db.add(obj)

    try:
        db.commit()
        db.refresh(obj)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print("DB error in add_to_db:", e)
        return False
