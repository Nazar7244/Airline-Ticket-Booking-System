from typing import Optional

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class FlightBase(SQLModel):
    """Рейстің жалпы өрістері. API-да кіріс схемасы ретінде де қолданылады
    (table=True модельдері кіріс деректерін валидацияламайды)."""

    flight_number: str = Field(index=True, unique=True)
    origin: str
    destination: str
    # Әуежайдың жергілікті уақыты (уақыт белдеуінсіз)
    departure_time: NaiveDatetime
    arrival_time: NaiveDatetime
    price: float
    seats_total: int


class Flight(FlightBase, table=True):
    """Рейс."""

    id: Optional[int] = Field(default=None, primary_key=True)
