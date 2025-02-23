import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv('main_data.csv')

st.title("Bike Sharing Dashboard")
st.markdown("""
Analisis data peminjaman sepeda, termasuk tren harian, perbandingan pengguna, dan pengaruh cuaca.
""")

# Perbandingan Pengguna Kasual dengan yang Terdaftar
st.header("Perbandingan Jumlah Pengguna Kasual dan Terdaftar")
user_data = pd.DataFrame({
    'User Type': ['Casual', 'Registered'],
    'Count': [day_df['casual'].sum(), day_df['registered'].sum()]
})

fig, ax = plt.subplots()
sns.barplot(data=user_data, x='User Type', y='Count', palette='pastel', ax=ax)
ax.set_title('Total Pengguna Kasual vs Terdaftar')
st.pyplot(fig)

# Tren Peminjaman Sepeda per Bulan
st.header("Tren Peminjaman Sepeda per Bulan")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['month'] = day_df['dteday'].dt.month_name()
monthly_rentals = day_df.groupby('month')['cnt'].sum().sort_index()

fig, ax = plt.subplots()
monthly_rentals.plot(kind='line', marker='o', ax=ax)
ax.set_title('Total Peminjaman Sepeda per Bulan')
ax.set_ylabel('Jumlah Peminjaman')
plt.xticks(rotation=45)
st.pyplot(fig)


st.header("Insight dari Data 📊")
st.markdown("""
1. Pengguna terdaftar jauh lebih sering meminjam sepeda dibandingkan pengguna kasual.
2. Tren peminjaman meningkat selama musim panas dan menurun di musim dingin.
3. Cuaca yang cerah mendorong lebih banyak peminjaman sepeda.
""")
