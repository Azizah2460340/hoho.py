# ==================== PABRIK ====================
if role == "pabrik":

    # ===== METRIC =====
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

    # ===== TABS =====
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 Manajemen Stok",
        "➕ Tambah Produk",
        "🛒 Order Masuk",
        "✅ Konfirmasi Pesanan",
        "🚚 Stok Distributor"
    ])

    # ==================== TAB 1 ====================
    with tab1:

        st.markdown('<div class="white-card">', unsafe_allow_html=True)

        st.subheader("📦 Stok Produk")

        df_produk = get_df("""
            SELECT nama, stok, stok_minimum, harga_jual
            FROM produk
        """)

        st.dataframe(
            df_produk,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("➕ Tambah Stok")

        pilih = st.selectbox(
            "Pilih Produk",
            df_produk['nama']
        )

        stok_tambah = st.number_input(
            "Jumlah stok ditambahkan",
            min_value=0,
            step=1
        )

        if st.button("Tambah Stok"):

            run_query(
                "UPDATE produk SET stok = stok + ? WHERE nama = ?",
                (stok_tambah, pilih)
            )

            st.success("Stok berhasil ditambahkan")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 2 ====================
    with tab2:

        st.markdown('<div class="white-card">', unsafe_allow_html=True)

        st.subheader("➕ Tambah Produk Baru")

        with st.form("tambah_produk"):

            nama_produk = st.text_input("Nama Produk")

            stok_awal = st.number_input(
                "Stok Awal",
                min_value=0,
                step=1
            )

            stok_min = st.number_input(
                "Stok Minimum",
                min_value=0,
                value=50
            )

            harga = st.number_input(
                "Harga Jual",
                min_value=0,
                step=1000
            )

            submit_produk = st.form_submit_button(
                "Tambah Produk"
            )

            if submit_produk:

                cek = get_df(
                    "SELECT * FROM produk WHERE nama=?",
                    (nama_produk,)
                )

                if cek.empty:

                    run_query("""
                        INSERT INTO produk
                        (nama, stok, stok_minimum, harga_jual)
                        VALUES (?,?,?,?)
                    """, (
                        nama_produk,
                        stok_awal,
                        stok_min,
                        harga
                    ))

                    st.success("Produk berhasil ditambahkan")
                    st.rerun()

                else:
                    st.error("Produk sudah ada")

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 3 ====================
    with tab3:

        st.markdown('<div class="white-card">', unsafe_allow_html=True)

        st.subheader("🛒 Order Masuk")

        df_order = get_df("""
            SELECT *
            FROM pesanan
            WHERE status='Menunggu Konfirmasi'
        """)

        if df_order.empty:

            st.info("Tidak ada order masuk")

        else:

            for _, row in df_order.iterrows():

                with st.expander(
                    f"{row['produk']} - {row['klien']}"
                ):

                    st.write(f"Jumlah : {row['jumlah']}")
                    st.write(f"Tanggal : {row['tanggal_masuk']}")

                    colA, colB = st.columns(2)

                    with colA:

                        if st.button(
                            "✅ Setujui",
                            key=f"ok_{row['id']}"
                        ):

                            run_query("""
                                UPDATE pesanan
                                SET status='Diproses'
                                WHERE id=?
                            """, (row['id'],))

                            st.success("Pesanan disetujui")
                            st.rerun()

                    with colB:

                        if st.button(
                            "❌ Tolak",
                            key=f"tolak_{row['id']}"
                        ):

                            run_query("""
                                UPDATE pesanan
                                SET status='Ditolak'
                                WHERE id=?
                            """, (row['id'],))

                            st.error("Pesanan ditolak")
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 4 ====================
    with tab4:

        st.markdown('<div class="white-card">', unsafe_allow_html=True)

        st.subheader("✅ Konfirmasi Hasil Produksi")

        df_konfirmasi = get_df("""
            SELECT *
            FROM pesanan
            WHERE jenis_pesanan='makloon'
        """)

        if df_konfirmasi.empty:

            st.info("Belum ada pesanan")

        else:

            for _, row in df_konfirmasi.iterrows():

                with st.expander(
                    f"{row['produk']} - {row['klien']}"
                ):

                    st.write(f"Jumlah : {row['jumlah']}")
                    st.write(f"Status : {row['status']}")

                    if row['status'] != "Selesai":

                        if st.button(
                            "✅ Tandai Selesai",
                            key=f"done_{row['id']}"
                        ):

                            run_query("""
                                UPDATE pesanan
                                SET status='Selesai'
                                WHERE id=?
                            """, (row['id'],))

                            st.success("Pesanan selesai")
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ==================== TAB 5 ====================
    with tab5:

        st.markdown('<div class="white-card">', unsafe_allow_html=True)

        st.subheader("🚚 Stok Distributor")

        df_dist = get_df("""
            SELECT
                klien,
                produk,
                jumlah,
                status
            FROM pesanan
            WHERE jenis_pesanan='order_stok'
        """)

        if df_dist.empty:

            st.info("Belum ada distribusi stok")

        else:

            st.dataframe(
                df_dist,
                use_container_width=True,
                hide_index=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# ==================== KLIEN ====================
elif role == "klien":

    st.markdown('<div class="white-card">', unsafe_allow_html=True)

    st.subheader("🤝 Portal Klien")

    tabC, tabD = st.tabs([
        "🏭 Pesan Makloon",
        "📋 Status Pesanan"
    ])

    # ==================== PESAN MAKLOON ====================
    with tabC:

        st.markdown("### Form Pemesanan Makloon")

        with st.form("form_klien_makloon"):

            nama_produk = st.text_input(
                "Nama Produk",
                placeholder="Contoh: Sari Kurma Premium"
            )

            jumlah = st.number_input(
                "Jumlah Produksi",
                min_value=1,
                step=1
            )

            asal_pt = st.text_input(
                "Asal PT / Brand",
                placeholder="Contoh: PT Herbal Nusantara"
            )

            catatan = st.text_area(
                "Catatan Tambahan",
                placeholder="Kemasan, rasa, ukuran, dll"
            )

            submit = st.form_submit_button(
                "Kirim Pesanan"
            )

            if submit:

                if nama_produk and asal_pt:

                    run_query("""
                        INSERT INTO pesanan
                        (klien, produk, jumlah, status,
                         tanggal_masuk, jenis_pesanan, created_by)

                        VALUES (?,?,?,?,?,?,?)
                    """, (
                        asal_pt,
                        nama_produk,
                        jumlah,
                        "Menunggu Konfirmasi",
                        datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "makloon",
                        username
                    ))

                    st.success(
                        "Pesanan berhasil dikirim"
                    )

                    st.rerun()

                else:
                    st.error("Lengkapi semua data")

    # ==================== STATUS ====================
    with tabD:

        st.markdown("### Status Pesanan")

        df = get_df("""
            SELECT
                produk,
                jumlah,
                status,
                tanggal_masuk
            FROM pesanan
            WHERE created_by=?
            ORDER BY id DESC
        """, (username,))

        if df.empty:

            st.info("Belum ada pesanan")

        else:

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
