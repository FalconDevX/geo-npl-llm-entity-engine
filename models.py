from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AdminSearch(Base):
    __tablename__ = "v_admin_search"

    nazwa = Column(String)
    typ = Column(String)
    kod = Column(String, primary_key=True)

    woj = Column(String)
    pow = Column(String)
    gmi = Column(String)