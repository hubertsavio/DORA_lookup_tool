# DORA Compliance Lookup Tool - Deployment Guide

## Prerequisites

### System Requirements
- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL 13+ (recommended for production) or SQLite (development)
- 2GB RAM minimum
- 10GB disk space

### Required Software
- Git
- pip (Python package manager)
- npm or yarn (Node package manager)

## Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd DORA
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Initialize Database
```bash
python -m models.database
```

#### Run Scraper (Optional - to populate data)
```bash
python -m scrapers.eiopa_scraper
```

#### Start Backend Server
```bash
python app.py
# Server will run on http://localhost:8000
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd ../frontend
npm install
```

#### Start Development Server
```bash
npm run dev
# Frontend will run on http://localhost:3000
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment

### Option 1: Docker Deployment (Recommended)

#### Create Dockerfile for Backend
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: dora_db
      POSTGRES_USER: dora_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://dora_user:${DB_PASSWORD}@postgres:5432/dora_db
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    volumes:
      - ./backend:/app
      - search_index:/app/search_index

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
  search_index:
```

#### Deploy with Docker Compose
```bash
docker-compose up -d
```

### Option 2: Traditional Server Deployment

#### Backend (Ubuntu/Debian)

1. **Install System Dependencies**
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv postgresql nginx
```

2. **Setup PostgreSQL**
```bash
sudo -u postgres createuser dora_user
sudo -u postgres createdb dora_db
sudo -u postgres psql -c "ALTER USER dora_user WITH PASSWORD 'your_password';"
```

3. **Deploy Backend**
```bash
cd /opt
sudo git clone <repository-url> dora
cd dora/backend
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
```

4. **Configure Systemd Service**
Create `/etc/systemd/system/dora-backend.service`:
```ini
[Unit]
Description=DORA Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/dora/backend
Environment="PATH=/opt/dora/backend/venv/bin"
ExecStart=/opt/dora/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable dora-backend
sudo systemctl start dora-backend
```

#### Frontend

1. **Build Frontend**
```bash
cd /opt/dora/frontend
npm install
npm run build
```

2. **Configure Nginx**
Create `/etc/nginx/sites-available/dora`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /opt/dora/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

3. **Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/dora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Cloud Platform Deployment

#### Heroku

1. **Backend (Heroku)**
```bash
cd backend
heroku create dora-backend
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

2. **Frontend (Netlify/Vercel)**
- Connect GitHub repository
- Set build command: `npm run build`
- Set publish directory: `dist`
- Add environment variable: `VITE_API_URL=https://dora-backend.herokuapp.com`

#### AWS

1. **Backend (Elastic Beanstalk)**
- Create Python 3.9 environment
- Deploy using EB CLI or console
- Configure RDS PostgreSQL instance

2. **Frontend (S3 + CloudFront)**
- Build frontend: `npm run build`
- Upload to S3 bucket
- Configure CloudFront distribution
- Set up custom domain

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dora_db
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-domain.com
SEARCH_INDEX_DIR=search_index
LOG_LEVEL=INFO
```

### Frontend
```bash
VITE_API_URL=https://api.your-domain.com
```

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Database**: Use strong passwords and restrict access
3. **CORS**: Configure allowed origins properly
4. **Rate Limiting**: Implement API rate limiting
5. **Secrets**: Never commit .env files
6. **Updates**: Keep dependencies updated

## Monitoring

### Health Checks
- Backend: `GET /api/health`
- Database: Monitor connection pool
- Search Index: Monitor disk usage

### Logging
- Backend logs: `/var/log/dora-backend/`
- Nginx logs: `/var/log/nginx/`
- Application logs: Check systemd journal

### Metrics
- API response times
- Search query performance
- Database query performance
- Error rates

## Backup Strategy

### Database Backup
```bash
pg_dump -U dora_user dora_db > backup_$(date +%Y%m%d).sql
```

### Search Index Backup
```bash
tar -czf search_index_backup_$(date +%Y%m%d).tar.gz search_index/
```

## Maintenance

### Update Application
```bash
git pull origin main
cd backend && pip install -r requirements.txt
cd ../frontend && npm install && npm run build
sudo systemctl restart dora-backend
sudo systemctl reload nginx
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

### Re-index Search
```bash
cd backend
python -m utils.reindex
```

## Troubleshooting

### Backend Won't Start
- Check logs: `sudo journalctl -u dora-backend -f`
- Verify database connection
- Check port availability: `sudo netstat -tlnp | grep 8000`

### Frontend Build Fails
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node version: `node --version`
- Verify API URL configuration

### Search Not Working
- Check search index directory permissions
- Rebuild index: `python -m utils.reindex`
- Verify disk space

## Support

For issues and questions:
- Check documentation: `/docs`
- Review logs
- Contact system administrator

## License

[To be determined]