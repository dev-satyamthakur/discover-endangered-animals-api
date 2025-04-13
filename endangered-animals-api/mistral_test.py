import os
from mistralai import Mistral

api_key = "kKoIGSS7dfDQxTAjknlSbH8MZyPK5fVB"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def findEndangeredSpecies(species_name): 
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"""Return a JSON array of 10 endangered {species_name} from the IUCN red list. 
                Each object should have exactly these fields:
                - common_name: the common name of the species
                - scientific_name: the scientific/biological name
                - iucn_status: the IUCN Red List status
                
                Format the response as a valid JSON array only, with no additional text."""
            },
        ]
    )
    return chat_response.choices[0].message.content