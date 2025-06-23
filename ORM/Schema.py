from pydantic import BaseModel, constr

class ClientCreate(BaseModel):
    inn: constr(pattern=r"^\d{10}$")
    fullname: str
    company: str
    phone: constr(pattern=r"^\+7\s\d{3}\s\d{3}-\d{2}-\d{2}$")
    worker_fullname: str

    class Config:
        orm_mode = True
