from models.db import db


class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return self.id
