import streamlit as st
import sys, os, tempfile
from gtts import gTTS
import requests
import os
import tempfile
import base64


# 🎵 Función para reproducir audio invisible (igual que en tu chatbot original)
def reproducir_audio(archivo):
    import base64
    with open(archivo, "rb") as f:
        audio_bytes = f.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    import streamlit as st
    st.markdown(
        f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )




# --- Configurar rutas para poder importar chatbot desde ../er ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ER_PATH = os.path.join(ROOT, "er")
if ER_PATH not in sys.path:
    sys.path.insert(0, ER_PATH)

# Importar chatbot
try:
    from chatbot import enviar_mensaje
except Exception as e:
    enviar_mensaje = None
    st.error(f"No se pudo importar chatbot.py: {e}")

# --- Configuración de la página ---
st.set_page_config(layout="wide", page_title="Pepper Dashboard")
st.markdown(
    "<h2 style='text-align:center; color:white; background-color:orange;'>"
    "📢 PRESENTANDO NOVEDADES TECNOLÓGICAS CON PEPPER</h2>",
    unsafe_allow_html=True,
)
st.write("")

# --- Layout con tres columnas ---
col1, col2, col3 = st.columns([1.2, 2, 1.5])

# ==============================
# 🎥 Columna Izquierda: Videos
# ==============================
with col1:
    st.markdown("### 🎬 Videos de Pepper")

    videos = {
        "Video 1": "Video_1.mp4",
        "Video 2": "Video_2.mp4",
        "Video 3": "Video_3.mp4"
    }

    seleccion = st.selectbox("Elige un video:", list(videos.keys()))

    if st.button("▶️ Start Video"):
        video_path = os.path.join(ROOT, videos[seleccion])
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.error(f"No se encontró {videos[seleccion]} en la carpeta principal.")

# ==============================
# 📚 Columna Centro: Novedades
# ==============================
with col2:
    st.markdown("### 🚀 Novedades Tecnológicas")

    st.subheader("1️⃣ Energía undimotriz inteligente")
    st.info("Aprovecha el movimiento de las olas para generar energía limpia, integrándose con sistemas digitales que optimizan la producción y el control en tiempo real.")

    st.subheader("2️⃣ Robots blandos (Soft Robotics)")
    st.info("Robots inspirados en organismos vivos, hechos con materiales flexibles. Los sistemas digitales permiten control de movimiento preciso y aplicaciones médicas innovadoras.")

    st.subheader("3️⃣ Terapias con exosomas modificados")
    st.info("Exosomas alterados genéticamente aplicados como terapias innovadoras, con monitoreo digital para evaluar y mejorar resultados en salud.")

# ==============================
# 🤖 Columna Derecha: Chatbot
# ==============================
with col3:
    st.subheader("🤖 Chatbot de Confianza")

    # Historial en sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada del usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if enviar_mensaje:
            respuesta = enviar_mensaje(prompt)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

            with st.chat_message("assistant"):
                st.markdown(respuesta)

                # 🔊 Generar audio invisible
                try:
                    tts = gTTS(respuesta, lang="es")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                        tts.save(tmpfile.name)
                        reproducir_audio(tmpfile.name)  # 🎵 Se reproduce sin barra
                except Exception as e:
                    st.warning("No se pudo generar audio TTS: " + str(e))
        else:
            st.error("⚠️ El chatbot no está disponible.")
