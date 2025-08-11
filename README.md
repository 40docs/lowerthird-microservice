# Lowerthird Microservice

A Flask-based microservice for generating customizable lowerthird graphics, following the 40docs microservice architecture pattern.

## Features

- **RESTful API** for video generation
- **Multiple brand styles** (default, minimal, corporate, tech)
- **Customizable text** and duration
- **Professional animations** with smooth easing
- **Docker containerized** for easy deployment
- **Health check** endpoint for orchestration

## API Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

### Generate Lowerthird
```http
POST /create-lowerthird
Content-Type: application/json

{
  "main_title": "DataDash",
  "subtitle": "Short Tech Insights", 
  "output_name": "my_lowerthird",
  "duration": 4.0,
  "style": "default"
}
```

Response:
```json
{
  "status": "ok",
  "video": "/app/outputs/my_lowerthird.mp4",
  "parameters": {
    "main_title": "Your Brand",
    "subtitle": "Short Tech Insights",
    "duration": 4.0,
    "style": "default"
  }
}
```

### List Styles
```http
GET /styles
```

Response:
```json
{
  "styles": ["default", "minimal", "corporate", "tech"]
}
```

## Available Styles

- **default**: Blue branding theme
- **minimal**: Grayscale professional
- **corporate**: Traditional blue corporate
- **tech**: Modern green tech theme

## Docker Usage

### Build Image
```bash
docker build -t lowerthird-microservice .
```

### Run Container
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/outputs:/app/outputs \
  --name lowerthird \
  lowerthird-microservice
```

### Test API
```bash
# Health check
curl http://localhost:5000/health

# Generate lowerthird
curl -X POST http://localhost:5000/create-lowerthird \
  -H "Content-Type: application/json" \
  -d '{
    "main_title": "Your Brand",
    "subtitle": "Innovation in Code",
    "output_name": "test_video",
    "duration": 5.0,
    "style": "tech"
  }'
```

## Development

### Local Setup
```bash
pip install -r requirements.txt
python main.py
```

### Project Structure
```
lowerthird-microservice/
├── main.py                    # Flask API application
├── lowerthird_service.py      # Core video generation logic
├── requirements.txt           # Python dependencies
├── Dockerfile                # Container configuration
└── README.md                 # Documentation
```

## Technical Specifications

- **Video Output**: 1920x1080 HD, 30fps, MP4 format
- **Animation**: Smooth easing with quartic/sine curves
- **Fonts**: DejaVu Sans (fallback to default)
- **Processing**: OpenCV + PIL for video generation
- **Architecture**: Follows 40docs microservice patterns

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid parameters)
- `500`: Server error (processing failed)

Error responses include descriptive messages:
```json
{
  "error": "Duration must be a positive number"
}
```