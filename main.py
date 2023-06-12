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

num_col = ['skd.nilai', 'mtk.nilai', 'hasil.akhir_x']
korelasi = df_eda_01[num_col].corr()

# START HERE
with st.sidebar:
    # Menambahkan logo perusahaan
    # st.image("https://stis.ac.id/media/source/up.png", width=150)
    st.markdown('<img style="text-align:center;max-width:100%;padding-bottom:32px" src="https://stis.ac.id/media/source/up.png">', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center">Wahyu Dwi Prasetio</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;padding-bottom:32px">wdprsto@gmail.com</div>', unsafe_allow_html=True)

    pilihan_lokasi = st.selectbox(
        "Pilih Lokasi Anda",
        ['Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi',
        'Sumatera Selatan', 'Bengkulu', 'Lampung',
        'Kepulauan Bangka Belitung', 'Kepulauan Riau',
        'Nusa Tenggara Timur', 'Nusa Tenggara Barat', 'Kalimantan Barat',
        'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur',
        'Kalimantan Utara', 'Sulawesi Utara', 'Sulawesi Tengah',
        'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo',
        'Sulawesi Barat', 'Maluku', 'Maluku Utara', 'Papua Barat', 'Papua',
        'D I Yogyakarta', 'Banten', 'Bali', 'Papua Barat (Afirmasi)',
        'Papua (Afirmasi)', 'Pusat', 'DKI Jakarta', 'Jawa Barat',
        'Jawa Tengah', 'Jawa Timur']
    )
    


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

colb1, colb2 = st.columns(2)

with colb1:
    st.dataframe(pg_skd)

with colb2:
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

"## Infografis"

cold1, cold2 = st.columns(2)

with cold1:
    pass

with cold2:
    pass

"---"

"## Analisis Korelasi"

"Plot korelasi terhadap variabel SKD, Matematika, dan Hasil Akhir menunjukkan bahwa SKD memiliki korelas yang lemah dengan hasil seleksi penerimaan. Di sisi lain, diketahui bahwa nilai Matematika memiliki korelasi yang sedang dengan hasil seleksi penerimaan."

cole1, cole2 = st.columns(2)

with cole1:
    "### Korelasi di "+pilihan_lokasi
    korelasi_prov = df_eda_01[df_eda_01['lokasi.formasi']==pilihan_lokasi][num_col].corr()
    fig = plt.figure(figsize=(6, 5))
    ax = sns.heatmap(korelasi_prov, annot=True, fmt=".2f");
    st.pyplot(fig)

with cole2:
    "### Korelasi Secara Nasional"
    fig = plt.figure(figsize=(6, 5))
    ax = sns.heatmap(korelasi, annot=True, fmt=".2f");
    st.pyplot(fig)

"---"

"## Rekomendasi"
"- Peserta seleksi penerimaan mahasiswa baru Polstat STIS hendaknya memaksimalkan nilai tes Matematika mereka di tahap 2 agar tingkat kelulusannya makin tinggi. Agar dapat lulus ke tahap 2, mereka setidaknya perlu memenuhi kriteria nilai lulus minimal SKD di masing-masing daerah."
"- Setelah lolos ke tahap 2 dan mendapatkan nilai tes Matematika yang maksimal, peserta seleksi hanya perlu memastikan bahwa dirinya mampu memenuhi kriteria minimal untuk tes Psikologi dan tes Kesehatan & Kebugaran agar diterima di Polstat STIS."

"---"

"## Sumber Data"
"Data diperoleh dari hasil resmi seleksi SPMB STIS yang tersedia di portal [SPMB STIS](https://spmb.stis.ac.id/site/pengumuman) tahun 2022 dan dapat diakses pada pranala berikut:"
"*   [Tahap 1 - Pengumuman Hasil SKD](https://drive.google.com/file/d/16UszKsdZWdAwBU87AizDSxVZr1WmDIa3/view)"
"*   [Tahap 2 - Pengumuman Hasil MTK](https://drive.google.com/file/d/17BJnUrBT1G8e47BUDjSF6XmW4b4Xoeh5/view)"
"*   [Tahap 3 - Pengumuman Hasil TKK](https://drive.google.com/file/d/1z0XXPWVxszq4KWVnzv-LHItQBPZaauMj/view)"
"*   [Tahap 4 - Kelulusan Cadangan](https://drive.google.com/file/d/1IHmZppCAR-lOD543KRJHAThJCiKdPBTy/view)"