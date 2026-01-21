import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Konfigurasi Halaman (Wajib di baris pertama setelah imports)
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide"
)

# Setup tema plot
sns.set(style='whitegrid')

# ==============================================================================
# HELPER FUNCTIONS (Menyiapkan Data)
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

# Load data bersih (pastikan file ini ada di folder yang sama)
try:
    all_df = pd.read_csv("main_data.csv")
    all_df["dteday"] = pd.to_datetime(all_df["dteday"])
    all_df.sort_values(by="dteday", inplace=True)
    all_df.reset_index(inplace=True)
except FileNotFoundError:
    st.error("File 'main_data.csv' tidak ditemukan. Pastikan sudah digenerate di notebook.")
    st.stop()

# ==============================================================================
# SIDEBAR (Filter)
# ==============================================================================

with st.sidebar:
    st.header("⚙️ Konfigurasi")

    # Logo (Opsional)
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png")

    # Filter Rentang Waktu
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Dataframe Utama
main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                 (all_df["dteday"] <= str(end_date))]

# Siapkan dataframe visualisasi
daily_orders_df = create_daily_orders_df(main_df)
season_df = create_by_season_df(main_df)
weather_df = create_by_weather_df(main_df)

# ==============================================================================
# MAIN PAGE
# ==============================================================================

st.title("🚲 Dashboard Analisis Bike Sharing")
st.markdown(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")

# --- ROW 1: KEY METRICS ---
col1, col2, col3 = st.columns(3)

with col1:
    total_all = daily_orders_df.cnt.sum()
    st.metric("Total Penyewaan", value=f"{total_all:,}")

with col2:
    total_casual = daily_orders_df.casual.sum()
    st.metric("Pengguna Biasa (Casual)", value=f"{total_casual:,}")

with col3:
    total_reg = daily_orders_df.registered.sum()
    st.metric("Pengguna Terdaftar", value=f"{total_reg:,}")

st.markdown("---")

# --- ROW 2: TABS LAYOUT ---
tab1, tab2 = st.tabs(["📈 Tren Harian", "🌤️ Analisis Cuaca & Musim"])

# TAB 1: Fokus pada performa waktu
with tab1:
    st.subheader("Tren Penyewaan Harian")

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(
        daily_orders_df["dteday"],
        daily_orders_df["cnt"],
        marker='o',
        linewidth=2,
        color="#007ACC" # Biru profesional
    )
    ax.set_ylabel("Jumlah Penyewaan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# TAB 2: Fokus pada kategori
with tab2:
    col_season, col_weather = st.columns(2)

    with col_season:
        st.subheader("Penyewaan Berdasarkan Musim")
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot(
            y="cnt",
            x="season",
            data=season_df.sort_values(by="cnt", ascending=False),
            palette="Blues_d",
            ax=ax
        )
        ax.set_xlabel(None)
        ax.set_ylabel("Total Sewa")
        st.pyplot(fig)

    with col_weather:
        st.subheader("Pengaruh Cuaca")
        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot(
            y="cnt",
            x="weathersit",
            data=weather_df.sort_values(by="cnt", ascending=False),
            palette="Greens_d",
            ax=ax
        )
        ax.set_xlabel(None)
        ax.set_ylabel(None)
        st.pyplot(fig)

# Footer
st.caption("Copyright © Dicoding 2024")
