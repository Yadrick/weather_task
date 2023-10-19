def city_name_validation(weather_data_list: dict):
    if weather_data_list is None:
        return False
    return True


def location_validation(lat: float, lon: float):
    if lat > 180 or lon > 180:
        return False
    else:
        return True
