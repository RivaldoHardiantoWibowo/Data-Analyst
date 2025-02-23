import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

file_path = os.path.join(os.path.dirname(__file__), 'main_data.csv')

if os.path.exists(file_path):
    st.success("File ditemukan!")
else:
    st.error("File tidak ditemukan!")

day_df = pd.read_csv(file_path)

hour_file_path = os.path.join(os.path.dirname(__file__), 'hour.csv')
if os.path.exists(hour_file_path):
    st.success("File hour.csv ditemukan!")
else:
    st.error("File hour.csv tidak ditemukan!")

hour_df = pd.read_csv(hour_file_path)
    
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

st.title("Bike Sharing Dashboard")
st.markdown("""
Analisis data peminjaman sepeda, termasuk tren harian, perbandingan pengguna, dan pengaruh cuaca.
""")

# Sidebar filter interaktif
st.sidebar.header("Filter Interaktif")
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal", 
    [day_df['dteday'].min(), day_df['dteday'].max()]
)

selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

# Filter data
filtered_df = day_df[
    (day_df['dteday'] >= pd.to_datetime(date_range[0])) &
    (day_df['dteday'] <= pd.to_datetime(date_range[1])) &
    (day_df['season'].isin(selected_seasons))
]

# Perbandingan Pengguna Kasual dengan yang Terdaftar
st.header("Perbandingan Jumlah Pengguna Kasual dan Terdaftar")
user_data = pd.DataFrame({
    'User Type': ['Casual', 'Registered'],
    'Count': [filtered_df['casual'].sum(), filtered_df['registered'].sum()]
})

fig, ax = plt.subplots()
sns.barplot(data=user_data, x='User Type', y='Count', palette='pastel', ax=ax)
ax.set_title('Total Pengguna Kasual vs Terdaftar (Filtered)')
st.pyplot(fig)

# Tren Peminjaman Sepeda per Bulan
st.header("Tren Peminjaman Sepeda per Bulan")
filtered_df['month'] = filtered_df['dteday'].dt.month_name()
monthly_rentals = filtered_df.groupby('month')['cnt'].sum().sort_index()

fig, ax = plt.subplots()
monthly_rentals.plot(kind='line', marker='o', ax=ax)
ax.set_title('Total Peminjaman Sepeda per Bulan (Filtered)')
ax.set_ylabel('Jumlah Peminjaman')
plt.xticks(rotation=45)
st.pyplot(fig)

#Jumlah Pengguna di Berbagai Musim
st.header("Distribusi Jumlah Pengguna Sepeda di Setiap Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=day_df, x='season', y='cnt', palette='coolwarm', ax=ax)
ax.set_title("Distribusi Jumlah Pengguna Sepeda di Setiap Musim")
ax.set_xlabel("Musim (Spring, Summer, Fall, Winter)")
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

#tren penyewaan sepeda dari pagi hingga malam

hourly_agg = hour_df.groupby('hr')['cnt'].mean()

st.header("Tren Penyewaan Sepeda dari Pagi hingga Malam")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(hourly_agg, marker='o', color='coral')
ax.set_title('Tren Penyewaan Sepeda dari Pagi hingga Malam')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
ax.set_xticks(range(0, 24))
ax.grid(True)
st.pyplot(fig)

# Insight
st.header("Insight dari Data 📊")
st.markdown("""
1. Pengguna terdaftar jauh lebih sering meminjam sepeda dibandingkan pengguna kasual.
2. Tren peminjaman meningkat selama musim panas dan menurun di musim dingin.
3. Cuaca yang cerah mendorong lebih banyak peminjaman sepeda.
""")
