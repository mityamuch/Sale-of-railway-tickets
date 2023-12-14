import datetime
import random

import requests


def generate_ticket_data(train_id):
    return {
        "ticket_id": train_id,
        "train_id": random.choice([i for i in range(0,20)]),
        "seat_number": random.choice([i for i in range(0, 50)]),
        "status": "string",
        "booking_time":  datetime.datetime.now(),
        "payment_time":  datetime.datetime.now(),
        "route_id": random.choice([i for i in range(0, 50)]),
    }


def main():
    url = "http://localhost:8000/train/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    for ticket_id in range(0, 1000):
        station_data = generate_ticket_data(ticket_id)
        response = requests.post(url, json=station_data, headers=headers)
        if response.status_code == 200:
            print(f"Станция {ticket_id} успешно добавлена.")
        else:
            print(f"Ошибка при добавлении станции {ticket_id}: {response.text}")


if __name__ == "__main__":
    main()