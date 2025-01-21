from flask import Flask
from flask_caching import Cache

cache = Cache()

def create_app():
    app = Flask(__name__)

    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    cache.init_app(app)

    from app.routes import pokemon
    app.register_blueprint(pokemon.api, url_prefix='/api')

    app.cache = cache
    return app
