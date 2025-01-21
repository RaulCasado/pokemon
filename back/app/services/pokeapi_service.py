import requests

def fetch_pokemon_list(limit=151):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return [
        {"name": pokemon["name"], "url": pokemon["url"]}
        for pokemon in data["results"]
    ]

def get_pokemon_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()