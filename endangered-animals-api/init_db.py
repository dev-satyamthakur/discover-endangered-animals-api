from app import app
from database import db, Animal

def init_db():
    with app.app_context():
        db.create_all()
        
        # Sample data
        sample_animal = Animal(
            animal_type='Mammals',
            animal_name='Sumatran Rhinoceros',
            biological_name='Dicerorhinus sumatrensis',
            conservation_status='Critically Endangered',
            image_url='https://example.com/sumatran-rhino.jpg'
        )
        
        db.session.add(sample_animal)
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")