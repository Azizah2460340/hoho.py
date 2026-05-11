import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="OrderStock - CV Amal Mulia",
    layout="wide",
    page_icon="🌴",
    initial_sidebar_state="expanded"
)

# ==================== CSS ====================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family: 'Poppins', sans-serif;
}

/* ================= MAIN ================= */

.stApp{
    background:
    linear-gradient(
        135deg,
        #04281c 0%,
        #0b5136 45%,
        #166845 100%
    );
    color:white;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #031d15 0%,
        #0d4b32 100%
    );

    border-right:
    1px solid rgba(255,255,255,0.08);
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
        rgba(255,255,255,0.03)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    padding:2rem;

    border-radius:30px;

    backdrop-filter: blur(10px);

    box-shadow:
    0 10px 30px rgba(0,0,0,0.25);

    margin-bottom:1.5rem;
}

.hero-title{
    font-size:3rem;
    font-weight:800;
    line-height:1.1;
    color:white;
}

.hero-gold{
    color:#f4c76b;
}

.hero-sub{
    margin-top:12px;
    font-size:1rem;
    color:#d7f5e2;
}

/* ================= LOGIN CARD ================= */

.login-card{

    background:
    linear-gradient(
        180deg,
        rgba(255,255,255,0.96),
        rgba(255,255,255,0.90)
    );

    border-radius:30px;

    padding:2rem;

    color:#163a2b;

    box-shadow:
    0 12px 35px rgba(0,0,0,0.20);

    border:
    1px solid rgba(255,255,255,0.25);
}

/* ================= WHITE CARD ================= */

.white-card{

    background:
    linear-gradient(
        180deg,
        rgba(255,255,255,0.97),
        rgba(255,255,255,0.92)
    );

    border-radius:28px;

    padding:1.5rem;

    color:#17382c;

    box-shadow:
    0 8px 25px rgba(0,0,0,0.18);

    margin-bottom:1rem;

    border:
    1px solid rgba(255,255,255,0.20);
}

/* ================= METRIC ================= */

.metric-box{

    background:
    linear-gradient(
        135deg,
        #fff8ea,
        #ffe7b0
    );

    border-radius:26px;

    padding:1.5rem;

    text-align:center;

    box-shadow:
    0 8px 20px rgba(0,0,0,0.15);

    border:
    2px solid rgba(244,199,107,0.4);
}

.metric-value{
    font-size:2.5rem;
    font-weight:800;
    color:#0d4b32;
}

.metric-label{
    color:#6e4d11;
    font-weight:600;
}

/* ================= BUTTON ================= */

.stButton button{

    background:
    linear-gradient(
        135deg,
        #c98d25,
        #f4c76b
    ) !important;

    color:#17382c !important;

    border:none !important;

    border-radius:18px !important;

    padding:0.7rem 1.4rem !important;

    font-weight:700 !important;

    transition:0.3s !important;
}

.stButton button:hover{

    transform:scale(1.03);

    box-shadow:
    0 8px 18px rgba(244,199,107,0.4);
}

/* ================= FORM BUTTON ================= */

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
}

/* ================= TABS ================= */

.stTabs [data-baseweb="tab-list"]{
    gap:10px;
}

.stTabs [data-baseweb="tab"]{

    background:
    rgba(255,255,255,0.08);

    border-radius:20px;

    color:white;

    padding:12px 20px;

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

/* ================= INPUT ================= */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]{

    border-radius:18px !important;

    border:
    2px solid #ecd7ab !important;
}

/* ================= DATAFRAME ================= */

[data-testid="stDataFrame"]{

    background:white;

    border-radius:24px;

    padding:10px;

    overflow:hidden;
}

/* ================= ALERT ================= */

.stAlert{
    border-radius:20px;
}

/* ================= FOOTER ================= */

