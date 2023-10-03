from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://adm:goToSleep@localhost/COURS_DOCKER'

db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Livre(db.Model):
    isbn = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)
    urlImage = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, isbn, nom, description, urlImage):
        self.isbn = isbn
        self.nom = nom
        self.description = description
        self.urlImage = urlImage

class Achat(db.Model):
    isbn = db.Column(db.ForeignKey('livre.isbn'), primary_key=True)
    id_user = db.Column(db.ForeignKey('user.email'), primary_key=True)
    purchase_date = db.Column(db.String(10), unique=False, nullable=False)

    livre = db.relationship('Livre', backref='achats')
    user = db.relationship('User', backref='achats')

    def __init__(self, isbn, id_user, purchase_date):
        self.isbn = isbn
        self.id_user = id_user
        self.purchase_date = purchase_date


#Create database
with app.app_context():
    db.create_all()