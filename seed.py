"""Сынақ рейстерін базаға қосады. Қайта іске қосқанда қайталамайды.

Іске қосу: python seed.py
"""
from datetime import datetime

from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.models import Flight, Passenger

PASSENGERS = [
    Passenger(full_name="Aigerim Sadykova", email="aigerim@example.com", passport_number="N1234567"),
    Passenger(full_name="Dias Nurlanov", email="dias@example.com", passport_number="N7654321"),
    Passenger(full_name="Madina Ospanova", email="madina@example.com", passport_number="N1122334"),
]

FLIGHTS = [
    Flight(flight_number="KC101", origin="Astana", destination="Almaty",
           departure_time=datetime(2026, 12, 1, 8, 0), arrival_time=datetime(2026, 12, 1, 9, 45),
           price=28000, seats_total=150),
    Flight(flight_number="KC102", origin="Almaty", destination="Astana",
           departure_time=datetime(2026, 12, 1, 18, 30), arrival_time=datetime(2026, 12, 1, 20, 15),
           price=29500, seats_total=150),
    Flight(flight_number="KC215", origin="Astana", destination="Istanbul",
           departure_time=datetime(2026, 12, 3, 6, 15), arrival_time=datetime(2026, 12, 3, 10, 30),
           price=145000, seats_total=180),
    Flight(flight_number="KC330", origin="Almaty", destination="Dubai",
           departure_time=datetime(2026, 12, 5, 2, 40), arrival_time=datetime(2026, 12, 5, 6, 0),
           price=160000, seats_total=180),
    Flight(flight_number="KC408", origin="Astana", destination="Moscow",
           departure_time=datetime(2026, 12, 7, 11, 0), arrival_time=datetime(2026, 12, 7, 12, 50),
           price=95000, seats_total=160),
    Flight(flight_number="KC512", origin="Shymkent", destination="Astana",
           departure_time=datetime(2026, 12, 9, 14, 20), arrival_time=datetime(2026, 12, 9, 16, 30),
           price=34000, seats_total=120),
]


def main() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        existing = set(session.exec(select(Flight.flight_number)).all())
        new = [f for f in FLIGHTS if f.flight_number not in existing]
        session.add_all(new)

        emails = set(session.exec(select(Passenger.email)).all())
        new_passengers = [p for p in PASSENGERS if p.email not in emails]
        session.add_all(new_passengers)

        session.commit()
        print(f"Рейстер қосылды: {len(new)}, бұрыннан бар: {len(FLIGHTS) - len(new)}")
        print(f"Жолаушылар қосылды: {len(new_passengers)}, бұрыннан бар: {len(PASSENGERS) - len(new_passengers)}")


if __name__ == "__main__":
    main()
