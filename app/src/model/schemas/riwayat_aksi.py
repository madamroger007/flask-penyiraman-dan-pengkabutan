from app import db
from app.src.utils.get_timezone import get_timezone
class RiwayatAksi(db.Model):
    __tablename__ = 'riwayat_aksi'
    id = db.Column(db.Integer, primary_key=True)
    jenis_aksi = db.Column(db.Enum('penyiraman', 'pengkabutan', name='riwayat_aksi_enum'))
    status = db.Column(db.Enum('aktif', 'nonaktif', name='status_aksi_enum'))
    dibuat_sejak = db.Column(db.DateTime(timezone=True), default=get_timezone)
