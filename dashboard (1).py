import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# 1. Konfigurasi Halaman (Harus di paling atas)
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Setup style seaborn biar lebih clean
sns.set(style='whitegrid')

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def create_daily_orders_df(df):
    daily_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    return daily_df.reset_index()

def create_by_season_df(df):
    return df.groupby("season").cnt.sum().reset_index()

def create_by_weather_df(df):
    return df.groupby("weathersit").cnt.sum().reset_index()

# ==============================================================================
# LOAD DATA
# ==============================================================================

# Load data yang sudah bersih
all_df = pd.read_csv("main_data.csv")

# Pastikan tipe data datetime aman
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

# ==============================================================================
# SIDEBAR (FILTER)
# ==============================================================================

with st.sidebar:
    # Header profil atau logo sederhana
    st.header("Dashboard Filters")
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png") # Bisa diganti logo lain
    
    # Batas tanggal
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()

    # Input Date Picker
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Tanggal tidak valid")

# Filter data utama
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                 (all_df["dteday"] <= str(end_date))]

# Siapkan dataframe untuk visualisasi
daily_orders_df = create_daily_orders_df(main_df)
season_df = create_by_season_df(main_df)
weather_df = create_by_weather_df(main_df)

# ==============================================================================
# MAIN DASHBOARD UI
# ==============================================================================

st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard ini menampilkan performa penyewaan sepeda berdasarkan data historis.")
st.markdown("---")

# 1. KEY METRICS (Baris Pertama)
# Kita pakai kolom biar rapi berjajar ke samping
col1, col2, col3 = st.columns(3)

with col1:
    total_all = daily_orders_df.cnt.sum()
    st.metric("Total Penyewaan", value=f"{total_all:,}")

with col2:
    total_casual = daily_orders_df.casual.sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

with col3:
    total_reg = daily_orders_df.registered.sum()
    st.metric("Pengguna Terdaftar", value=f"{total_reg:,}")

st.markdown("---")

# 2. CHARTS DENGAN TABS (Biar tidak scroll panjang)
tab1, tab2 = st.tabs(["📈 Tren Harian", "🌤️ Analisis Cuaca & Musim"])

with tab1:
    st.subheader("Bagaimana Tren Penyewaan Seiring Waktu?")
    
    # Plot line chart
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Plot total
    ax.plot(
        daily_orders_df["dteday"],
        daily_orders_df["cnt"],
        marker='o', 
        linewidth=2,
        color="#007ACC", # Warna biru profesional
        label="Total Rides"
    )
    
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xlabel(None)
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.subheader("Faktor Lingkungan terhadap Penyewaan")
    
    # Bagi jadi 2 kolom lagi di dalam tab
    col_season, col_weather = st.columns(2)
    
    with col_season:
        st.markdown("**Performa Musim**")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Barplot Musim
        sns.barplot(
            y="cnt", 
            x="season",
            data=season_df.sort_values(by="cnt", ascending=False),
            palette="Blues_r", # Gradasi biru
            ax=ax
        )
        ax.set_ylabel("Total Sewa")
        ax.set_xlabel(None)
        st.pyplot(fig)
        
    with col_weather:
        st.markdown("**Pengaruh Cuaca**")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Barplot Cuaca
        sns.barplot(
            y="cnt", 
            x="weathersit",
            data=weather_df.sort_values(by="cnt", ascending=False),
            palette="Greens_r", # Gradasi hijau biar beda dikit
            ax=ax
        )
        ax.set_ylabel(None) # Biar ga numpuk teksnya
        ax.set_xlabel(None)
        st.pyplot(fig)

# Footer
st.caption("Copyright © Dicoding 2024 | Dibuat dengan Streamlit")
