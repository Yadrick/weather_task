import geocoder
import requests

def get_location():
    location = geocoder.ip('me')
    return location

def get_info_by_ip(ip='127.0.0.1'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        print(response)
        data = {
            'latitude:': response.get('lat'),
            'longitude:': response.get('lon'),
        }

        print(data.get("latitude"))
    except requests.exceptions.ConnectionError:
        print("[!] Please check your connection!")

    return data


if __name__ == '__main__':
    location = get_location()

    if location.ok:

        # latitude, longitude = location.latlng
        # address = location.address
        # print(f"Ваши координаты: Широта {latitude}, Долгота {longitude}")
        # print(f"Ваше местоположение: {address}")


        get_info_by_ip()
    else:
        print("Не удалось определить местоположение.")