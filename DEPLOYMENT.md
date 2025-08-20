# 🚀 Deployment Guide

This guide covers deploying the Smartphone Price Prediction application to production.

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Server/VPS with SSH access

## 🌐 Production Deployment

### 1. Backend Deployment (Flask)

#### Option A: Traditional Server
```bash
# Clone repository
git clone https://github.com/yourusername/smartphone-price-prediction.git
cd smartphone-price-prediction

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production WSGI server
pip install gunicorn

# Start with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 app:app
```

#### Option B: Docker
```bash
# Build Docker image
docker build -t smartphone-price-prediction .

# Run container
docker run -p 8501:8501 smartphone-price-prediction
```

### 2. Frontend Deployment (React)

#### Build Production Version
```bash
cd frontend
npm install
npm run build
```

#### Serve Static Files
```bash
# Using Python
cd build
python -m http.server 3000

# Using Node.js
npm install -g serve
serve -s build -l 3000

# Using Nginx (recommended)
# Copy build/ contents to /var/www/html/
```

### 3. Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /predict {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔧 Environment Variables

Create `.env` file for production:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
```

## 📊 Monitoring

### Health Checks
```bash
# Test backend
curl http://yourdomain.com/health

# Test frontend
curl http://yourdomain.com/
```

### Logs
```bash
# Backend logs
tail -f /var/log/flask-app.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## 🚀 Quick Deploy Script

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying Smartphone Price Prediction..."

# Pull latest changes
git pull origin main

# Backend
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart smartphone-price-prediction

# Frontend
cd frontend
npm install
npm run build
sudo cp -r build/* /var/www/html/

echo "✅ Deployment complete!"
```

## 🔒 Security Considerations

1. **HTTPS**: Use Let's Encrypt for SSL certificates
2. **Firewall**: Configure UFW or iptables
3. **Updates**: Keep system and dependencies updated
4. **Backups**: Regular database and file backups
5. **Monitoring**: Set up alerts for downtime

## 📈 Scaling

### Load Balancing
```nginx
upstream backend {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}
```

### Multiple Instances
```bash
# Start multiple backend instances
gunicorn -w 4 -b 127.0.0.1:8501 app:app &
gunicorn -w 4 -b 127.0.0.1:8502 app:app &
gunicorn -w 4 -b 127.0.0.1:8503 app:app &
```

## 🐛 Troubleshooting

### Common Issues
1. **Port conflicts**: Check if ports 3000/8501 are free
2. **Permission errors**: Ensure proper file permissions
3. **Dependency issues**: Verify Python/Node versions
4. **CORS errors**: Check API endpoint configuration

### Debug Mode
```bash
# Enable debug logging
export FLASK_DEBUG=1
python app.py
```

---

**Need help?** Create an issue in the GitHub repository or contact the development team.
