import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import altair as alt
from numerize import numerize

st.set_page_config(page_title="Analisis SPMB STIS 2020 - Wahyu",
                   layout="wide")

sns.set(style='dark')
# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe


# Load cleaned data
df_eda = pd.read_csv("df_keseluruhan.csv")

# Filter data
df_eda_01 = df_eda.copy()
df_eda_01['hasil.akhir_x'].replace({"Tidak Lulus":0, "Lulus":1, np.NaN:0}, inplace=True)
df_eda_01['skd.keterangan'].replace({"P/L":1, "P":0, "TL":0, "TH":0, "PA/L":0}, inplace=True)
df_eda_01['t2.keterangan'].replace({"P/L":1, "P":0, "TL":0}, inplace=True)

# metrics data
keketatan = df_eda_01[df_eda_01["hasil.akhir_x"]==1].count()/df_eda_01[df_eda_01["hasil.akhir_x"]==0].count()*100
pg_skd = df_eda_01[df_eda_01['hasil.akhir_x']==1].groupby('lokasi.formasi').agg(
    nilai_min_skd = ('skd.nilai','min'),
    nilai_max_skd = ('skd.nilai','max'),
    nilai_rerata_skd = ('skd.nilai','mean')
)
pg_mtk = df_eda_01[df_eda_01['hasil.akhir_x']==1].groupby('lokasi.formasi').agg(
    nilai_min_mtk = ('mtk.nilai','min'),
    nilai_max_mtk = ('mtk.nilai','max'),
    nilai_rerata_mtk = ('mtk.nilai','mean')
)

# START HERE
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.svg")

    st.markdown('<div style="text-align:center">Wahyu Dwi Prasetio</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center">wdprsto@gmail.com</div>', unsafe_allow_html=True)
    


"# Analisis Hasil Seleksi Penerimaan Mahasiswa Baru Politeknik Statistika STIS Tahun 2022"
"oleh Wahyu Dwi Prasetio"
"---"

"Perguruan tinggi kedinasan (PTK) merupakan salah satu tujuan siswa SMA dalam melanjutkan pendidikannya. Pemilihan perguruan tinggi kedinasan sebagai pendidikan lanjutan didasari pada keuntungan yang diberikan oleh instansi tersebut, mulai dari biaya pendidikan yang gratis sampai jaminan menjadi Aparatur Sipil Negara (ASN) ketika lulus nanti. Salah satu perguruan tinggi kedinasan yang menawarkan keuntungan tersebut adalah Politeknik Statistika STIS."

"Politeknik Statistika STIS merupakan perguruan tinggi kedinasan di bawah Badan Pusat Statistik (BPS). Berdasarkan rilis Badan Kepegawaian Negara (BKN), jumlah pendaftar di Polstat STIS pada tahun 2023 menduduki urutan ke-3 sebanyak 18.261 orang. Angka ini juga diikuti dengan masifnya jumlah pendaftar di tahun 2023. BKN dalam unggahannya di bulan April menunjukkan jumlah pendaftar di Polstat STIS menduduki peringkat kedua dengan total 12441 pendaftar. Dengan total penerimaan hanya 500 peserta (keketatan 4.167%), peserta seleksi penerimaan mahasiswa baru haru menganalisis kondisi dan berstrategi agar peluang ia diterima lebih besar."

"---"

"## Fakta & Data"
"- Kuota penerimaan yang sangat sedikit dibandingkan dengan jumlah pendaftar. Keketatan sekolah kedinasan ini mencapai 2.87%, atau 1 banding 34 orang."

cola1, cola2 = st.columns(2)
with cola1:
    # sales_cat1 = alt.Chart(df_eda).mark_bar().encode(alt.X('hasil.akhir_x', title="Status", axis=alt.Axis(labelAngle=0)), alt.Y('hasil.akhir_x', title="Pendaftar", aggregate="count")
    #                                                         )

    # st.altair_chart(sales_cat1, use_container_width=True)
    fig = plt.figure(figsize=(6, 4))
    ax=sns.countplot(data = df_eda, x = "hasil.akhir_x")
    ax.set(xlabel='Hasil Akhir', ylabel='Jumlah')
    st.pyplot(fig)

with cola2:
    st.metric(label="Keketatan",
            value=f"{numerize.numerize(keketatan['hasil.akhir_x'])}%"
            )

"- Passing grade SKD dan Matematika yang tinggi agar dapat lolos ke tahap selanjutnya "

colc1, colc2 = st.columns(2)

with colc1:
    st.dataframe(pg_skd)

with colc2:
    st.dataframe(pg_mtk)

"- Adanya kuota formasi per Provinsi yang diatur oleh BPS"

"---"

colc1, colc2 = st.columns([4,1])

with colc1:
    fig = plt.figure(figsize=(6, 4))
    ax = sns.countplot(data=df_eda, y='nama.pendidikan')
    ax.set(xlabel='Jumlah Pendaftar', ylabel='Tingkat Pendidikan')
    st.pyplot(fig)

with colc2:
    st.markdown('<div style="font-size:40px;font-weight:bold;">Lantas?</div>', unsafe_allow_html=True)
    st.markdown('Dapatkan peserta berpegang kepada nilai SKD atau Matematika sebagai penentu kelulusan mereka?')

"---"
