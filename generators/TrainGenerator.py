import datetime
import random

import requests


def generate_train_data(train_id):
    return {
        "train_id": train_id,
        "route_id": random.choice(list(range(0, 50))),
        "departure_date": str(datetime.datetime.now()),
        "arrival_date": str(datetime.datetime.now())
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
            print(f"Поезд {train_id} успешно добавлен.")
        else:
            print(f"Ошибка при добавлении поезда {train_id}: {response.text}")


if __name__ == "__main__":
    main()
