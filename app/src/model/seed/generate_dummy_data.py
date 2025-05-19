import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))


from faker import Faker
import random
import argparse
from datetime import datetime
from app import create_app, db
from app.src.model.schemas import NomorHP, JadwalPenyiraman, RiwayatAksi, DataSensor

# Initialize Flask app
app = create_app()
fake = Faker()

# Function to generate dummy data for DataSensor
# def generate_sensor_data():
#     sensor_data = []
#     for _ in range(10):
#         sensor = DataSensor(
#             suhu=round(random.uniform(20, 35), 2),
#             kelembapan_udara=round(random.uniform(40, 80), 2),
#             kelembapan_tanah=round(random.uniform(20, 60), 2),
#             dibuat_sejak=fake.date_time_this_year()
#         )
#         sensor_data.append(sensor)
#     db.session.add_all(sensor_data)
#     db.session.commit()


# Function to generate dummy data for JadwalPenyiraman
def generate_watering_schedules():
    watering_schedules = []

    # Data pertama: penyiraman
    schedule_1 = JadwalPenyiraman(
        waktu_1=fake.time(),
        waktu_2=fake.time(),
        jenis_aksi='penyiraman',

        dibuat_sejak=fake.date_time_this_year(),
        diubah_sejak=fake.date_time_this_year()
    )
    watering_schedules.append(schedule_1)

    # Data kedua: pengkabutan
    schedule_2 = JadwalPenyiraman(
        waktu_1=fake.time(),
        waktu_2=fake.time(),
        jenis_aksi='pengkabutan',

        dibuat_sejak=fake.date_time_this_year(),
        diubah_sejak=fake.date_time_this_year()
    )
    watering_schedules.append(schedule_2)

    db.session.add_all(watering_schedules)
    db.session.commit()


# Function to generate dummy data for RiwayatAksi
# def generate_action_history():
#     action_history = []
#     for _ in range(10):
#         action = RiwayatAksi(
#             jenis_aksi=random.choice(['penyiraman', 'pengkabutan']),
#             status=random.choice(['aktif', 'nonaktif']),
#             dibuat_sejak=fake.date_time_this_year()
#         )
#         action_history.append(action)
#     db.session.add_all(action_history)
#     db.session.commit()

# Function to generate dummy data for nomor_hp
def generate_nomor_hp():
    nomor_hp_data = []
    for _ in range(10):
        nomor = NomorHP(
            nomor_hp=fake.phone_number(),
            dibuat_sejak=fake.date_time_this_year()
        )
        nomor_hp_data.append(nomor)
    db.session.add_all(nomor_hp_data)
    db.session.commit()
    
# Function to generate all data
def generate_data():
    with app.app_context():
        print("Generating dummy data...")
        # generate_sensor_data()
        generate_watering_schedules()
        # generate_action_history()
        print("Dummy data generated successfully!")

# Function to remove all data
def remove_all_data():
    with app.app_context():
        print("Removing all data...")
        db.session.query(DataSensor).delete()
        db.session.query(JadwalPenyiraman).delete()
        db.session.query(RiwayatAksi).delete()
        db.session.commit()
        print("All dummy data has been successfully removed!")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Manage dummy data in the database.")
    parser.add_argument(
        '--action',
        choices=['generate', 'remove'],
        required=True,
        help="Choose an action: 'generate' to generate data or 'remove' to delete data."
    )

    args = parser.parse_args()

    if args.action == 'generate':
        generate_data()
    elif args.action == 'remove':
        remove_all_data()

if __name__ == '__main__':
    main()
