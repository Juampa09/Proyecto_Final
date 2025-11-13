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

client1 = paho.Client("multimodal_streamlit")
client1.on_publish = on_publish
client1.on_message = on_message
client
