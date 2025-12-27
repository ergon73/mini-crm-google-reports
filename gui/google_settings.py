"""
Модуль для работы с настройками Google интеграции.
"""

import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

SETTINGS_FILE = Path("data/google_settings.json")


def load_settings() -> dict:
    """Загрузить настройки из файла."""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_settings(settings: dict):
    """Сохранить настройки в файл."""
    SETTINGS_FILE.parent.mkdir(exist_ok=True)
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


class GoogleSettingsTab(tk.Frame):
    """Вкладка настроек Google интеграции."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = load_settings()
        self._create_widgets()
        self._load_values()
    
    def _create_widgets(self):
        """Создать виджеты."""
        # Service Account
        tk.Label(self, text="Service Account JSON:").grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.sa_entry = tk.Entry(self, width=50)
        self.sa_entry.grid(row=0, column=1, pady=5, padx=5)
        tk.Button(self, text="Выбрать", command=self._browse_sa).grid(row=0, column=2, pady=5, padx=5)
        
        # Client Secret
        tk.Label(self, text="Client Secret JSON:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.cs_entry = tk.Entry(self, width=50)
        self.cs_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Button(self, text="Выбрать", command=self._browse_cs).grid(row=1, column=2, pady=5, padx=5)
        
        # Folder ID
        tk.Label(self, text="Drive Folder ID:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.folder_entry = tk.Entry(self, width=50)
        self.folder_entry.grid(row=2, column=1, pady=5, padx=5)
        tk.Button(self, text="Вставить", command=self._paste_folder).grid(row=2, column=2, pady=5, padx=5)
        
        # Save button
        tk.Button(
            self, 
            text="Сохранить", 
            command=self._save,
            bg="#4CAF50", 
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        ).grid(row=3, column=1, pady=20)
    
    def _browse_sa(self):
        """Выбрать файл Service Account."""
        path = filedialog.askopenfilename(
            title="Выбрать Service Account JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            self.sa_entry.delete(0, tk.END)
            self.sa_entry.insert(0, path)
    
    def _browse_cs(self):
        """Выбрать файл Client Secret."""
        path = filedialog.askopenfilename(
            title="Выбрать Client Secret JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            self.cs_entry.delete(0, tk.END)
            self.cs_entry.insert(0, path)
    
    def _paste_folder(self):
        """Вставить из буфера обмена (Ctrl+V не работает в Tkinter!)."""
        try:
            text = self.clipboard_get()
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, text)
        except tk.TclError:
            messagebox.showwarning("Ошибка", "Буфер обмена пуст")
    
    def _load_values(self):
        """Загрузить сохранённые значения."""
        self.sa_entry.insert(0, self.settings.get('service_account_path', ''))
        self.cs_entry.insert(0, self.settings.get('client_secret_path', ''))
        self.folder_entry.insert(0, self.settings.get('folder_id', ''))
    
    def _save(self):
        """Сохранить настройки."""
        self.settings = {
            'service_account_path': self.sa_entry.get(),
            'client_secret_path': self.cs_entry.get(),
            'folder_id': self.folder_entry.get()
        }
        save_settings(self.settings)
        messagebox.showinfo("Успех", "Настройки сохранены!")
    
    def get_settings(self) -> dict:
        """Получить текущие настройки."""
        return {
            'service_account_path': self.sa_entry.get(),
            'client_secret_path': self.cs_entry.get(),
            'folder_id': self.folder_entry.get()
        }

