import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ========================
# LOAD DATA
# ========================
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    return df

df = load_data()

# ========================
# SIDEBAR (IDENTITAS)
# ========================
with st.sidebar:
    st.title("🚲 Bike Dashboard")
    st.markdown("---")
    st.markdown("### 👨‍💻 Profil Analis")
    st.markdown("**Nama:** Muhammad Alfarobi")
    st.markdown("**Cohort ID:** CDCC282D6Y1002")
    st.markdown("---")

    selected_year = st.multiselect(
        "📅 Pilih Tahun",
        options=sorted(df['year'].unique()),
        default=sorted(df['year'].unique()) 
    )

# ========================
# FILTER
# ========================
if len(selected_year) == 0:
    st.markdown("""
    <div style="
        text-align:center;
        padding:60px;
        background-color:#f8f9fa;
        border-radius:12px;
        margin-top:60px;
    ">
        <h1 style="color:#6c757d;">❌ Data Tidak Dapat Ditemukan</h1>
        <p style="font-size:20px; color:#6c757d;">
            Silakan pilih minimal satu tahun pada sidebar
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

filtered_df = df[df['year'].isin(selected_year)]

# ========================
# TITLE
# ========================
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown(
    "Dashboard ini menganalisis pengaruh **musim** dan **kondisi cuaca** terhadap jumlah penyewaan sepeda "
    "berdasarkan data historis tahun 2011–2012."
)

# ========================
# KPI
# ========================
col1, col2, col3 = st.columns(3)

total = filtered_df['cnt'].sum()
avg = filtered_df['cnt'].mean()
days = filtered_df.shape[0]

col1.metric("Total Penyewaan", f"{int(total):,}")
col2.metric("Rata-rata Harian", f"{int(avg)}")
col3.metric("Jumlah Hari", days)

st.markdown("---")

# ========================
# VISUAL 1 — SEASON
# ========================
st.subheader("📊 Pengaruh Musim terhadap Penyewaan Sepeda")

season_avg = filtered_df.groupby("season")["cnt"].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8,5))
colors = ["#2a9d8f", "#264653", "#e9c46a", "#e76f51"]

bars = ax.bar(season_avg.index, season_avg.values, color=colors[:len(season_avg)])

ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan")

max_val = season_avg.max()
ax.set_ylim(0, max_val * 1.15)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height,
            f"{int(height)}",
            ha='center', va='bottom', fontsize=9)

ax.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

with st.expander("💡 Insight & Kesimpulan (Musim)"):
    highest = season_avg.idxmax()
    lowest = season_avg.idxmin()

    st.write(f"""
    **Insight Utama:**
Musim **{highest}** memiliki rata-rata penyewaan tertinggi yaitu sekitar **5644 penyewaan per hari**, 
sedangkan musim **{lowest}** terendah yaitu sekitar **2604 penyewaan per hari**.

**Analisis:**
Terdapat pola peningkatan dari Spring → Summer → Fall, yang menunjukkan bahwa kondisi lingkungan seperti suhu dan kenyamanan sangat mempengaruhi aktivitas bersepeda.

**Kesimpulan:**
Musim merupakan faktor penting dalam menentukan permintaan penyewaan sepeda, dengan puncak terjadi pada musim Fall.

**Rekomendasi:**
- Tambahkan armada sepeda pada musim **{highest}**
- Optimalkan strategi operasional pada musim **{lowest}**
""")

st.markdown("---")

# ========================
# VISUAL 2 — WEATHER
# ========================
st.subheader("🌦️ Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

weather_avg = filtered_df.groupby("weathersit")["cnt"].mean().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(8,5))
colors2 = ["#2a9d8f", "#fcbf49", "#f77f00", "#d62828"]

bars2 = ax2.bar(weather_avg.index, weather_avg.values, color=colors2[:len(weather_avg)])

ax2.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
ax2.set_xlabel("Kondisi Cuaca")
ax2.set_ylabel("Rata-rata Penyewaan")

max_val2 = weather_avg.max()
ax2.set_ylim(0, max_val2 * 1.15)

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height,
             f"{int(height)}",
             ha='center', va='bottom', fontsize=9)

ax2.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
st.pyplot(fig2)

with st.expander("💡 Insight & Kesimpulan (Cuaca)"):
    highest_w = weather_avg.idxmax()
    lowest_w = weather_avg.idxmin()

    st.write(f"""
    **Insight Utama:**
Cuaca **{highest_w}** menghasilkan rata-rata penyewaan tertinggi yaitu sekitar **4877 penyewaan per hari**, 
sedangkan cuaca **{lowest_w}** terendah yaitu sekitar **1803 penyewaan per hari**.

**Analisis:**
Semakin buruk kondisi cuaca, semakin rendah minat pengguna untuk melakukan penyewaan sepeda.

**Kesimpulan:**
Cuaca memiliki pengaruh langsung terhadap jumlah penyewaan sepeda.

**Rekomendasi:**
- Maksimalkan operasional saat cuaca **{highest_w}**
- Terapkan strategi promosi saat kondisi **{lowest_w}**
""")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("© 2026 Muhammad Alfarobi | Dicoding Submission")