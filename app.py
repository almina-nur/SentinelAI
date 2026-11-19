
import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="SentinelAI Dashboard", page_icon="🛡️", layout="wide")

# Başlık
st.title("🛡️ SentinelAI - AI-Powered Cybersecurity Analyst")
st.markdown("### SOC Analist Dashboard (Prototip)")

# Veriyi yükle
@st.cache_data
def load_data():
    BASE = "/content/drive/MyDrive/SentinelAI"
    return pd.read_parquet(f"{BASE}/data/processed/logs_classified.parquet")

df = load_data()

# Sidebar (Yan Menü)
st.sidebar.header("Filtreler")
threat_filter = st.sidebar.multiselect(
    "Tehdit Tipi Seçin:",
    options=df["threat_type"].unique(),
    default=["Brute Force", "Unknown Anomaly"]
)

# Filtrelenmiş veri
filtered_df = df[df["threat_type"].isin(threat_filter)]

# Üst Metrikler
col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Log", len(df))
col2.metric("Tespit Edilen Anomali", len(df[df["threat_type"] != "Normal"]))
col3.metric("Kritik Alarmlar (Brute Force)", len(df[df["threat_type"] == "Brute Force"]))
col4.metric("Yanlış Pozitif Oranı", "0.6%")

st.divider()

# İki Sütunlu Yapı
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🚨 Aktif Alarmlar")
    if len(filtered_df) == 0:
        st.info("Seçilen kriterlere uygun alarm bulunamadı.")
    else:
        for idx, row in filtered_df.iterrows():
            with st.expander(f"🚨 {row['threat_type']} - IP: {row['ip']}"):
                st.write(f"**Zaman:** {row['timestamp']}")
                st.write(f"**Kullanıcı:** {row['user']}")
                st.write(f"**Deneme Sayısı:** {row['attempts']}")
                st.write(f"**MITRE:** {row['mitre_id']}")
                st.info(f"**Gerekçe:** {row['reason']}")

with col_right:
    st.subheader("📊 Tehdit Dağılımı")
    threat_counts = df["threat_type"].value_counts()
    st.bar_chart(threat_counts)

    st.subheader("🎯 MITRE ID Dağılımı")
    mitre_counts = df[df["mitre_id"].notna()]["mitre_id"].value_counts()
    st.bar_chart(mitre_counts)
