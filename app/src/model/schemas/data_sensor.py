from datetime import datetime
from app import db
class DataSensor(db.Model):
    __tablename__ = 'data_sensor'
    id = db.Column(db.Integer, primary_key=True)
    suhu = db.Column(db.Float)
    kelembapan_udara = db.Column(db.Float)
    kelembapan_tanah = db.Column(db.Float)
    ketinggian_air = db.Column(db.Float)
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)

