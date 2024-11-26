from fastapi import FastAPI, UploadFile, File, Form
from app.search import search_by_image
from app.register import register_person
from app.util import Util
from app.person_service import PersonService
from app.person_repository import PersonRepository
import os
from pydantic import BaseModel

# Inisialisasi FastAPI
app = FastAPI()

# Setup koneksi Elasticsearch dan service
es_db = Util.get_connection()
person_repo = PersonRepository(es_db, Util.get_index_name())
person_service = PersonService(person_repo)

# Folder untuk menyimpan file gambar
DATASET_FOLDER = "dataset/persons"
os.makedirs(DATASET_FOLDER, exist_ok=True)


@app.post("/register/")
async def register_person_api(
    full_name: str = Form(...),
    birth_place: str = Form(...),
    birth_date: str = Form(...),
    address: str = Form(...),
    nationality: str = Form(...),
    passport_number: str = Form(...),
    gender: str = Form(...),
    national_id_number: str = Form(...),
    marital_status: str = Form(...),
    image: UploadFile = Form(...)
):
    """
    Endpoint untuk mendaftarkan satu orang berdasarkan input pengguna.
    Args:
        full_name: Nama lengkap orang.
        birth_place: Tempat lahir.
        birth_date: Tanggal lahir.
        address: Alamat.
        nationality: Kewarganegaraan.
        passport_number: Nomor paspor.
        gender: Jenis kelamin.
        national_id_number: Nomor identitas nasional.
        marital_status: Status pernikahan.
        image: File gambar yang diunggah.
    """
    # Simpan file gambar ke folder dataset/persons
    image_filename = os.path.join(DATASET_FOLDER, image.filename)
    with open(image_filename, "wb") as f:
        f.write(await image.read())

    # Siapkan data untuk disimpan
    person_data = {
        "image_path": image_filename,
        "full_name": full_name,
        "birth_place": birth_place,
        "birth_date": birth_date,
        "address": address,
        "nationality": nationality,
        "passport_number": passport_number,
        "gender": gender,
        "national_id_number": national_id_number,
        "marital_status": marital_status,
    }

    # Registrasi ke Elasticsearch
    response = register_person(person_service, person_data)

    return response

@app.post("/search/")
async def search_person(image: UploadFile = File(...)):
    """
    Endpoint untuk mencari orang berdasarkan gambar.
    Args:
        file: Gambar yang diunggah.
    """
    temp_filename = f"temp_{image.filename}"
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(await image.read())
    
    # Gunakan search_by_image
    result = search_by_image(person_service, temp_filename)
    
    # Hapus file sementara
    os.remove(temp_filename)
    
    if result:
        return result
    return {"message": "Person not found"}
