import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="OrderStock - CV Amal Mulia",
    layout="wide",
    page_icon="🌴"
)

# ================= CSS =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins', sans-serif;
}

/* ================= BACKGROUND ================= */

.stApp{
    background:
    linear-gradient(
        135deg,
        #052e21 0%,
        #0b5136 45%,
        #176b46 100%
    );
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #031d15 0%,
        #0d4d33 100%
    );
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* ================= CARD ================= */

.white-card{

    background:
    linear-gradient(
        135deg,
        rgba(10,45,32,0.96),
        rgba(18,79,53,0.93)
    );

    border-radius:28px;

    padding:1.5rem;

    margin-bottom:1rem;

    border:
    1px solid rgba(244,199,107,0.2);

    box-shadow:
    0 10px 30px rgba(0,0,0,0.18);
}

/* ================= TEXT ================= */

h1,h2,h3,h4,h5,h6,
p,label,span,div{
    color:white !important;
}

/* ================= GOLD TITLE ================= */

.gold-title{
    color:#f4c76b !important;
    font-weight:800;
}

/* ================= BUTTON ================= */

.stButton button,
.stFormSubmitButton button{

    background:
    linear-gradient(
        135deg,
        #c98d25,
        #f4c76b
    ) !important;

    color:#17382c !important;

    border:none !important;

    border-radius:18px !important;

    font-weight:700 !important;

    transition:0.3s;
}

.stButton button:hover,
.stFormSubmitButton button:hover{

    transform:scale(1.03);

    box-shadow:
    0 8px 18px rgba(244,199,107,0.4);
}

/* ================= RADIO ================= */

.stRadio label{
    color:white !important;
    font-weight:600;
}

/* ================= TABS ================= */

.stTabs [data-baseweb="tab"]{

    background:
    rgba(255,255,255,0.08);

    border-radius:20px;

    padding:10px 20px;

    color:white !important;

    font-weight:600;
}

.stTabs [aria-selected="true"]{

    background:
    linear-gradient(
        135deg,
        #c98d25,
        #f4c76b
    ) !important;

    color:#17382c !important;
}

/* ================= METRIC ================= */

.metric-box{

    background:
    linear-gradient(
        135deg,
        #fff8e7,
        #ffe2a8
    );

    border-radius:24px;

    padding:1.2rem;

    text-align:center;

    border:
    2px solid rgba(244,199,107,0.35);

    box-shadow:
    0 8px 18px rgba(0,0,0,0.12);
}

.metric-value{

    font-size:2.2rem;

    font-weight:800;

    color:#0d4d33 !important;
}

.metric-label{
    color:#6f4f12 !important;
    font-weight:700;
}

/* ================= INPUT ================= */

.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label{
    color:#f4c76b !important;
    font-weight:600;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]{

    border-radius:16px !important;

    border:
    2px solid #ecd7ab !important;

    color:#17382c !important;

    font-weight:500;
}

/* ================= TABLE ================= */

[data-testid="stDataFrame"]{

    background:white;

    border-radius:20px;

    padding:10px;
}

[data-testid="stDataFrame"] *{
    color:#17382c !important;
}

/* ================= ALERT ================= */

.stAlert{
    border-radius:20px;
}

/* ================= FOOTER ================= */

