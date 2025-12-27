# Contributing

Thank you for your interest in contributing to Mini-CRM!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mini-crm-google-reports.git
   cd mini-crm-google-reports
   ```

3. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up Google credentials (see README.md)

6. Run the application:
   ```bash
   docker compose up --build  # Backend
   python gui/start_gui.py    # GUI
   ```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

## Submitting Changes

1. Create a feature branch from `main`
2. Make your changes
3. Test your changes thoroughly
4. Commit with descriptive messages
5. Push to your fork
6. Create a Pull Request

## Reporting Issues

Please use GitHub Issues to report bugs or request features. Include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

