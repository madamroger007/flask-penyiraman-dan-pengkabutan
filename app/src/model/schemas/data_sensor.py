from app import db
from app.src.utils.get_timezone import get_timezone

class DataSensor(db.Model):
    __tablename__ = 'data_sensor'
    id = db.Column(db.Integer, primary_key=True)
    suhu = db.Column(db.Float)
    kelembapan_udara = db.Column(db.Float)
    kelembapan_tanah = db.Column(db.Float)
    penyiraman = db.Column(db.Boolean, default=False)
    pengkabutan = db.Column(db.Boolean, default=False)
    dibuat_sejak = db.Column(db.DateTime(timezone=True), default=get_timezone)
