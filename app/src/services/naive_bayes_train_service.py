import os
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Model dan variabel global
model = None
required_features = ['Suhu Udara', 'Kelembapan Udara', 'Kelembapan Tanah']
target_columns = ['Penyiraman', 'Pengkabutan']

def load_data_from_csv(filename='sensor_data.csv'):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    if not os.path.isfile(file_path):
        print(f"❌ File tidak ditemukan: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)

        # Pastikan kolom target numerik
        df['Penyiraman'] = df['Penyiraman'].map({'Perlu': 1, 'Tidak perlu': 0})
        df['Pengkabutan'] = df['Pengkabutan'].map({'Perlu': 1, 'Tidak perlu': 0})

        if df[target_columns].isnull().any().any():
            print("❌ Data target mengandung nilai tak valid setelah konversi.")
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

    model = MultiOutputClassifier(GaussianNB())
    model.fit(X, y)

    y_pred = model.predict(X)
    acc_penyiraman = accuracy_score(y['Penyiraman'], y_pred[:, 0])
    acc_pengkabutan = accuracy_score(y['Pengkabutan'], y_pred[:, 1])

    print(f"🎯 Akurasi Penyiraman: {acc_penyiraman:.2f}")
    print(f"🎯 Akurasi Pengkabutan: {acc_pengkabutan:.2f}")

def predict_status(sensor_data):
    global model
    if model is None:
        print("⚠️ Model belum dilatih.")
        return None

    try:
        data_input = pd.DataFrame([{
            'Suhu Udara': float(sensor_data['Suhu Udara']),
            'Kelembapan Udara': float(sensor_data['Kelembapan Udara']),
            'Kelembapan Tanah': float(sensor_data['Kelembapan Tanah'])
        }])

        prediction = model.predict(data_input)[0]
        # logic_result = apply_manual_logic(data_input.iloc[0])

        result = {
            'Penyiraman': 'Perlu' if prediction[0] else 'Tidak perlu',
            'Pengkabutan': 'Perlu' if prediction[1] else 'Tidak perlu',
        }
        return result
    except Exception as e:
        print(f"❌ Gagal memproses prediksi: {e}")
        return None

