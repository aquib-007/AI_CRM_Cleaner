# AI CRM Cleaner Project

This project enhances CRM data accuracy using AI with a FastAPI backend and a React frontend.

## 🚀 How to Run

### 🖥 Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 🌐 Frontend (React)

```bash
cd frontend
npm install
npm start
```

### 🐳 Run Both with Docker Compose

```bash
docker-compose up --build
```

## 📄 Sample CSV Format

```csv
name,email,phone,address
John Doe,john@example.com,1234567890,123 Elm Street
Jon Doe,john.d@example.com,1234567890,123 Elm St.
Jane Smith,jane@example.com,,456 Oak Avenue
```

## 🔗 API Endpoints

- `POST /upload-csv/` - Upload CSV and receive cleaned data
- `POST /clean-data/` - Send JSON records directly

## ✅ Features

- Duplicate detection with fuzzy matching
- Missing value handling
- Text normalization
- Frontend table to view cleaned records
