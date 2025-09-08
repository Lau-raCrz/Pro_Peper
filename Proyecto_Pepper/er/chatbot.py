
import streamlit as st
import requests
from gtts import gTTS
import os
import tempfile
import base64

# 🔑 Configuración API
API_KEY = "sk-53751d5c6f344a5dbc0571de9f51313e"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 📩 Función para enviar mensajes
def enviar_mensaje(mensaje, modelo="deepseek-chat"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {       
	 "model": modelo,
         "messages": [
  	{"role": "system","content":"Responde como un experto en temas de innovación tecnológica. " "Tu especialidad son tres áreas clave: " "1) Energía undimotriz inteligente y su impacto en los sistemas digitales, " "2) Robots blandos (soft robotics) y su innovación en los sistemas digitales, " "3) Terapias con exosomas modificados. " "Explica con claridad, ejemplos sencillos y un estilo motivador y cercano. " "Debes enseñar de forma comprensible pero con rigor técnico, " "destacando siempre cómo estas innovaciones se relacionan con los sistemas digitales." }	


            ,
            {"role": "user", "content": mensaje}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error en la API: {result}"

# 🎵 Función para reproducir audio sin barra
def reproducir_audio(archivo):
    with open(archivo, "rb") as f:
        audio_bytes = f.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(
        f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )

# 🧠 Manejo de historial
if "messages" not in st.session_state:
    st.session_state.messages = []


# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    respuesta = enviar_mensaje(prompt)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    with st.chat_message("assistant"):
        st.markdown(respuesta)

        # 🔊 Generar audio invisible
        tts = gTTS(respuesta, lang="es")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            reproducir_audio(tmpfile.name)  # 🎵 Sonará automáticamente sin barra
