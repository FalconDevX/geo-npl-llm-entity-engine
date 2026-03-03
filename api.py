from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM search_admin(:q)"), {"q": q})
    return result.mappings().all()
