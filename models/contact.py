from models.db import db


# Contact model
class ContactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    fax = db.Column(db.String, default="no fax")
    phone = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.id
