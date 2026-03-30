from pydantic import BaseModel

class NewRole(BaseModel):
    role: str