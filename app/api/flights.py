from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Booking, Flight, FlightBase

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("/", response_model=list[Flight])
def list_flights(session: Session = Depends(get_session)):
    return session.exec(select(Flight)).all()


@router.get("/{flight_id}/availability")
def flight_availability(flight_id: int, session: Session = Depends(get_session)):
    """Рейстегі бос орындар саны."""
    flight = session.get(Flight, flight_id)
    if not flight:
        raise HTTPException(404, "Рейс табылмады")
    booked = len(
        session.exec(
            select(Booking.id).where(Booking.flight_id == flight_id, Booking.status == "confirmed")
        ).all()
    )
    return {"flight_id": flight_id, "seats_total": flight.seats_total,
            "seats_booked": booked, "seats_available": flight.seats_total - booked}


@router.post("/", response_model=Flight, status_code=201)
def create_flight(data: FlightBase, session: Session = Depends(get_session)):
    if session.exec(select(Flight).where(Flight.flight_number == data.flight_number)).first():
        raise HTTPException(409, "Бұл нөмірмен рейс бұрыннан бар")
    flight = Flight.model_validate(data)
    session.add(flight)
    session.commit()
    session.refresh(flight)
    return flight
