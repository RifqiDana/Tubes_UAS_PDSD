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
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'jun', 
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

    sns.histplot(data["cnt"], kde=True)
    plt.title("Distribusi Jumlah Penyewaan Sepeda (cnt)")
    plt.show()

file = st.file_uploader('Unggah File CSV',type='csv')

if file is not None :
    data = pd.read_csv(file)
    st.write('Isi Dari DataFrame Adalah : ')
    st.dataframe(data)



 