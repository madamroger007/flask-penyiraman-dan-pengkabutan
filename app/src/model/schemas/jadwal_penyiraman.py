from datetime import datetime, time
from app import db

class JadwalPenyiraman(db.Model):
    __tablename__ = 'jadwal_penyiraman'
    id = db.Column(db.Integer, primary_key=True)
    waktu_1 = db.Column(db.Time, default=time(8, 0))   # ✅ default 08:00 pagi
    waktu_2 = db.Column(db.Time, default=time(16, 0))  # ✅ default 16:00 sore
    jenis_aksi = db.Column(db.Enum('penyiraman', 'pengkabutan', name='jenis_aksi_enum'))
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)
    diubah_sejak = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
