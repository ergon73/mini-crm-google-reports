"""
Точка входа для GUI приложения.
"""

import sys
from pathlib import Path

# Добавить корневую директорию проекта в путь
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import tkinter as tk
from gui.crm_gui import CRMGUI


def main():
    """Запустить GUI приложение."""
    root = tk.Tk()
    app = CRMGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

