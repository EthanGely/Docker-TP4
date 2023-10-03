class Achat(db.Model):
    isbn = db.Column(db.ForeignKey('livre.isbn'), primary_key=True)
    id_user = db.Column(db.ForeignKey('user.email'), primary_key=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)

    livre = db.relationship('Livre', backref='achats')
    user = db.relationship('User', backref='achats')

    def __init__(self, isbn, id_user, date):
        self.livre_isbn = livre_isbn
        self.user_email = user_email
        self.purchase_date = purchase_date
