from pydantic import BaseModel

class ClientSchema(BaseModel):
    id: int
    