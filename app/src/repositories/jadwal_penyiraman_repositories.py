from app import db
from app.src.model.schemas.jadwal_penyiraman import JadwalPenyiraman
from datetime import datetime

def update_jadwal_by_id_repository(jadwal_id, waktu_1, waktu_2, jenis):
    jadwal = JadwalPenyiraman.query.filter_by(id=jadwal_id, jenis_aksi=jenis).first()
    if not jadwal:
        raise Exception("Jadwal tidak ditemukan.")

    jadwal.waktu_1 = datetime.strptime(waktu_1, "%H:%M").time()
    jadwal.waktu_2 = datetime.strptime(waktu_2, "%H:%M").time()
    db.session.commit()
    return jadwal

def create_jadwal_penyiraman_repository(jadwal):
    try:
        new_jadwal = JadwalPenyiraman(
            waktu_1=jadwal['waktu_1'],
            waktu_2=jadwal['waktu_2'],
            jenis_aksi=jadwal['jenis_aksi']
        )
        db.session.add(new_jadwal)
        db.session.commit()
        return new_jadwal
    except Exception as e:
        print("Error creating jadwal:", e)
        return None
    
def get_jadwal_penyiraman_by_jenis_repository(jenis_aksi):
    jadwal = JadwalPenyiraman.query.filter_by(jenis_aksi=jenis_aksi).first()
    if not jadwal:
        raise Exception("Jadwal tidak ditemukan.")
    return jadwal