.footer{

    text-align:center;

    margin-top:2rem;

    color:#d6efe0;

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

def init_db():

    with get_connection() as conn:

        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS produk(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT UNIQUE,
            stok INTEGER,
            stok_minimum INTEGER,
            harga_jual INTEGER
        )
        """)

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

        c.execute("""
        CREATE TABLE IF NOT EXISTS stok_distributor(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distributor TEXT,
            produk TEXT,
            stok INTEGER
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
        """)

        c.execute("SELECT COUNT(*) FROM users")

        if c.fetchone()[0] == 0:

            users = [
                ("pabrik","pabrik123","pabrik"),
                ("distributor1","dist123","distributor"),
                ("distributor2","dist123","distributor"),
                ("klien1","klien123","klien")
            ]

            c.executemany(
                "INSERT INTO users VALUES (?,?,?)",
                users
            )

        c.execute("SELECT COUNT(*) FROM produk")

        if c.fetchone()[0] == 0:

            produk = [
                ("Sari Kurma Premium",500,50,35000),
                ("Sari Kurma Herbal",300,50,40000),
                ("Sari Kurma Lambung",250,50,45000),
                ("Sari Kurma Al-Jazira",600,50,30000)
            ]

            c.executemany("""
            INSERT INTO produk
            (nama,stok,stok_minimum,harga_jual)
            VALUES (?,?,?,?)
            """, produk)

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

# ==================== SESSION ====================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# =========================================================
# ==================== LOGIN PAGE =========================
# =========================================================

if not st.session_state.authenticated:

    st.markdown("""
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

    menu = st.radio(
        "",
        ["Masuk","Daftar"],
        horizontal=True
    )

    c1,c2,c3 = st.columns([1,2,1])

    with c2:

        st.markdown("""
        <div class="login-card">
        """, unsafe_allow_html=True)

        if menu == "Masuk":

            with st.form("login"):

                st.subheader("🔐 Login")

                u = st.text_input("Username")

                p = st.text_input(
                    "Password",
                    type="password"
                )

                submit = st.form_submit_button(
                    "Masuk"
                )

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

                submit = st.form_submit_button(
                    "Daftar"
                )

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

                        st.success("Akun berhasil dibuat")

                    else:
                        st.error("Username sudah ada")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# =========================================================
# ==================== USER SESSION =======================
# =========================================================

role = st.session_state.role
username = st.session_state.username

# ==================== SIDEBAR ====================

with st.sidebar:

    st.markdown(f"""
    # 🌴 OrderStock

    ### 👤 {username}

    Role :
    **{role.upper()}**
    """)

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.authenticated = False

        st.rerun()

# ==================== HEADER ====================

st.markdown(f"""
<div class="hero-box">

<div class="hero-title">
DASHBOARD
<span class="hero-gold">{role.upper()}</span>
</div>

<div class="hero-sub">
{datetime.now().strftime('%A, %d %B %Y')}
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# ==================== ROLE PABRIK ========================
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
            <div class="metric-label">
            Total Stok
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{total_order}</div>
            <div class="metric-label">
            Order Pending
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{selesai}</div>
            <div class="metric-label">
            Pesanan Selesai
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    tab1,tab2,tab3 = st.tabs([
        "📦 Produk",
        "🛒 Pesanan",
        "📊 Distributor"
    ])

    # ================= TAB PRODUK =================

    with tab1:

        st.markdown("""
        <div class="white-card">
        <h3>📦 Data Produk</h3>
        </div>
        """, unsafe_allow_html=True)

        df_produk = get_df("""
        SELECT nama,stok,harga_jual
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

    # ================= TAB PESANAN =================

    with tab2:

        st.markdown("""
        <div class="white-card">
        <h3>🛒 Pesanan Masuk</h3>
        </div>
        """, unsafe_allow_html=True)

        df_order = get_df("""
        SELECT produk,klien,jumlah,status
        FROM pesanan
        """)

        st.dataframe(
            df_order,
            use_container_width=True,
            hide_index=True
        )

    # ================= TAB DISTRIBUTOR =================

    with tab3:

        st.markdown("""
        <div class="white-card">
        <h3>📊 Data Distributor</h3>
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
            "Stok":[20,45]
        })

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# ==================== ROLE DISTRIBUTOR ===================
# =========================================================

elif role == "distributor":

    tab1,tab2 = st.tabs([
        "📦 Produk",
        "🛒 Order"
    ])

    with tab1:

        st.markdown("""
        <div class="white-card">
        <h3>📦 Produk Tersedia</h3>
        </div>
        """, unsafe_allow_html=True)

        df = get_df("""
        SELECT nama,stok,harga_jual
        FROM produk
        """)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    with tab2:

        st.markdown("""
        <div class="white-card">
        <h3>🛒 Order Produk</h3>
        </div>
        """, unsafe_allow_html=True)

        with st.form("order_produk"):

            produk = st.selectbox(
                "Pilih Produk",
                get_df(
                    "SELECT nama FROM produk"
                )["nama"]
            )

            jumlah = st.number_input(
                "Jumlah",
                min_value=1
            )

            submit = st.form_submit_button(
                "Kirim Order"
            )

            if submit:

                st.success("Order berhasil dikirim")

# =========================================================
# ==================== ROLE KLIEN =========================
# =========================================================

elif role == "klien":

    st.markdown("""
    <div class="white-card">
    <h3>🏭 Form Pesanan Makloon</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.form("makloon"):

        produk = st.text_input(
            "Nama Produk"
        )

        jumlah = st.number_input(
            "Jumlah Produksi",
            min_value=1
        )

        catatan = st.text_area(
            "Catatan"
        )

        submit = st.form_submit_button(
            "Kirim Pesanan"
        )

        if submit:
            st.success("Pesanan berhasil dikirim")

# ==================== FOOTER ====================

st.markdown("""
<div class="footer">
🌴 © 2026 CV Amal Mulia — Premium Distribution System
</div>
""", unsafe_allow_html=True)
