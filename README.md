# Scrape2Dashboard-iPhone-Analytics-System
---
End-to-end data engineering and analytics project that scrapes iPhone listings, transforms and standardizes the data, stores it in ClickHouse, and delivers pricing and demand insights using Apache Superset dashboards.

---

# 📌 Project Overview
This repository contains:

- Scrapy spider for web scraping
- Pandas transformation script
- Cleaned dataset
- ClickHouse table schema
- Dockerized Superset setup
- Dashboard creation workflow
Everything runs from this single project repository.

---

# 🏗️ Architecture

Scrapy  
↓  
Raw CSV  
↓  
Pandas Transformation  
↓  
ClickHouse  
↓  
Apache Superset  
↓  
Dashboard
---

# 🛠️ Tech Stack

- Python
- Scrapy
- Pandas
- NumPy
- ClickHouse
- Apache Superset
- Docker
---

# 📂 Project Structure

```
iPhone-Pricing-Demand-Analysis/
│
├── scrapy_project/
│   ├── scrapy.cfg
│   └── iphones/
│       ├── spiders/
│       │   └── flipmobiles.py
│
├── transformation/
│   └── transform_script.py
│
├── data/
│   ├── Iphones.csv
│   └── Iphones_transformed_data.csv
│
├── docker/
│   └── docker-compose.yml
│
└── Compose up and Login Superset 
```

---
# 🚀 Complete Execution Steps

# 1️⃣ Install Python Dependencies

```bash
pip install scrapy pandas numpy
```

---

# 2️⃣ Run Web Scraping
Move into scrapy project folder:
```bash
cd scrapy_project
```

Run spider:
```bash
scrapy crawl flipmobiles -o ../data/Iphones.csv
scrapy crawl flipmobiles -o ../data/Iphones.json
```

This generates:
```
data/Iphones.csv
data/Iphones.json
```

# 3️⃣ Run Data Standardization/Transformation
```bash
Script/DataStandardizationCode.py
```

Output:
```
Iphones_flipkart.csv
```

This script:
- Separates Storage/Camera/processor/Warranty/Battery/Information
- Standardize Names

```bash
Script/DataTransformationCode.py
```

Output:
```
Iphones_Data_transformed.csv
```

This script:
- Extracts RAM and ROM
- Expandable or Not
- Detects expandable storage
- Aggregates colours
- Cleans price columns
- Standardizes fields
---

# 4️⃣ Install Docker
Verify installation:
```bash
docker --version
docker compose version
```

---

# 5️⃣ Setup Apache Superset

Clone Superset:
```bash
git clone https://github.com/apache/superset.git
cd superset
```

Add ClickHouse dependency:

Create:
```
docker/requirements-local.txt
```

Add:
```
clickhouse-connect>=0.7.0
```

Add service: in Compose file
```
clickhouse:
    image: clickhouse/clickhouse-server:26.1   # or :latest or :25.12 — 26.x is current stable in Feb 2026
    container_name: superset-clickhouse
    ulimits:
      nofile:
        soft: 262144
        hard: 262144
    volumes:
      - clickhouse-data:/var/lib/clickhouse
      - [Folder to mount into docker container]
    ports:
      - "8123:8123"     # HTTP interface (useful for testing)
      - "9000:9000"     # Native TCP (optional)
    environment:
      - CLICKHOUSE_DB=default
      - CLICKHOUSE_USER=default
      - CLICKHOUSE_PASSWORD=****          # ← empty = no password (for dev only!)
      - CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "localhost:8123/ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  clickhouse-data:  

 ```

Start Superset:
```bash
docker compose -f docker-compose-image-tag.yml up -d
```

Wait until containers are healthy.

---
#  Start ClickHouse
From root directory:
```bash
docker run -d \
--name clickhouse-server \
-p 8123:8123 \
-p 9000:9000 \
clickhouse/clickhouse-server:26.1
```

---

# 6️⃣ Create Database and Table

Enter container:

```bash
docker exec -it clickhouse-server clickhouse-client
```

Create database with SQL commands and exit

# 7️⃣ Insert Data into ClickHouse

```bash
docker exec -i clickhouse-server \
clickhouse-client --query="INSERT INTO analytics.Iphones FORMAT CSVWithNames" \
< data/Iphones_transformed_data.csv
```

---

# 9️⃣ Connect Superset to ClickHouse
Open:
```
http://localhost:8088
```

Add new database:
- Driver: ClickHouse Connect
- Host: clickhouse
- Port: 8123
- Database: analytics
- Username: default
- Password: (empty if not set) [Necessary]

Test and save.

---

# 🔟 Create Dashboard

Created dataset from:

```
<Database_name>.<Table_name>
```

Create:

## KPIs
- Average Premium Model Price
- Average Standard Model Price
- Average Discount Provided 

## Charts
- Price vs Storage
- Ratings Distribution
- Model Distribution
- Warranty Availability
- Top Rated Models
- Most Reviewed Models

Combine into dashboard:

**iPhone Analytics System Dashboard**

<img width="2001" height="1820" alt="image" src="https://github.com/user-attachments/assets/36684551-cedd-40ef-8e00-ddc7547b85c1" />
---

# 🎯 Project Outcome

- Real-world web scraping
- Structured data transformation
- Analytical schema design
- Columnar database implementation
- Containerized BI deployment
- Pricing & demand strategy insights

---

# 👩‍💻 Author

S Srimathi
