# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-12-27

### Added
- Full CRUD API for clients, deals, and tasks (FastAPI)
- SQLite database with schema for clients, deals, tasks
- Desktop GUI application (Tkinter) with tabbed interface
- Google Drive integration for creating spreadsheets via OAuth2
- Google Sheets integration for writing and formatting reports
- Report generation with analytics (totals, averages, breakdowns)
- Search and filtering functionality
- Column sorting in tables (click column headers)
- Test data generator script (Faker)
- Docker configuration for backend
- Google Settings configuration tab in GUI

### Features
- **Clients Management**: Create, read, update, delete clients
- **Deals Management**: Track deals with amounts, currencies, statuses
- **Tasks Management**: Manage tasks with due dates and completion status
- **Report Export**: Export data to Google Sheets with formatted reports
- **OAuth2 Authentication**: Secure Google API access
- **Search**: Case-insensitive search across multiple fields
- **Filtering**: Filter by status, completion, client/deal relationships

### Technical Stack
- Backend: FastAPI, Uvicorn, SQLite3, Pydantic
- Frontend: Tkinter
- Google APIs: Drive API v3, Sheets API v4, OAuth2
- DevOps: Docker, Docker Compose
- Testing: Faker for test data generation

---

**Author:** Георгий Белянин (Georgy Belyanin)  
**Email:** georgy.belyanin@gmail.com

