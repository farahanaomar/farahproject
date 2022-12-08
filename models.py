from hello import db
from datetime import datetime

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), unique=True, nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    image_file= db.Column(db.String(20), nullable=False, default='default.jpg')
    # Password in String for now not integer
    password= db.Column(db.String(15), nullable=False)  
    date_created= db.Column(db.DateTime, default= datetime.utnow)

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.date_created}'