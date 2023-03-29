from flask import Flask, request,jsonify
from modsl import db, User, People, Planet, Favorite
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)



@app.route('/')
def home():
    return 'Hello SQLAlchemy y flask'



@app.route('/users', methods=['POST'])
def create_user():
    user = User()
    user.username = request.json.get('username')
    user.lastname = request.json.get('lastname')
    user.gmail = request.json.get('gmail')

    password = request.json.get('password')
    password_hash = generate_password_hash(password)
    user.password = password_hash

    db.session.add(user)
    db.session.commit()

    return 'Usuario Guardado'



@app.route('/users/list', methods=['GET'])
def get_user():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result)    


@app.route('/users/<int:id>', methods=['PUT', 'DELETE'])
def update_user(id):
    user = User.query.get(id)
    if user is not None:
        if request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()

            return jsonify('Eliminar'), 204
        else:    
            user.age = request.json.get('age')


            db.session.commit()
            return jsonify('Usuario actualizado')

    return jsonify('usuario no encontrado')

#people

#POST
@app.route('/people', methods=['POST'])
def create_people():
    people = People()
    
    people.name = request.json.get('name')
    people.favorite_id = request.json.get('favorite_id')
    

    db.session.add(people)
    db.session.commit()

    return 'Usuario Guardado'


#GET
@app.route('/people/list', methods=['GET'])
def get_people():
    peoples = People.query.all()
    result = []
    for people in peoples:
        result.append(people.serialize())
    return jsonify(result)    

#GET UNICO
@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    people = People.query.get(id)
    if people is not None:
        return jsonify(people.serialize())
    else:
        return jsonify('No se encontró el objeto People con el ID especificado')
    





#PUT DELETE
@app.route('/people/<int:id>', methods=['PUT', 'DELETE'])
def update_People(id):
    people = People.query.get(id)
    if people is not None:
        if request.method == 'DELETE':
            db.session.delete(people)
            db.session.commit()

            return jsonify('Eliminar'), 204
        else:
                
             people.name = request.json.get('name')
             

             db.session.commit()
             return jsonify('Usuario actualizado'), 200

    return jsonify('usuario no encontrado'), 404



#PLANETS

#POST
@app.route('/planet', methods=['POST'])
def create_planet():
    planet = Planet()
    
    planet.name = request.json.get('name')
    planet.people_id = request.json.get('people_id')
    
    
    

    db.session.add(planet)
    db.session.commit()

    return 'Usuario Guardado'


#GET
@app.route('/planets/list', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    result = []
    for planet in planets:
        result.append(planet.serialize())
    return jsonify(result)    

#GET UNICO
@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_id(id):
    planet = Planet.query.get(id)
    if planet is not None:
        return jsonify(planet.serialize())
    else:
        return jsonify('No se encontró el objeto People con el ID especificado')


#PUT DELETE
@app.route('/planet/<int:id>', methods=['PUT', 'DELETE'])
def update_planet(id):
    planet = Planet.query.get(id)
    if planet is not None:
        if request.method == 'DELETE':
            db.session.delete(planet)
            db.session.commit()

            return jsonify('Eliminar'), 204
        else:    
            
             planet.name = request.json.get('name')
             

             db.session.commit()
             return jsonify('Usuario actualizado'), 200

    return jsonify('usuario no encontrado'), 404














##POST
@app.route('/favorite', methods=['POST'])
def create_favorite():
    favorite = Favorite()
    favorite.name = request.json.get('name')
    favorite.user_id = request.json.get('user_id')
    
    

    db.session.add(favorite)
    db.session.commit()

    return 'Usuario Guardado'



#GET
@app.route('/favorites/list', methods=['GET'])
def get_favorite():
    favorites = Favorite.query.all()
    result = []
    for favorite in favorites:
        result.append(favorite.serialize())
    return jsonify(result)   






#PUT DELETE
@app.route('/favorite/<int:id>', methods=['PUT', 'DELETE'])
def update_favorite(id):
    favorite = Favorite.query.get(id)
    if favorite is not None:
        if request.method == 'DELETE':
            db.session.delete(favorite)
            db.session.commit()

            return jsonify('Eliminar'), 204
        else:    
             
             favorite.name = request.json.get('name')
             

             db.session.commit()
             return jsonify('Usuario actualizado'), 200

    return jsonify('usuario no encontrado'), 404


#listar todos los people que pertenecen a favorite
@app.route('/people/favorite/<int:favorite_id>', methods=['GET'])
def get_people_by_favorite(favorite_id):
    peoples = db.session.query(People).join(Favorite).filter(Favorite.id == favorite_id).all()
    result = []
    for people in peoples:
        result.append(people.serialize())
    return jsonify(result)

#acceder a favorite desde people
@app.route('/people/<int:people_id>/favorite', methods=['GET'])
def get_favorite_by_people(people_id):
    people = People.query.get(people_id)
    favorite = people.favorite
    result = favorite.serialize()
    return jsonify(result)


#Listar todos los favoritos que pertenecen al usuario actual.
@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def get_favorite_user(user_id):
    favorites = db.session.query(Favorite).join(User).filter(User.id==user_id).all()
    result = []
    for favorite in favorites:
        result.append(favorite.serialize())
    return jsonify(result)


if __name__ == "__main__":
 app.run(host='localhost', port='8080')