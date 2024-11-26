import os
import json
import math
from util import Util
from person import Person
from person_repository import PersonRepository
from person_service import PersonService
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Image as ShowImage

# Start a connection
es_db = Util.get_connection()
Util.delete_index(es_db, Util.get_index_name())

# Register one person
person_repo = PersonRepository(es_db, Util.get_index_name())
person_service = PersonService(person_repo)

# Register a sample person
filename = "/home/me/app/image_search/image-search-people/dataset/persons/arif.jpg"

if os.path.exists(filename):
    display(ShowImage(filename=filename, width=300, height=300))
    person = Person(None, filename, "Arif Munawar", "Semarang", "2001-01-01", "Semarang", 
                    "Indonesia", "A12345678", "Male", "987654321", "Single")
    person_service.register_person(person)
    print("register arif success")
else:
    print(f"File not found: {filename}")

# JSON data for bulk insert
data = '''
{
  "persons": [
    {
      "people_id":"None",
      "image_path": "/home/me/app/image_search/image-search-people/dataset/persons/gisna.png",
      "full_name": "Gisna Fauzian Dermawan",
      "birth_place": "Tasikmalaya",
      "birth_date": "2003-01-01",
      "address": "Sariwangi-Tasikmalaya",
      "nationality": "Indonesia",
      "passport_number": "B12345678",
      "gender": "Male",
      "national_id_number": "123456789",
      "marital_status": "Single"
    },
    {
      "people_id":"None",
      "image_path": "/home/me/app/image_search/image-search-people/dataset/persons/parlin.jpg",
      "full_name": "Parlindungan Duha",
      "birth_place": "Nias",
      "birth_date": "2000-01-01",
      "address": "Nias",
      "nationality": "Indonesia",
      "passport_number": "C98765432",
      "gender": "Male",
      "national_id_number": "987654321",
      "marital_status": "Married"
    }
  ]
}
'''

persons_data = json.loads(data)

# Register bulk persons
for person_info in persons_data["persons"]:
    image_path = person_info["image_path"]
    if os.path.exists(image_path):
        person = Person(
            None,
            person_info["image_path"],
            person_info["full_name"],
            person_info["birth_place"],
            person_info["birth_date"],
            person_info["address"],
            person_info["nationality"],
            person_info["passport_number"],
            person_info["gender"],
            person_info["national_id_number"],
            person_info["marital_status"]
        )
        person_service.register_person(person)
    else:
        print(f"File not found: {image_path}")

# Visualizing the new persons
num_persons = len(persons_data["persons"])
cols = int(math.sqrt(num_persons))
rows = math.ceil(num_persons / cols)

plt.figure(figsize=(5, 5))
for i, person_info in enumerate(persons_data["persons"]):
    filename = person_info["image_path"]
    if os.path.exists(filename):
        img = mpimg.imread(filename)
        plt.subplot(rows, cols, i+1)
        plt.imshow(img)
        plt.axis('off')
    else:
        print(f"Image not found for {person_info['full_name']}")

plt.show()

# Search for a lost person
filename = "/home/me/app/image_search/image-search-people/dataset/lost-persons/lost_arif.jpg"
if os.path.exists(filename):
    display(ShowImage(filename=filename, width=300, height=300))
    result = person_service.find_person_by_image(filename)
    if result['hits']['hits']:
        person_data = result['hits']['hits'][0]['_source']
        print(person_data)
    else:
        print("Person not found!")
else:
    print(f"Lost person image not found: {filename}")
