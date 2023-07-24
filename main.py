import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from numerize import numerize
from helper import set_bar_pcnt, rainbow_text
from matplotlib import transforms
from matplotlib.lines import Line2D

st.set_page_config(page_title="Analisis SPMB STIS 2022 - Wahyu",
                   page_icon="📈",
                   layout="wide")
# sns.set(style='dark')

# fungsi styling

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
# define colors
GRAY1, GRAY2, GRAY3 = '#231F20', '#414040', '#555655'
GRAY4, GRAY5, GRAY6 = '#646369', '#76787B', '#828282'
GRAY7, GRAY8, GRAY9 = '#929497', '#A6A6A5', '#BFBEBE'
BLUE1, BLUE2, BLUE3, BLUE4 = '#174A7E', '#4A81BF', '#94B2D7', '#94AFC5'
BLUE5, BLUE6 = '#92CDDD', '#2E869D'
RED1, RED2, RED3 = '#C3514E', '#E6BAB7', '#DFDEDE'
GREEN1, GREEN2 = '#0C8040', '#9ABB59'
ORANGE1, ORANGE2, ORANGE3 = '#F79747', '#FAC090', '#F36721'
TURQ1, TURQ2, TURQ3 = "#31859C", "#4bacc6", "#28728a"

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
).reset_index()
pg_mtk = df_eda_01[df_eda_01['hasil.akhir_x']==1].groupby('lokasi.formasi').agg(
    nilai_min_mtk = ('mtk.nilai','min'),
    nilai_max_mtk = ('mtk.nilai','max'),
    nilai_rerata_mtk = ('mtk.nilai','mean')
).reset_index()

num_col = ['skd.nilai', 'mtk.nilai', 'hasil.akhir_x']
korelasi = df_eda_01[num_col].corr()

# START HERE
"# Analisis Hasil Seleksi Penerimaan Mahasiswa Baru Politeknik Statistika STIS Tahun 2022"
"Politeknik Statistika STIS sebagai perguruan tinggi kedinasan di bawah Badan Pusat Statistik (BPS) menduduki urutan ke-3 jumlah pendaftar terbanyak dengan total 18.261 orang. Dengan total penerimaan hanya 500 orang (keketatan 4.167%), peserta seleksi harus menganalisis kondisi dan merancang strategi agar peluang diterima jauh lebih besar."
"---"

"## Fakta & Data"
"- Kuota penerimaan yang sangat sedikit. Keketatan mencapai 1 banding 34 orang."

cola1, cola2 = st.columns(2)
with cola1:
    label = df_eda_01['hasil.akhir_x'].value_counts()

    fig, ax1 = plt.subplots(figsize=(7.45, 3.5), dpi=110)
    fig.subplots_adjust(left=0.154, right=0.77, top=0.89, bottom=0.1)
    bars = plt.bar([0, 1], [label[0], label[1]],
                color=[BLUE5, BLUE1],
                linewidth=0.5,
                width=0.55)
    ax1.tick_params(bottom=False, left=False, labelleft=False, labelbottom='on')

    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    plt.xticks([0, 1], ['Tidak Lolos', 'Lolos'])
    ax1.spines['bottom'].set_color(GRAY9)
    for item in ax1.get_xticklabels():
        item.set_fontsize(12)
        item.set_color(GRAY4)

    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + 0.2,
                bar.get_height() + (-1500, 500)[i==1],
                label[i],
                fontsize=12,
                color=('white','black')[i==1])

    # title the plot
    fig.text(0.18, 0.9, 'Hasil Seleksi Penerimaan', color=GRAY3,
            fontsize=12)
    # ax1.text(-0.35, 46, 'Tarif pajak maksimum', fontsize=14, color=GRAY7)
    # ax1.axvline(0.31, ymin=0.05, ymax=0.8, color=BLUE1, linewidth=1.2)
    # ax1.axvline(1.3, ymin=0.05, ymax=0.89, color=BLUE1, linewidth=1.2)
    st.pyplot(fig,
                use_container_width=True)

with cola2:
    fig2, ax2 = plt.subplots(figsize=(7.45, 4.9), # width, height in inches
                            dpi=110)
    ax2.text(0, 1,
            f"{numerize.numerize(keketatan['hasil.akhir_x'])}%",
            verticalalignment='top', horizontalalignment='left',
            color=TURQ3, fontsize=42, fontweight = 'bold')
    
    rainbow_text(
    0, 0.78,
    'Keketatan||        Seleksi Penerimaan STIS',
    colors=[
        [TURQ3, GRAY1]], 
        ax=ax2,
    fontsize=14, spacing=140)

    ax2.axis('off');
    st.pyplot(fig2,
                use_container_width=True)

