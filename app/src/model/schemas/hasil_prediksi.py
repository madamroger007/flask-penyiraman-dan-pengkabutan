from datetime import datetime
from app import db

class HasilPrediksi(db.Model):
    __tablename__ = 'hasil_prediksi'
    id = db.Column(db.Integer, primary_key=True)
    prediksi_siram = db.Column(db.Boolean)
    prediksi_kabut = db.Column(db.Boolean)
    probabilitas_siram = db.Column(db.Float)
    probabilitas_kabut = db.Column(db.Float)
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)
