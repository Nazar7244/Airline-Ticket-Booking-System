from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Booking(SQLModel, table=True):
    """Брондау: жолаушы мен рейсті байланыстырады."""

    id: Optional[int] = Field(default=None, primary_key=True)
    flight_id: int = Field(foreign_key="flight.id")
    passenger_id: int = Field(foreign_key="passenger.id")
    seat_number: Optional[str] = None
    status: str = Field(default="confirmed")  # confirmed | cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BookingCreate(SQLModel):
    """Брондау жасау үшін клиент жіберетін деректер."""

    flight_id: int
    passenger_id: int
    seat_number: Optional[str] = None  # бос болса, бос орын автоматты берілетін болады
