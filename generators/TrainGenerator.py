import datetime
import random

import requests


def generate_train_data(train_id):
    return {
        "station_id": train_id,
        "route_id": random.choice([i for i in range(0, 50)]),
        "departure_date": datetime.datetime.now(),
        "arrival_date": datetime.datetime.now()
    }


def main():
    url = "http://localhost:8000/train/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    for train_id in range(0, 1000):
        station_data = generate_train_data(train_id)
        response = requests.post(url, json=station_data, headers=headers)
        if response.status_code == 200:
            print(f"Станция {train_id} успешно добавлена.")
        else:
            print(f"Ошибка при добавлении станции {train_id}: {response.text}")


if __name__ == "__main__":
    main()
