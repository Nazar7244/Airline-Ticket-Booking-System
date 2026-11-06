from typing import Optional

from sqlmodel import Field, SQLModel


class Passenger(SQLModel, table=True):
    """Жолаушы."""

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(index=True, unique=True)
    passport_number: Optional[str] = None
