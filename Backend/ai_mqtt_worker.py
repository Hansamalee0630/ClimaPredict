import paho.mqtt.client as mqtt
import json
import joblib
import pandas as pd

# --- CONFIGURATION ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC_SUBSCRIBE = "sliit/climapredict/hansa_node_1"
TOPIC_PUBLISH = "sliit/climapredict/hansa_node_1/ai_feedback"

# --- LOAD AI MODELS ---
print("Loading AI Models...")
try:
    anomaly_model = joblib.load('anomaly_model.pkl')
    forecast_model = joblib.load('forecast_model.pkl')
    print("✅ AI Models Ready. Listening to hardware...")
except Exception as e:
    print(f"⚠️ Error: Run advanced_ml.py first! {e}")
    exit()

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to HiveMQ! Subscribed to {TOPIC_SUBSCRIBE}")
        client.subscribe(TOPIC_SUBSCRIBE)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        
        # Ensure sensor is warmed up before running AI
        if payload.get("ens160", {}).get("status") == "warming_up":
            client.publish(TOPIC_PUBLISH, "WARMUP")
            return

        # Extract data
        temp = payload["dht22"]["temperature"]
        hum = payload["dht22"]["humidity"]
        pressure = payload["bmp280"]["pressure_hpa"]
        co2 = payload["ens160"]["eco2"]
        
        if co2 is not None:
            # 1. Anomaly Detection
            df_anomaly = pd.DataFrame([[temp, hum, co2]], columns=['temperature', 'humidity', 'eco2'])
            is_anomaly = anomaly_model.predict(df_anomaly)[0] == -1
            
            # 2. Future Forecast (1-Hour)
            df_forecast = pd.DataFrame([[temp, hum, pressure, co2]], columns=['temperature', 'humidity', 'pressure', 'eco2'])
            predicted_co2 = forecast_model.predict(df_forecast)[0]
            
            # 3. AI Decision Engine
            if is_anomaly or predicted_co2 >= 1000:
                command = "DANGER"
            elif predicted_co2 >= 700:
                command = "WARNING"
            else:
                command = "SAFE"
                
            print(f"Current CO2: {co2} | Predicted: {predicted_co2:.1f} | Command Sent: {command}")
            client.publish(TOPIC_PUBLISH, command)

    except Exception as e:
        pass # Ignore malformed data

# --- START WORKER ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()