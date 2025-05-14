import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set halaman
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv("main_data.csv")
    data['dteday'] = pd.to_datetime(data['dteday'])
    data['month'] = data['dteday'].dt.month
    data['year'] = data['dteday'].dt.year
    data['day_of_week'] = data['dteday'].dt.dayofweek
    data['day_name'] = data['dteday'].dt.day_name()
    
    # Mapping untuk musim
    season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    data['season_name'] = data['season'].map(season_mapping)
    
    # Mapping untuk hari kerja dan hari libur
    data['holiday_name'] = data['holiday'].map({0: 'Hari Kerja', 1: 'Hari Libur'})
    data['workingday_name'] = data['workingday'].map({0: 'Weekend/Libur', 1: 'Hari Kerja'})
    
    # Mapping kondisi cuaca
    weather_mapping = {
        1: 'Cerah',
        2: 'Berawan/Berkabut',
        3: 'Hujan Ringan',
        4: 'Hujan Lebat'
    }
    data['weather_condition'] = data['weathersit'].map(weather_mapping)
    
    return data

# Load data
df = load_data()

# Sidebar
st.sidebar.title("Dashboard Analisis Bike Sharing")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=100)

# Filter data
st.sidebar.header("Filter Data")

# Filter berdasarkan tahun
year_options = df['year'].unique().tolist()
selected_year = st.sidebar.multiselect("Pilih Tahun", year_options, default=year_options)

# Filter berdasarkan musim
season_options = df['season_name'].unique().tolist()
selected_season = st.sidebar.multiselect("Pilih Musim", season_options, default=season_options)

# Filter berdasarkan tipe hari
day_type_options = df['workingday_name'].unique().tolist()
selected_day_type = st.sidebar.multiselect("Pilih Tipe Hari", day_type_options, default=day_type_options)

# Terapkan filter
filtered_df = df[
    (df['year'].isin(selected_year)) &
    (df['season_name'].isin(selected_season)) &
    (df['workingday_name'].isin(selected_day_type))
]

# Main dashboard
st.title("🚲 Dashboard Analisis Penyewaan Sepeda")
st.markdown("Dashboard ini menampilkan analisis dari dataset penyewaan sepeda untuk memahami pola penggunaan dan faktor-faktor yang mempengaruhinya.")

# Tambahkan penjelasan mengenai tipe pengguna
st.markdown("""
* **Pengguna Kasual (Casual)**: Pengguna yang menyewa sepeda tanpa pendaftaran keanggotaan, cenderung menggunakan layanan untuk rekreasi.
* **Pengguna Terdaftar (Registered)**: Pengguna yang telah mendaftar sebagai anggota layanan, cenderung menggunakan sepeda sebagai transportasi harian/rutin.
""")

# Metrics dengan presentasi perubahan
col1, col2, col3 = st.columns(3)

