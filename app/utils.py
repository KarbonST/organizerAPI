from typing import Type, Any, List
from sqlalchemy.orm import Session

def get_all_from_db(db: Session, model: Type[Any]) -> List[Any]:
    return db.query(model).all()