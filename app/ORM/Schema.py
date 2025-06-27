from pydantic import BaseModel, constr

class ClientBase(BaseModel):
    worker_fullname: str
    inn: constr(pattern=r"^\d{10}$")
    company_name: str
    is_client: constr(pattern=r"^(да|нет)$")
    working_sphere: str
    fullname: str
    phone: constr(pattern=r"^\+7\s\d{3}\s\d{3}-\d{2}-\d{2}$")
    client_request: str


    model_config = {
        "from_attributes": True,  # вместо orm_mode
    }