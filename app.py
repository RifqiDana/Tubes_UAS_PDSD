import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file = st.file_uploader('Unggah File CSV',type = 'csv')

if file is not None:
    data = pd.read_csv(file)
    st.write('Isi dari Dataframe Adalah : ')
    st.dataframe(data)

    # INFORMASI DATA
    st.header('Informasi Data')

    st.subheader('Statistik Deskriptif')
    st.write(data.describe())

    st.subheader('Missing Value')
    st.write(data.isna().sum())
    
    #DATA CLEANING
    data['dteday'] = pd.to_datetime(data['dteday'])
    data['season'] = data['season'].map({
        1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
    })
    
    data['yr'] = data['yr'].map({0: '2011', 1: '2012'})
    data['mnth'] = data['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 
        7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Sep', 12: 'Des' 
        })
    data['weathersit'] = data['weathersit'].map({
        1: 'Cerah/Berawan',
        2: 'Kabut/Mendung',
        3: 'Salju/Hujan Ringan',
        4: 'Cuaca Ekstrem'
    })
    data['weekday'] = data['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'selasa', 3: 'Rabu', 4: 'Kamis',
        5: 'Jumat', 6: 'Sabtu'
    })

    # Exploratory Data Analysis (EDA)
    st.header('Exploratory Data Analysis (EDA)')

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.histplot(data["cnt"], kde=True, ax=ax, color='skyblue')

    ax.set_title("Distribusi Jumlah Penyewaan Sepeda (cnt)")
    ax.set_xlabel("Jumlah")
    ax.set_ylabel("Frekuensi")

    st.pyplot(fig)
    
    #Distribusi Fitur Numerik
    fig, ax = plt.subplots(figsize=(12,8))
    
    st.subheader("Distribusi Fitur Numerik")
    num_cols = ["temp", "atemp", "hum", "windspeed"]
    
    data[num_cols].hist(bins=20, ax=ax)
    
    plt.suptitle("Distribusi Fitur Numerik")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    st.pyplot(fig)
    
    #Boxplot
    st.subheader('Pemeriksaan Outliers dengan Boxplot')
    num_cols = ["temp", "atemp", "hum", "windspeed"]

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.boxplot(data=data[num_cols], ax=ax, palette="Set3")

    ax.set_title("Boxplot Fitur Numerik", fontsize=14)

    st.pyplot(fig)

    # heatmap korelasi
    st.header("Analisis Hubungan Antar Variabel")

    numeric_data = data.select_dtypes(include=['int64', 'float64'])

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(numeric_data.corr(), 
                annot=True, 
                cmap="coolwarm", 
                fmt=".2f", 
                ax=ax)

    ax.set_title("Heatmap Korelasi (Kolom Numerik)")

    st.pyplot(fig)
    
    # SCATTER PLOT: FITUR VS TARGET
    st.header("Analisis Hubungan Fitur dengan Jumlah Penyewaan (cnt)")

    num_cols = ["temp", "atemp", "hum", "windspeed"]

    cols = st.columns(2)

    for i, col_name in enumerate(num_cols):
        with cols[i % 2]:
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.scatterplot(x=data[col_name], y=data['cnt'], ax=ax, alpha=0.5, color='orange')
            
            ax.set_title(f"{col_name} vs cnt", fontsize=12)
            ax.set_xlabel(col_name)
            ax.set_ylabel("Total Penyewaan (cnt)")
            
            st.pyplot(fig)
    
    #VISUALISASI PER MUSIM
            
    st.header("Analisis Penyewaan Berdasarkan Musim")

    fig, ax = plt.subplots(figsize=(10, 6))


    sns.barplot(x="season", y="cnt", data=data, ax=ax, palette="viridis")

    ax.set_title("Rata-rata Penyewaan Sepeda per Musim", fontsize=14)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")

    st.pyplot(fig)
    
    # ANALISIS HARI KERJA & HARI LIBUR
    st.header("Analisis Berdasarkan Status Hari")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hari Kerja vs Akhir Pekan")
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        sns.barplot(x="workingday", y="cnt", data=data, ax=ax1, palette="Blues")
        ax1.set_title("Rata-rata Penyewaan: Workingday (1) vs Weekend (0)")
        st.pyplot(fig1)

    with col2:
        st.subheader("Hari Libur (Holiday) vs Hari Biasa")
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        sns.barplot(x="holiday", y="cnt", data=data, ax=ax2, palette="Reds")
        ax2.set_title("Rata-rata Penyewaan: Holiday (1) vs Normal Day (0)")
        st.pyplot(fig2)
        
    # ANALISIS PER TAHUN
    st.header("Pertumbuhan Penyewaan Per Tahun")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(x="yr", y="cnt", data=data, ax=ax, palette="coolwarm")

    ax.set_title("Rata-rata Penyewaan Sepeda: 2011 vs 2012", fontsize=14)
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")

    st.pyplot(fig)
    
    #ANALISIS TREN BULANAN
    st.header("Tren Pertumbuhan Bulanan")

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        x="mnth", 
        y="cnt", 
        data=data, 
        marker="o", 
        linewidth=2, 
        color="tab:blue",
        ax=ax
    )
    ax.set_title("Tren Rata-rata Penyewaan Sepeda per Bulan", fontsize=16)
    ax.set_xlabel("Bulan", fontsize=12)
    ax.set_ylabel("Total Penyewaan (cnt)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)

    # ANALISIS TIME SERIES (KESELURUHAN)
    st.header("Tren Penyewaan Sepeda (Jan 2011 - Des 2012)")

    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(x="dteday", y="cnt", data=data, ax=ax, color='teal')

    ax.set_title("Pergerakan Harian Penyewaan Sepeda", fontsize=14)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.xticks(rotation=45) 
    
    st.pyplot(fig)