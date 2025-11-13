import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("WhiteKnuckle")
client1.on_message = on_message



st.title("Control manual")
st.subheader("Botones para encender la luz")

if st.button('ON'):
    act1="ON"
    client1= paho.Client("DeepRock")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("Aristizabal", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('OFF'):
    act1="OFF"
    client1= paho.Client("bloodborne")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("Aristizabal", message)
  
    
else:
    st.write('')

values = st.slider('Posicón de la ventana',0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1= paho.Client("DOOM")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("Aristizabal", message)
    
 
else:
    st.write('')
