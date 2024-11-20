from pydantic import BaseModel

class Inventory(BaseModel):
    name: str = ""
    location: str = ""
    id: int= -1
