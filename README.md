# Bike Sharing Analysis Dashboard

Dashboard untuk menganalisis pola penyewaan sepeda berdasarkan dataset Bike Sharing.

## Setup Environment

1. Clone repository ini
```
git clone https://github.com/[username]/bike-sharing-analysis.git
cd bike-sharing-analysis
```

2. Buat virtual environment
```
python -m venv venv
```

3. Aktifkan virtual environment
   - Windows:
   ```
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```
   source venv/bin/activate
   ```

4. Install dependencies
```
pip install -r requirements.txt
```

## Menjalankan Dashboard

1. Masuk ke direktori dashboard
```
cd dashboard
```

2. Jalankan aplikasi Streamlit
```
streamlit run dashboard.py
```

3. Buka browser dan akses URL yang ditampilkan di terminal (biasanya http://localhost:8501)

## Struktur Proyek
```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───day.csv
│   └───hour.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
```

## Dataset
Dataset Bike Sharing berisi informasi penyewaan sepeda harian dan per jam dengan variabel seperti:
- Tanggal
- Musim
- Hari kerja/libur
- Kondisi cuaca
- Temperatur
- Jumlah penyewaan (casual dan registered)

## Pertanyaan Bisnis
1. Bagaimana perbandingan tren penggunaan sepeda antara hari kerja (workday) dan hari libur (holiday)?
2. Bagaimana distribusi penyewaan sepeda berdasarkan musim dan bagaimana pengaruhnya terhadap tipe pengguna (casual vs registered)?

## Insights Utama
- Terdapat perbedaan pola penggunaan yang signifikan antara pengguna kasual dan terdaftar berdasarkan hari dan musim
- Musim gugur dan panas memiliki tingkat penyewaan tertinggi
- Pengguna terdaftar dominan pada hari kerja, sedangkan pengguna kasual meningkat pada hari libur
- Kondisi cuaca memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda

## Author
Desnia Anindy Irni Hareva