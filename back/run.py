from flask import Flask, jsonify
from flask_caching import Cache
import requests

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

@app.route('/')
def home():
    return jsonify({"message": "Servidor funcionando!"})

@app.route('/load_data', methods=['GET'])
def load_data():
    try:
        url = "https://pokeapi.co/api/v2/pokemon?limit=151"
        response = requests.get(url)
        data = response.json()

        pokemon_list = [
            {
                "name": pokemon['name'],
                "url": pokemon['url']
            }
            for pokemon in data['results']
        ]
        cache.set('pokemon_list', pokemon_list)
        return jsonify(pokemon_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
