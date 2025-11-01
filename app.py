import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Analisis Trading AI",
    page_icon="📈",
    layout="centered"
)

# --- Judul di Halaman Aplikasi ---
st.title("Analisis Indikator Trading AI 📈")
st.markdown("Unggah screenshot chart Anda, dan AI (Gemini) akan menganalisisnya.")

# --- ======================================================= ---
# ---                 BAGIAN TES DEBUGGING                    ---
# --- ======================================================= ---

# PERINGATAN: JANGAN UPLOAD FILE INI KE GITHUB
# TEMPEL (PASTE) KEY BARU ANDA LANGSUNG DI SINI:
api_key = "gen-lang-client-0280181801" 

# Kita tidak lagi menggunakan st.secrets untuk tes ini
try:
    if not api_key or api_key == "gen-lang-client-0280181801":
        st.error("Harap masukkan API key Anda langsung ke dalam kode app.py di baris 24.")
        st.stop()
        
    genai.configure(api_key=api_key)
    
except Exception as e:
    # Error ini akan muncul jika key-nya valid TAPI API-nya tidak aktif
    st.error(f"Gagal mengkonfigurasi Google AI. Error: {e}")
    st.stop()

# --- ======================================================= ---
# ---                AKHIR BAGIAN TES DEBUGGING               ---
# --- ======================================================= ---


# --- Konfigurasi Model AI ---
try:
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
except Exception as e:
    st.error(f"Gagal memuat model Gemini. Error: {e}")
    st.stop()


# --- Sistem Prompt (Instruksi Permanen untuk AI) ---
system_prompt = """Anda adalah seorang analis teknikal trading AI yang ahli. 
Tugas utama Anda adalah menganalisis gambar screenshot chart trading yang diberikan dan secara proaktif mengidentifikasi pola indikator untuk memprediksi sinyal bullish atau bearish.
Pengguna akan memberikan konteks timeframe (misal: '1 Menit', '1 Jam', '1 Hari'). Gunakan informasi timeframe ini untuk menyempurnakan analisis Anda. Timeframe yang lebih pendek (scalping) memiliki implikasi yang berbeda dari timeframe harian (swing).

Fokus pada:
1.  **Analisis Indikator:** Cari sinyal di RSI (overbought, oversold, divergence), MACD (crossover, divergence), Moving Averages (golden cross, death cross), Bollinger Bands (squeeze, breakout).
2.  **Analisis Pola Candlestick:** Identifikasi pola reversal atau continuation (doji, hammer, engulfing).
3.  **Analisis Pola Chart:** Cari pola yang lebih besar (double top/bottom, head and shoulders, triangles, wedges).
4.  **Volume:** Analisis volume untuk mengkonfirmasi kekuatan sinyal.

**PENTING:** Jika ada pola chart yang jelas atau level support/resistance yang terlihat, coba identifikasi potensi target pergerakan harga atau level penting dalam analisis Anda. Namun, **TEGASKAN BAHWA INI SANGAT SPEKULATIF DAN HANYA BERDASARKAN VISUAL, BUKAN DATA REAL-TIME.** AI tidak memiliki akses ke data harga langsung atau fundamental pasar.

Setelah menganalisis semua ini, berikan kesimpulan prediksi: **BULLISH**, **BEARISH**, atau **NETRAL/SIDEWAYS**.
Jelaskan alasan Anda secara ringkas dan jelas berdasarkan apa yang Anda lihat di gambar.

Selalu akhiri dengan peringatan bahwa ini bukan nasihat keuangan (DYOR).
Jawab dalam Bahasa Indonesia.
"""

# --- UI (Tampilan) Aplikasi Streamlit ---

# 1. Input Gambar
uploaded_file = st.file_uploader("Pilih Gambar Screenshot", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 2. Pratinau Gambar
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar yang Diunggah", use_column_width=True)
    except Exception as e:
        st.error(f"Gagal memuat gambar: {e}")
        st.stop()
    
    # 3. Pilih Timeframe
    timeframe = st.selectbox(
        "Pilih Timeframe Chart",
        ("1 Menit", "5 Menit", "15 Menit", "30 Menit", "1 Jam", "4 Jam", "1 Hari", "1 Minggu", "Lainnya / Tidak Tahu"),
        index=4  # Default pilihan ke '1 Jam'
    )

    # 4. Tombol Analisis
    if st.button("Analisis Sekarang"):
        with st.spinner("AI sedang menganalisis gambar Anda..."):
            try:
                # --- Versi perbaikan untuk library lama ---
                user_task = f"Lakukan analisis prediktif (bullish/bearish) pada gambar chart ini. Konteks timeframe adalah: {timeframe}."
                full_prompt = f"{system_prompt}\n\n---\n\nPERINTAH SPESIFIK:\nGambar terlampir.\n{user_task}"
                
                contents = [
                    {
                        "role": "user",
                        "parts": [
                            {"text": full_prompt}, 
                            {"inline_data": {
                                "mime_type": uploaded_file.type,
                                "data": uploaded_file.getvalue()
                            }}
                        ]
                    }
                ]
                
                response = model.generate_content(contents)
                # --- Akhir versi perbaikan ---
                
                # 5. Tampilkan Hasil
                st.subheader("Hasil Analisis AI:")
                st.markdown(response.text)
                
                st.warning(
                    "**Peringatan Penting:** Prediksi target harga atau pergerakan spesifik oleh AI hanya berdasarkan "
                    "analisis visual gambar statis dan sangat spekulatif. JANGAN gunakan ini sebagai dasar keputusan "
                    "trading Anda. AI TIDAK memiliki akses ke data harga real-time atau informasi pasar terkini.\n\n"
                    "*Ini adalah analisis AI dan bukan nasihat keuangan. Selalu lakukan riset Anda sendiri (DYOR).*"
                )

            except Exception as e:
                # Jika error 'API key not valid' MUNCUL LAGI, berarti key Anda 100% salah.
                st.error(f"Terjadi kesalahan saat menghubungi API Gemini: {e}")
else:
    st.info("Silakan unggah gambar untuk memulai analisis.")

