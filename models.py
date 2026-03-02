from pydantic import BaseModel

class GISLocation(BaseModel):
    name: str
    teryt: str
