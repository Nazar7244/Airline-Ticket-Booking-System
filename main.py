from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # қосымша іске қосылғанда кестелерді жасау
    yield


app = FastAPI(title="Airline Ticket Booking System", lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Airline Ticket Booking System API"}
