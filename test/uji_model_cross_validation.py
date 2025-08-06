from fileinput import filename
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import accuracy_score
import numpy as np
import os

# Load data dari file CSV
filename = 'sensor_data.csv'
df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))

# Konversi label ke format numerik (0 dan 1)
df['Penyiraman'] = df['Penyiraman'].map({'Perlu': 1, 'Tidak perlu': 0})
df['Pengkabutan'] = df['Pengkabutan'].map({'Perlu': 1, 'Tidak perlu': 0})

# Fitur dan Target
X = df[['Suhu Udara', 'Kelembapan Udara', 'Kelembapan Tanah']]
y_penyiraman = df['Penyiraman']
y_pengkabutan = df['Pengkabutan']

# Konfigurasi Cross Validation
k = 5
kf = KFold(n_splits=k, shuffle=True, random_state=42)

# Model
model = GaussianNB()

# ----------------------------
# Evaluasi untuk Penyiraman
# ----------------------------
acc_scores_penyiraman = cross_val_score(model, X, y_penyiraman, cv=kf, scoring='accuracy')

print("📊 Hasil Cross Validation - Penyiraman")
for i, acc in enumerate(acc_scores_penyiraman, start=1):
    print(f"Fold {i}: {acc:.4f}")
print(f"Rata-rata Akurasi Penyiraman: {acc_scores_penyiraman.mean():.4f}\n")

# ----------------------------
# Evaluasi untuk Pengkabutan
# ----------------------------
acc_scores_pengkabutan = cross_val_score(model, X, y_pengkabutan, cv=kf, scoring='accuracy')

print("📊 Hasil Cross Validation - Pengkabutan")
for i, acc in enumerate(acc_scores_pengkabutan, start=1):
    print(f"Fold {i}: {acc:.4f}")
print(f"Rata-rata Akurasi Pengkabutan: {acc_scores_pengkabutan.mean():.4f}")
