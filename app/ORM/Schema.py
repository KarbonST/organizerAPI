from pydantic import BaseModel, constr

class ClientCreateBase(BaseModel):
    worker_fullname: str
    inn: constr(pattern=r"^\d{10,}$")
    company_name: str
    is_client: constr(pattern=r'^(?i)(?:да|нет)$')
    working_sphere: str
    contact_fullname: str
    phone: str
    client_request: str

    event_number: int

    model_config = {
        "from_attributes": True,
    }

class ClientReadBase(BaseModel):
    worker_fullname: str
    event_name: str
    inn: constr(pattern=r"^\d{10,}$")
    company_name: str
    is_client: constr(pattern=r"^(?i)(?:да|нет)$")
    working_sphere: str
    contact_fullname: str
    phone: str
    client_request: str


    model_config = {
        "from_attributes": True,
    }

class EventCreateBase(BaseModel):
    name: str

    model_config = {
        "from_attributes": True,
    }

class EventReadModel(BaseModel):
    name: str
    event_number: int

    model_config = {
        "from_attributes": True,
    }