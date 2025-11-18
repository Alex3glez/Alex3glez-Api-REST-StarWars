"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.session.execute(db.select(User)).scalars())
    result = [user.to_dict() for user in users]
    return jsonify(result), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)

    return jsonify(user.to_dict()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = list(db.session.execute(db.select(Planet)).scalars())
    result = [planet.to_dict() for planet in planets]
    return jsonify(result), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = db.session.get(Planet, id)

    return jsonify(planet.to_dict()), 200


@app.route('/peoples', methods=['GET'])
def get_peoples():
    peoples = list(db.session.execute(db.select(People)).scalars())
    result = [people.to_dict() for people in peoples]
    return jsonify(result), 200


@app.route('/peoples/<int:id>', methods=['GET'])
def get_people(id):
    people = db.session.get(People, id)

    return jsonify(people.to_dict()), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.create_user(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
        name=data.get("name"),
        last_name=data.get("last_name")
    )

    return jsonify(user.to_dict())


@app.route('/peoples', methods=['POST'])
def create_people():
    data = request.get_json()
    people = People.create_people(
        gender=data.get("gender"),
        url=data.get("url"),
        mass=data.get("mass"),
        name=data.get("name"),
        height=data.get("height")
    )

    return jsonify(people.to_dict())


@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.get_json()
    planet = Planet.create_planet(
        population=data.get("population"),
        url=data.get("url"),
        diameter=data.get("diameter"),
        name=data.get("name"),
        climate=data.get("climate")
    )

    return jsonify(planet.to_dict())


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = db.session.get(User, id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"mensaje": f"usuario '{user.username}' eliminado"}), 200


@app.route('/peoples/<int:id>', methods=['DELETE'])
def delete_people(id):

    people = db.session.get(People, id)

    db.session.delete(people)
    db.session.commit()

    return jsonify({"mensaje": f"people '{people.name}' eliminado"}), 200


@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):

    planet = db.session.get(Planet, id)

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"mensaje": f"planeta '{planet.name}' eliminado"}), 200


@app.route('/users/<int:id>', methods=['PUT'])
def modify_user(id):

    data = request.get_json()
    user = db.session.get(User, id)

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'name' in data:
        user.name = data['name']
    if 'last_name' in data:
        user.last_name = data['last_name']

    db.session.commit()

    return jsonify(user.to_dict()), 200


@app.route('/peoples/<int:id>', methods=['PUT'])
def modify_people(id):

    data = request.get_json()
    people = db.session.get(People, id)

    if 'gender' in data:
        people.gender = data['gender']
    if 'url' in data:
        people.url = data['url']
    if 'mass' in data:
        people.mass = data['mass']
    if 'name' in data:
        people.name = data['name']
    if 'height' in data:
        people.height = data['height']

    db.session.commit()

    return jsonify(people.to_dict()), 200


@app.route('/planets/<int:id>', methods=['PUT'])
def modify_planet(id):

    data = request.get_json()
    planet = db.session.get(Planet, id)

    if 'population' in data:
        planet.population = data['population']
    if 'url' in data:
        planet.url = data['url']
    if 'diameter' in data:
        planet.diameter = data['diameter']
    if 'name' in data:
        planet.name = data['name']
    if 'climate' in data:
        planet.climate = data['climate']

    db.session.commit()

    return jsonify(planet.to_dict()), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):

    user = db.session.get(User, user_id)

    fav_planets = [planet.to_dict() for planet in user.favorite_planets]
    fav_people = [person.to_dict() for person in user.favorite_peoples]
    # podría añadir tambien vehicles y films

    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "favorites": {
            "planets": fav_planets,
            "people": fav_people
        }
    }), 200


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_fav_planet(user_id, planet_id):

    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    user.favorite_planets.append(planet)
    db.session.commit()

    return jsonify({"mensaje": f"Planeta '{planet.name}' añadido a favoritos"}), 200


@app.route('/users/<int:user_id>/favorites/peoples/<int:people_id>', methods=['POST'])
def add_fav_person(user_id, people_id):

    user = db.session.get(User, user_id)
    person = db.session.get(People, people_id)

    user.favorite_peoples.append(person)
    db.session.commit()

    return jsonify({"mensaje": f"Personaje '{person.name}' añadido a favoritos"}), 200


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(user_id, planet_id):

    user = db.session.get(User, user_id)
    planet = db.session.get(Planet, planet_id)

    user.favorite_planets.remove(planet)
    db.session.commit()

    return jsonify({"mensaje": f"Planeta '{planet.name}' eliminado de favoritos"}), 200


@app.route('/users/<int:user_id>/favorites/peoples/<int:people_id>', methods=['DELETE'])
def delete_fav_person(user_id, people_id):

    user = db.session.get(User, user_id)
    person = db.session.get(People, people_id)

    user.favorite_peoples.remove(person)
    db.session.commit()

    return jsonify({"mensaje": f"Personaje '{person.name}' eliminado de favoritos"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
