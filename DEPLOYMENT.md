# Deployment Guide

## Quick Deploy Options

### Option 1: Docker (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 2: Local Setup

```bash
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env
# Edit .env with your settings

# 4. Run
python app.py
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | No | - | OpenAI API key (falls back to demo mode) |
| `FLASK_DEBUG` | No | False | Enable debug mode |
| `FLASK_PORT` | No | 5000 | Server port |
| `CORS_ORIGINS` | No | * | Allowed CORS origins (comma-separated) |

## Production Deployment

### Security Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure specific `CORS_ORIGINS` (not `*`)
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Setup proper firewall rules
- [ ] Configure rate limiting appropriately

### Recommended Stack

- **Web Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **SSL**: Let's Encrypt
- **Monitoring**: Prometheus + Grafana

### Example Gunicorn Command

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Docker Production Deploy

```bash
# Build
docker build -t prompt-eval-platform:latest .

# Run with prod settings
docker run -d \
  -p 5000:5000 \
  -e FLASK_DEBUG=False \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/results:/app/results \
  --name prompt-eval \
  prompt-eval-platform:latest
```

## Health Checks

```bash
# Check if running
curl http://localhost:5000/

# Check API
curl http://localhost:5000/api/prompts
```

## Troubleshooting

**Issue**: Dependencies fail to install  
**Solution**: Upgrade pip `python -m pip install --upgrade pip`

**Issue**: Model downloads fail  
**Solution**: Check internet connection, models download on first use

**Issue**: API returns 429 (rate limit)  
**Solution**: Adjust rate limits in app.py or wait for limit reset
