import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

st.title("🚲 Dashboard Analisis Data Penyewaan Sepeda")

file = st.file_uploader('Unggah File CSV', type='csv')

if file is not None:
    # --- LOAD & PREPARE DATA ---
    data = pd.read_csv(file)
    
    # Cleaning & Mapping
    data['dteday'] = pd.to_datetime(data['dteday'])
    data['season'] = data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    data['yr'] = data['yr'].map({0: '2011', 1: '2012'})
    data['mnth'] = data['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 
        7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des' 
    })
    data['weathersit'] = data['weathersit'].map({
        1: 'Cerah/Berawan', 2: 'Kabut/Mendung', 3: 'Salju/Hujan Ringan', 4: 'Cuaca Ekstrem'
    })
    data['weekday'] = data['weekday'].map({
        0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
    })

    # --- MEMBUAT TAB ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Data & Stats", "📊 Distribusi & Outliers", "🔗 Analisis Korelasi", "📈 Tren & Waktu", "🚀 Advanced Analysis"])

    # --- TAB 1: INFORMASI DATA ---
    with tab1:
        st.header('Informasi Dataframe')
        st.dataframe(data.head(100)) # Menampilkan 100 baris pertama agar tidak berat
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.subheader('Statistik Deskriptif')
            st.write(data.describe())
        with col_info2:
            st.subheader('Pengecekan Missing Value')
            st.write(data.isna().sum())

    # --- TAB 2: EXPLORATORY DATA ANALYSIS (EDA) ---
    with tab2:
        st.header('Distribusi Variabel')
        
        # Distribusi Target
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(data["cnt"], kde=True, ax=ax, color='skyblue')
        ax.set_title("Distribusi Total Penyewaan (cnt)")
        st.pyplot(fig)

        # Distribusi Fitur Numerik
        st.subheader("Distribusi Fitur Numerik & Outliers")
        num_cols = ["temp", "atemp", "hum", "windspeed"]
        
        col_plot1, col_plot2 = st.columns(2)
        with col_plot1:
            fig1, ax1 = plt.subplots()
            data[num_cols].hist(bins=20, ax=ax1)
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col_plot2:
            fig2, ax2 = plt.subplots()
            sns.boxplot(data=data[num_cols], ax=ax2, palette="Set3")
            ax2.set_title("Boxplot Fitur Numerik")
            st.pyplot(fig2)

    # --- TAB 3: HUBUNGAN ANTAR VARIABEL ---
    with tab3:
        st.header("Analisis Hubungan & Korelasi")
        
        # Heatmap
        numeric_data = data.select_dtypes(include=['int64', 'float64'])
        fig_heat, ax_heat = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax_heat)
        st.pyplot(fig_heat)

        # Scatter Plot
        st.subheader("Scatter Plot: Fitur vs Total Penyewaan")
        cols = st.columns(2)
        for i, col_name in enumerate(num_cols):
            with cols[i % 2]:
                fig, ax = plt.subplots()
                sns.scatterplot(x=data[col_name], y=data['cnt'], ax=ax, alpha=0.4, color='orange')
                ax.set_title(f"{col_name} vs cnt")
                st.pyplot(fig)

    # --- TAB 4: TREN & MUSIM ---
    with tab4:
        st.header("Analisis Berdasarkan Waktu & Kondisi")

        # Musim dan Tahun
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader("Penyewaan per Musim")
            fig_s, ax_s = plt.subplots()
            sns.barplot(x="season", y="cnt", data=data, ax=ax_s, palette="viridis")
            st.pyplot(fig_s)
        
        with col_t2:
            st.subheader("Pertumbuhan per Tahun")
            fig_y, ax_y = plt.subplots()
            sns.barplot(x="yr", y="cnt", data=data, ax=ax_y, palette="coolwarm")
            st.pyplot(fig_y)

        # Tren Bulanan
        st.subheader("Tren Rata-rata Penyewaan per Bulan")
        fig_m, ax_m = plt.subplots(figsize=(12, 5))
        sns.lineplot(x="mnth", y="cnt", data=data, marker="o", linewidth=2, ax=ax_m)
        st.pyplot(fig_m)

        # Time Series Harian
        st.subheader("Pergerakan Harian (Jan 2011 - Des 2012)")
        fig_ts, ax_ts = plt.subplots(figsize=(12, 5))
        sns.lineplot(x="dteday", y="cnt", data=data, ax=ax_ts, color='teal')
        plt.xticks(rotation=45)
        st.pyplot(fig_ts)

    with tab5:
        st.header("🚀 Analisis Lanjutan & Insight")
        
        # 1. Clustering Sederhana (Manual Binning untuk Segmentasi)
        # Mengelompokkan hari berdasarkan tingkat penyewaan: Low, Medium, High
        st.subheader("Segmentasi Hari Berdasarkan Volume Penyewaan")
        
        bins = [0, 2000, 5000, data['cnt'].max()]
        labels = ['Low Demand', 'Medium Demand', 'High Demand']
        data['demand_category'] = pd.cut(data['cnt'], bins=bins, labels=labels)
        
        fig_segment, ax_segment = plt.subplots(figsize=(8, 5))
        sns.countplot(x='demand_category', data=data, palette='magma', ax=ax_segment)
        ax_segment.set_title("Distribusi Kategori Permintaan")
        st.pyplot(fig_segment)
        
        with st.expander("💡 Lihat Penjelasan Analisis Segmentasi"):
            st.write("""
            **Analisis:**
            Berdasarkan grafik di atas, kita dapat mengidentifikasi hari-hari dengan permintaan 'High Demand'. 
            Hal ini membantu operasional dalam memastikan stok sepeda tersedia pada hari-hari tersebut. 
            Segmentasi ini merupakan teknik *data mining* sederhana untuk profil pelanggan.
            """)

        # 2. Geoanalysis / Regional Analysis (Jika ada data latitude/longitude, jika tidak, gunakan perbandingan hari kerja vs libur)
        st.subheader("Analisis Perilaku: Hari Kerja vs Akhir Pekan")
        
        fig_work, ax_work = plt.subplots(figsize=(8, 5))
        sns.boxplot(x='workingday', y='cnt', data=data, palette='Set2', ax=ax_work)
        ax_work.set_xticklabels(['Hari Libur', 'Hari Kerja'])
        ax_work.set_title("Perbandingan Penyewaan: Hari Kerja vs Libur")
        st.pyplot(fig_work)

        # --- EXPLANATORY SECTION ---
        st.divider()
        st.header("📝 Kesimpulan Utama (Explanatory Analysis)")
        st.info("""
        1. **Pengaruh Cuaca:** Terdapat korelasi positif yang kuat antara suhu (`temp`) dan jumlah penyewaan. Semakin hangat cuaca, semakin tinggi minat penyewa.
        2. **Tren Tahunan:** Terjadi kenaikan signifikan jumlah penyewaan dari tahun 2011 ke 2012, yang menunjukkan bisnis ini sedang berkembang.
        3. **Puncak Musim:** Musim Gugur (Fall) merupakan periode dengan rata-rata penyewaan tertinggi dibandingkan musim lainnya.
        4. **Insight Strategis:** Tim operasional harus menambah unit sepeda pada bulan-bulan puncak (Mei - Oktober) dan melakukan perawatan rutin pada musim dingin (Winter) saat permintaan menurun.
        """)

else:
    st.info("Silakan unggah file CSV Anda untuk memulai analisis.")