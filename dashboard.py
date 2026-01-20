import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup gaya plot
sns.set(style='dark')

# --- Fungsi Helper ---
def create_daily_orders_df(df):
    daily_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    return daily_df.reset_index()

def create_by_season_df(df):
    return df.groupby("season").cnt.sum().reset_index()

# --- Load Data ---
# Pastikan file main_data.csv satu folder dengan script ini
all_df = pd.read_csv("main_data.csv")

# Ubah ke datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

# --- Sidebar Filter ---
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Logo (Opsional, pakai logo default atau hapus baris ini)
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png")
    
    # Input Tanggal
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                 (all_df["dteday"] <= str(end_date))]

# Siapkan Dataframe
daily_orders_df = create_daily_orders_df(main_df)
season_df = create_by_season_df(main_df)

# --- Tampilan Utama ---
st.header('Dicoding Bike Sharing Dashboard 🚲')

# Metrik Atas
col1, col2 = st.columns(2)
with col1:
    total_rentals = daily_orders_df.cnt.sum()
    st.metric("Total Penyewaan", value=total_rentals)
with col2:
    avg_rentals = round(daily_orders_df.cnt.mean(), 1)
    st.metric("Rata-rata Harian", value=avg_rentals)

# Chart 1: Tren Harian
st.subheader("Tren Penyewaan Harian")
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_ylabel("Jumlah Sewa")
st.pyplot(fig)

# Chart 2: Musim
st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="cnt", 
    x="season",
    data=season_df.sort_values(by="cnt", ascending=False),
    palette="Blues_d",
    ax=ax
)
ax.set_ylabel("Total Penyewaan")
ax.set_xlabel("Musim")
st.pyplot(fig)

st.caption('Copyright (c) 2024')
