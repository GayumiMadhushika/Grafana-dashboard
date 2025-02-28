from influxdb import InfluxDBClient
import random
import time

# Connect to InfluxDB
client = InfluxDBClient(host='localhost', port=8086, database='grafana')

# Function to generate and insert random temperature data
def insert_temperature_data():
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)  # Generate random temperature between 20 and 30
        json_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "location": "room"
                },
                "fields": {
                    "value": temperature
                }
            }
        ]
        client.write_points(json_body)
        print(f"Inserted: {temperature}°C into InfluxDB")
        time.sleep(5)  # Wait for 5 seconds before inserting the next value

# Run the function
if __name__ == "__main__":
    insert_temperature_data()
