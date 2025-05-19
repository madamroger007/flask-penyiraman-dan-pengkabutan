from datetime import datetime
from app import db

class RiwayatAksi(db.Model):
    __tablename__ = 'riwayat_aksi'
    id = db.Column(db.Integer, primary_key=True)
    jenis_aksi = db.Column(db.Enum('penyiraman', 'pengkabutan', name='riwayat_aksi_enum'))
    status = db.Column(db.Enum('aktif', 'nonaktif', name='status_aksi_enum'))
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)
