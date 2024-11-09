import requests

def get_city_coordinates(city):
    api_key = 'YOUR_API_KEY'  # Replace with your own API key
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        results = data['results'][0]
        geometry = results['geometry']
        bounds = geometry['bounds']

        northeast = bounds['northeast']
        southwest = bounds['southwest']

        upper_latitude = northeast['lat']
        lower_latitude = southwest['lat']
        eastern_longitude = northeast['lng']
        western_longitude = southwest['lng']

        return upper_latitude, lower_latitude, eastern_longitude, western_longitude

# Example usage
city = 'New York'
upper_latitude, lower_latitude, eastern_longitude, western_longitude = get_city_coordinates(city)
print(f'Upper Latitude: {upper_latitude}')
print(f'Lower Latitude: {lower_latitude}')
print(f'Eastern Longitude: {eastern_longitude}')
print(f'Western Longitude: {western_longitude}')