# Function untuk menghitung perubahan persentase
def calculate_percentage_change(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

total_rentals = filtered_df['cnt'].sum()
casual_rentals = filtered_df['casual'].sum()
registered_rentals = filtered_df['registered'].sum()

with col1:
    st.metric("Total Penyewaan", f"{total_rentals:,}")
    
with col2:
    st.metric("Pengguna Kasual", f"{casual_rentals:,}", 
              f"{casual_rentals/total_rentals:.1%} dari total")
    
with col3:
    st.metric("Pengguna Terdaftar", f"{registered_rentals:,}", 
              f"{registered_rentals/total_rentals:.1%} dari total")

# Tabs untuk navigasi
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Tren Waktu", "Pola Hari Kerja vs Libur", "Analisis Musiman", "Pola Mingguan", "Pengaruh Cuaca"])

with tab1:
    st.header("Tren Penggunaan Sepeda Berdasarkan Waktu")
    
    # Visualisasi tren bulanan
    monthly_trend = filtered_df.groupby(['year', 'month']).agg({
        'cnt': 'mean',
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()
    
    monthly_trend['period'] = monthly_trend['year'].astype(str) + '-' + monthly_trend['month'].astype(str).str.zfill(2)
    
    # Create plot
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot total, casual, and registered users
    ax1.plot(monthly_trend['period'], monthly_trend['cnt'], marker='o', linewidth=2, label='Total')
    ax1.plot(monthly_trend['period'], monthly_trend['casual'], marker='s', linewidth=2, label='Kasual')
    ax1.plot(monthly_trend['period'], monthly_trend['registered'], marker='^', linewidth=2, label='Terdaftar')
    
    plt.xticks(rotation=45)
    plt.title('Tren Rata-rata Penggunaan Sepeda per Bulan')
    plt.xlabel('Periode (Tahun-Bulan)')
    plt.ylabel('Rata-rata Penggunaan')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(fig1)
    
    # Generate insights based on filtered data
    peak_period = monthly_trend.loc[monthly_trend['cnt'].idxmax()]
    lowest_period = monthly_trend.loc[monthly_trend['cnt'].idxmin()]
    
    # Insight berdasarkan data yang difilter
    st.subheader("Insight Tren Waktu:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Periode Puncak Penggunaan:**
        - Periode: {peak_period['period']}
        - Rata-rata penyewaan: {peak_period['cnt']:.2f} per hari
        - Pengguna kasual: {peak_period['casual']:.2f} per hari
        - Pengguna terdaftar: {peak_period['registered']:.2f} per hari
        """)
    
    with col2:
        st.info(f"""
        **Periode Terendah Penggunaan:**
        - Periode: {lowest_period['period']}
        - Rata-rata penyewaan: {lowest_period['cnt']:.2f} per hari
        - Pengguna kasual: {lowest_period['casual']:.2f} per hari
        - Pengguna terdaftar: {lowest_period['registered']:.2f} per hari
        """)
    
    # Tren dan pola yang terlihat
    casual_trend = "meningkat" if monthly_trend['casual'].iloc[-1] > monthly_trend['casual'].iloc[0] else "menurun"
    registered_trend = "meningkat" if monthly_trend['registered'].iloc[-1] > monthly_trend['registered'].iloc[0] else "menurun"
    
    st.success(f"""
    **Analisis Tren:**
    - Tren pengguna kasual secara keseluruhan {casual_trend} sepanjang periode yang ditampilkan
    - Tren pengguna terdaftar secara keseluruhan {registered_trend} sepanjang periode yang ditampilkan
    - Terlihat pola musiman yang jelas dengan peningkatan penggunaan pada bulan-bulan hangat (musim panas dan gugur)
    - Pengguna terdaftar konsisten memiliki angka lebih tinggi dibandingkan pengguna kasual
    """)

with tab2:
    st.header("Perbandingan Hari Kerja vs Hari Libur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Berdasarkan workingday
        workday_data = filtered_df.groupby('workingday_name')[['casual', 'registered', 'cnt']].mean().reset_index()
        workday_melted = workday_data.melt(id_vars='workingday_name', value_vars=['casual', 'registered'], 
                                      var_name='Tipe Pengguna', value_name='Rata-rata Pengguna')
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='workingday_name', y='Rata-rata Pengguna', hue='Tipe Pengguna', data=workday_melted, palette='viridis', ax=ax2)
        plt.title('Penggunaan Sepeda: Hari Kerja vs Weekend/Libur')
        plt.xlabel('Tipe Hari')
        plt.ylabel('Rata-rata Jumlah Pengguna')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig2)
        
        # Insight berdasarkan data workday vs weekend - WITH ERROR HANDLING
        workday_exists = 'Hari Kerja' in workday_data['workingday_name'].values
        weekend_exists = 'Weekend/Libur' in workday_data['workingday_name'].values
        
        if workday_exists and weekend_exists:
            weekday_casual = workday_data[workday_data['workingday_name'] == 'Hari Kerja']['casual'].values[0]
            weekend_casual = workday_data[workday_data['workingday_name'] == 'Weekend/Libur']['casual'].values[0]
            weekday_registered = workday_data[workday_data['workingday_name'] == 'Hari Kerja']['registered'].values[0]
            weekend_registered = workday_data[workday_data['workingday_name'] == 'Weekend/Libur']['registered'].values[0]
            
            casual_pct_change = ((weekend_casual - weekday_casual) / weekday_casual) * 100
            registered_pct_change = ((weekend_registered - weekday_registered) / weekday_registered) * 100
            
            st.info(f"""
            **Insight Hari Kerja vs Weekend/Libur:**
            
            - Pengguna kasual: {'meningkat' if casual_pct_change > 0 else 'menurun'} **{abs(casual_pct_change):.1f}%** pada akhir pekan dibanding hari kerja
            - Pengguna terdaftar: {'meningkat' if registered_pct_change > 0 else 'menurun'} **{abs(registered_pct_change):.1f}%** pada akhir pekan dibanding hari kerja
            """)
        else:
            st.info("""
            **Insight Hari Kerja vs Weekend/Libur:**
            
            Pilih kedua tipe hari (Hari Kerja dan Weekend/Libur) untuk melihat perbandingan.
            """)
    
    with col2:
        # Berdasarkan holiday
        holiday_data = filtered_df.groupby('holiday_name')[['casual', 'registered', 'cnt']].mean().reset_index()
        holiday_melted = holiday_data.melt(id_vars='holiday_name', value_vars=['casual', 'registered'], 
                                      var_name='Tipe Pengguna', value_name='Rata-rata Pengguna')
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='holiday_name', y='Rata-rata Pengguna', hue='Tipe Pengguna', data=holiday_melted, palette='magma', ax=ax3)
        plt.title('Penggunaan Sepeda: Hari Kerja vs Hari Libur Nasional')
        plt.xlabel('Tipe Hari')
        plt.ylabel('Rata-rata Jumlah Pengguna')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig3)
        
        # Insight berdasarkan data holiday - WITH ERROR HANDLING
        workday_exists = 'Hari Kerja' in holiday_data['holiday_name'].values
        holiday_exists = 'Hari Libur' in holiday_data['holiday_name'].values
        
        if workday_exists and holiday_exists:
            workday_casual = holiday_data[holiday_data['holiday_name'] == 'Hari Kerja']['casual'].values[0]
            holiday_casual = holiday_data[holiday_data['holiday_name'] == 'Hari Libur']['casual'].values[0]
            workday_registered = holiday_data[holiday_data['holiday_name'] == 'Hari Kerja']['registered'].values[0]
            holiday_registered = holiday_data[holiday_data['holiday_name'] == 'Hari Libur']['registered'].values[0]
            
            casual_hol_change = ((holiday_casual - workday_casual) / workday_casual) * 100 if workday_casual > 0 else 0
            registered_hol_change = ((holiday_registered - workday_registered) / workday_registered) * 100 if workday_registered > 0 else 0
            
            st.info(f"""
            **Insight Hari Kerja vs Hari Libur Nasional:**
            
            - Pengguna kasual: {'meningkat' if casual_hol_change > 0 else 'menurun'} **{abs(casual_hol_change):.1f}%** pada hari libur nasional dibanding hari kerja biasa
            - Pengguna terdaftar: {'meningkat' if registered_hol_change > 0 else 'menurun'} **{abs(registered_hol_change):.1f}%** pada hari libur nasional dibanding hari kerja biasa
            """)
        else:
            st.info("""
            **Insight Hari Kerja vs Hari Libur Nasional:**
            
            Pilih kedua tipe hari (Hari Kerja dan Hari Libur) untuk melihat perbandingan.
            """)
    
    # Kesimpulan kombinasi dari kedua grafik
    if len(workday_data) > 1 and len(holiday_data) > 1:  # Only show if we have enough data for comparison
        st.success("""
        **Analisis Pola Hari Kerja vs Libur:**
        
        - Pengguna kasual menunjukkan preferensi yang kuat untuk menggunakan layanan pada akhir pekan dan hari libur
        - Pengguna terdaftar lebih konsisten menggunakan layanan pada hari kerja
        - Pola ini mengindikasikan bahwa pengguna terdaftar cenderung menggunakan sepeda sebagai transportasi harian untuk pergi ke tempat kerja atau aktivitas rutin
        - Sementara pengguna kasual lebih cenderung menggunakan layanan untuk rekreasi atau aktivitas sosial pada saat libur
        """)
    else:
        st.success("""
        **Analisis Pola Hari Kerja vs Libur:**
        
        Pilih semua tipe hari untuk melihat analisis lengkap perbandingan pola penggunaan sepeda antara hari kerja dan hari libur.
        """)

with tab3:
    st.header("Pengaruh Musim Terhadap Penggunaan Sepeda")
    
    # Analisis musiman
    season_data = filtered_df.groupby('season_name').agg({
        'cnt': 'mean',
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()
    
    # Urutkan musim secara kronologis
    season_order = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
    season_data['season_order'] = season_data['season_name'].apply(lambda x: season_order.index(x))
    season_data = season_data.sort_values('season_order')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Total penggunaan berdasarkan musim
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season_name', y='cnt', data=season_data, palette='coolwarm', order=season_order, ax=ax4)
        plt.title('Rata-rata Penggunaan Sepeda Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Rata-rata Jumlah Penyewaan per Hari')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig4)
        
        # Insight tentang total penyewaan per musim
        best_season = season_data.loc[season_data['cnt'].idxmax()]
        worst_season = season_data.loc[season_data['cnt'].idxmin()]
        
        st.info(f"""
        **Insight Penyewaan Total per Musim:**
        
        - Musim dengan penyewaan tertinggi: **{best_season['season_name']}** ({best_season['cnt']:.2f} penyewaan/hari)
        - Musim dengan penyewaan terendah: **{worst_season['season_name']}** ({worst_season['cnt']:.2f} penyewaan/hari)
        - Perbedaan: {((best_season['cnt'] - worst_season['cnt']) / worst_season['cnt'] * 100):.1f}% lebih tinggi
        """)
    
    with col2:
        # Perbandingan tipe pengguna berdasarkan musim
        season_melted = season_data.melt(id_vars=['season_name', 'season_order'], 
                                    value_vars=['casual', 'registered'],
                                    var_name='Tipe Pengguna', value_name='Rata-rata Pengguna')
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season_name', y='Rata-rata Pengguna', hue='Tipe Pengguna', 
                   data=season_melted, palette='viridis', order=season_order, ax=ax5)
        plt.title('Perbandingan Tipe Pengguna Berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Rata-rata Jumlah Pengguna per Hari')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig5)
        
        # Insight tentang tipe pengguna per musim
        casual_best = season_data.loc[season_data['casual'].idxmax()]
        casual_worst = season_data.loc[season_data['casual'].idxmin()]
        registered_best = season_data.loc[season_data['registered'].idxmax()]
        registered_worst = season_data.loc[season_data['registered'].idxmin()]
        
        st.info(f"""
        **Insight Tipe Pengguna per Musim:**
        
        - Pengguna kasual:
          * Tertinggi di **{casual_best['season_name']}** ({casual_best['casual']:.2f}/hari)
          * Terendah di **{casual_worst['season_name']}** ({casual_worst['casual']:.2f}/hari)
        
        - Pengguna terdaftar:
          * Tertinggi di **{registered_best['season_name']}** ({registered_best['registered']:.2f}/hari)
          * Terendah di **{registered_worst['season_name']}** ({registered_worst['registered']:.2f}/hari)
        """)
    
    # Analisis tren musiman
    seasonal_ratio = season_data.copy()
    seasonal_ratio['casual_pct'] = seasonal_ratio['casual'] / seasonal_ratio['cnt'] * 100
    seasonal_ratio['registered_pct'] = seasonal_ratio['registered'] / seasonal_ratio['cnt'] * 100
    
    st.subheader("Proporsi Pengguna per Musim")
    
    # Membuat stacked bar chart proporsi
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    
    seasonal_ratio['casual_pct'] = seasonal_ratio['casual'] / seasonal_ratio['cnt'] * 100
    seasonal_ratio['registered_pct'] = seasonal_ratio['registered'] / seasonal_ratio['cnt'] * 100
    
    x = np.arange(len(seasonal_ratio))
    width = 0.5
    
    ax6.bar(x, seasonal_ratio['registered_pct'], width, label='Terdaftar', color='#5cb85c')
    ax6.bar(x, seasonal_ratio['casual_pct'], width, bottom=seasonal_ratio['registered_pct'], label='Kasual', color='#f0ad4e')
    
    ax6.set_title('Proporsi Pengguna Kasual vs Terdaftar per Musim')
    ax6.set_xlabel('Musim')
    ax6.set_ylabel('Persentase (%)')
    ax6.set_xticks(x)
    ax6.set_xticklabels(seasonal_ratio['season_name'])
    ax6.legend()
    ax6.grid(axis='y', linestyle='--', alpha=0.7)
    
    for i, v in enumerate(seasonal_ratio['registered_pct']):
        ax6.text(i, v/2, f"{v:.1f}%", ha='center', color='white', fontweight='bold')
        
    for i, v in enumerate(seasonal_ratio['casual_pct']):
        ax6.text(i, seasonal_ratio['registered_pct'].iloc[i] + v/2, f"{v:.1f}%", ha='center', color='white', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig6)
    
    # Kesimpulan keseluruhan analisis musiman
    highest_casual_pct_season = seasonal_ratio.loc[seasonal_ratio['casual_pct'].idxmax()]['season_name']
    
    st.success(f"""
    **Analisis Musiman:**
    
    - Musim panas dan musim gugur menunjukkan jumlah penyewaan tertinggi, sementara musim semi konsisten menjadi musim dengan penyewaan terendah
    - Proporsi pengguna kasual tertinggi terjadi pada **{highest_casual_pct_season}**, menunjukkan peningkatan aktivitas rekreasi pada musim tersebut
    - Pengguna terdaftar menunjukkan pola yang lebih konsisten sepanjang tahun dibandingkan pengguna kasual yang lebih terpengaruh faktor musiman
    - Suhu dan kondisi cuaca yang lebih baik pada musim panas dan gugur tampaknya menjadi faktor utama yang mendorong peningkatan penyewaan
    """)

with tab4:
    st.header("Pola Penggunaan Mingguan")
    
    # Persiapan data hari dalam seminggu
    weekday_data = filtered_df.groupby('day_name')[['cnt', 'casual', 'registered']].mean().reset_index()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_data['day_order'] = weekday_data['day_name'].apply(lambda x: weekday_order.index(x))
    weekday_data = weekday_data.sort_values('day_order')
    
    # Mengubah nama hari ke Bahasa Indonesia untuk display
    day_name_id = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu', 
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }
    weekday_data['day_name_id'] = weekday_data['day_name'].map(day_name_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pola mingguan total
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='day_name_id', y='cnt', data=weekday_data, marker='o', linewidth=2, ax=ax7)
        plt.title('Pola Penggunaan Sepeda Sepanjang Minggu')
        plt.xlabel('Hari')
        plt.ylabel('Rata-rata Jumlah Penyewaan')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig7)
        
        # Insight tentang pola mingguan total
        busiest_day = weekday_data.loc[weekday_data['cnt'].idxmax()]
        slowest_day = weekday_data.loc[weekday_data['cnt'].idxmin()]
        
        st.info(f"""
        **Insight Pola Mingguan Total:**
        
        - Hari tersibuk: **{busiest_day['day_name_id']}** dengan rata-rata {busiest_day['cnt']:.2f} penyewaan
        - Hari terendah: **{slowest_day['day_name_id']}** dengan rata-rata {slowest_day['cnt']:.2f} penyewaan
        - Akhir pekan (Sabtu-Minggu) menunjukkan pola penggunaan yang {'lebih tinggi' if weekday_data[weekday_data['day_name'].isin(['Saturday', 'Sunday'])]['cnt'].mean() > weekday_data[~weekday_data['day_name'].isin(['Saturday', 'Sunday'])]['cnt'].mean() else 'lebih rendah'} dibandingkan hari kerja
        """)
    
    with col2:
        # Distribusi tipe pengguna berdasarkan hari
        weekday_melted = weekday_data.melt(id_vars=['day_name', 'day_name_id'], 
                                      value_vars=['casual', 'registered'],
                                      var_name='Tipe Pengguna', value_name='Rata-rata Pengguna')
        
        fig8, ax8 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='day_name_id', y='Rata-rata Pengguna', hue='Tipe Pengguna', data=weekday_melted, palette='magma', ax=ax8)
        plt.title('Perbandingan Tipe Pengguna Berdasarkan Hari')
        plt.xlabel('Hari')
        plt.ylabel('Rata-rata Jumlah Pengguna')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Tipe Pengguna')
        plt.tight_layout()
        st.pyplot(fig8)
        
        # Insight tentang tipe pengguna per hari
        casual_best_day = weekday_data.loc[weekday_data['casual'].idxmax()]
        casual_worst_day = weekday_data.loc[weekday_data['casual'].idxmin()]
        registered_best_day = weekday_data.loc[weekday_data['registered'].idxmax()]
        registered_worst_day = weekday_data.loc[weekday_data['registered'].idxmin()]
        
        st.info(f"""
        **Insight Tipe Pengguna per Hari:**
        
        - Pengguna kasual:
          * Tertinggi pada **{casual_best_day['day_name_id']}** ({casual_best_day['casual']:.2f}/hari)
          * Terendah pada **{casual_worst_day['day_name_id']}** ({casual_worst_day['casual']:.2f}/hari)
        
        - Pengguna terdaftar:
          * Tertinggi pada **{registered_best_day['day_name_id']}** ({registered_best_day['registered']:.2f}/hari)
          * Terendah pada **{registered_worst_day['day_name_id']}** ({registered_worst_day['registered']:.2f}/hari)
        """)
    
    # Analisis komposisi pengguna per hari
    weekday_ratio = weekday_data.copy()
    weekday_ratio['casual_pct'] = weekday_ratio['casual'] / weekday_ratio['cnt'] * 100
    weekday_ratio['registered_pct'] = weekday_ratio['registered'] / weekday_ratio['cnt'] * 100
    
    # Plot line chart persentase per hari
    fig9, ax9 = plt.subplots(figsize=(12, 6))
    
    ax9.plot(weekday_ratio['day_name_id'], weekday_ratio['casual_pct'], marker='o', linewidth=2, label='Pengguna Kasual (%)')
    ax9.plot(weekday_ratio['day_name_id'], weekday_ratio['registered_pct'], marker='s', linewidth=2, label='Pengguna Terdaftar (%)')
    
    ax9.set_title('Persentase Tipe Pengguna per Hari')
    ax9.set_xlabel('Hari')
    ax9.set_ylabel('Persentase (%)')
    ax9.set_ylim(0, 100)
    ax9.legend()
    ax9.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    st.pyplot(fig9)
    
    # Kesimpulan keseluruhan pola mingguan
    st.success("""
    **Analisis Pola Mingguan:**
    
    - Terdapat perbedaan yang jelas antara pola penggunaan pada hari kerja dan akhir pekan
    - Pengguna kasual menunjukkan peningkatan signifikan pada akhir pekan, mengindikasikan penggunaan untuk aktivitas rekreasi
    - Pengguna terdaftar memiliki puncak penggunaan pada hari kerja, menunjukkan penggunaan sepeda sebagai transportasi komuter
    - Persentase pengguna kasual tertinggi terjadi pada akhir pekan, sementara persentase pengguna terdaftar dominan pada hari kerja
    """)

with tab5:
    st.header("Pengaruh Cuaca Terhadap Penyewaan Sepeda")
    
    # Analisis berdasarkan cuaca
    weather_analysis = filtered_df.groupby('weather_condition').agg({
        'cnt': 'mean',
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()
    
    # Urutkan kondisi cuaca dari yang terbaik ke terburuk
    weather_order = ['Cerah', 'Berawan/Berkabut', 'Hujan Ringan', 'Hujan Lebat']
    weather_analysis['weather_order'] = weather_analysis['weather_condition'].apply(lambda x: weather_order.index(x))
    weather_analysis = weather_analysis.sort_values('weather_order')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Total penggunaan berdasarkan cuaca
        fig10, ax10 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='weather_condition', y='cnt', data=weather_analysis, palette='Blues_r', order=weather_order, ax=ax10)
        plt.title('Rata-rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Jumlah Penyewaan')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig10)
        
        # Insight tentang penggunaan berdasarkan cuaca
        best_weather = weather_analysis.loc[weather_analysis['cnt'].idxmax()]
        worst_weather = weather_analysis.loc[weather_analysis['cnt'].idxmin()]
        
        weather_impact = ((best_weather['cnt'] - worst_weather['cnt']) / best_weather['cnt']) * 100
        
        st.info(f"""
        **Insight Pengaruh Cuaca Terhadap Total Penyewaan:**
        
        - Kondisi cuaca terbaik untuk penyewaan: **{best_weather['weather_condition']}** ({best_weather['cnt']:.2f} penyewaan/hari)
        - Kondisi cuaca terburuk untuk penyewaan: **{worst_weather['weather_condition']}** ({worst_weather['cnt']:.2f} penyewaan/hari)
        - Penurunan: {weather_impact:.1f}% dari kondisi terbaik ke terburuk
        """)
    
    with col2:
        # Perbandingan tipe pengguna berdasarkan cuaca
        weather_melted = weather_analysis.melt(id_vars=['weather_condition', 'weather_order'], 
                                         value_vars=['casual', 'registered'],
                                         var_name='Tipe Pengguna', value_name='Rata-rata Pengguna')
        
        fig11, ax11 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='weather_condition', y='Rata-rata Pengguna', hue='Tipe Pengguna', 
                   data=weather_melted, palette='viridis', order=weather_order, ax=ax11)
        plt.title('Perbandingan Tipe Pengguna Berdasarkan Kondisi Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Jumlah Pengguna')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig11)
        
        # Insight tentang pengaruh cuaca terhadap tipe pengguna
        casual_best_weather = weather_analysis.loc[weather_analysis['casual'].idxmax()]
        casual_worst_weather = weather_analysis.loc[weather_analysis['casual'].idxmin()]
        registered_best_weather = weather_analysis.loc[weather_analysis['registered'].idxmax()]
        registered_worst_weather = weather_analysis.loc[weather_analysis['registered'].idxmin()]
        
        casual_impact = ((casual_best_weather['casual'] - casual_worst_weather['casual']) / casual_best_weather['casual']) * 100
        registered_impact = ((registered_best_weather['registered'] - registered_worst_weather['registered']) / registered_best_weather['registered']) * 100
        
        st.info(f"""
        **Insight Pengaruh Cuaca Terhadap Tipe Pengguna:**
        
        - Pengguna kasual:
          * Tertinggi saat **{casual_best_weather['weather_condition']}** ({casual_best_weather['casual']:.2f}/hari)
          * Terendah saat **{casual_worst_weather['weather_condition']}** ({casual_worst_weather['casual']:.2f}/hari)
          * Penurunan: {casual_impact:.1f}%
        
        - Pengguna terdaftar:
          * Tertinggi saat **{registered_best_weather['weather_condition']}** ({registered_best_weather['registered']:.2f}/hari)
          * Terendah saat **{registered_worst_weather['weather_condition']}** ({registered_worst_weather['registered']:.2f}/hari)
          * Penurunan: {registered_impact:.1f}%
        """)
    
    # Analisis proporsi berdasarkan cuaca
    weather_ratio = weather_analysis.copy()
    weather_ratio['casual_pct'] = weather_ratio['casual'] / weather_ratio['cnt'] * 100
    weather_ratio['registered_pct'] = weather_ratio['registered'] / weather_ratio['cnt'] * 100
    
    # Plot pie chart untuk setiap kondisi cuaca
    st.subheader("Proporsi Pengguna Berdasarkan Kondisi Cuaca")
    
    # Create grid of pie charts
    fig12, axes = plt.subplots(1, len(weather_ratio), figsize=(15, 5))
    
    for i, (idx, row) in enumerate(weather_ratio.iterrows()):
        labels = ['Kasual', 'Terdaftar']
        sizes = [row['casual_pct'], row['registered_pct']]
        colors = ['#f0ad4e', '#5cb85c']
        
        axes[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        axes[i].set_title(row['weather_condition'])
        axes[i].axis('equal')
    
    plt.tight_layout()
    st.pyplot(fig12)
    
    # Kesimpulan keseluruhan pengaruh cuaca
    max_casual_pct_weather = weather_ratio.loc[weather_ratio['casual_pct'].idxmax()]['weather_condition']
    
    st.success(f"""
    **Analisis Pengaruh Cuaca:**
    
    - Kondisi cuaca memiliki dampak yang signifikan terhadap jumlah penyewaan sepeda
    - Cuaca cerah konsisten menghasilkan jumlah penyewaan tertinggi, sementara kondisi hujan menurunkan jumlah penyewaan secara drastis
    - Pengguna kasual lebih sensitif terhadap perubahan kondisi cuaca dibandingkan pengguna terdaftar
    - Proporsi pengguna kasual tertinggi terjadi pada kondisi **{max_casual_pct_weather}**, menunjukkan bahwa cuaca baik mendorong lebih banyak penggunaan rekreasional
    - Pengguna terdaftar menunjukkan konsistensi yang lebih tinggi dalam menggunakan layanan pada berbagai kondisi cuaca, mengindikasikan ketergantungan pada sepeda sebagai transportasi utama
    """)

# Kesimpulan dan Rekomendasi
st.header("Kesimpulan dan Rekomendasi")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kesimpulan Utama")
    st.write("""
    1. **Perbedaan Pola Hari Kerja vs Libur**:
       - Pengguna kasual menunjukkan preferensi yang kuat untuk menyewa sepeda pada hari libur dan akhir pekan
       - Pengguna terdaftar lebih dominan pada hari kerja, mengindikasikan penggunaan sepeda sebagai transportasi rutin

    2. **Pengaruh Musim Terhadap Penyewaan**:
       - Musim gugur dan musim panas menjadi periode dengan tingkat penyewaan tertinggi
       - Musim semi konsisten menjadi musim dengan tingkat penyewaan terendah

    3. **Pola Mingguan**:
       - Terdapat pola mingguan yang jelas dalam penggunaan layanan penyewaan sepeda
       - Akhir pekan menunjukkan peningkatan pada pengguna kasual
       - Hari kerja (Senin-Jumat) menunjukkan dominasi pengguna terdaftar

    4. **Pengaruh Kondisi Cuaca**:
       - Cuaca cerah dan berawan memiliki tingkat penyewaan tertinggi
       - Cuaca hujan, terutama hujan lebat, secara signifikan menurunkan jumlah penyewaan
       - Pengguna terdaftar cenderung lebih konsisten dalam penggunaan sepeda pada berbagai kondisi cuaca dibandingkan pengguna kasual
    """)

with col2:
    st.subheader("Rekomendasi Bisnis")
    st.write("""
    1. **Strategi Distribusi Armada**:
       - Meningkatkan jumlah sepeda yang tersedia pada hari kerja di lokasi perkantoran untuk mengakomodasi pengguna terdaftar
       - Mengalokasikan lebih banyak sepeda di area rekreasi pada akhir pekan untuk pengguna kasual

    2. **Program Pemasaran**:
       - Menawarkan promo khusus untuk pengguna kasual pada hari kerja untuk meningkatkan utilisasi
       - Membuat program loyalitas untuk pengguna terdaftar pada akhir pekan
       - Mengembangkan kampanye pemasaran yang berbeda untuk kedua segmen pengguna

    3. **Penyesuaian Musiman**:
       - Meningkatkan armada sepeda selama musim panas dan gugur untuk mengantisipasi permintaan tinggi
       - Melakukan pemeliharaan armada pada musim semi ketika permintaan rendah
       - Pertimbangkan untuk menerapkan tarif musiman untuk mengoptimalkan pendapatan

    4. **Antisipasi Cuaca**:
       - Mengembangkan sistem prediksi berbasis prakiraan cuaca untuk mengoptimalkan distribusi sepeda
       - Menyediakan perlengkapan hujan atau insentif khusus pada hari hujan untuk mempertahankan tingkat penyewaan
    """)

# Bagian data detail
with st.expander("Lihat Data Detail"):
    st.dataframe(filtered_df)
    
    # Opsi download data
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data Terfilter sebagai CSV",
        data=csv,
        file_name='bike_rental_filtered.csv',
        mime='text/csv',
    )

# Footer
st.markdown("---")
st.markdown("Desnia Anindy Irni Hareva| Data: Bike Sharing Dataset")