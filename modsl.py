from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50), nullable= False, unique=True)
    lastname = db.Column(db.String(50), nullable= False)
    password = db.Column(db.String(100), nullable= False)
    gmail = db.Column(db.String(28), nullable= False)
    favorite = db.relationship("Favorite",  backref='user')

    

    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
            'lastname': self.lastname,
            'gmail': self.lastname,    
            'favorite': [personal.serialize() for personal in self.favorite]                                     
        }
    
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(28), nullable= False)
    favorite_id = db.Column(db.Integer, db.ForeignKey("favorite.id"))
    planet = db.relationship("Planet", uselist=False, backref="people")

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            "favorite_id": self.favorite_id,
            "planet": self.planet.serialize() if self.planet else None                                      
        }    
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(28), nullable= False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    
    
    

    

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'people_id': self.people_id                                         
        }        
    
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(28), nullable= False)
    people = db.relationship("People",  backref='favorite')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            "user_id": self.user_id,      
            'people': [person.serialize() for person in self.people]                                    
        }            