from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Passenger

router = APIRouter(prefix="/passengers", tags=["passengers"])


@router.get("/", response_model=list[Passenger])
def list_passengers(session: Session = Depends(get_session)):
    return session.exec(select(Passenger)).all()


@router.post("/", response_model=Passenger, status_code=201)
def create_passenger(passenger: Passenger, session: Session = Depends(get_session)):
    if session.exec(select(Passenger).where(Passenger.email == passenger.email)).first():
        raise HTTPException(409, "Бұл email-мен жолаушы бұрыннан бар")
    session.add(passenger)
    session.commit()
    session.refresh(passenger)
    return passenger
