import geocoder

def get_location():
    location = geocoder.ip('me')
    print(location)
    return location

if __name__ == '__main__':
    location = get_location()

    if location.ok:

        latitude, longitude = location.latlng
        address = location.address
        print(f"Ваши координаты: Широта {latitude}, Долгота {longitude}")
        print(f"Ваше местоположение: {address}")
    else:
        print("Не удалось определить местоположение.")