from flask import Blueprint, jsonify, current_app
from app.services.pokeapi_service import fetch_pokemon_list
from flask import request
from threading import Thread
import requests
import random

api = Blueprint('pokemon', __name__)

def preload_pokemon_data(pokemon_list, cache):
    for pokemon in pokemon_list:
        pokemon_name = pokemon['name']
        if cache.get(f"pokemon_{pokemon_name}"):
            continue

        response = requests.get(pokemon['url'])
        if response.status_code == 200:
            detailed_data = response.json()
            cache.set(f"pokemon_{pokemon_name}", detailed_data)


@api.route('/load_data', methods=['GET'])
def load_data():
    try:
        url = "https://pokeapi.co/api/v2/pokemon?limit=151"
        response = requests.get(url)
        data = response.json()

        pokemon_list = [{"name": pokemon['name'], "url": pokemon['url']} for pokemon in data['results']]
        current_app.cache.set('pokemon_list', pokemon_list)

        thread = Thread(target=preload_pokemon_data, args=(pokemon_list,current_app.cache))
        thread.start()

        return jsonify({"message": "Datos basicos cargados", "data": pokemon_list})
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
    
@api.route('/setup_game', methods=['POST'])
def setup_game():
    try:
        data = request.get_json()
        language = data.get('language', 'en')
        difficulty = data.get('difficulty', 'easy')

        game_config = {
            "language": language,
            "difficulty": difficulty,
            "questions": []
        }
        current_app.cache.set('game_config', game_config)
        return jsonify({"message": "Configuración del juego guardada", "config": game_config})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/generate_question', methods=['GET'])
def generate_question():
    try:
        game_config = current_app.cache.get('game_config')
        if not game_config:
            return jsonify({"error": "No game configuration found. Use /setup_game first."}), 400

        pokemon_list = current_app.cache.get('pokemon_list')
        if not pokemon_list:
            return jsonify({"error": "No Pokemon data in cache. Use /load_data first."}), 400

        difficulty = game_config.get('difficulty', 'easy')
        question = {}

        if difficulty == 'easy':
            question = {
                "question": f"Nombra 4 Pokemon de la primera generacion.",
                "options": []
            }
            for _ in range(4):
                random_pokemon = random.choice(pokemon_list)
                question['options'].append(random_pokemon['name'])
            random.shuffle(question['options'])

        else:
            selected_pokemon = random.choice(pokemon_list)
            detailed_data = current_app.cache.get(f"pokemon_{selected_pokemon['name']}")

            if not detailed_data:
                question = {
                    "question": f"Nombra 4 Pokemon de la primera generacion.",
                    "options": []
                }
                for _ in range(4):
                    random_pokemon = random.choice(pokemon_list)
                    question['options'].append(random_pokemon['name'])
            else:
                medium_question_types = ["type", "ability", "height", "weight"]
                hard_question_types = ["type", "ability", "stat", "weight"]
                
                if difficulty == 'medium':
                    chosen_q_type = random.choice(medium_question_types)
                else:
                    chosen_q_type = random.choice(hard_question_types)

                if chosen_q_type == "type":
                    types = [t['type']['name'] for t in detailed_data['types']]
                    all_known_types = [
                        "normal", "fire", "water", "grass", "electric", "ice",
                        "fighting", "poison", "ground", "flying", "psychic", "bug",
                        "rock", "ghost", "dragon", "dark", "steel", "fairy"
                    ]
                    distractors = list(set(all_known_types) - set(types))
                    options = random.sample(types, k=1) + random.sample(distractors, k=3)
                    random.shuffle(options)
                    question = {
                        "question": f"¿De que tipo (o uno de los tipos) es {selected_pokemon['name']}?",
                        "options": options,
                        "answer": types[0]
                    }

                elif chosen_q_type == "ability":
                    abilities = [ab['ability']['name'] for ab in detailed_data['abilities']]
                    if not abilities:
                        question = {
                            "question": f"Nombra 4 Pokemon de la primera generacion.",
                            "options": [p['name'] for p in random.sample(pokemon_list, 4)]
                        }
                    else:
                        fake_abilities = ["overgrow", "blaze", "torrent", "run-away", "keen-eye",
                                        "rock-head", "intimidate", "levitate", "shed-skin"]
                        distractors = list(set(fake_abilities) - set(abilities))
                        distractors = random.sample(distractors, k=min(3, len(distractors)))
                        options = [abilities[0]] + distractors
                        random.shuffle(options)
                        question = {
                            "question": f"Cual de estas habilidades pertenece a {selected_pokemon['name']}?",
                            "options": options,
                            "answer": abilities[0]
                        }

                elif chosen_q_type == "height":
                    height = detailed_data.get("height", 0)
                    height_m = height * 0.1
                    distractors = []
                    for _ in range(3):
                        distractor = round(height_m + random.uniform(-0.5, 0.5), 1)
                        distractor = max(0.1, distractor)
                        distractors.append(distractor)
                    options = [round(height_m, 1)] + distractors
                    options_str = [f"{opt} m" for opt in options]
                    random.shuffle(options_str)
                    question = {
                        "question": f"Cual es la altura aproximada de {selected_pokemon['name']}?",
                        "options": options_str,
                        "answer": f"{round(height_m, 1)} m"
                    }

                elif chosen_q_type == "weight":
                    weight = detailed_data.get("weight", 0)
                    weight_kg = weight * 0.1
                    distractors = []
                    for _ in range(3):
                        random_offset = weight_kg * random.uniform(-0.3, 0.3)
                        distractor = round(weight_kg + random_offset, 1)
                        distractor = max(0.1, distractor)
                        distractors.append(distractor)
                    options = [round(weight_kg, 1)] + distractors
                    options_str = [f"{opt} kg" for opt in options]
                    random.shuffle(options_str)
                    question = {
                        "question": f"Cual es el peso aproximado de {selected_pokemon['name']}?",
                        "options": options_str,
                        "answer": f"{round(weight_kg, 1)} kg"
                    }

                if chosen_q_type == "stat":
                    stats = detailed_data['stats']
                    stats_dict = {stat['stat']['name']: stat['base_stat'] for stat in stats}
                    highest_stat = max(stats_dict, key=stats_dict.get)
                    question = {
                        "question": f"Cual es la estadística base más alta de {selected_pokemon['name']}?",
                        "options": ["hp", "attack", "defense", "special-attack", "special-defense", "speed"],
                        "answer": highest_stat
                    }

        game_config['questions'].append(question)
        current_app.cache.set('game_config', game_config)

        return jsonify(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
