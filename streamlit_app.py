import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="MDMS - CV Amal Mulia",
    layout="wide",
    page_icon="🌴"
)

# ==================== CSS TEMA HIJAU ELEGAN ====================
st.markdown("""
<style>
/* ===== WARNA UTAMA ===== */
:root{
    --green-dark:#0f3d2e;
    --green-main:#1f7a59;
    --green-soft:#2f9e75;
    --green-light:#dff5ea;
    --green-bg:#f4fbf7;
    --white:#ffffff;
    --text:#18352a;
}

/* ===== BACKGROUND APP ===== */
.stApp{
    background: linear-gradient(135deg,#eef8f1,#f7fcf8);
    color: var(--text);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#0f3d2e,#1b5e45);
    border-right: 2px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] *{
    color: #f2fff8 !important;
}

/* ===== HEADER CARD ===== */
.white-card{
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(8px);
    border-radius: 24px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    border-left: 8px solid var(--green-main);
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* ===== METRIC BOX ===== */
.metric-box{
    background: linear-gradient(135deg,#ffffff,#f0faf4);
    border-radius: 22px;
    padding: 1.2rem;
    text-align:center;
    border:1px solid #d9eee2;
    box-shadow:0 4px 10px rgba(0,0,0,0.04);
    transition:0.2s;
}

.metric-box:hover{
    transform: translateY(-3px);
}

.metric-value{
    font-size:2.4rem;
    font-weight:700;
    color:var(--green-dark);
}

.metric-title{
    color:#3d5f52;
    font-weight:600;
    margin-top:8px;
}

/* ===== BUTTON ===== */
.stButton button{
    width:100%;
    background: linear-gradient(135deg,#1f7a59,#2f9e75);
    color:white;
    border:none;
    border-radius:30px;
    padding:0.65rem 1rem;
    font-weight:700;
    transition:0.25s;
}

.stButton button:hover{
    background: linear-gradient(135deg,#17684b,#23805f);
    transform:scale(1.01);
    color:white;
}

/* ===== INPUT ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"]{
    border-radius:16px !important;
    border:1px solid #bfe3cf !important;
    background-color:#fcfffd !important;
}

/* ===== TAB ===== */
.stTabs [data-baseweb="tab-list"]{
    gap:14px;
}

.stTabs [data-baseweb="tab"]{
    background:#e7f5ec;
    border-radius:30px;
    padding:10px 22px;
    color:#1b5e45;
    font-weight:700;
}

.stTabs [aria-selected="true"]{
    background:linear-gradient(135deg,#1f7a59,#2f9e75);
    color:white !important;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
    border:1px solid #dceee3;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader{
    background:#edf8f1;
    border-radius:14px;
    color:#1b5e45 !important;
    font-weight:700;
}

/* ===== INFO / SUCCESS ===== */
.stSuccess{
    border-radius:14px;
}

.stInfo{
    border-radius:14px;
}

/* ===== FOOTER ===== */
.footer{
    text-align:center;
    margin-top:2rem;
    padding:1rem;
    color:#4d6b5f;
    font-size:0.85rem;
}

/* ===== HR ===== */
hr{
    border:1px solid #bfe3cf;
}

/* ===== TITLE ===== */
h1,h2,h3{
    color:#174d38;
}

/* ===== RADIO ===== */
div[role="radiogroup"]{
    background:#edf8f1;
    padding:10px;
    border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

# ==================== LOGO / HEADER SIDEBAR ====================
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    st.sidebar.markdown("## 🌴 CV AMAL MULIA")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# ==================== DATABASE ====================
def get_connection():
    return sqlite3.connect('makloon.db', check_same_thread=False)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS produk (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT UNIQUE,
                    stok INTEGER,
                    stok_minimum INTEGER DEFAULT 50,
                    harga_jual INTEGER)''')

        c.execute('''CREATE TABLE IF NOT EXISTS pesanan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    klien TEXT,
                    produk TEXT,
                    jumlah INTEGER,
                    status TEXT,
                    tanggal_masuk TEXT,
                    jenis_pesanan TEXT,
                    created_by TEXT,
                    tanggal_konfirmasi TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    role TEXT)''')

        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            users_data = [
                ('pabrik', 'pabrik123', 'pabrik'),
                ('distributor1', 'dist123', 'distributor'),
                ('klien1', 'klien123', 'klien')
            ]
            c.executemany("INSERT INTO users VALUES (?,?,?)", users_data)

        c.execute("SELECT COUNT(*) FROM produk")
        if c.fetchone()[0] == 0:
            produk_data = [
                ('Sari Kurma Alami', 500, 50, 15000),
                ('Sari Kurma Madu', 300, 50, 25000)
            ]
            c.executemany(
                "INSERT INTO produk (nama, stok, stok_minimum, harga_jual) VALUES (?,?,?,?)",
                produk_data
            )

        conn.commit()

def run_query(query, params=()):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()

def get_df(query, params=()):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)

init_db()

# ==================== LOGIN ====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.markdown("""
    <div class="white-card">
        <h1>🌴 OrderStock - CV Amal Mulia</h1>
        <p>Sistem Manajemen Produksi & Distribusi Herbal</p>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio("", ["Masuk", "Daftar"], horizontal=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        if menu == "Masuk":

            with st.form("login"):
                st.subheader("🔐 Login")

                u = st.text_input("Username")
                p = st.text_input("Password", type="password")

                if st.form_submit_button("Masuk"):
                    res = get_df(
                        "SELECT role FROM users WHERE username=? AND password=?",
                        (u, p)
                    )

                    if not res.empty:
                        st.session_state.authenticated = True
                        st.session_state.username = u
                        st.session_state.role = res.iloc[0]['role']
                        st.rerun()
                    else:
                        st.error("Username atau password salah")

        else:

            with st.form("register"):
                st.subheader("📝 Daftar Akun Baru")

                new_u = st.text_input("Username baru")
                new_p = st.text_input("Password", type="password")

                role = st.selectbox(
                    "Daftar sebagai",
                    ["distributor", "klien"]
                )

                if st.form_submit_button("Daftar"):
                    if new_u and new_p:

                        cek = get_df(
                            "SELECT * FROM users WHERE username=?",
                            (new_u,)
                        )

                        if cek.empty:
                            run_query(
                                "INSERT INTO users VALUES (?,?,?)",
                                (new_u, new_p, role)
                            )
                            st.success("Akun berhasil dibuat")
                        else:
                            st.error("Username sudah terdaftar")

    st.stop()

# ==================== SIDEBAR ====================
with st.sidebar:

    st.markdown(f"### 👤 {st.session_state.username}")
    st.markdown(f"**Role:** `{st.session_state.role.upper()}`")
    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ==================== DASHBOARD ====================
st.markdown(f"""
<div class="white-card">
    <h2>🌱 Selamat Datang, {st.session_state.username}</h2>
    <p>{datetime.now().strftime('%A, %d %B %Y')}</p>
</div>
""", unsafe_allow_html=True)

role = st.session_state.role
username = st.session_state.username

# ==================== PABRIK ====================
if role == "pabrik":

    total_stok = get_df(
        "SELECT SUM(stok) FROM produk"
    ).iloc[0,0] or 0

    pesanan_makloon = get_df(
        "SELECT SUM(jumlah) FROM pesanan WHERE jenis_pesanan='makloon'"
    ).iloc[0,0] or 0

    order_wait = get_df(
        "SELECT SUM(jumlah) FROM pesanan WHERE status='Menunggu Konfirmasi'"
    ).iloc[0,0] or 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{total_stok}</div>
            <div class="metric-title">📦 Total Stok</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{pesanan_makloon}</div>
            <div class="metric-title">🏭 Pesanan Makloon</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{order_wait}</div>
            <div class="metric-title">⏳ Menunggu</div>
        </div>
        """, unsafe_allow_html=True)

    st.success("Tema dashboard berhasil dibuat dominan hijau 🌿")
