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

- Docker and Docker Compose installed
- Git (for cloning the repository)

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=db
DB_PORT=5432
DB_NAME=feature_detector_db
DB_USER=user
DB_PASSWORD=password
```

### 3. Run the Service

```bash
# Start all services
docker-compose up --build
```

### 4. Verify Installation

- **API Documentation**: http://localhost:8002/docs

## API Endpoints

### Process Image
- **URL**: `POST /process-image`
- **Description**: Upload and process an image file
- **Content-Type**: `multipart/form-data`
- **Parameters**: 
  - `file`: Image file (JPG, PNG, etc.)

**Example using curl:**
```bash
curl -X POST -F "file=@image.jpg" http://localhost:8002/process-image
```

### Check Service Status
- **URL**: `GET /check-status`
- **Description**: Check if the feature detector is ready

```bash
curl http://localhost:8002/check-status
```

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

### Running in Development Mode

For development with hot-reload:

```bash
# Update docker-compose.yml to add reload flag
docker-compose up --build
```

### Accessing the Database

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U user -d feature_detector_db

# Common SQL commands
\dt                              # List tables
SELECT * FROM log_requests;      # View logs
\q                              # Quit
```

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs -f fastapi
docker-compose logs -f db
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | Database host | `db` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `feature_detector_db` |
| `DB_USER` | Database user | `user` |
| `DB_PASSWORD` | Database password | `password` |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8003:8002"  # Use port 8003 instead
   ```

2. **Database connection errors**:
   ```bash
   # Check if database is running
   docker-compose ps
   
   # Restart services
   docker-compose down
   docker-compose up --build
   ```

3. **Permission denied errors**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

4. **Image processing fails**:
   - Ensure the uploaded file is a valid image format
   - Check if OpenCV dependencies are properly installed in the container

### Reset Everything

```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose up --build
```

### Check Service Health

```bash
# Test basic connectivity
curl http://localhost:8002/

# Test image processing (replace with actual image)
curl -X POST -F "file=@test.jpg" http://localhost:8002/process-image

# Check detector status
curl http://localhost:8002/check-status
```
