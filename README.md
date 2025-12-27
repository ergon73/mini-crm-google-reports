# Mini-CRM with Google Drive/Sheets Integration

> **MVP CRM system** for managing clients, deals, and tasks with automated report exports to Google Sheets

A lightweight CRM application built with FastAPI, SQLite, and Tkinter. Features automated report generation with analysis blocks and export to Google Drive via OAuth2.

**Author:** Георгий Белянин (Georgy Belyanin)  
**Email:** georgy.belyanin@gmail.com

## ✨ Features

- 📊 **Full CRUD** for clients, deals, and tasks
- 🔍 **Search & filtering** (case-insensitive, multi-field)
- 📈 **Column sorting** in tables (click column headers)
- 🐳 **Docker-ready** backend (FastAPI + SQLite)
- 🖥️ **Desktop GUI** (Tkinter) with tabs interface
- ☁️ **Google Drive** integration for automated report exports
- 📊 **Smart analytics** in reports (totals, averages, breakdowns by status)
- 🔐 **OAuth2 authentication** for secure Google access
- 🎲 **Test data generator** (1000+ realistic records via Faker)

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI, Uvicorn, SQLite3, Pydantic |
| Frontend | Tkinter |
| Google APIs | Drive API v3, Sheets API v4, OAuth2 |
| DevOps | Docker, Docker Compose |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker Desktop
- Google Cloud project with Drive & Sheets APIs enabled

### Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/mini-crm-google-sheets.git
cd mini-crm-google-sheets

# Add credentials to secrets/
# - client_secret.json (OAuth Desktop)
# - service_account.json

# Install dependencies
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run

```bash
# Backend
docker compose up --build

# GUI (new terminal)
python gui/start_gui.py

# Generate test data
python scripts/fill_test_data.py --base-url http://localhost:8000 --n 1000
```

### Export Reports

1. Open GUI → Settings tab → configure Google credentials
2. Go to Clients/Deals/Tasks tab
3. Click **"Выгрузить отчет"**
4. First time: authorize in browser
5. Report opens in Google Sheets

## 📚 API Endpoints

| Entity | Methods | Query Params |
|--------|---------|--------------|
| `/api/clients` | CRUD | `?q=`, `?status=` |
| `/api/deals` | CRUD | `?q=`, `?status=`, `?client_id=` |
| `/api/tasks` | CRUD | `?q=`, `?is_done=`, `?client_id=`, `?deal_id=` |
| `/health` | GET | — |

## 📁 Structure

```
backend/          # FastAPI + SQLite
gui/              # Tkinter interface
google_integration/  # Drive & Sheets APIs
scripts/          # Test data generator
```

## 🔐 Security

**Never commit:** `.env`, `secrets/*.json`, `token.pickle`

## 📸 Report Format

```
┌─────────────────────────────────────────┐
│ ОТЧЕТ: Клиенты                          │
│ Дата: 27.12.2024 15:30                  │
├─────────────────────────────────────────┤
│ АНАЛИЗ ДАННЫХ                           │
│ Всего: 1000 | Активных: 850             │
├─────────────────────────────────────────┤
│ ID │ Имя │ Email │ Компания │ Статус    │
│ 1  │ ... │ ...   │ ...      │ active    │
└─────────────────────────────────────────┘
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| OAuth "access denied" | Add email to Test users in Google Cloud |
| Service account can't see folder | Share folder with service account email |
| Ctrl+V doesn't work | Use "Вставить" button |

## 📝 License

MIT

---

## 👤 Author

**Георгий Белянин (Georgy Belyanin)**  
📧 georgy.belyanin@gmail.com

⭐ Built as part of "Vibe Coding" course
