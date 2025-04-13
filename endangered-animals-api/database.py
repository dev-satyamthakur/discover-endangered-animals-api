from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class Animal(db.Model):
    __tablename__ = 'animals'
    
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(50), nullable=False)  # Mammals, Reptiles, etc.
    animal_name = db.Column(db.String(100), nullable=False)
    biological_name = db.Column(db.String(100), nullable=False)
    conservation_status = db.Column(db.String(50), nullable=False)  # IUCN status
    image_url = db.Column(db.String(500))  # URL for animal image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'animal_type': self.animal_type,
            'animal_name': self.animal_name,
            'biological_name': self.biological_name,
            'conservation_status': self.conservation_status,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }