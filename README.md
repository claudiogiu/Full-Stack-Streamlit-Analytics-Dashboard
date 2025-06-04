# Interactive Analytics Dashboard via ClickHouse, FastAPI and Streamlit 

## Introduction  

This repository is designed for deploying an interactive analytics dashboard by adopting a full-stack architecture via ClickHouse as the database, FastAPI as the backend and Streamlit as the frontend.  

ClickHouse enables efficient execution of OLAP queries for high-performance data analysis. FastAPI provides a scalable and responsive API layer for seamless data communication, while Streamlit delivers an intuitive and interactive user interface for effective visualization.
## Getting Started 

To set up the repository properly, follow these steps:  

**1.** **Set Up the ClickHouse Database Environment**  

The `packages/db/` directory contains all necessary files to set up the **ClickHouse database environment**. It is structured as follows:  

- `clickhouse-server/etc/`: Provides configuration for the ClickHouse server.  
  - `config.d/`: Defines core database settings via `config.xml`.  
  - `users.d/`: Manages user authentication and access control via `users.xml`.  
- `clickhouse-keeper/etc/`: Defines cluster coordination settings via `keeper_config.xml`.  
- `docker-entrypoint-initdb.d/`: Initializes the database via `init.sql`.

`init.sql` creates the table, preprocesses, and inserts data extracted from **The UK Property Prices Dataset**, available at [this link](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid#:~:text=This%20data%20contains%20prices%20paid%20for%20real-estate%20property,data%20%C2%A9%20Crown%20copyright%20and%20database%20right%202021).

To set up the database environment, navigate to the `packages/db/` directory and execute the following command:  

```bash
docker-compose up -d
```

This command initializes three key services that enable ClickHouse to function properly:
- **ClickHouse Server** – The core analytical database engine, optimized for executing high-performance queries on large datasets.  
- **ClickHouse Keeper** – A distributed coordination system that manages cluster synchronization and metadata operations, ensuring stability in multi-node configurations.  
- **Tabix** – A lightweight web-based interface that allows users to execute queries, monitor database performance, and interact with ClickHouse via a graphical UI.  

Before running the ClickHouse services, create a `.env` file inside the `packages/db/` directory with the necessary configuration:  

```env
CHVER=23.4  
CHKVER=23.4-alpine  
```

**2.** **Set Up the Backend and Frontend Environment**   
 
The `apps/` directory contains all necessary files to set up the **backend and frontend environment** for the analytics dashboard. It is structured as follows:  

- `api/`: Implements the backend service using **FastAPI**.  
  - `server.py`: Provides API endpoints for executing queries on ClickHouse and retrieving data.  
- `web/`: Implements the frontend service using **Streamlit**.  
  - `app.py`: Creates the user interface for data visualization and interaction.  

To set up the backend and frontend environment, navigate to the repository root directory and execute the following command:  

```bash
docker-compose up -d
```
This command initializes two key services that enable the backend and frontend to function properly:  
- **api_container** – The FastAPI-based backend that processes queries and interacts with the ClickHouse database.  
- **web_container** – The Streamlit-based frontend that provides an intuitive interface for data exploration and visualization.  

Before running the backend and frontend services, create a `.env` file inside the repository root directory with the necessary configuration:  

```env
API_URL=http://api:8000
```

**3.** **Launch the Dashboard** 

Once the backend and frontend services are running, the dashboard will be accessible via Streamlit. Open your browser and navigate to `localhost:8501`.

## License  

This project is licensed under the **MIT License**, which allows for open-source use, modification, and distribution with minimal restrictions. For more details, refer to the file included in this repository. 
