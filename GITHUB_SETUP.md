# Настройка GitHub репозитория

## Description для GitHub

**Короткое описание (поле Description):**
```
MVP CRM system with Google Drive/Sheets integration - Desktop app for managing clients, deals, and tasks with automated report exports
```

**Полное описание (About section):**
MVP CRM system with Google Drive/Sheets integration. Desktop application for managing clients, deals, and tasks with automated report exports to Google Sheets. Built with FastAPI, SQLite, Tkinter, and Google APIs.

## Topics (теги)

```
crm
customer-relationship-management
fastapi
sqlite
tkinter
google-drive-api
google-sheets-api
oauth2
python
desktop-application
rest-api
report-generation
docker
pydantic
mvp
data-analytics
business-automation
```

## Первый коммит

```bash
git add .
git commit -m "feat: initial implementation of Mini-CRM with Google Drive/Sheets integration

- Add FastAPI backend with SQLite database (clients, deals, tasks)
- Implement Tkinter GUI with tabbed interface
- Add Google Drive API integration via OAuth2
- Add Google Sheets API integration for report generation
- Implement CRUD operations for all entities
- Add search and filtering functionality
- Add column sorting in tables
- Add report export with analytics (totals, averages, breakdowns)
- Add test data generator script (Faker)
- Add Docker configuration for backend
- Add Google Settings configuration in GUI

Author: Георгий Белянин (Georgy Belyanin)
Email: georgy.belyanin@gmail.com"
```

## Настройка автора Git (если нужно изменить)

```bash
git config user.name "Georgy Belyanin"
git config user.email "georgy.belyanin@gmail.com"
```

## Проверка перед коммитом

Перед коммитом убедитесь, что эти файлы НЕ будут добавлены (проверьте `git status`):
- ✅ `secrets/*.json` - не должны быть в коммите
- ✅ `token.pickle` - не должен быть в коммите
- ✅ `data/*.db` - не должна быть в коммите
- ✅ `data/*.json` - не должен быть в коммите (если содержит пути к секретам)
- ✅ `__pycache__/` - не должны быть в коммите
- ✅ `.venv/` - не должно быть в коммите

