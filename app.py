import streamlit as st
import csv
from datetime import datetime
import base64

# ===== ADMIN SYSTEM =====
admin_mode = st.query_params.get("admin") == "true"

if admin_mode:
    password = st.text_input("🔐 Admin Login", type="password")
else:
    password = ""

is_admin = admin_mode and (password == "Suryasaputra5")

# ===== CONFIG =====
st.set_page_config(page_title="MicroProgress 🌱", layout="centered")

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

                with open("microprogress.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([str(datetime.now()), judul, isi, img_data])

                st.success("Posted 🔥")
            else:
                st.warning("Isi dulu ya!")

# ===== DISPLAY =====
st.subheader("📖 Stories")

try:
    with open("microprogress.csv", "r", encoding="utf-8") as f:
        original_data = list(csv.reader(f))

    display_data = list(reversed(original_data))

    for i, row in enumerate(display_data):

        if len(row) == 4:
            tanggal, judul, isi, img = row
        else:
            tanggal, judul, isi = row
            img = ""

        tgl = datetime.fromisoformat(tanggal)
        tanggal_format = tgl.strftime('%d %B %Y • %H:%M')

        st.markdown(f"""
        ### {judul}
        *{tanggal_format}*

        {isi}
        """)

        if img:
            st.image(base64.b64decode(img))

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

except:
    st.write("Belum ada cerita hari ini 👀")
