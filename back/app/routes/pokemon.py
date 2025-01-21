from flask import Blueprint, jsonify, current_app
from app.services.pokeapi_service import fetch_pokemon_list

api = Blueprint('pokemon', __name__)

@api.route('/load_data', methods=['GET'])
def load_data():
    try:
        pokemon_list = fetch_pokemon_list()
        current_app.cache.set('pokemon_list', pokemon_list)
        return jsonify(pokemon_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/get_data', methods=['GET'])
def get_data():
    try:
        pokemon_list = current_app.cache.get('pokemon_list')
        if not pokemon_list:
            return jsonify({"error": "No hay datos en caché. Usa /load_data primero."}), 400
        return jsonify(pokemon_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