.footer{

    text-align:center;

    margin-top:2rem;

    color:#d9f2e3;
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

# ================= DATABASE =================

def get_connection():
    return sqlite3.connect(
        "makloon.db",
        check_same_thread=False
    )

def init_db():

    with get_connection() as conn:

        c = conn.cursor()

        # ===== PRODUK =====
        c.execute("""
        CREATE TABLE IF NOT EXISTS produk(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT UNIQUE,
            stok INTEGER,
            stok_minimum INTEGER,
            harga_jual INTEGER
        )
        """)

        # ===== PESANAN =====
        c.execute("""
        CREATE TABLE IF NOT EXISTS pesanan(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            klien TEXT,
            produk TEXT,
            jumlah INTEGER,
            status TEXT,
            tanggal_masuk TEXT,
            jenis_pesanan TEXT,
            created_by TEXT
        )
        """)

        # ===== STOK DISTRIBUTOR =====
        c.execute("""
        CREATE TABLE IF NOT EXISTS stok_distributor(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distributor TEXT,
            produk TEXT,
            stok INTEGER
        )
        """)

        # ===== USERS =====
        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
        """)

        # ===== DEFAULT USER =====
        c.execute("SELECT COUNT(*) FROM users")

        if c.fetchone()[0] == 0:

            users = [
                ("pabrik","pabrik123","pabrik"),
                ("distributor1","dist123","distributor"),
                ("distributor2","dist123","distributor"),
                ("distributor3","dist123","distributor"),
                ("klien1","klien123","klien")
            ]

            c.executemany(
                "INSERT INTO users VALUES (?,?,?)",
                users
            )

        # ===== DEFAULT PRODUK =====
        c.execute("SELECT COUNT(*) FROM produk")

        if c.fetchone()[0] == 0:

            produk = [
                ("Sari Kurma Premium",500,50,35000),
                ("Sari Kurma Herbal Obat Batuk",300,50,40000),
                ("Sari Kurma Lambung",250,50,45000),
                ("Sari Kurma Al-Jazira",600,50,30000)
            ]

            c.executemany("""
            INSERT INTO produk
            (nama,stok,stok_minimum,harga_jual)
            VALUES (?,?,?,?)
            """, produk)

        # ===== AUTO BUAT STOK DISTRIBUTOR =====
        distributors = pd.read_sql_query("""
        SELECT username
        FROM users
        WHERE role='distributor'
        """, conn)

        products = pd.read_sql_query("""
        SELECT nama
        FROM produk
        """, conn)

        for _, d in distributors.iterrows():

            for _, p in products.iterrows():

                cek = pd.read_sql_query("""
                SELECT *
                FROM stok_distributor
                WHERE distributor=? AND produk=?
                """, conn, params=(d["username"], p["nama"]))

                if cek.empty:

                    c.execute("""
                    INSERT INTO stok_distributor
                    (distributor,produk,stok)
                    VALUES (?,?,?)
                    """, (
                        d["username"],
                        p["nama"],
                        0
                    ))

        conn.commit()

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

init_db()

# ================= LOGIN =================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ================= BELUM LOGIN =================

if not st.session_state.authenticated:

    st.markdown("""
    <div class="white-card">

        <h1 class="gold-title">
        🌴 OrderStock - CV Amal Mulia Sejahtera
        </h1>

        <p>
        Manajemen Pesanan & Distribusi Stok Premium
        </p>

    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "",
        ["Masuk","Daftar"],
        horizontal=True
    )

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        # ===== LOGIN =====
        if menu == "Masuk":

            with st.form("login"):

                st.subheader("🔐 Login")

                u = st.text_input("Username")

                p = st.text_input(
                    "Password",
                    type="password"
                )

                submit = st.form_submit_button("Masuk")

                if submit:

                    res = get_df(
                        "SELECT role FROM users WHERE username=? AND password=?",
                        (u,p)
                    )

                    if not res.empty:

                        st.session_state.authenticated = True
                        st.session_state.username = u
                        st.session_state.role = res.iloc[0]["role"]

                        st.rerun()

                    else:
                        st.error("Username/password salah")

        # ===== REGISTER =====
        else:

            with st.form("register"):

                st.subheader("📝 Daftar")

                new_u = st.text_input("Username")

                new_p = st.text_input(
                    "Password",
                    type="password"
                )

                role = st.selectbox(
                    "Daftar sebagai",
                    ["distributor","klien"]
                )

                submit = st.form_submit_button("Daftar")

                if submit:

                    cek = get_df(
                        "SELECT * FROM users WHERE username=?",
                        (new_u,)
                    )

                    if cek.empty:

                        run_query(
                            "INSERT INTO users VALUES (?,?,?)",
                            (new_u,new_p,role)
                        )

                        if role == "distributor":

                            produk_list = get_df("""
                            SELECT nama
                            FROM produk
                            """)

                            for _, row in produk_list.iterrows():

                                run_query("""
                                INSERT INTO stok_distributor
                                (distributor,produk,stok)
                                VALUES (?,?,?)
                                """,(
                                    new_u,
                                    row["nama"],
                                    0
                                ))

                        st.success("Akun berhasil dibuat")

                    else:
                        st.error("Username sudah ada")

    st.stop()

# ================= SESSION =================

role = st.session_state.role
username = st.session_state.username

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown(f"""
    ## 👤 {username}
    """)

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.authenticated = False
        st.rerun()

# ================= HEADER =================

st.markdown(f"""
<div class="white-card">

    <h2 class="gold-title">
    🏢 Selamat Datang, {username}
    </h2>

    <p>
    {datetime.now().strftime('%A, %d %B %Y')}
    </p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# ================= ROLE PABRIK ===========================
# =========================================================

if role == "pabrik":

    total_stok = get_df("""
    SELECT SUM(stok) as total
    FROM produk
    """).iloc[0]["total"] or 0

    total_order = get_df("""
    SELECT COUNT(*) as total
    FROM pesanan
    WHERE status='Menunggu Konfirmasi'
    """).iloc[0]["total"] or 0

    selesai = get_df("""
    SELECT COUNT(*) as total
    FROM pesanan
    WHERE status='Selesai'
    """).iloc[0]["total"] or 0

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{total_stok}</div>
            <div class="metric-label">Total Stok Pabrik</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{total_order}</div>
            <div class="metric-label">Pesanan Pending</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{selesai}</div>
            <div class="metric-label">Pesanan Selesai</div>
        </div>
        """, unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5 = st.tabs([
        "📦 Stok Pabrik",
        "➕ Tambah Produk",
        "🛒 Order Masuk",
        "✅ Konfirmasi",
        "📊 Semua Stok Distributor"
    ])

    # ================= TAB 1 =================
    with tab1:

        df_produk = get_df("""
        SELECT nama,stok,stok_minimum,harga_jual
        FROM produk
        """)

        df_produk["harga_jual"] = df_produk["harga_jual"].apply(
            lambda x: f"Rp {x:,.0f}".replace(",", ".")
        )

        st.dataframe(
            df_produk,
            use_container_width=True,
            hide_index=True
        )

# ================= FOOTER =================

st.markdown("""
<div class="footer">
🌴 © 2026 CV Amal Mulia — OrderStock
</div>
""", unsafe_allow_html=True)
