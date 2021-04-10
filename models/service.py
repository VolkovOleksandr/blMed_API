from models.db import db


class ServiceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    position = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"DB SERVICE: id={self.id}, title={self.title}, desc={self.description}, position={self.position}"
