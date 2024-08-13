from db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    matric = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    fullname = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now)

    def __init__(self, matric, email, password, fullname):
        self.matric = matric
        self.email = email
        self.password = password
        self.fullname = fullname

    def to_json(self):
        return {
            'id': self.id,
            'matric': self.matric,
            'email': self.email,
            'fullname': self.fullname,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __repr__(self):
        return f'<id={self.id}, matric={self.matric}, fullname={self.fullname}, email={self.email}>'

def create_db_tables(app):
    with app.app_context():
        db.drop_all()
        db.create_all()