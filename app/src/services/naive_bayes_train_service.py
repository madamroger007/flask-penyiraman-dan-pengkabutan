import os
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Inisialisasi model global
model = None
required_features = ['Suhu Udara', 'Kelembapan Udara', 'Kelembapan Tanah']
target_columns = ['Penyiraman', 'Pengkabutan']

def load_data_from_csv(filename='sensor_data.csv'):
    """
    Memuat dan memvalidasi data dari file CSV yang berada di direktori yang sama dengan skrip ini.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    if not os.path.isfile(file_path):
        print(f"❌ File tidak ditemukan: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
        required_columns = set(required_features + target_columns)
        if not required_columns.issubset(df.columns):
            print(f"❌ Kolom yang dibutuhkan tidak ditemukan dalam file CSV: {required_columns}")
            return None
        return df
    except Exception as e:
        print(f"❌ Gagal membaca file CSV: {e}")
        return None

def train_naive_bayes(csv_path='sensor_data.csv'):
    global model

    df = load_data_from_csv(csv_path)
    if df is None or len(df) < 5:
        print("📉 Data terlalu sedikit atau tidak valid.")
        return

    X = df[required_features]
    y = df[target_columns]

    # Membuat pipeline dengan OneHotEncoder untuk fitur kategorikal
    preprocessor = ColumnTransformer(
        transformers=[
            ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), ['Suhu Udara', 'Kelembapan Udara', 'Kelembapan Tanah'])
        ],
        remainder='passthrough'
    )

    # Membuat pipeline lengkap
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', MultiOutputClassifier(GaussianNB()))
    ])

    # Melatih model
    pipeline.fit(X, y)
    model = pipeline

    # Evaluasi model
    y_pred = model.predict(X)
    acc_penyiraman = accuracy_score(y['Penyiraman'], y_pred[:, 0])
    acc_pengkabutan = accuracy_score(y['Pengkabutan'], y_pred[:, 1])

    print(f"🎯 Akurasi Penyiraman: {acc_penyiraman:.2f}")
    print(f"🎯 Akurasi Pengkabutan: {acc_pengkabutan:.2f}")

def predict_status(sensor_data):
    global model

    if model is None:
        print("⚠️ Model belum dilatih. Silakan latih model terlebih dahulu.")
        return None

    try:
        if not all(feature in sensor_data for feature in required_features):
            print(f"❌ Data sensor tidak lengkap. Harus mengandung: {required_features}")
            return None

        df_raw = pd.DataFrame([{
            'Suhu Udara': float(sensor_data['Suhu Udara']),
            'Kelembapan Udara': float(sensor_data['Kelembapan Udara']),
            'Kelembapan Tanah': float(sensor_data['Kelembapan Tanah'])
        }])


        # Pastikan tipe data kolom adalah numerik
        df_raw = df_raw.apply(pd.to_numeric, errors='coerce')


        prediction = model.predict(df_raw)[0]
        result = dict(zip(target_columns, prediction))
   
        return result
    except Exception as e:
        print(f"❌ Gagal melakukan prediksi: {e}")
        return None

