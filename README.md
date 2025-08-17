# Image Processing Service

A FastAPI-based image processing service with feature detection capabilities, built with Docker and PostgreSQL.

## Features

- 🖼️ Image upload and processing
- 🔍 Feature detection using OpenCV
- 📊 Request/response logging
- 🗄️ PostgreSQL database integration
- 🐳 Containerized with Docker
- 🚀 Automatic database table creation
- 📝 Comprehensive API documentation

## Prerequisites

- Docker and Docker Compose installed (https://docs.docker.com/compose/install/)
- Git (for cloning the repository)

## Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:NastiaFasova/feature-detector.git
cd feature_detector
```

### 2. Environment Configuration

You may see, that I left .env file for testing purposes. If you're willing to create your own database,
please change .env file, so that it contains parameters with credentials to your recently created db

Feel free to use sql query below:
```sql
CREATE DATABASE <db_name>;
```

More information can be found here:
https://www.postgresql.org/docs/current/manage-ag-createdb.html


### 3. Run the Service

Open Docker Desktop (to start docker daemon)
```bash
# Start all services
docker-compose up --build
```

### 4. Verify Installation
In order to verify successful running of application, we may open a page in browser with SWAGGER

- **SWAGGER Documentation**: http://localhost:8002/docs#/

## API Endpoints

### Process Image
- **URL**: `POST /process-image`
- **Description**: Upload and process an image file
- **Content-Type**: `multipart/form-data`
- **Parameters**: 
  - `file`: Image file (JPG, PNG, etc.)

#### Testing example
After opening http://localhost:8002/docs#/ , feel free to test both endpoints simultaneously

![img.png](img.png)
![img_1.png](img_1.png)


### Check status
- **URL**: `GET /check-status`
- **Description**: Checks if feature-detector was initialized
  
![img_2.png](img_2.png)

## Project Structure

```
├── app/
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── database.py        # Database setup
│   ├── middleware/
│   │   └── logging.py         # Request/response logging
│   ├── models/
│   │   └── log_request_model.py     # Database models
│   ├── repositories/
│   │   └── repositories.py    # Data access layer
│   ├── routes/
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── logging_service.py # Logging business logic
│   │   └── process_image_service.py # Image processing logic
│   └── utils/
│       ├── feature_detector.py        # OpenCV feature detection
│       ├── feature_detector_manager.py # Detector singleton
│       └── file_hash.py               # File hashing utilities
│       └── request_analyze_helper.py  # File hashing utilities
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env                       # Environment variables
└── README.md
```

## Development

In order to check if all requests were successfully written into database, we can access 
database and select rows.


### Accessing the Database

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U user -d feature_detector_db

# Common SQL commands
\dt                              # List tables
SELECT * FROM log_requests;      # View logs
\q                               # Quit
```

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)

### Reset Everything

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose up --build
```
