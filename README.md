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

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
```

### 3. Run the Service

```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Verify Installation

- **API Documentation**: http://localhost:8002/docs
- **Health Check**: http://localhost:8002/check-status

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

**Example using Python:**
```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8002/process-image', files=files)
    print(response.json())
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
│   │   └── log_request.py     # Database models
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

## Production Deployment

For production deployment:

1. **Remove development volume mount**:
   ```yaml
   # Comment out in docker-compose.yml
   # volumes:
   #   - .:/usr/src/app
   ```

2. **Set production environment variables**:
   ```env
   DEBUG=false
   LOG_LEVEL=WARNING
   ```

3. **Use environment-specific configurations**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the logs: `docker-compose logs -f`
3. Open an issue in the repository