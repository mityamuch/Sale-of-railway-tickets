import datetime
import random

import requests


def generate_ticket_data(ticket_id):
    return {
        "ticket_id": ticket_id,
        "train_id": random.choice([i for i in range(0,20)]),
        "seat_number": random.choice([i for i in range(0, 50)]),
        "status": "string",
        "booking_time":  str(datetime.datetime.now()),
        "price": random.choice([i for i in (100,1000,10000)]),
        "payment_time":  str(datetime.datetime.now()),
        "route_id": random.choice([i for i in range(0, 50)]),
    }


def main():
    url = "http://localhost:8000/ticket/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    for ticket_id in range(0, 1000):
        station_data = generate_ticket_data(ticket_id)
        response = requests.post(url, json=station_data, headers=headers)
        if response.status_code == 200:
            print(f"Билет {ticket_id} успешно добавлен.")
        else:
            print(f"Ошибка при добавлении билета {ticket_id}: {response.text}")


if __name__ == "__main__":
    main()