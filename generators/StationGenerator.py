import requests
import random


def generate_station_data(station_id):
    # Генерируем некоторые данные для станции
    name = f"Станция {station_id}"
    region = random.choice(
        ["Московская область", "Ленинградская область", "Нижегородская область", "Краснодарский край"])
    return {
        "station_id": station_id,
        "name": name,
        "region": region
    }


def main():
    url = "http://localhost:8000/station/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    for station_id in range(0, 1000):
        station_data = generate_station_data(station_id)
        response = requests.post(url, json=station_data, headers=headers)
        if response.status_code == 200:
            print(f"Станция {station_id} успешно добавлена.")
        else:
            print(f"Ошибка при добавлении станции {station_id}: {response.text}")


if __name__ == "__main__":
    main()
