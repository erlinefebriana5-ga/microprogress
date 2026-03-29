import streamlit as st
import csv
from datetime import datetime
import base64

# ===== CONFIG =====
st.set_page_config(page_title="MicroProgress 🌱", layout="centered")

# ===== STYLE =====
st.markdown("""
<style>
body {
    background-color: #f4f1ec;
}

/* Container */
.block-container {
    max-width: 750px;
}

/* HEADER */
h1 {
    color: #3e3e3e;
}

/* CARD */
.card {
    background-color: #ffffff;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 30px;
    border: 1px solid #eee;
}

/* TITLE */
.title {
    font-size: 26px;
    font-weight: 700;
    color: #2f2f2f;
    margin-bottom: 8px;
}

/* DATE */
.date {
    color: #8c8c8c;
    font-size: 13px;
    margin-bottom: 15px;
}

/* CONTENT */
.content {
    font-size: 16px;
    line-height: 1.8;
    color: #4a4a4a;
    font-family: 'Georgia', serif;
}

/* BUTTON */
.stButton button {
    background-color: #7a8f7b;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 6px 16px;
}

/* EXPANDER */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #5a5a5a;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.title("🌱 MicroProgress")
st.caption("Small steps. Every day.")

st.divider()

# ===== ADMIN INPUT =====
with st.expander("✍️ Tulis Post "):

    judul = st.text_input("Judul")
    isi = st.text_area("Cerita hari ini")
    foto = st.file_uploader("Upload foto 📸", type=["png", "jpg", "jpeg"])

    if st.button("Post 🚀"):
        if judul and isi:

            img_data = ""
            if foto:
                img_data = base64.b64encode(foto.read()).decode()

            with open("microprogress.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now(), judul, isi, img_data])

            st.success("Posted 🔥")

        else:
            st.warning("Isi dulu ya!")

st.divider()
st.markdown("<hr style='border:1px solid #e0ddd7;'>", unsafe_allow_html=True)

# ===== DISPLAY =====
st.subheader("📖 Stories")
st.markdown("<h1 style='font-family: Georgia;'>🌱 MicroProgress</h1>", unsafe_allow_html=True)

try:
    with open("microprogress.csv", "r", encoding="utf-8") as f:
        data = list(csv.reader(f))
        data.reverse()

    for i, row in enumerate(data):

        tanggal, judul, isi, img = row

        # FORMAT DATE
        tgl = datetime.fromisoformat(tanggal)
        tanggal_format = tgl.strftime("%d %B %Y • %H:%M")

        # CARD UI
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

        # DELETE BUTTON
        if st.button("🗑 Hapus", key=f"delete_{i}"):
            data.pop(i)

            with open("microprogress.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(reversed(data))

            st.rerun()

except:
    st.write("Belum ada cerita hari ini 👀")