"- Passing grade SKD dan Matematika yang tinggi agar dapat lolos ke tahap selanjutnya "

colb1, colb2 = st.columns(2)

with colb1:
    st.dataframe(pg_skd,
                 column_config={
                    "lokasi.formasi": "Lokasi Formasi",
                    "nilai_min_skd": "Minimum SKD",
                    "nilai_max_skd": "Maksimum SKD",
                    "nilai_rerata_skd": "Rerata SKD",
                    # "stars": st.column_config.NumberColumn(
                    #     "Github Stars",
                    #     help="Number of stars on GitHub",
                    #     format="%d ⭐",
                    # ),
                    # "url": st.column_config.LinkColumn("App URL"),
                    # "views_history": st.column_config.LineChartColumn(
                    #     "Views (past 30 days)", y_min=0, y_max=5000
                    # ),
                },
                hide_index=True,
                use_container_width=True
            )

with colb2:
    st.dataframe(pg_mtk,                 
                 column_config={
                    "lokasi.formasi": "Lokasi Formasi",
                    "nilai_min_mtk": "Minimum MTK",
                    "nilai_max_mtk": "Maksimum MTK",
                    "nilai_rerata_mtk": "Rerata MTK",
                },
                hide_index=True,
                use_container_width=True
                 )

"- Adanya kuota formasi per Provinsi yang diatur oleh BPS"

"---"

colc1, colc2 = st.columns([3,2])

with colc1:
    label = df_eda['nama.pendidikan'].value_counts()
    fig, ax1 = plt.subplots(figsize=(7, 2.65), # width, height in inches
                        dpi=110)           # resolution of the figure
    ax1.invert_yaxis()
    # tune the subplot layout by setting sides of the figure
    fig.subplots_adjust(left=0.445, right=0.765, top=0.77, bottom=0.01)

    # draw horizontal colored bars
    bars = ax1.barh(range(len(label)),
                    label.tolist(),
                    height=0.65,
                    color=[BLUE2] + [BLUE3] + [BLUE4]*3)
    
    # set properties for axes object (ticks for all issues with labels)
    plt.setp(ax1, yticks=np.arange(len(label)), yticklabels=['SMA IPA', 'MA IPA', 'SMA IPS',
       'SMK TIK', 'MA IPS'])

    # change the appearance of ticks, tick labels, and gridlines
    ax1.tick_params(bottom='off', left='off', labelbottom='off')

    # configure y tick label appearance
    for item in ax1.get_yticklabels():
        item.set_fontsize(7)
        item.set_color(GRAY3)

        offset = transforms.ScaledTranslation(3, 0, fig.dpi_scale_trans)
        item.set_transform(item.get_transform() + offset)

    
    # add numerical data labels for each bar
    for i, b in enumerate(bars):
        plt.text(b.get_width()+(300,-300)[i==0], b.get_y() + b.get_height()*0.6,
                str(label.tolist()[i]),
                fontsize=6,
                color=('black','white')[i==0],
                horizontalalignment=('left','right')[i==0])
    
    # remove chart border
    for spine in ax1.spines.values():
        spine.set_visible(False)

    # remove x tick
    ax1.tick_params(axis='both', which='both', length=0, labelbottom=False)

    ax1.text(-3500, -1, 'Sebaran Pendidikan Peserta', fontsize=10, color=GRAY1)

    st.pyplot(fig,
              use_container_width=True)

with colc2:
    st.markdown('<div style="font-size:40px;font-weight:bold;">Lantas?</div>', unsafe_allow_html=True)
    st.markdown('Dapatkah peserta berpegang kepada nilai SKD atau Matematika sebagai penentu kelulusan mereka?')

"---"

"## Infografis SPMB STIS di Indonesia"

cold11, cold21 = st.columns(2)

