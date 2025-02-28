# Grafana Dashboard with MQTT and InfluxDB

## 📖 Project Overview
This project sets up a **Grafana Dashboard** with **MQTT** and **InfluxDB** for data visualization. The dashboard includes **role-based access control** (Admin and Viewer).

## 📌 Features
- **Grafana Dashboard**
- **MQTT Integration** → To send data
- **InfluxDB** → As a data source
- **Docker** → Compose for easy deployment
- **Role-Based Access**
  - **Admin** → Edit & View
  - **Viewer** → Can only View
- **3D Floor Plan Integration**

## 🛠 Setup Instructions

### 1. Install Required Tools
Ensure you have the following installed:
- **Docker & Docker-Compose**
- **Python 3.x** (for MQTT data simulation)

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Grafana-dashboard.git
cd Grafana-dashboard
```

### 3. Run Docker Containers
```bash
docker-compose up -d
```
This command will start **Grafana, MQTT, InfluxDB, and MySQL** in containers. In this project, we only use **Grafana, MQTT, and InfluxDB**. MySQL is included for future modifications.

### 4. Open Grafana in Your Browser
- **URL:** `http://localhost:8000`
- **Login as Admin**

## 🎛 Configure Grafana Dashboard

### **Step 1: Add Data Sources**
- Go to **Grafana → Connections → Data Sources → Add new data source**
- Add the following:
  - **InfluxDB**
  - **MQTT**
  - **MySQL** (optional for future modifications)

### **Step 2: Configure Data Sources**
#### **InfluxDB:**
```
URL: http://influxdb:8086
Database: grafana
User: admin
Password: admin123
```

#### **MQTT:**
```
Type: MQTT
Broker: mqtt://mosquitto
Port: 1883
Topic: sensor/data
```

### **Step 3: Set Roles in Grafana**
- Go to **Administration → Users**
- Click **Invite User**
- Assign **Admin** and **Viewer** roles
- **Access Control:**
  - **Admin** → Full control
  - **Viewer** → Read-only access

### **Step 4: Create a New Dashboard**
- **Go to:** `Dashboards → New Dashboard → Add a New Panel`
- **Name:** "Automated Sensor Dashboard"
- **Click:** "Save Dashboard" and enter a description

### **Step 5: Configure Panels**

#### **Panel 1: Soil Moisture Level**
```
Select → Time series
Data source → InfluxDB
Query → SELECT mean(soil_moisture) FROM sensor_data WHERE time > now() - 6h GROUP BY time(10s)
```

#### **Panel 2: Light Intensity**
```
Select → Time series
Data source → InfluxDB
Query → SELECT mean(Light_intensity) FROM sensor_data WHERE time > now() - 6h GROUP BY time(10s)
```

#### **Panel 3: pH Level**
```
Select → Time series
Data source → InfluxDB
Query → SELECT mean(pH) FROM sensor_data WHERE time > now() - 6h GROUP BY time(10s)
```

#### **Panel 4: Sensor Data (Gauge)**
```
Select → Gauge
Data source → InfluxDB
Query → SELECT time, soil_moisture, light_intensity, pH FROM sensor_data ORDER BY time DESC LIMIT 10
```

#### **Panel 5: 3D Floor Plan**
```
Select → Text
Mode → HTML
Content → <iframe src="/public/interactive_floor.html" width="100%" height="600px" style="border:none;"></iframe>
Data source → InfluxDB
```

> You can customize the panels to enhance visualization.

### **Save Dashboard**
- Click **Save Dashboard** → Enter a name & description

## 🔐 Login Credentials

### **Admin:**
```
Username: admin
Password: admin123
```
> (Ensure your configuration uses this password for consistency)

### **Viewer:**
```
Username: viewer
Password: viewer123
```
> (Ensure your configuration uses this password for consistency)

---

**Now your Grafana dashboard is ready for real-time data visualization!** 

## Author: Gayumi Madhushika Vithanage
