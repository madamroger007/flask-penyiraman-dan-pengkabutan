from app import db
from app.src.utils.get_timezone import get_timezone

from datetime import time

class JadwalPenyiraman(db.Model):
    __tablename__ = 'jadwal_penyiraman'
    id = db.Column(db.Integer, primary_key=True)
    waktu_1 = db.Column(db.Time(timezone=True), default=time(8, 0))
    waktu_2 = db.Column(db.Time(timezone=True), default=time(12, 0))
    jenis_aksi = db.Column(db.Enum('penyiraman', 'pengkabutan', name='jenis_aksi_enum'))
    dibuat_sejak = db.Column(db.DateTime(timezone=True), default=get_timezone)
    diubah_sejak = db.Column(db.DateTime(timezone=True), default=get_timezone, onupdate=get_timezone)
