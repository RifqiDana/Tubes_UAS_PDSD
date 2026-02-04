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
        "Q1: Keamanan Cuaca", 
        "Q2: Stok Optimal", 
        "Q3: Tren Pertumbuhan", 
        "Q4: Pola Hari Kerja", 
        "Q5: Member vs Casual"
    ])
    
    with tab1:
        st.subheader("Pertanyaan 1: Keamanan & Cuaca (M Arvian Nazmy)")
        #ikutin kaya pertanyaan 2 cara pengetikannya
    
    with tab2:
        st.subheader("Pertanyaan 2: Stok Sepeda Optimal (Muhamad Naufal Ikbar)")
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
        - Jika batang biru (Workday) lebih tinggi, berarti stok harus difokuskan untuk komuter.
        - Jika batang merah (Holiday) naik, berarti stok harus dialihkan ke area wisata.
        """)
        
        st.success("""
        **Kesimpulan Strategi:**
        Strategi paling optimal adalah menjaga **persediaan tertinggi pada hari kerja di Musim Gugur/Panas** dan berada di level terendah pada akhir pekan di Musim Semi.
        """)
        
    with tab3:
        st.subheader("Pertanyaan 3: Tren Pertumbuhan (Rifqi Andana)")
        #ikutin kaya pertanyaan 2 cara pengetikannya
        pass
    
    with tab4:
        st.subheader("Pertanyaan 4: Pola Hari Kerja (Dimas Munawar)")
        #ikutin kaya pertanyaan 2 cara pengetikannya
        pass
    
    with tab5:
        st.subheader("Pertanyaan 5: Segmentasi Pengguna (Sonjaya Baruna)")
        #tambah tuh yang pertanyaan 5
        pass
    
else:
    st.info("Silakan unggah file CSV Anda untuk memulai analisis.")
    
