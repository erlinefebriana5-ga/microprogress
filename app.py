# ===== DISPLAY =====
st.subheader("📖 Stories")
st.markdown("<h1 style='font-family: Georgia;'>🌱 MicroProgress</h1>", unsafe_allow_html=True)

try:
    with open("microprogress.csv", "r", encoding="utf-8") as f:
        original_data = list(csv.reader(f))

    # untuk tampilan (dibalik)
    display_data = list(reversed(original_data))

    for i, row in enumerate(display_data):

        # handle data lama & baru
        if len(row) == 4:
            tanggal, judul, isi, img = row
        else:
            tanggal, judul, isi = row
            img = ""

        # FORMAT DATE
        tgl = datetime.fromisoformat(tanggal)
        tanggal_format = tgl.strftime('%d %B %Y • %H:%M')

        # CARD
        st.markdown(f"""
        <div class="card">
            <div class="title">{judul}</div>
            <div class="date">{tanggal_format}</div>
            <div class="content">{isi}</div>
        </div>
        """, unsafe_allow_html=True)

        # IMAGE
        if img:
            st.image(base64.b64decode(img))

        # DELETE (AMAN)
        if is_admin:
    if st.button("🗑 Hapus", key=f"delete_{i}"):

        with open("microprogress.csv", "r", encoding="utf-8") as f:
            original_data = list(csv.reader(f))

        original_index = len(original_data) - 1 - i

        if 0 <= original_index < len(original_data):
            original_data.pop(original_index)

            with open("microprogress.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(original_data)

        st.rerun()
        writer.writerow([str(datetime.now()), judul, isi, img_data])

except:
    st.write("Belum ada cerita hari ini 👀")
