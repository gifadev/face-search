import os
from sentence_transformers import SentenceTransformer
from PIL import Image
import uuid 

class Person:
    model = SentenceTransformer('clip-ViT-B-32')

    def __init__(self, people_id=None, image_path=None, full_name=None, birth_place=None, birth_date=None, address=None, nationality=None, passport_number=None, gender=None, national_id_number=None, marital_status=None):
        self.people_id = people_id if people_id else str(uuid.uuid4())
        self.image_path = image_path
        self.full_name = full_name
        self.birth_place = birth_place
        self.birth_date = birth_date
        self.address = address
        self.nationality = nationality
        self.passport_number = passport_number
        self.gender = gender
        self.national_id_number = national_id_number
        self.marital_status = marital_status


    @staticmethod
    def get_embedding(image_path: str):
        temp_image = Image.open(image_path)
        return Person.model.encode(temp_image)

    def generate_embedding(self):
        self.image_embedding = Person.get_embedding(self.image_path)

    def __repr__(self):
        return (f"Person(people_id={self.people_id}, image_path={self.image_path}, "
                f"full_name={self.full_name}, image_embedding={self.image_embedding})")

    def to_dict(self):
        return {
            "people_id": self.people_id,
            "image_path": self.image_path,
            "full_name": self.full_name,
            "birth_place": self.birth_place,
            "birth_date": self.birth_date,
            "address": self.address,
            "nationality": self.nationality,
            "passport_number": self.passport_number,
            "gender": self.gender,
            "national_id_number": self.national_id_number,
            "marital_status": self.marital_status,
            "image_embedding": self.image_embedding
        }
