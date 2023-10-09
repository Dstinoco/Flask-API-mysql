from passlib.hash import pbkdf2_sha256
from db import db

class UsersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        
    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)    

