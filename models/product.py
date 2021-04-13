from models.db import db
import datetime


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    image_url = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, default='No information')
    featured = db.Column(db.Boolean, default=False,  nullable=False)
    date_time = db.Column(
        db.DateTime, default=datetime.datetime.utcnow,  nullable=False)

    def __repr__(self):
        return self.id
