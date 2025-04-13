from mistral_test import findEndangeredSpecies
import json
import sys
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Import after path modification
from image_scraper.image_scraper_headless import get_image_urls
from app import app
from database import db, Animal

def get_endangered_species(species_name):
    response = findEndangeredSpecies(species_name)
    
    # Handle the response that begins with ```json
    if response.startswith("```json"):
        json_start = response.find("[")
        json_end = response.rfind("]") + 1
        json_content = response[json_start:json_end]
        return json.loads(json_content)
    else:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Could not parse response as JSON"}

def save_animals_to_db(animals_data, animal_type):
    with app.app_context():
        for animal in animals_data:
            # Get image URL for the animal
            image_urls = get_image_urls(f"{animal['common_name']} animal", max_images=1)
            image_url = image_urls[0] if image_urls else None

            # Create new Animal instance
            new_animal = Animal(
                animal_type=animal_type,
                animal_name=animal['common_name'],
                biological_name=animal['scientific_name'],
                conservation_status=animal['iucn_status'],
                image_url=image_url
            )
            
            # Add to database
            db.session.add(new_animal)
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"Successfully saved {len(animals_data)} {animal_type} to database")
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to database: {str(e)}")

if __name__ == "__main__":
    # Test with different animal types
    animal_types = ["Birds", "Mammals", "Reptiles", "Amphibians", "Fish"]
    
    for animal_type in animal_types:
        print(f"\nProcessing {animal_type}...")
        endangered_animals = get_endangered_species(animal_type)
        
        if isinstance(endangered_animals, list) and endangered_animals:
            print(f"Found {len(endangered_animals)} endangered {animal_type}")
            save_animals_to_db(endangered_animals, animal_type)
        else:
            print(f"Error getting {animal_type} data")