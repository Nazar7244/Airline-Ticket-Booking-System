from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Booking, BookingCreate, Flight, Passenger

router = APIRouter(prefix="/bookings", tags=["bookings"])


def _taken_seats(session: Session, flight_id: int) -> set[str]:
    """Рейстегі расталған брондаулармен алынған орындар."""
    rows = session.exec(
        select(Booking.seat_number).where(
            Booking.flight_id == flight_id, Booking.status == "confirmed"
        )
    ).all()
    return {seat for seat in rows if seat}


@router.get("/", response_model=list[Booking])
def list_bookings(session: Session = Depends(get_session)):
    return session.exec(select(Booking)).all()


@router.get("/{booking_id}", response_model=Booking)
def get_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Брондау табылмады")
    return booking


@router.post("/", response_model=Booking, status_code=201)
def create_booking(data: BookingCreate, session: Session = Depends(get_session)):
    flight = session.get(Flight, data.flight_id)
    if not flight:
        raise HTTPException(404, "Рейс табылмады")
    if not session.get(Passenger, data.passenger_id):
        raise HTTPException(404, "Жолаушы табылмады")

    taken = _taken_seats(session, flight.id)
    if len(taken) >= flight.seats_total:
        raise HTTPException(409, "Бұл рейсте бос орын қалмады")

    seat = data.seat_number
    if seat is None:
        # ең алғашқы бос орынды береміз: 1, 2, 3, ...
        seat = next(
            (str(n) for n in range(1, flight.seats_total + 1) if str(n) not in taken), None
        )
        if seat is None:
            raise HTTPException(409, "Бұл рейсте бос орын қалмады")
    elif seat in taken:
        raise HTTPException(409, f"{seat} орны бос емес")

    booking = Booking(flight_id=flight.id, passenger_id=data.passenger_id, seat_number=seat)
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


@router.post("/{booking_id}/cancel", response_model=Booking)
def cancel_booking(booking_id: int, session: Session = Depends(get_session)):
    booking = session.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Брондау табылмады")
    if booking.status == "cancelled":
        raise HTTPException(409, "Брондау бұрыннан бас тартылған")
    booking.status = "cancelled"  # орын босайды
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking
