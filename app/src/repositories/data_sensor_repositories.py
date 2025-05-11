from typing import List, Dict, Any
from sqlalchemy.orm import Session
from model.schemas.data_sensor import DataSensor  # Pastikan Anda memiliki model DataSensor yang sudah didefinisikan

def create_sensor_data(db_session: Session, data: Dict[str, Any]) -> DataSensor:
    new_data = DataSensor(**data)
    db_session.add(new_data)
    db_session.commit()
    db_session.refresh(new_data)
    return new_data

def read_sensor_data(db_session: Session, sensor_id: int) -> DataSensor:
    return db_session.query(DataSensor).filter(DataSensor.id == sensor_id).first()

def read_all_sensor_data(db_session: Session) -> List[DataSensor]:
    return db_session.query(DataSensor).all()

def update_sensor_data(db_session: Session, sensor_id: int, updated_data: Dict[str, Any]) -> DataSensor:
    sensor_data = db_session.query(DataSensor).filter(DataSensor.id == sensor_id).first()
    if not sensor_data:
        return None
    for key, value in updated_data.items():
        setattr(sensor_data, key, value)
    db_session.commit()
    db_session.refresh(sensor_data)
    return sensor_data

def delete_sensor_data(db_session: Session, sensor_id: int) -> bool:
    sensor_data = db_session.query(DataSensor).filter(DataSensor.id == sensor_id).first()
    if not sensor_data:
        return False
    db_session.delete(sensor_data)
    db_session.commit()
    return True
