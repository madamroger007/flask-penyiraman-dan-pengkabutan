from app.src.model.schemas.riwayat_aksi import RiwayatAksi
from app import db
 
def create_riwayat_aksi_repository(data):
    riwayat_aksi = RiwayatAksi(**data)
    db.session.add(riwayat_aksi)
    db.session.commit()
    return riwayat_aksi

def get_all_riwayat_aksi_repository():
    return RiwayatAksi.query.all()

def get_riwayat_aksi_by_id_repository(riwayat_aksi_id):
    return RiwayatAksi.query.get(riwayat_aksi_id)

def update_riwayat_aksi_repository(riwayat_aksi_id, data):
    riwayat_aksi = RiwayatAksi.query.get(riwayat_aksi_id)
    if riwayat_aksi:
        for key, value in data.items():
            setattr(riwayat_aksi, key, value)
        db.session.commit()
        return riwayat_aksi
    return None