with cold11:
    "### ⠀"
    diterima = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)].count()
    ditolak = df_eda_01[(df_eda_01["hasil.akhir_x"]==0)].count() 
    keketatan = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)].count()/df_eda_01[(df_eda_01["hasil.akhir_x"]==0)].count()*100

    diterima_lk = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)&(df_eda_01['jk']=="Lk")].count()
    diterima_pr = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)&(df_eda_01['jk']=="Pr")].count()
    
    cold110, cold111 = st.columns(2)

    with cold110:
        st.metric(label="Tidak Diterima",
        value=f"{ditolak[0]}"
        )

        st.metric(label="Keketatan Nasional",
        value=f"{numerize.numerize(keketatan['hasil.akhir_x'])}%"
        )

    with cold111:
        st.metric(label="Diterima",
        value=f"{diterima[0]}"
        )

        st.metric(label="Diterima Lk",
        value=f"{diterima_lk[0]}"
        )

        st.metric(label="Diterima Pr",
        value=f"{diterima_pr[0]}"
        )
    
    "Latar Belakang Pendidikan Peserta yang Lulus"
    st.dataframe(
        df_eda[df_eda['hasil.akhir_x']=='Lulus']['nama.pendidikan'].value_counts().reset_index(),
        column_config={
            "index": "Tingkat Pendidikan",
            "nama.pendidikan": "Jumlah Lulusan",
        },
        hide_index=True,
        use_container_width=True
                 
        )



with cold21:
    "### Distribusi Nilai SKD Nasional"
    fig = plt.figure(figsize=(6, 5))
    ax = sns.kdeplot(df_eda_01, x='skd.nilai', hue="hasil.akhir_x",)

    ax.set(xlabel='', ylabel='')
    ax.lines[0].set_color(BLUE2)
    ax.lines[1].set_color(GRAY9)

    ytick_labs = np.arange(0, ax.lines[1].get_ydata().max()+0.001, 0.001)

    plt.setp(ax,
         yticks=ytick_labs,
         yticklabels=[f"{round(y*100,2)}%" for y in ytick_labs]
         )
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRAY5)
    ax.spines['bottom'].set_color(GRAY5)
    
    legend_elements = [Line2D([0], [0], color=GRAY9, lw=3, label='Tidak Lulus'),
                       Line2D([0], [0], color=BLUE2, lw=3, label='Lulus',
                              markerfacecolor='g', markersize=15),
                    ]
    ax.legend(handles=legend_elements, loc='upper left')

    for item in ax.get_xticklabels():
        item.set_color(GRAY3)
    for item in ax.get_yticklabels():
        item.set_color(GRAY3)
    
    st.pyplot(fig)

    "Peserta yang lulus cenderung memiliki nilai SKD yang lebih tinggi dibandingkan dengan yang tidak lolos. Hal ini terlihat dari puncak orange berada di sebelah kanan dari distribusi grafik biru."


cold12, cold22 = st.columns(2)

with cold12:
    "### Korelasi Secara Nasional"
    fig = plt.figure(figsize=(5, 5))
    ax = sns.heatmap(korelasi, 
                     annot=True, 
                     fmt=".2f",
                    yticklabels=['Nilai SKD','Nilai MTK', 'Hasil'],
                    xticklabels=['Nilai SKD','Nilai MTK', 'Hasil'],
                    cmap="Blues");
    ax.collections[0].colorbar.remove()
    st.pyplot(fig)

    "Plot korelasi terhadap atribut SKD, Matematika, dan Hasil Akhir menunjukkan bahwa SKD memiliki korelasi yang lemah dengan atribut Hasil Seleksi. Di sisi lain, ditemukan bahwa tes Matematika memiliki korelasi yang sedang dengan Hasil Seleksi."

with cold22:
    "### Distribusi Nilai MTK Nasional"
    fig = plt.figure(figsize=(6,5))
    ax = sns.kdeplot(df_eda_01, x='mtk.nilai', hue="hasil.akhir_x")
    
    ax.set(xlabel='', ylabel='')
    ax.lines[0].set_color(BLUE2)
    ax.lines[1].set_color(GRAY9)

    ytick_labs = np.arange(0, ax.lines[1].get_ydata().max()+0.001, 0.001)

    plt.setp(ax,
         yticks=ytick_labs,
         yticklabels=[f"{round(y*100,2)}%" for y in ytick_labs]
         )
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRAY5)
    ax.spines['bottom'].set_color(GRAY5)
    
    legend_elements = [Line2D([0], [0], color=GRAY9, lw=3, label='Tidak Lulus'),
                       Line2D([0], [0], color=BLUE2, lw=3, label='Lulus',
                              markerfacecolor='g', markersize=15),
                    ]
    ax.legend(handles=legend_elements, loc='upper left')

    for item in ax.get_xticklabels():
        item.set_color(GRAY3)
    for item in ax.get_yticklabels():
        item.set_color(GRAY3)
    
    st.pyplot(fig)

    "Peserta yang lulus memiliki nilai tes Matematika yang lebih besar dibandingkan dengan yang tidak lolos. Hal ini terlihat dari puncak orange berada di sebelah kanan dari distribusi grafik biru. Perbedaan nilai yang paling sering muncul ini bahkan menyentuh angka 50 poin."

