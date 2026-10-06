# 🛠️ Setup & Operations Manual

## System Requirements
- OS: Windows 10/11, macOS, or Ubuntu 20.04+
- Docker Desktop with Compose support
- Python 3.11+ (for local development outside Docker)
- Node.js 18+ (for local frontend development)

---

## Step-by-Step Deployment

### 1. Environment Configuration
Create `.env` file from template:
```bash
cp .env.example .env
```

Required keys:
```env
GEMINI_API_KEY=AIzaSy...
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rag_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 2. Docker Operations
```bash
# Build and start all containers
docker compose up -d --build

# View real-time logs
docker compose logs -f backend

# Stop services
docker compose down
```

### 3. Database Maintenance & Inspection
```bash
# Connect to PostgreSQL shell
docker exec -it rag-db-1 psql -U postgres -d rag_db

# Count indexed document chunks
SELECT COUNT(*) FROM document_chunks;
```


---

## ⚠️ Disclaimer Notice
This document and all associated dataset examples are synthetic mock artifacts engineered exclusively for independent portfolio demonstration purposes. This project is not affiliated with or endorsed by Walmart Inc.