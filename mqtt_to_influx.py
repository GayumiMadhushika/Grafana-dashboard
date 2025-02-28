import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import random
import time  # ✅ For periodic publishing

# 🔹 MQTT Broker Settings
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

# 🔹 InfluxDB Settings
INFLUXDB_ADDRESS = "influxdb"  # ✅ Use Docker service name instead of "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = "grafana"
INFLUXDB_USER = "admin"
INFLUXDB_PASSWORD = "password"

# ✅ Function to Connect to InfluxDB (Handles Errors)
def connect_influx():
    try:
        influx_client = InfluxDBClient(
            INFLUXDB_ADDRESS, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_DATABASE
        )
        print("✅ Connected to InfluxDB")
        return influx_client
    except Exception as e:
        print("❌ InfluxDB Connection Failed:", e)
        return None

# 🔹 Create Initial Connection
influx_client = connect_influx()

# 🔹 Function to Generate Random Sensor Data
def generate_random_data():
    return {
        "para1": round(random.uniform(10, 50), 2),  # Soil Moisture (10% - 50%)
        "para2": round(random.uniform(200, 800), 2),  # Light Intensity (200 - 800)
        "para3": round(random.uniform(5.5, 7.5), 2)  # pH Level (5.5 - 7.5)
    }

# 🔹 Function to Write Data to InfluxDB
def write_to_influx(sensor_data):
    global influx_client
    if not influx_client:
        influx_client = connect_influx()
        if not influx_client:
            print("❌ Skipping InfluxDB Write: No Connection")
            return

    json_body = [
        {
            "measurement": "sensor_data",
            "fields": {
                "soil_moisture": float(sensor_data["para1"]),
                "light_intensity": float(sensor_data["para2"]),
                "pH": float(sensor_data["para3"])
            }
        }
    ]
    try:
        influx_client.write_points(json_body)
        print("✅ Data Written to InfluxDB:", json_body)
    except Exception as e:
        print("❌ InfluxDB Write Error:", e)

# 🔹 MQTT Callback (When New Data Arrives)
def on_message(client, userdata, msg):
    try:
        # ✅ Simulate MQTT message with random values
        payload = {"sensor_data": [generate_random_data()]}

        print("Simulated payload:", json.dumps(payload, indent=2))  # Debugging output

        # Extract first sensor entry
        latest_data = payload["sensor_data"][0]

        # Debugging output
        print(f"Extracted Data - Soil Moisture: {latest_data['para1']}, Light: {latest_data['para2']}, pH: {latest_data['para3']}")

        # ✅ Write data to InfluxDB
        write_to_influx(latest_data)

    except Exception as e:
        print("Error in on_message:", e)

# ✅ Connect to MQTT Broker
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.subscribe(MQTT_TOPIC)
    print(f"📡 Listening for MQTT messages on topic: {MQTT_TOPIC}")
    mqtt_client.loop_start()  # ✅ Runs in the background instead of blocking
except Exception as e:
    print("❌ MQTT Connection Failed:", e)

# ✅ **Automatically Publish Data Every 5 Seconds**
while True:
    try:
        simulated_data = generate_random_data()
        json_payload = json.dumps({"sensor_data": [simulated_data]})

        # ✅ Publish simulated data to the MQTT broker
        result = mqtt_client.publish(MQTT_TOPIC, json_payload)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print("MQTT Publish Failed")

        print(" Published to MQTT:", json_payload)

        # ✅ Write directly to InfluxDB
        write_to_influx(simulated_data)

    except Exception as e:
        print("❌ Error in publishing data:", e)

    time.sleep(5)  # ✅ Wait for 5 seconds before sending new data
