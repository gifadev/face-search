import os
import json
from IPython.display import display, Image as ShowImage
from util import Util
from person_repository import PersonRepository
from person_service import PersonService

def search_by_image(service, filename):
    """
    Search for a person by image.
    Args:
        service: The person service instance.
        filename: Path to the image to search.
    """
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return None

    # Display the image being searched
    display(ShowImage(filename=filename, width=300, height=300))

    # Perform search
    result = service.find_person_by_image(filename)
    print("ini result embeding", result)
    # Handle search result
    if not result['hits']['hits']:
        print("Person not found!")
        return None

    # Extract person data
    person_data = result['hits']['hits'][0]['_source']

    # Display the matching person's image and details
    # display(ShowImage(filename=person_data['image_path'], width=300, height=300))
    print("Match found:")
    print(f"People ID: {person_data['people_id']}")
    print(f"Full Name: {person_data['full_name']}")
    print(f"Address: {person_data['address']}")
    print(f"Nationality: {person_data['nationality']}")
    print(f"Marital Status: {person_data['marital_status']}")

    return person_data


if __name__ == "__main__":
    # Initialize Elasticsearch connection
    es_db = Util.get_connection()
    person_repo = PersonRepository(es_db, Util.get_index_name())
    person_service = PersonService(person_repo)

    # Hardcoded image path
    image_path = "/home/me/app/image_search/image-search-people/dataset/lost-persons/jay-idzes.jpg"

    # Perform search
    result = search_by_image(person_service, image_path)
    if result:
        print("\nSearch Result:")
        print(json.dumps(result, indent=4))
