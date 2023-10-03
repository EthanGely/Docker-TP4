class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