"---"

w11, w12 = st.columns([1,2])
with w11:
    "Pilih lokasi anda"
with w12:
    pilihan_lokasi = st.selectbox(
        "Provinsi",
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
    
f"## Analisis di {pilihan_lokasi}"

"Analisis terhadap data tahun 2022 dapat membantu peserta dalam menetapkan strategi untuk meraih nilai terbaik dalam tes SKD dan Matematika. Dengan mengejar target nilai yang sesuai, kemungkinan diterimanya peserta dalam SPMB STIS akan meningkat. Adapun komponen yang dapat dilihat meliputi distribusi nilai SKD dan MTK dari peserta yang lulus dari daerah yang sama di tahun 2022."

cold10, cold20 = st.columns(2)

with cold10:
    "### Jumlah Peserta Lulus"

    label = df_eda_01[df_eda_01['lokasi.formasi']==pilihan_lokasi]['hasil.akhir_x'].value_counts()

    fig, ax1 = plt.subplots(figsize=(7.45, 3.5), dpi=110)
    fig.subplots_adjust(left=0.154, right=0.77, top=0.89, bottom=0.1)
    bars = plt.bar([0, 1], [label[0], label[1]],
                color=[BLUE5, BLUE1],
                linewidth=0.5,
                width=0.55)
    ax1.tick_params(bottom=False, left=False, labelleft=False, labelbottom=True)

    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    plt.xticks([0, 1], ['Tidak Diterima', 'Diterima'])
    ax1.spines['bottom'].set_color(GRAY9)
    for item in ax1.get_xticklabels():
        item.set_fontsize(12)
        item.set_color(GRAY4)

    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + 0.2,
                bar.get_height()+(-10,10)[i==1],
                label[i],
                fontsize=12,
                verticalalignment=('top','bottom')[i==1],
                color=('white','black')[i==1])

    st.pyplot(fig,
                use_container_width=True)


with cold20:
    "### ⠀"
    diterima_prov = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)&(df_eda_01['lokasi.formasi']==pilihan_lokasi)].count()
    ditolak_prov = df_eda_01[(df_eda_01["hasil.akhir_x"]==0)&(df_eda_01['lokasi.formasi']==pilihan_lokasi)].count() 
    keketatan_prov = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)&(df_eda_01['lokasi.formasi']==pilihan_lokasi)].count()/df_eda_01[(df_eda_01["hasil.akhir_x"]==0)&(df_eda_01['lokasi.formasi']==pilihan_lokasi)].count()*100

    diterima_prov_lk = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)&(df_eda_01['lokasi.formasi']==pilihan_lokasi)&(df_eda_01['jk']=="Lk")].count()
    diterima_prov_pr = df_eda_01[(df_eda_01["hasil.akhir_x"]==1)&(df_eda_01['lokasi.formasi']==pilihan_lokasi)&(df_eda_01['jk']=="Pr")].count()
    
    cold100, cold101 = st.columns(2)

    with cold100:
        st.metric(label="Keketatan Provinsi",
        value=f"{numerize.numerize(keketatan_prov['hasil.akhir_x'])}%"
        )

    with cold101:
        st.metric(label="Diterima Lk",
        value=f"{diterima_prov_lk[0]}"
        )

        st.metric(label="Diterima Pr",
        value=f"{diterima_prov_pr[0]}"
        )



        

cole11, cole21 = st.columns(2)

