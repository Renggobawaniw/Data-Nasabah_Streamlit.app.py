import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Judul dan Pengantar
st.title("Analisis Data Nasabah Bank")
st.markdown("""
**Nama**: Renggo Bawani Wijayaningrum  
**Program**: Beasiswa Data Science Digital Scholarship by KOMDIGI  
**Latar Belakang**:  
Data berisi informasi nasabah bank yang mencakup: usia, jenis kelamin, pendapatan, saldo, jenis produk (tabungan, kredit, deposito), skor kredit, dan lainnya.
""")

# Load Data
uploaded_file = st.file_uploader("Data_Nasabah.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter=';')

    # Tampilkan Dataframe
    st.subheader("📋 Data Nasabah (Preview)")
    st.dataframe(df.head())

    # Bersihkan data
    df.columns = df.columns.str.strip()
    df["jenis_kelamin"] = df["jenis_kelamin"].str.strip().str.capitalize()
    df["jenis_produk"] = df["jenis_produk"].str.strip().str.lower()

    if "pengguna_mobile_banking" in df.columns:
        df["pengguna_mobile_banking"] = df["pengguna_mobile_banking"].str.upper().map({"YA": 1, "TIDAK": 0})

    # Konversi kolom numerik
    num_cols = ["umur", "pendapatan", "saldo_rata_rata", "jumlah_transaksi", "frekuensi_kunjungi_cabang", "skor_kredit"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    st.subheader("📊 Statistik Deskriptif")
    st.write(df.describe())

    # 🔹 Visualisasi 1: Histogram Pendapatan
    st.subheader("📈 Distribusi Pendapatan")
    fig1, ax1 = plt.subplots()
    sns.histplot(df["pendapatan"], bins=20, kde=True, ax=ax1)
    st.pyplot(fig1)

    # Tombol download gambar histogram
    buffer1 = io.BytesIO()
    fig1.savefig(buffer1, format="png")
    buffer1.seek(0)
    st.download_button("📥 Unduh Histogram", data=buffer1, file_name="histogram_pendapatan.png", mime="image/png")

    # 🔹 Visualisasi 2: Boxplot Mobile Banking vs Skor Kredit
    if "pengguna_mobile_banking" in df.columns:
        st.subheader("📊 Skor Kredit Berdasarkan Penggunaan Mobile Banking")
        fig2, ax2 = plt.subplots()
        sns.boxplot(x="pengguna_mobile_banking", y="skor_kredit", data=df, ax=ax2)
        ax2.set_xticklabels(["TIDAK", "YA"])
        st.pyplot(fig2)

        # Tombol download boxplot
        buffer2 = io.BytesIO()
        fig2.savefig(buffer2, format="png")
        buffer2.seek(0)
        st.download_button("📥 Unduh Boxplot Skor Kredit", data=buffer2, file_name="boxplot_mobile_banking.png", mime="image/png")

    # 🔹 Visualisasi 3: Bar Chart Rata-rata Pendapatan per Produk
    st.subheader("📉 Rata-rata Pendapatan Berdasarkan Jenis Produk")
    avg_income = df.groupby("jenis_produk")["pendapatan"].mean().sort_values()
    fig3, ax3 = plt.subplots()
    avg_income.plot(kind='bar', ax=ax3)
    ax3.set_ylabel("Rata-rata Pendapatan")
    st.pyplot(fig3)

    # Tombol download bar chart
    buffer3 = io.BytesIO()
    fig3.savefig(buffer3, format="png")
    buffer3.seek(0)
    st.download_button("📥 Unduh Bar Chart Produk vs Pendapatan", data=buffer3, file_name="bar_produk_pendapatan.png", mime="image/png")

else:
    st.info("Data_Nasabah.csv.")
