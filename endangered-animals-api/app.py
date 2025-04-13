from flask import Flask, jsonify
from database import db, Animal
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'animals.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/')
def home():
    return {"message": "Welcome to the Endangered Animals API"}

@app.route('/animals/<string:animal_type>', methods=['GET'])
def get_animals_by_type(animal_type):
    animals = Animal.query.filter_by(animal_type=animal_type.capitalize()).all()
    if not animals:
        return jsonify({"error": f"No {animal_type} found"}), 404
    return jsonify([animal.to_dict() for animal in animals])

# Specific routes for each animal type
@app.route('/mammals', methods=['GET'])
def get_mammals():
    mammals = Animal.query.filter_by(animal_type='Mammals').all()
    return jsonify([mammal.to_dict() for mammal in mammals])

@app.route('/birds', methods=['GET'])
def get_birds():
    birds = Animal.query.filter_by(animal_type='Birds').all()
    return jsonify([bird.to_dict() for bird in birds])

@app.route('/reptiles', methods=['GET'])
def get_reptiles():
    reptiles = Animal.query.filter_by(animal_type='Reptiles').all()
    return jsonify([reptile.to_dict() for reptile in reptiles])

@app.route('/amphibians', methods=['GET'])
def get_amphibians():
    amphibians = Animal.query.filter_by(animal_type='Amphibians').all()
    return jsonify([amphibian.to_dict() for amphibian in amphibians])

@app.route('/fish', methods=['GET'])
def get_fish():
    fish = Animal.query.filter_by(animal_type='Fish').all()
    return jsonify([fish.to_dict() for fish in fish])

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)