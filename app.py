import streamlit as st 
import pandas as pd 
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Penyewaan Sepeda", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Penyewaan Sepeda")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

#membaca dataset
file = st.file_uploader('Unggah File CSV', type='csv')
if file is not None:
    df = pd.read_csv(file, encoding="ISO-8859-1")
    
    # Cleaning & Mapping
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    df['yr'] = df['yr'].map({0: '2011', 1: '2012'})
    df['mnth'] = df['mnth'].map({
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 
        7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des' 
    })
    df['weathersit'] = df['weathersit'].map({
        1: 'Clear/Few clouds', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'
    })
    df['weekday'] = df['weekday'].map({
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'
    })
    df['workingday'] = df['workingday'].map({
        0: 'Working Day', 1: 'Holiday/Weekend'
    })
    
    col1, col2 = st.columns((2))
    df['dteday'] = pd.to_datetime(df['dteday'])

    #mendapatkan tanggal minimum dan maksimum
    startDate = pd.to_datetime(df['dteday']).min()
    endDate = pd.to_datetime(df['dteday']).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))
        
    df = df[(df['dteday'] >= date1) & (df['dteday'] <= date2)].copy()
    
    #membuat filter sidebar 
    st.sidebar.header("Pilih filter Anda: ")
    
    #untuk bulan
    bulan = st.sidebar.multiselect("Pilih Bulan", df['mnth'].unique())
    if not bulan:
        df2 = df.copy()
    else:
        df2 = df[df['mnth'].isin(bulan)]
        
    #untuk kodisi musim
    musim = st.sidebar.multiselect("Pilih Musim", df2['season'].unique())
    if not musim:
        df3 = df2.copy()
    else:
        df3 = df2[df2['season'].isin(musim)]
        
    #untuk kodisi cuaca
    cuaca = st.sidebar.multiselect("Pilih Kondisi Cuaca", df3['weathersit'].unique())
    if not cuaca:
        df4 = df3.copy()
    else:
        df4 = df3[df3['weathersit'].isin(cuaca)]
       
    #untuk hari
    hari = st.sidebar.multiselect("Pilih Hari", df4['weekday'].unique())
    if not hari:
        filter_df = df4.copy()
    else:
        filter_df = df4[df4['weekday'].isin(hari)]
        
    #gruping data
    #berdasarkan musim
    keadan_musim = filter_df.groupby(by='season', as_index=False)["cnt"].sum()
    #berdasarkan bulan
    keadan_bulan = filter_df.groupby(by='mnth', as_index=False)["cnt"].sum()
    #berdasarkan cuaca
    data_cuaca = filter_df.groupby(by='weathersit', as_index=False)["cnt"].sum()
    
    st.subheader("penyewaan Berdasarkan Musim")
    col3, col4 = st.columns((2))
    with col3:
        fig = px.bar (keadan_musim, x='season', y="cnt",
                      text_auto='.2s',
                      title="Total Penyewaan per Musim",
                      template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
     
    with col4:
         fig = px.pie(keadan_musim, values="cnt", names="season",
                      hole=0.5,
                      title="Kontribusi Penyawaan Per Musim")
         fig.update_traces(textinfo='percent+label')
         st.plotly_chart(fig, use_container_width=True)
         
    st.subheader("Tren Penyewaan Harian")
    line_data = filter_df.groupby(by='dteday', as_index=False)["cnt"].sum()
    
    fig2 = px.line(line_data, x='dteday', y="cnt",
                   title="Jumlah Penyewaan Sepeda",
                   markers=True,
                   template="gridon")
    fig2.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")
    fig3 = px.bar(data_cuaca, x='weathersit', y='cnt',
                  color='weathersit',title="Rata-rata Sewa per Kondisi Cuaca")
    st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("Hierarki Penyewaan: Musim & Hari Kerja")
    fig4 = px.sunburst(filter_df, path=['season', 'workingday'], values="cnt",
                       color='season', title="Distribusi Sewa: Musim > Status Hari",
                       height=700)
    st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Data Sudah Terfilter")
    with st.expander("Klik Untuk melihat detail data"):
        st.dataframe(filter_df)
        csv = filter_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Unduh Data Sebagai CSV",
            data=csv,
            file_name='data_sepeda_filter.csv',
            mime='text/csv'
        )
        
    # ANALISIS PERTANYAAN BISNIS 
    st.markdown("---")
    st.header("Analisis & Jawaban Pertanyaan Bisnis")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Q1: Aktivitas Penyewaan", 
        "Q2: Pola Hari Kerja Berdasarkan Musim", 
        "Q3: Promosi Strategis Penyewaan Sepeda", 
        "Q4: Optimal stok pada setiap musim", 
        "Q5: Member vs Casual"
    ])
    
    with tab1:
        st.subheader("Pertanyaan 1: Aktivitas Penyewaan Berdasarkan Kondisi Cuaca (M Arvian Nazmy)")
        st.info("**Pertanyaan:**  Pada kondisi apa pengguna paling aktif menyewa sepeda, dan kapan permintaan paling rendah terjadi? ")
        
        #gruping data
        stok_analisis = filter_df.groupby(['season','workingday'])["cnt"].mean().reset_index()
        
         # membuat grafik
        kondisi_avg = (
        filter_df.groupby("weathersit")["cnt"]
        .mean()
        .reset_index()
        .sort_values("cnt", ascending=False)
    )

    fig_q1 = px.bar(
        kondisi_avg,
        x="weathersit",
        y="cnt",
        color="weathersit",
        text_auto=".0f",
        title="Rata-rata Penyewaan Sepeda per Kondisi Cuaca",
        labels={
            "cnt": "Rata-rata Penyewaan",
            "weathersit": "Kondisi Cuaca"
        }
    )

    st.plotly_chart(fig_q1, use_container_width=True)
    
    #penjelasan
    st.write("""
    **Penjelasan :**
    Pengguna paling aktif menyewa sepeda saat cuaca cerah dan musim hangat (sekitar pertengahan tahun) serta pada hari kerja, karena kondisi tersebut mendukung aktivitas luar ruangan dan mobilitas. Sebaliknya, permintaan paling rendah terjadi saat cuaca buruk seperti hujan/kabut dan pada awal tahun atau musim dingin, ketika orang cenderung mengurangi penggunaan sepeda.
    """)
    
    st.success(""" 
    **Kesimpulan :**
    Permintaan penyewaan sepeda sangat dipengaruhi oleh kondisi cuaca dan musim. Penggunaan paling tinggi terjadi saat cuaca cerah dan suhu nyaman di pertengahan tahun, sedangkan permintaan menurun saat cuaca buruk dan pada periode musim awal tahun. Artinya, semakin mendukung kondisi lingkungan untuk aktivitas luar, semakin tinggi tingkat penyewaan sepeda.

    """)
    
    with tab2:
        st.subheader("Pertanyaan 2: Pola Hari Kerja Berdasarkan Musim (Muhamad Naufal Ikbar)")
        st.info("**Pertanyaan:** Bagaimana kombinasi faktor musim dan hari kerja mempengaruhi jumlah sepeda yang harus disediakan?")
        
        #gruping data
        stok_analisis = filter_df.groupby(['season','workingday'])["cnt"].mean().reset_index()
        
        #membuat grafik
        fig_q2 = px.bar(stok_analisis, x="season", y="cnt",
                        color="workingday",barmode="group",
                        labels={"cnt": "Rata-rata Sewa", "season": "Musim", "workingday": "Tipe Hari"},
                        title="Rata-rata Penyewaan: Musim vs Tipe Hari",
                        color_discrete_map={'Workday': '#636EFA', 'Holiday/Weekend': '#EF553B'})
        st.plotly_chart(fig_q2, use_container_width=True)
        #penjelasan
        st.write("""
        **Analisis Visual:**
        - Jika batang pink (Workday) lebih tinggi, berarti stok harus difokuskan untuk komuter.
        - Jika batang merah (Holiday) naik, berarti stok harus dialihkan ke area wisata.
        """)
        
        st.success("""
        **Kesimpulan Strategi:**
        Strategi paling optimal adalah menjaga **persediaan tertinggi pada hari kerja di Musim Gugur/Panas** dan berada di level terendah pada akhir pekan di Musim Semi.
        """)
        
    with tab3:
        st.subheader("Pertanyaan 3: Promosi Strategis Penyewaan Sepeda (Rifqi Andana)")
        st.info("**Pertanyaan:** Berdasarkan hasil analisis di atas, rekomendasi strategis apa yang dapat diberikan kepada operator layanan penyewaan sepeda (misalnya, mengenai strategi promosi untuk hari/musim tertentu atau pengguna tertentu) untuk meningkatkan jumlah total sewa?")

        # Rata-rata untuk melihat tren perilaku umum
        user_type_analysis = filter_df.groupby(['season', 'workingday'])[['casual', 'registered']].mean().reset_index()

        #Melt data agar cocok untuk grafik bar yang membandingkan tipe user
        user_type_melted = user_type_analysis.melt (
            id_vars = ['season', 'workingday'],
            value_vars = ['casual', 'registered'], 
            var_name = 'user_type',
            value_name = 'avg_rentals'
        )
        # Visualisasi : Perbandingan perilaku casual vs registered
        fig_promo = px.bar(
            user_type_melted,
            x= "season",
            y= "avg_rentals", 
            color = "user_type",
            barmode = "group",
            facet_col = "workingday",
            labels = {
                "avg_rentals" : "Rata-rata Sewa", 
                "season" : "Musim", 
                "user_type" : "Tipe Pengguna"
                },
            title = "Pola Sewa : casual vs registered (Berdasarkan & Hari)",
            color_discrete_map = {'casual' : '#FFA15A', 'registered' : '#19D3AF'},
            category_orders = {"season" : ["Spring", "Summer", "Fall", "Winter"]}
        ) 

        fig_promo.update_layout(margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig_promo, use_container_width=True)

        #Penjelasan 
        st.markdown("""
        ### Rekomendasi Strategis:

         **1.) Strategi Promosi 'casual' (Target: Turis/Rekreasi):**
             Karena pengguna casual melonjak drastis di Weekend/Holiday (terutama Musim Panas & Gugur), berikan promo 'Weekend Pass' atau diskon bundling keluarga di lokasi wisata.
                    
         **2.)Strategi Loyalitas 'registered' (Target: Komuter):**
             Pengguna registered sangat stabil di Working Day. Fokuskan pada program subscription bulanan dengan harga khusus untuk rute perkantoran.
                    
         **3.) Antisipasi 'Low Season' (Musim Dingin):**
             Saat penyewaan turun di Musim Dingin, lakukan maintenance besar-besaran atau berikan promo 'Winter Challenge' dengan poin reward ganda untuk menjaga keterikatan pengguna.
        """)

        st.success("""
        **Kesimpulan Utama:** Tingkatkan anggaran pemasaran digital pada akhir pekan di Musim Gugur untuk menjaring pengguna kasual, dan perkuat kemitraan korporat untuk menjaga volume pengguna terdaftar di hari kerja.
        """)
        
    with tab4:
        st.subheader("Pertanyaan 4: Optimal stok pada setiap musim (Dimas Munawar)")
        st.info("**Pertanyaan:** Berapa jumlah sepeda optimal yang harus tersedia tiap musim/hari berdasarkan pola permintaan historis?")

        # Visualisasi Pola Permintaan Berdasarkan Musim
        fig1 = px.box(
            filter_df, 
            x='season', 
            y='cnt', #gruping data
            color='season', 
            category_orders={'season': ['Spring', 'Summer', 'Fall', 'Winter']},
            title='<b>Distribusi Jumlah Total Penyewaan Sepeda (cnt) per Musim</b>',
            labels={'season': 'Musim', 'cnt': 'Jumlah Total Penyewaan'},
            points="outliers",
            template='plotly_white' 
        )

        fig1.update_layout(
            showlegend=False,
            xaxis_title="Musim",
            yaxis_title="Jumlah Total Penyewaan",
            yaxis=dict(
                showgrid=True, 
                gridcolor='LightGray', 
                gridwidth=1, 
                griddash='dash'
            )
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Penjelasan analisis
        st.write("""
        **Analisis Visual:**
        
        1.) Musim Puncak (Optimal Tertinggi): Permintaan tertinggi terjadi pada Fall (Musim Gugur), Summer (Musim Panas), diikuti oleh Winter (Musim Dingin). 
            Ini adalah periode kritis di mana stok sepeda harus dimaksimalkan untuk menghindari stock-out.
            Rata-rata harian penyewaan pada musim Fall (sekitar 5644 sepeda/hari), musim Summer (sekitar 4992 sepeda/hari), dan musim Winter(sekitar 4721 sepeda/hari).

        2.) Musim Rendah (Optimal Terendah): Permintaan terendah terjadi pada musim Spring (Musim Semi) dengan variabilitas yang lebih kecil.
            Stok sepeda dapat dikurangi pada periode ini, tetapi harus tetap di atas kuartil pertama untuk mengakomodasi lonjakan mendadak.
            Rata-rata harian penyewaan pada musim Spring (sekitar 2604 sepeda/hari).
        """)

        st.success("""
        **Kesimpulan Strategi:**
        Untuk menjamin ketersediaan stok, penyedia layanan harus menempatkan unit sepeda paling banyak pada Musim Puncak. Agar dapat mengurangi efisiensi biaya perawatan, stok pada musim Rendah dikurangi.
        """)
    
    with tab5:
        st.subheader("Pertanyaan 5: Segmentasi Pengguna (Sonjaya Baruna)")
        #tambah tuh yang pertanyaan 5
        pass
    
else:
    st.info("Silakan unggah file CSV Anda untuk memulai analisis.")
    
