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

# ==================== CUSTOM CSS (EMERALD & GOLD) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ================= BACKGROUND ================= */
.stApp {
    background: linear-gradient(135deg, #062f22 0%, #0f5132 40%, #176944 100%);
    color: white;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #05281d 0%, #0f5132 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ================= HERO HEADER ================= */
.hero-box {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 2rem;
    border-radius: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: white;
}
.hero-gold {
    color: #f2c66d;
}

/* ================= CARD ================= */
.white-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 1.5rem;
    color: #062f22;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-bottom: 1rem;
    border-left: 6px solid #c58d2a;
}
.white-card h1, .white-card h2, .white-card h3 {
    color: #062f22 !important;
}

/* ================= METRIC ================= */
.metric-box {
    background: linear-gradient(135deg, #fff7e7, #fff1cf);
    border-radius: 24px;
    padding: 1.4rem;
    text-align: center;
    box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    border: 2px solid #f2c66d;
}
.metric-value {
    font-size: 2.4rem;
    font-weight: 800;
    color: #0f5132;
}
.metric-label {
    color: #6b4b12;
    font-weight: 600;
}

/* ================= BUTTON ================= */
.stButton button {
    background: linear-gradient(135deg, #c58d2a, #f2c66d) !important;
    color: #143728 !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.2rem !important;
    transition: 0.3s;
}

/* ================= TABS ================= */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 18px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c58d2a, #f2c66d) !important;
    color: #143728 !important;
}

/* ================= INPUT ================= */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
    background: white !important;
}

[data-testid="stDataFrame"] {
    background: white;
    border-radius: 20px;
    padding: 5px;
}

.footer {
    text-align: center;
    margin-top: 2rem;
    color: #d8f0df;
}
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE ====================
def get_connection():
    return sqlite3.connect("makloon.db", check_same_thread=False)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS produk(id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT UNIQUE, stok INTEGER, stok_minimum INTEGER, harga_jual INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS pesanan(id INTEGER PRIMARY KEY AUTOINCREMENT, klien TEXT, produk TEXT, jumlah INTEGER, status TEXT, tanggal_masuk TEXT, jenis_pesanan TEXT, created_by TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS stok_distributor(id INTEGER PRIMARY KEY AUTOINCREMENT, distributor TEXT, produk TEXT, stok INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, role TEXT)""")
        
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            users = [("pabrik","pabrik123","pabrik"), ("distributor1","dist123","distributor"), ("klien1","klien123","klien")]
            c.executemany("INSERT INTO users VALUES (?,?,?)", users)

        c.execute("SELECT COUNT(*) FROM produk")
        if c.fetchone()[0] == 0:
            produk = [("Sari Kurma Premium",500,50,35000), ("Sari Kurma Al-Jazira",600,50,30000)]
            c.executemany("INSERT INTO produk (nama,stok,stok_minimum,harga_jual) VALUES (?,?,?,?)", produk)
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

# ==================== LOGIN SYSTEM ====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="hero-box"><div class="hero-title">ORDERSTOCK <span class="hero-gold">CV AMAL MULIA</span></div></div>', unsafe_allow_html=True)
    
    menu = st.radio("", ["Masuk", "Daftar"], horizontal=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        if menu == "Masuk":
            with st.form("login"):
                st.subheader("🔐 Login")
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Masuk"):
                    res = get_df("SELECT role FROM users WHERE username=? AND password=?", (u,p))
                    if not res.empty:
                        st.session_state.authenticated = True
                        st.session_state.username = u
                        st.session_state.role = res.iloc[0]["role"]
                        st.rerun()
                    else: st.error("Salah password!")
        else:
            with st.form("register"):
                st.subheader("📝 Daftar")
                nu = st.text_input("Username")
                np = st.text_input("Password", type="password")
                nr = st.selectbox("Role", ["distributor", "klien"])
                if st.form_submit_button("Daftar"):
                    try:
                        run_query("INSERT INTO users VALUES (?,?,?)", (nu, np, nr))
                        st.success("Berhasil!")
                    except: st.error("User sudah ada!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== MAIN APP ====================
role = st.session_state.role
username = st.session_state.username

with st.sidebar:
    st.markdown(f"## 👤 {username}")
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.markdown(f'<div class="hero-box"><div class="hero-title">SELAMAT DATANG <span class="hero-gold">{username.upper()}</span></div></div>', unsafe_allow_html=True)

# ==================== LOGIC ROLE PABRIK ====================
if role == "pabrik":
    col1, col2, col3 = st.columns(3)
    t_stok = get_df("SELECT SUM(stok) FROM produk").iloc[0,0] or 0
    t_pend = get_df("SELECT COUNT(*) FROM pesanan WHERE status='Menunggu Konfirmasi'").iloc[0,0] or 0
    
    with col1: st.markdown(f'<div class="metric-box"><div class="metric-value">{t_stok}</div><div class="metric-label">Total Stok</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-box"><div class="metric-value">{t_pend}</div><div class="metric-label">Order Pending</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-box"><div class="metric-value">Active</div><div class="metric-label">Sistem</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📦 Stok", "🛒 Order Masuk", "📊 Distributor"])
    with tab1:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.dataframe(get_df("SELECT * FROM produk"), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        df_ord = get_df("SELECT * FROM pesanan WHERE status='Menunggu Konfirmasi'")
        for _, r in df_ord.iterrows():
            with st.expander(f"{r['produk']} - {r['klien']}"):
                if st.button("Setujui", key=f"ok_{r['id']}"):
                    run_query("UPDATE pesanan SET status='Selesai' WHERE id=?", (r['id'],))
                    st.rerun()
    with tab3:
        st.dataframe(get_df("SELECT * FROM stok_distributor"), use_container_width=True, hide_index=True)

# ==================== LOGIC ROLE KLIEN ====================
elif role == "klien":
    tab1, tab2 = st.tabs(["🏭 Pesan Makloon", "📋 Status"])
    with tab1:
        with st.form("makloon"):
            prod = st.text_input("Produk")
            jml = st.number_input("Jumlah", min_value=1)
            if st.form_submit_button("Kirim"):
                run_query("INSERT INTO pesanan (klien, produk, jumlah, status, tanggal_masuk, jenis_pesanan, created_by) VALUES (?,?,?,?,?,?,?)",
                          ("Client", prod, jml, "Menunggu Konfirmasi", datetime.now().strftime("%Y-%m-%d"), "makloon", username))
                st.success("Terkirim!")

# ==================== LOGIC ROLE DISTRIBUTOR ====================
elif role == "distributor":
    tab1, tab2 = st.tabs(["📦 Stok Pabrik", "🛒 Order Stok"])
    with tab1:
        st.dataframe(get_df("SELECT nama, stok FROM produk"), use_container_width=True, hide_index=True)
    with tab2:
        with st.form("ord_dist"):
            p_sel = st.selectbox("Produk", get_df("SELECT nama FROM produk")["nama"])
            qty = st.number_input("Qty", 1)
            if st.form_submit_button("Order"):
                run_query("INSERT INTO pesanan (klien, produk, jumlah, status, tanggal_masuk, jenis_pesanan, created_by) VALUES (?,?,?,?,?,?,?)",
                          (username, p_sel, qty, "Menunggu Konfirmasi", datetime.now().strftime("%Y-%m-%d"), "order_stok", username))
                st.success("Order Berhasil!")

st.markdown('<div class="footer">🌴 © 2026 CV Amal Mulia — OrderStock</div>', unsafe_allow_html=True)
