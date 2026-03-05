from pydantic import BaseModel

class SearchResult(BaseModel):
    nazwa: str
    kod: str
    typ: str