import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="OrderStock - CV Amal Mulia",
    layout="wide",
    page_icon="🌴"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family: 'Poppins', sans-serif;
}

/* ================= BACKGROUND ================= */
.stApp{
    background:
    linear-gradient(
        135deg,
        #062f22 0%,
        #0f5132 40%,
        #176944 100%
    );
    color:white;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #05281d 0%,
        #0f5132 100%
    );
    border-right:2px solid rgba(255,255,255,0.1);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* ================= HEADER ================= */
.hero-box{
    background:
    linear-gradient(
        135deg,
        rgba(255,255,255,0.10),
        rgba(255,255,255,0.05)
    );

    border:1px solid rgba(255,255,255,0.12);

    padding:2rem;
    border-radius:28px;

    backdrop-filter: blur(12px);

    box-shadow:
    0 8px 30px rgba(0,0,0,0.25);

    margin-bottom:1.5rem;
}

.hero-title{
    font-size:3rem;
    font-weight:800;
    line-height:1.1;
    color:white;
}

.hero-gold{
    color:#f2c66d;
}

.hero-sub{
    margin-top:10px;
    color:#d9f5e5;
    font-size:1rem;
}

/* ================= CARD ================= */
.white-card{
    background:
    linear-gradient(
        180deg,
        rgba(255,255,255,0.96),
        rgba(255,255,255,0.90)
    );

    border-radius:26px;

    padding:1.5rem;

    color:#133a2b;

    box-shadow:
    0 10px 25px rgba(0,0,0,0.15);

    border:
    1px solid rgba(255,255,255,0.3);

    margin-bottom:1rem;
}

/* ================= METRIC ================= */
.metric-box{
    background:
    linear-gradient(
        135deg,
        #fff7e7,
        #fff1cf
    );

    border-radius:24px;

    padding:1.4rem;

    text-align:center;

    box-shadow:
    0 5px 18px rgba(0,0,0,0.12);

    border:2px solid rgba(242,198,109,0.35);
}

.metric-value{
    font-size:2.4rem;
    font-weight:800;
    color:#0f5132;
}

.metric-label{
    color:#6b4b12;
    font-weight:600;
}

/* ================= BUTTON ================= */
.stButton button{
    background:
    linear-gradient(
        135deg,
        #c58d2a,
        #f2c66d
    ) !important;

    color:#143728 !important;

    border:none !important;

    border-radius:18px !important;

    font-weight:700 !important;

    padding:0.6rem 1.2rem !important;

    transition:0.3s;
}

.stButton button:hover{
    transform:scale(1.03);
    box-shadow:
    0 6px 18px rgba(242,198,109,0.4);
}

/* ================= TABS ================= */
.stTabs [data-baseweb="tab-list"]{
    gap:10px;
}

.stTabs [data-baseweb="tab"]{
    background:
    rgba(255,255,255,0.1);

    color:white;

    border-radius:18px;

    padding:12px 24px;

    font-weight:600;
}

.stTabs [aria-selected="true"]{
    background:
    linear-gradient(
        135deg,
        #c58d2a,
        #f2c66d
    ) !important;

    color:#143728 !important;
}

/* ================= INPUT ================= */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]{
    border-radius:16px !important;
    border:2px solid #e9d3a1 !important;
}

/* ================= TABLE ================= */
[data-testid="stDataFrame"]{
    background:white;
    border-radius:22px;
    overflow:hidden;
    padding:10px;
}

/* ================= ALERT ================= */
.stAlert{
    border-radius:20px;
}

/* ================= FOOTER ================= */
.footer{
    text-align:center;
    margin-top:2rem;
    color:#d8f0df;
    font-size:0.95rem;
    padding-bottom:1rem;
}

/* ================= HIDE STREAMLIT ================= */
#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================
def get_connection():
    return sqlite3.connect(
        "makloon.db",
        check_same_thread=False
    )

def run_query(query, params=()):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()

def get_df(query, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(
            query,
            conn,
            params=params
        )

# ==================== HEADER ====================
st.markdown(f"""
<div class="hero-box">

<div class="hero-title">
ORDERSTOCK
<span class="hero-gold">CV AMAL MULIA</span>
</div>

<div class="hero-sub">
Sistem Distribusi & Manajemen Pesanan Modern
</div>

</div>
""", unsafe_allow_html=True)

# ==================== DEMO METRIC ====================
col1,col2,col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">1650</div>
        <div class="metric-label">
            Total Stok
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">12</div>
        <div class="metric-label">
            Pesanan Pending
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">98</div>
        <div class="metric-label">
            Pesanan Selesai
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==================== TABS ====================
tab1,tab2,tab3 = st.tabs([
    "📦 Produk",
    "🛒 Pesanan",
    "📊 Distributor"
])

with tab1:

    st.markdown("""
    <div class="white-card">
    <h3>📦 Data Produk</h3>
    </div>
    """, unsafe_allow_html=True)

    data = pd.DataFrame({
        "Produk":[
            "Sari Kurma Premium",
            "Sari Kurma Herbal",
            "Sari Kurma Lambung"
        ],
        "Stok":[500,300,250],
        "Harga":[
            "Rp 35.000",
            "Rp 40.000",
            "Rp 45.000"
        ]
    })

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

with tab2:

    st.markdown("""
    <div class="white-card">
    <h3>🛒 Form Order</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.form("order"):

        st.text_input("Nama Produk")

        st.number_input(
            "Jumlah",
            min_value=1
        )

        st.text_area("Catatan")

        st.form_submit_button(
            "Kirim Pesanan"
        )

with tab3:

    st.markdown("""
    <div class="white-card">
    <h3>📊 Stok Distributor</h3>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame({
        "Distributor":[
            "Distributor 1",
            "Distributor 2"
        ],
        "Produk":[
            "Sari Kurma Premium",
            "Sari Kurma Herbal"
        ],
        "Stok":[25,40]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
🌴 © 2026 CV Amal Mulia — Premium Distribution System
</div>
""", unsafe_allow_html=True)
