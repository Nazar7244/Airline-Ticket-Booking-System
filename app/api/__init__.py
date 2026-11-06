from fastapi import APIRouter

from app.api import bookings, flights, passengers

api_router = APIRouter()
api_router.include_router(flights.router)
api_router.include_router(passengers.router)
api_router.include_router(bookings.router)

__all__ = ["api_router"]
