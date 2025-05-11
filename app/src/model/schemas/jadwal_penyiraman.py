from datetime import datetime
from app import db
class JadwalPenyiraman(db.Model):
    __tablename__ = 'jadwal_penyiraman'
    id = db.Column(db.Integer, primary_key=True)
    waktu_1 = db.Column(db.Time)
    waktu_2 = db.Column(db.Time)
    jenis_aksi = db.Column(db.Enum('penyiraman', 'pengkabutan', name='jenis_aksi_enum'))
    status = db.Column(db.Enum('aktif', 'nonaktif', name='status_enum'))
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)
    diubah_sejak = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)