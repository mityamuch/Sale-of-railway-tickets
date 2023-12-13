import random

import requests


def generate_route_data(route_id):
    # Генерируем данные для маршрута
    route_name = f"Маршрут {route_id}"
    stations = random.sample(range(100), random.randint(3, 10))
    return {
        "route_id": route_id,
        "stations": stations,
        "route_name": route_name
    }


def main():
    url = "http://localhost:8000/route/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    for route_id in range(0, 101):
        route_data = generate_route_data(route_id)
        response = requests.post(url, json=route_data, headers=headers)
        if response.status_code == 200:
            print(f"Маршрут {route_id} успешно добавлен.")
        else:
            print(f"Ошибка при добавлении маршрута {route_id}: {response.text}")


if __name__ == "__main__":
    main()
