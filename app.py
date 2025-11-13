import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json

# MQTT setup
broker = "broker.mqttdashboard.com"
port = 1883
message_received = ""

def on_publish(client, userdata, result):
    print("Dato publicado")

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.session_state["mqtt_msg"] = message_received

client1 = paho.Client("Proyecto_Final01")
client1.on_publish = on_publish
client1.on_message = on_message
client1.connect(broker, port)
client1.subscribe("pomodoro")
client1.loop_start()

# Streamlit UI
st.set_page_config(page_title="Asistente Multimodal", layout="centered")
st.title("🧠 Asistente Multimodal")
st.subheader("🎙️ Control por voz + Temporizador Pomodoro")

image = Image.open("speak.jpg")
st.image(image, width=200)

st.write("Toca el botón y habla")

# Botón de voz
stt_button = Button(label="🎤 Inicio", width=200)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# Publicar comando de voz
if result and "GET_TEXT" in result:
    comando = result.get("GET_TEXT").strip()
    st.write(f"🗣️ Comando recibido: {comando}")
    mensaje = json.dumps({"gesto": comando})
    client1.publish("Aristizabal", mensaje)

# Temporizador Pomodoro
if "mqtt_msg" in st.session_state and st.session_state["mqtt_msg"] == "pomodoro_start":
    st.success("🍅 Pomodoro iniciado: 5 minutos")
    with st.empty():
        for i in range(25 * 60, 0, -1):
            mins, secs = divmod(i, 60)
            st.metric("⏳ Tiempo restante", f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        st.success("✅ Pomodoro terminado")
        client1.publish("Aristizabal", "pomodoro_end")
        st.session_state["mqtt_msg"] = ""
