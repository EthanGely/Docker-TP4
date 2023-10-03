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
