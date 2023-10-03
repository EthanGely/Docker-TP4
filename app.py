from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://adm:goToSleep@localhost:5000/COURS_DOCKER'

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


@app.route('/')
def user():
    return render_template('index.html', title="Hello !")

@app.route('/addUser', methods=['POST'])
def addUser():
    email = request.form.get('email')
    psw = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        return render_template('index.html', title=f"User {email} is already created")
    else :
        new_user = User(email=email, password=psw)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return render_template('index.html', title=f"User added : {email}")


@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    username = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=username).first()
    if user:
        if user.password == password :
            db.session.delete(user)
            db.session.commit()
            db.session.close()
            return render_template('index.html', title=f"User {username} has been deleted.")
        else :
            return render_template('index.html', title='Password incorrect.')
    else :
        return render_template('index.html', title=f"User {username} does not exist.")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=username).first()
    if user:
        if user.password == password :
            return render_template('index.html', title=f"User connected")
        else :
            return render_template('index.html', title='Password incorrect.')
    else :
        return render_template('index.html', title=f"User {username} does not exist.")



@app.route('/addBook', methods=['POST'])
def addBook():
    isbn = request.form.get('isbn')
    bookName = request.form.get('title')
    description = request.form.get('description')
    urlImage = request.form.get('urlImage')

    book = Livre.query.filter_by(isbn=isbn).first()
    if book:
        return render_template('index.html', title=f"Book {bookName} with isbn : \"{isbn}\" already exists.")
    else :
        newBook = Livre(isbn=isbn, nom=bookName, description=description, urlImage=urlImage)
        db.session.add(newBook)
        db.session.commit()
        db.session.close()
        return render_template('index.html', title=f"Book added : {bookName}")

@app.route('/deleteBook', methods=['POST'])
def deleteBook():
    isbn = request.form.get('isbn')

    book = Livre.query.filter_by(isbn=isbn).first()
    if book:
        bookName = book.nom
        db.session.delete(book)
        db.session.commit()
        db.session.close()
        return render_template('index.html', title=f"Book \"{bookName}\" deleted.")
    else :
        return render_template('index.html', title=f"Book with isbn : \"{isbn}\" does not exists.")

@app.route('/createTransaction', methods=['POST'])
def createTransaction():
    isbn = request.form.get('isbn')
    userMail = request.form.get('userMail')

    book = Livre.query.filter_by(isbn=isbn).first()
    if not book:
        return render_template('index.html', title=f"Book {isbn} does not exists.")

    user = User.query.filter_by(email=userMail).first()
    if not user:
        return render_template('index.html', title=f"User {userMail} does not exists.")

    bookName = book.nom
    transaction = Achat.query.filter_by(isbn=isbn, id_user=userMail).first()

    if transaction:
        return render_template('index.html', title=f"User {userMail} already has book {bookName}.")
    else :
        newTransaction = Achat(isbn=isbn, id_user=userMail, purchase_date="03/10/2023")
        db.session.add(newTransaction)
        db.session.commit()
        db.session.close()
        return render_template('index.html', title=f"User : {userMail} has book : {bookName}")


@app.route('/deleteTransaction', methods=['POST'])
def deleteTransaction():
    isbn = request.form.get('isbn')
    userMail = request.form.get('userMail')
    password = request.form.get('password')

    book = Livre.query.filter_by(isbn=isbn).first()
    if not book:
        return render_template('index.html', title=f"Book {isbn} does not exists.")

    user = User.query.filter_by(email=userMail).first()
    if not user:
        return render_template('index.html', title=f"User {userMail} does not exists.")
    if user.password != password:
        return render_template('index.html', title=f"Passwords does not match.")

    bookName = book.nom
    transaction = Achat.query.filter_by(isbn=isbn, id_user=userMail).first()

    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        db.session.close()
        return render_template('index.html', title=f"Transaction has been deleted.")
    else :
        return render_template('index.html', title=f"This transaction does not exists.")

if __name__ == '__main__':
    app.run(debug=True)
