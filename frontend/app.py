import os

import requests  # streamlit-пен бірге орнатылады
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Airline Ticket Booking", page_icon="✈️")
st.title("✈️ Airline Ticket Booking System")


def api_get(path: str):
    return requests.get(f"{API_URL}{path}", timeout=5).json()


def api_post(path: str, payload: dict | None = None):
    return requests.post(f"{API_URL}{path}", json=payload, timeout=5)


def show_error(resp: requests.Response):
    st.error(resp.json().get("detail", resp.text))


try:
    flights = api_get("/flights/")
    passengers = api_get("/passengers/")
    bookings = api_get("/bookings/")
except requests.RequestException:
    st.error("API қолжетімсіз. Алдымен `python -m uvicorn main:app --reload` іске қосыңыз.")
    st.stop()

tab_flights, tab_book, tab_passengers, tab_bookings = st.tabs(
    ["Рейстер", "Брондау", "Жолаушылар", "Менің брондауларым"]
)

# --- Рейстер ---
with tab_flights:
    if flights:
        st.dataframe(flights, use_container_width=True)
    else:
        st.info("Әзірге рейстер жоқ.")

# --- Брондау ---
with tab_book:
    if not flights or not passengers:
        st.info("Брондау үшін кемінде бір рейс және бір жолаушы керек.")
    else:
        flight = st.selectbox(
            "Рейс",
            flights,
            format_func=lambda f: f"{f['flight_number']}: {f['origin']} → {f['destination']} ({f['price']:,.0f} ₸)",
        )
        availability = api_get(f"/flights/{flight['id']}/availability")
        st.caption(f"Бос орын: {availability['seats_available']} / {availability['seats_total']}")
        passenger = st.selectbox(
            "Жолаушы", passengers, format_func=lambda p: f"{p['full_name']} ({p['email']})"
        )
        seat = st.text_input("Орын (бос қалдырсаңыз, автоматты беріледі)")
        if st.button("Брондау"):
            resp = api_post(
                "/bookings/",
                {"flight_id": flight["id"], "passenger_id": passenger["id"],
                 "seat_number": seat.strip() or None},
            )
            if resp.ok:
                st.success(f"Брондалды! Брондау №{resp.json()['id']}, орын: {resp.json()['seat_number']}")
            else:
                show_error(resp)

# --- Жолаушылар ---
with tab_passengers:
    if passengers:
        st.dataframe(passengers, use_container_width=True)
    with st.form("new_passenger", clear_on_submit=True):
        st.subheader("Жаңа жолаушы")
        full_name = st.text_input("Аты-жөні")
        email = st.text_input("Email")
        passport = st.text_input("Төлқұжат нөмірі")
        if st.form_submit_button("Қосу"):
            if not full_name or not email:
                st.warning("Аты-жөні мен email міндетті.")
            else:
                resp = api_post(
                    "/passengers/",
                    {"full_name": full_name, "email": email, "passport_number": passport or None},
                )
                if resp.ok:
                    st.success("Жолаушы қосылды. Беттi жаңартыңыз.")
                else:
                    show_error(resp)

# --- Брондаулар ---
with tab_bookings:
    if not bookings:
        st.info("Әзірге брондау жоқ.")
    else:
        st.dataframe(bookings, use_container_width=True)
        active = [b for b in bookings if b["status"] == "confirmed"]
        if active:
            to_cancel = st.selectbox(
                "Бас тартылатын брондау",
                active,
                format_func=lambda b: f"№{b['id']} — рейс {b['flight_id']}, орын {b['seat_number']}",
            )
            if st.button("Брондаудан бас тарту"):
                resp = api_post(f"/bookings/{to_cancel['id']}/cancel")
                if resp.ok:
                    st.success("Брондау бас тартылды. Беттi жаңартыңыз.")
                else:
                    show_error(resp)
