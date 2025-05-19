from datetime import datetime
from app import db

class NomorHP(db.Model):
    __tablename__ = 'nomor_hp'
    id = db.Column(db.Integer, primary_key=True)
    nomor_hp = db.Column(db.String(15), unique=True, nullable=False)
    dibuat_sejak = db.Column(db.DateTime, default=datetime.utcnow)