from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

ENGINE = create_engine("sqlite:///:memory:")
# Engine = create_engine("sqlite:///x.db")
Localsession = sessionmaker(bind=ENGINE)


class Base(DeclarativeBase): ...
