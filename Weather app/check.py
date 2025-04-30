import requests

API_KEY = "8ee3a1b946fa2657b680e522834734a3815f1a14"

def get_coordinates(city_name):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    res = requests.get(url)
    data = res.json()
    print("Raw API response for", repr(city_name), "→", data)    # debug output

    # If the API returned an empty list, handle it
    if not data:
        print(f"No results found for city {city_name!r}")
        return None, None, None, None

    # Otherwise unpack the first result
    first = data[0]
    lat = first.get("lat")
    lon = first.get("lon")
    name = first.get("name")
    country = first.get("country")
    print(f"Parsed: lat={lat}, lon={lon}, name={name!r}, country={country!r}")
    return lat, lon, name, country

if __name__ == "__main__":
    # Test with a valid city
    print("\n--- Testing with valid city ---")
    get_coordinates("London")

    # Test with a nonsense city
    print("\n--- Testing with invalid city ---")
    get_coordinates("ThisCityDoesNotExist1234")

    # Test with an empty string
    print("\n--- Testing with empty string ---")
    get_coordinates("")
