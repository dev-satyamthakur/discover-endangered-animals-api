from mistral_test import findEndangeredSpecies
import json

def get_endangered_species(species_name):
    response = findEndangeredSpecies(species_name)
    
    # Handle the response that begins with ```json
    if response.startswith("```json"):
        # Find where the JSON content actually begins
        json_start = response.find("[")
        # Find where the JSON content ends
        json_end = response.rfind("]") + 1
        # Extract just the JSON part
        json_content = response[json_start:json_end]
        # Parse the JSON string into a Python object
        return json.loads(json_content)
    else:
        # If it's already a proper JSON string
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Could not parse response as JSON"}

if __name__ == "__main__":
    endangered_birds = get_endangered_species("birds")
    print(endangered_birds)
    
    # Example of accessing the parsed data
    if isinstance(endangered_birds, list) and endangered_birds:
        print(f"\nFound {len(endangered_birds)} endangered bird species")
        for bird in endangered_birds:
            print(f"- {bird['common_name']} ({bird['scientific_name']}): {bird['iucn_status']}")