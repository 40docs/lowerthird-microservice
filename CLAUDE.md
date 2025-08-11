# Lowerthird Microservice

## Overview
A Flask-based microservice for generating customizable lowerthird graphics, following the 40docs microservice architecture pattern.

## Architecture
- **Single Docker container** - Self-contained microservice
- **Flask REST API** - Simple JSON endpoints
- **Volume-based I/O** - Assets served via mounted volumes
- **Health check endpoint** - For container orchestration
- **Minimal dependencies** - Only Flask + video processing libraries

## API Endpoints

### Health Check
- `GET /health` - Returns `{"status": "ok"}`

### Generate Lowerthird
- `POST /create-lowerthird` - Creates branded video
- **Input**: JSON with title, subtitle, duration, style
- **Output**: JSON with video path and parameters

### List Styles  
- `GET /styles` - Returns available brand styles

## Development Commands

### Local Development
```bash
pip install -r requirements.txt
python main.py
```

### Docker Build
```bash
docker build -t lowerthird-microservice .
```

### Docker Run
```bash
docker run -d -p 5000:5000 -v $(pwd)/outputs:/app/outputs lowerthird-microservice
```

### Test API
```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/create-lowerthird -H "Content-Type: application/json" -d '{"main_title":"Your Brand","subtitle":"Test"}'
```

## Deployment Pattern
This microservice follows the same pattern as 40docs video-producer-microservice:
- Single container deployment
- GitHub Container Registry compatible
- Volume mounts for asset persistence  
- Standard Flask + subprocess architecture

## Technical Stack
- Python 3.11 + Flask
- OpenCV + Pillow for video generation
- 30fps 1080p MP4 output
- Multiple brand styles (default, minimal, corporate, tech)