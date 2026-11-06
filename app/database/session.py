import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./airline.db")

# check_same_thread=False — SQLite үшін FastAPI-мен жұмыс істеуге қажет
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Барлық модельдер бойынша кестелерді жасайды."""
    import app.models  # noqa: F401  (модельдерді SQLModel.metadata-ға тіркеу)

    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency: әр сұранысқа бір сессия."""
    with Session(engine) as session:
        yield session
