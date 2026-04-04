import streamlit as st
import csv
from datetime import datetime
import base64

# ===== CONFIG (HARUS PALING ATAS) =====
st.set_page_config(page_title="MicroProgress 🌱", layout="centered")

# ===== LOAD DATA KE SESSION =====
if "data" not in st.session_state:
    try:
        with open("microprogress.csv", "r", encoding="utf-8") as f:
            st.session_state.data = list(csv.reader(f))
    except:
        st.session_state.data = []

# ===== ADMIN SYSTEM =====
admin_mode = st.query_params.get("admin") == "true"

if admin_mode:
    password = st.text_input("🔐 Admin Login", type="password")
else:
    password = ""

is_admin = admin_mode and (password == "Suryasaputra5")

# ===== HEADER =====
st.title("🌱 MicroProgress")
st.caption("Small steps. Every day.")
st.markdown("<hr style='border:1px solid #e5e2dc;'>", unsafe_allow_html=True)

# ===== ADMIN INPUT =====
if is_admin:
    with st.expander("✍️ Tulis Post"):

        judul = st.text_input("Judul")
        isi = st.text_area("Cerita hari ini")
        foto = st.file_uploader("Upload foto 📸", type=["png","jpg","jpeg"])

        if st.button("Post 🚀"):
            if judul and isi:

                img_data = ""
                if foto:
                    img_data = base64.b64encode(foto.read()).decode()

                new_row = [str(datetime.now()), judul, isi, img_data]

                # 👉 SIMPAN KE SESSION (INI YANG DIPAKAI DISPLAY)
                st.session_state.data.append(new_row)

                # 👉 SIMPAN KE CSV (backup)
                try:
                    with open("microprogress.csv", "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(new_row)
                except:
                    pass

                st.success("Posted 🔥")
                st.rerun()

            else:
                st.warning("Isi dulu ya!")

# ===== DISPLAY =====
st.subheader("📖 Stories")

if len(st.session_state.data) == 0:
    st.write("Belum ada cerita hari ini 👀")

else:
    display_data = list(reversed(st.session_state.data))

    for i, row in enumerate(display_data):

        # HANDLE FORMAT
        if len(row) == 4:
            tanggal, judul, isi, img = row
        else:
            tanggal, judul, isi = row
            img = ""

        # FORMAT DATE (AMAN)
        try:
            tgl = datetime.fromisoformat(tanggal)
            tanggal_format = tgl.strftime('%d %B %Y • %H:%M')
        except:
            tanggal_format = tanggal

        # CARD
        st.markdown(f"""
        ### {judul}
        *{tanggal_format}*

        {isi}
        """)

        # IMAGE
        if img:
            try:
                st.image(base64.b64decode(img))
            except:
                pass

        # ===== DELETE =====
        if is_admin:
            if st.button("🗑 Hapus", key=f"delete_{i}"):

                # mapping index ke original
                original_index = len(st.session_state.data) - 1 - i

                if 0 <= original_index < len(st.session_state.data):
                    st.session_state.data.pop(original_index)

                    # update CSV (optional)
                    try:
                        with open("microprogress.csv", "w", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerows(st.session_state.data)
                    except:
                        pass

                st.rerun()
