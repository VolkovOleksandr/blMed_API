from models.db import db


# Showroom model
class ShowroomModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.id
