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

# ==================== VIBE AL-JAZIRA CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    :root {
        --aljazira-green: #1e3c2c; /* Hijau Tua Khas Kurma */
        --aljazira-gold: #c59d5f;  /* Emas Kurma */
        --aljazira-light: #fdfaf5; /* Background Krem Lembut */
        --aljazira-accent: #2e8b57;
    }

    /* Global Style */
    .stApp {
        background-color: var(--aljazira-light);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sidebar - Deep Green Gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c2c 0%, #0d1a13 100%) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #fdfaf5 !important;
    }

    /* White Card Al-Jazira Style */
    .white-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(30, 60, 44, 0.05);
        border-top: 5px solid var(--aljazira-gold);
        border-left: 1px solid #f1ece2;
    }

    /* Typography */
    h1, h2, h3 {
        color: var(--aljazira-green) !important;
        font-weight: 800 !important;
    }

    /* Metric Box - Gold Accent */
    .metric-box {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border-bottom: 4px solid var(--aljazira-gold);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--aljazira-green);
    }

    /* Buttons - Al-Jazira Green */
    .stButton button {
        background: var(--aljazira-green) !important;
        color: #fdfaf5 !important;
        border-radius: 8px !important;
        border: 2px solid var(--aljazira-gold) !important;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease;
        font-weight: 600 !important;
    }
    .stButton button:hover {
        background: var(--aljazira-gold) !important;
        color: var(--aljazira-green) !important;
        transform: translateY(-2px);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #e9edea;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 8px;
        color: var(--aljazira-green);
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--aljazira-green) !important;
        color: var(--aljazira-gold) !important;
    }

    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 12px;
    }

    .footer {
        text-align: center;
        padding: 2rem;
        background: var(--aljazira-green);
        color: var(--aljazira-gold);
        border-radius: 15px 15px 0 0;
        margin-top: 3rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE FUNCTIONS ====================
def get_connection():
    return sqlite3.connect("makloon_v3.db", check_same_thread=False)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS produk(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT UNIQUE, stok INTEGER,
                    stok_minimum INTEGER, harga_jual INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS pesanan(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, klien TEXT,
                    produk TEXT, jumlah INTEGER, status TEXT,
                    tanggal_masuk TEXT, jenis_pesanan TEXT, created_by TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS stok_distributor(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, distributor TEXT,
                    produk TEXT, stok INTEGER)""")
        c.execute("""CREATE TABLE IF NOT EXISTS users(
                    username TEXT PRIMARY KEY, password TEXT, role TEXT)""")
        
        # Default Data
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            users = [("pabrik","pabrik123","pabrik"), ("distributor1","dist123","distributor"), ("klien1","klien123","klien")]
            c.executemany("INSERT INTO users VALUES (?,?,?)", users)

        c.execute("SELECT COUNT(*) FROM produk")
        if c.fetchone()[0] == 0:
            produk = [("Sari Kurma Al-Jazira Premium", 600, 50, 35000),
                      ("Sari Kurma Al-Jazira Madu", 400, 50, 42000),
                      ("Sari Kurma Al-Jazira Anak", 250, 50, 30000)]
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

# ==================== AUTH SYSTEM ====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.title("🌴 OrderStock CV Amal Mulia")
    st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 Masuk", "📝 Daftar Baru"])
        
        with tab_log:
            with st.form("login_form"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("LOGIN SEKARANG", use_container_width=True):
                    res = get_df("SELECT role FROM users WHERE username=? AND password=?", (u,p))
                    if not res.empty:
                        st.session_state.authenticated = True
                        st.session_state.username = u
                        st.session_state.role = res.iloc[0]["role"]
                        st.rerun()
                    else:
                        st.error("Gagal login, periksa kembali akun Anda.")
        
        with tab_reg:
            with st.form("reg_form"):
                nu = st.text_input("Buat Username")
                np = st.text_input("Buat Password", type="password")
                nr = st.selectbox("Sebagai", ["distributor", "klien"])
                if st.form_submit_button("DAFTAR AKUN", use_container_width=True):
                    try:
                        run_query("INSERT INTO users VALUES (?,?,?)", (nu, np, nr))
                        st.success("Berhasil! Silakan klik tab Masuk.")
                    except:
                        st.error("Username sudah terdaftar.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== MAIN APP ====================
username = st.session_state.username
role = st.session_state.role

with st.sidebar:
    st.markdown(f"### 🍯 Al-Jazira Portal")
    st.markdown(f"**User:** `{username}`")
    st.markdown(f"**Role:** `{role.upper()}`")
    st.divider()
    if st.button("🚪 Keluar Sistem", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# Welcome Header
st.markdown(f"""
<div class="white-card">
    <h1 style='margin:0;'>Selamat Datang di Portal CV Amal Mulia</h1>
    <p style='color:var(--aljazira-gold); font-weight:600;'>{datetime.now().strftime('%A, %d %B %Y')} | Dedicated for Quality</p>
</div>
""", unsafe_allow_html=True)

# ==================== PABRIK DASHBOARD ====================
if role == "pabrik":
    c1, c2, c3 = st.columns(3)
    t_stok = get_df("SELECT SUM(stok) FROM produk").iloc[0,0] or 0
    t_pend = get_df("SELECT COUNT(*) FROM pesanan WHERE status='Menunggu Konfirmasi'").iloc[0,0] or 0
    
    with c1: st.markdown(f'<div class="metric-box"><div class="metric-value">{t_stok}</div><div>Unit Stok Tersedia</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-box"><div class="metric-value">{t_pend}</div><div>Antrian Pesanan</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-box"><div class="metric-value">Active</div><div>Status Pabrik</div></div>', unsafe_allow_html=True)

    tab_inv, tab_order, tab_dist = st.tabs(["📦 Inventori Pabrik", "🛒 Kelola Pesanan", "📊 Stok Mitra"])
    
    with tab_inv:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        df_p = get_df("SELECT nama, stok, harga_jual FROM produk")
        st.dataframe(df_p, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_order:
        orders = get_df("SELECT * FROM pesanan WHERE status='Menunggu Konfirmasi'")
        if orders.empty:
            st.info("Belum ada pesanan masuk.")
        else:
            for _, r in orders.iterrows():
                with st.expander(f"🔔 {r['jenis_pesanan'].upper()} - {r['klien']}"):
                    st.write(f"Produk: **{r['produk']}** | Jumlah: **{r['jumlah']}**")
                    if st.button("PROSES SEKARANG", key=f"p_{r['id']}"):
                        run_query("UPDATE pesanan SET status='Selesai' WHERE id=?", (r['id'],))
                        if r['jenis_pesanan'] == 'order_stok':
                            run_query("UPDATE produk SET stok = stok - ? WHERE nama=?", (r['jumlah'], r['produk']))
                        st.success("Pesanan diperbarui!")
                        st.rerun()

# ==================== DISTRIBUTOR DASHBOARD ====================
elif role == "distributor":
    tab_buy, tab_my_stok = st.tabs(["🛒 Belanja Stok", "📊 Inventori Saya"])
    
    with tab_buy:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        with st.form("buy"):
            plist = get_df("SELECT nama FROM produk")['nama'].tolist()
            p_sel = st.selectbox("Pilih Produk Sari Kurma", plist)
            qty = st.number_input("Jumlah Order", 1, 1000)
            if st.form_submit_button("KIRIM ORDER KE PABRIK"):
                run_query("INSERT INTO pesanan (klien, produk, jumlah, status, tanggal_masuk, jenis_pesanan, created_by) VALUES (?,?,?,?,?,?,?)",
                          (username, p_sel, qty, "Menunggu Konfirmasi", datetime.now().strftime("%Y-%m-%d"), "order_stok", username))
                st.success("Order telah dikirim!")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    🌴 CV AMAL MULIA — QUALITY CONTROL & DISTRIBUTION SYSTEM<br>
    <span style="font-size: 0.8rem; opacity: 0.8;">Inspired by Sari Kurma Al-Jazira Heritage</span>
</div>
""", unsafe_allow_html=True)
