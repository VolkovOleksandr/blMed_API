from models.db import db


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, unique=True, nullable=False)
    product = db.relationship('Products')

    def __repr__(self):
        return self.id
