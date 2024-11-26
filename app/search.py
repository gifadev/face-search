import os
from app.util import Util

def search_by_image(service, filename):
    """
    Cari orang berdasarkan gambar.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    # Cari orang
    result = service.find_person_by_image(filename)

    if not result['hits']['hits']:
        return None

    person_data = result['hits']['hits'][0]['_source']
    return person_data