with cole11:
    "### Distribusi Nilai SKD"
    skd_prov = df_eda_01[df_eda_01['lokasi.formasi']==pilihan_lokasi]
    fig = plt.figure(figsize=(6, 5))
    ax = sns.kdeplot(skd_prov, x='skd.nilai', hue="hasil.akhir_x")
    ax.set(xlabel='', ylabel='')
    ax.lines[0].set_color(BLUE2)
    ax.lines[1].set_color(GRAY9)

    ytick_labs = np.arange(0, ax.lines[1].get_ydata().max()+0.001, 0.001)

    plt.setp(ax,
         yticks=ytick_labs,
         yticklabels=[f"{round(y*100,2)}%" for y in ytick_labs]
         )
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRAY5)
    ax.spines['bottom'].set_color(GRAY5)
    
    legend_elements = [Line2D([0], [0], color=GRAY9, lw=3, label='Tidak Lulus'),
                       Line2D([0], [0], color=BLUE2, lw=3, label='Lulus',
                              markerfacecolor='g', markersize=15),
                    ]
    ax.legend(handles=legend_elements, loc='upper left')

    for item in ax.get_xticklabels():
        item.set_color(GRAY3)
    for item in ax.get_yticklabels():
        item.set_color(GRAY3)
    
    st.pyplot(fig)

    st.dataframe(
        pg_skd[pg_skd['lokasi.formasi']==pilihan_lokasi],
        column_config={
            "lokasi.formasi": "Lokasi Formasi",
            "nilai_min_skd": "Minimum SKD",
            "nilai_max_skd": "Maksimum SKD",
            "nilai_rerata_skd": "Rerata SKD",
        },
        hide_index=True,
        use_container_width=True
           
        )

with cole21:
    "### Distribusi Nilai MTK"
    mtk_prov = df_eda_01[df_eda_01['lokasi.formasi']==pilihan_lokasi]
    fig = plt.figure(figsize=(6, 5))
    ax = sns.kdeplot(mtk_prov, x='mtk.nilai', hue="hasil.akhir_x")
    ax.set(xlabel='', ylabel='')
    ax.lines[0].set_color(BLUE2)
    ax.lines[1].set_color(GRAY9)

    ytick_labs = np.arange(0, ax.lines[1].get_ydata().max()+0.001, 0.001)

    plt.setp(ax,
         yticks=ytick_labs,
         yticklabels=[f"{round(y*100,2)}%" for y in ytick_labs]
         )
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRAY5)
    ax.spines['bottom'].set_color(GRAY5)
    
    legend_elements = [Line2D([0], [0], color=GRAY9, lw=3, label='Tidak Lulus'),
                       Line2D([0], [0], color=BLUE2, lw=3, label='Lulus',
                              markerfacecolor='g', markersize=15),
                    ]
    ax.legend(handles=legend_elements, loc='upper left')

    for item in ax.get_xticklabels():
        item.set_color(GRAY3)
    for item in ax.get_yticklabels():
        item.set_color(GRAY3)
    
    st.pyplot(fig)

    st.dataframe(pg_mtk[pg_mtk['lokasi.formasi']==pilihan_lokasi].set_index('lokasi.formasi'),
                column_config={
                    "lokasi.formasi": "Lokasi Formasi",
                    "nilai_min_mtk": "Minimum MTK",
                    "nilai_max_mtk": "Maksimum MTK",
                    "nilai_rerata_mtk": "Rerata MTK",
                },
                hide_index=True,
                use_container_width=True
                )


cole12, cole22 = st.columns(2)

with cole12:
    "### Korelasi"
    korelasi_prov = df_eda_01[df_eda_01['lokasi.formasi']==pilihan_lokasi][num_col].corr()
    fig, ax = plt.subplots(figsize=(5,5))
    sns.heatmap(korelasi_prov, 
                     annot=True, 
                     fmt=".2f",
                    yticklabels=['Nilai SKD','Nilai MTK', 'Hasil'],
                    xticklabels=['Nilai SKD','Nilai MTK', 'Hasil'],
                    ax=ax,
                    cmap="Blues");
    ax.collections[0].colorbar.remove()
    st.pyplot(fig)

with cole22:
    "### ⠀"
    kor_sha = korelasi_prov['hasil.akhir_x']['skd.nilai']
    kor_mha = korelasi_prov['hasil.akhir_x']['mtk.nilai']
    f"- Korelasi antara variabel SKD dan Hasil Akhir di {pilihan_lokasi} bernilai {round(kor_sha,3)} yang berarti bahwa kedua variabel tersebut berkorelasi **{'rendah' if kor_sha < 0.3 else 'sedang' if kor_sha < 0.7 else 'tinggi' }**"
    f"- Korelasi antara variabel Matematika dan Hasil Akhir di {pilihan_lokasi} bernilai {round(kor_mha,3)} yang berarti bahwa kedua variabel tersebut berkorelasi **{'rendah' if kor_mha < 0.3 else 'sedang' if kor_mha < 0.7 else 'tinggi' }**"

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