from datetime import datetime
from app import db
class DataSensor(db.Model):
    __tablename__ = 'data_sensor'
    id = db.Column(db.Integer, primary_key=True)
    suhu = db.Column(db.Float)
    kelembapan_udara = db.Column(db.Float)
    kelembapan_tanah = db.Column(db.Float)
    penyiraman = db.Column(db.Boolean, default=False)
    pengkabutan = db.Column(db.Boolean, default=False)
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)

