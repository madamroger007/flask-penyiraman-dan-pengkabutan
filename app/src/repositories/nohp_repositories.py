from app import db
from app.src.model.schemas.nomor_hp import NomorHp

def get_all_nomor_hp():
    return NomorHp.query.all()

def get_nomor_hp_by_id(nomor_hp_id):
    return NomorHp.query.get(nomor_hp_id)

def create_nomor_hp(nomor_hp):
    new_nomor_hp = NomorHp(**nomor_hp)
    db.session.add(new_nomor_hp)
    db.session.commit()
    return new_nomor_hp

def update_nomor_hp(nomor_hp_id, nomor_hp):
    existing_nomor_hp = get_nomor_hp_by_id(nomor_hp_id)
    if existing_nomor_hp:
        for key, value in nomor_hp.items():
            setattr(existing_nomor_hp, key, value)
        db.session.commit()
    return existing_nomor_hp

def delete_nomor_hp(nomor_hp_id):
    existing_nomor_hp = get_nomor_hp_by_id(nomor_hp_id)
    if existing_nomor_hp:
        db.session.delete(existing_nomor_hp)
        db.session.commit()
    return existing_nomor_hp