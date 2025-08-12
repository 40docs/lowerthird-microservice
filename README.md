# DataDash Lowerthird Microservice

A Flask-based microservice for generating professional DataDash-branded lowerthird graphics for community content about Fortinet and Forticloud technologies.

## Features

- **Fortinet-Inspired Color Palette** - Uses secure red, cloud blue, sase purple, connectivity yellow
- **DataDash Community Branding** - Perfect for Fortinet/Forticloud educational content
- **Professional Animations** - Smooth quartic/sine easing for broadcast quality
- **Multiple Style Options** - Different color schemes for varied content types
- **RESTful API** for video generation
- **Docker containerized** for easy deployment

## DataDash Color Palette (Fortinet-Inspired)

| Color Name | RGB | Hex | Usage |
|------------|-----|-----|-------|
| **Cloud Blue** | RGB(48, 127, 226) | #307FE2 | Primary brand color |
| **Secure Red** | RGB(218, 41, 28) | #DA291C | Alerts/emphasis |
| **Connectivity Yellow** | RGB(255, 185, 0) | #FFB900 | Highlights/accents |
| **SASE Purple** | RGB(144, 99, 205) | #9063CD | Technical content |

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

### Generate DataDash Lowerthird
```http
POST /create-lowerthird
Content-Type: application/json

{
  "main_title": "DataDash",
  "subtitle": "Fortinet Security Deep Dive", 
  "output_name": "episode_intro",
  "duration": 4.0,
  "style": "cloud_blue"
}
```

Response:
```json
{
  "status": "ok",
  "video": "/app/outputs/episode_intro.mp4",
  "parameters": {
    "main_title": "DataDash",
    "subtitle": "Fortinet Security Deep Dive",
    "duration": 4.0,
    "style": "cloud_blue"
  }
}
```

### List Available Styles
```http
GET /styles
```

Response:
```json
{
  "styles": [
    "cloud_blue",
    "secure_red", 
    "sase_purple",
    "connectivity_yellow"
  ]
}
```

## Available DataDash Styles

### cloud_blue
- **Primary**: Cloud Blue (#307FE2)
- **Secondary**: Deep Blue
- **Best for**: General DataDash content, cloud security topics

### secure_red
- **Primary**: Secure Red (#DA291C)
- **Secondary**: Deep Red
- **Best for**: Security alerts, threat intelligence content

### sase_purple
- **Primary**: SASE Purple (#9063CD)
- **Secondary**: Deep Purple
- **Best for**: SASE, SD-WAN, technical deep dives

### connectivity_yellow
- **Primary**: Connectivity Yellow (#FFB900)
- **Secondary**: Deep Yellow
- **Best for**: Networking content, connectivity topics

## Docker Usage

### Using Pre-built Image (Recommended)
```bash
# Pull latest image from GitHub Container Registry
docker pull ghcr.io/40docs/lowerthird-microservice:latest

# Run container with volume mount for output videos
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/outputs:/app/outputs \
  --name lowerthird \
  ghcr.io/40docs/lowerthird-microservice:latest
```

**Note:** The `-v $(pwd)/outputs:/app/outputs` mount allows you to access generated videos in your local `./outputs/` directory for preview and download.

### Build Image Locally
```bash
# Build from source
docker build -t lowerthird-microservice .

# Run local build with volume mount
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

# Generate lowerthird (video will be saved to ./outputs/test_video.mp4)
curl -X POST http://localhost:5000/create-lowerthird \
  -H "Content-Type: application/json" \
  -d '{
    "main_title": "Your Brand",
    "subtitle": "Innovation in Code",
    "output_name": "test_video",
    "duration": 5.0,
    "style": "tech"
  }'

# Check your generated video
ls -la outputs/test_video.mp4
```

## Deployment

### GitHub Container Registry
This microservice is automatically built and published to GitHub Container Registry:

```bash
# Latest stable release
docker pull ghcr.io/40docs/lowerthird-microservice:latest

# Specific version
docker pull ghcr.io/40docs/lowerthird-microservice:v1.0.0
```

### Container Orchestration
```bash
# Docker with health checks
docker run -d \
  -p 5000:5000 \
  -v /path/to/outputs:/app/outputs \
  --health-cmd="curl -f http://localhost:5000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --restart=unless-stopped \
  --name lowerthird \
  ghcr.io/40docs/lowerthird-microservice:latest
```

### Integration with 40docs Ecosystem
This microservice can be integrated into video-as-code workflows:

```bash
# Example: Generate lowerthird, then process with video-producer-microservice
curl -X POST http://localhost:5000/create-lowerthird \
  -H "Content-Type: application/json" \
  -d '{"main_title":"My Video","subtitle":"Professional Content"}'
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

## CI/CD Pipeline

This microservice uses GitHub Actions for automated builds:
- **Trigger**: Push to main branch or manual workflow dispatch
- **Registry**: Automatically published to `ghcr.io/40docs/lowerthird-microservice:latest`
- **Integration**: Built-in container workflow following 40docs standards

## Technical Specifications

- **Video Output**: 1920x1080 HD, 30fps, MP4 format
- **Animation**: Smooth easing with quartic/sine curves
- **Fonts**: DejaVu Sans (fallback to default)
- **Processing**: OpenCV + PIL for video generation
- **Architecture**: Follows 40docs microservice patterns
- **Container Registry**: GitHub Container Registry (ghcr.io)
- **Automatic Builds**: GitHub Actions container.yml workflow

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