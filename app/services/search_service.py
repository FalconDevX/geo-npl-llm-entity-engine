from sqlalchemy import text
from sqlalchemy.orm import Session

def search_place(db: Session, query: str):
    result = db.execute(
        text("SELECT * FROM search_admin(:q)"),
        {"q": query}
    )

    return result.mappings().all()