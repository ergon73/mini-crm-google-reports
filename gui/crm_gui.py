"""
Главное окно GUI приложения CRM.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from typing import Optional
from gui.api_client import APIClient
from gui.google_settings import GoogleSettingsTab
from google_integration.report_generator import ReportGenerator


class CRMGUI:
    """Главное окно приложения CRM."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mini-CRM")
        self.root.geometry("1000x600")
        
        self.api_client = APIClient()
        self.google_settings_tab = None
        
        # Состояние сортировки для каждой таблицы
        self.clients_sort_column = None
        self.clients_sort_reverse = False
        self.deals_sort_column = None
        self.deals_sort_reverse = False
        self.tasks_sort_column = None
        self.tasks_sort_reverse = False
        
        # Создать вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладки
        self.clients_tab = self._create_clients_tab()
        self.deals_tab = self._create_deals_tab()
        self.tasks_tab = self._create_tasks_tab()
        self.settings_tab = self._create_settings_tab()
        
        self.notebook.add(self.clients_tab, text="Клиенты")
        self.notebook.add(self.deals_tab, text="Сделки")
        self.notebook.add(self.tasks_tab, text="Задачи")
        self.notebook.add(self.settings_tab, text="Настройки Google")
        
        # Обновить данные при запуске
        self.refresh_all()
    
    def _create_clients_tab(self) -> tk.Frame:
        """Создать вкладку клиентов."""
        frame = tk.Frame(self.notebook)
        
        # Панель управления
        control_frame = tk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(control_frame, text="Обновить", command=self.refresh_clients).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Добавить", command=self.add_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Редактировать", command=self.edit_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Удалить", command=self.delete_client).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Выгрузить отчет", command=self.export_clients_report, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=5)
        
        # Поиск
        search_frame = tk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_clients(search_entry.get()))
        
        # Таблица
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Имя", "Email", "Телефон", "Компания", "Статус", "Создан"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        # Настройка заголовков с сортировкой
        tree.heading("ID", text="ID", command=lambda: self._sort_clients("ID"))
        tree.heading("Имя", text="Имя", command=lambda: self._sort_clients("Имя"))
        tree.heading("Email", text="Email", command=lambda: self._sort_clients("Email"))
        tree.heading("Телефон", text="Телефон", command=lambda: self._sort_clients("Телефон"))
        tree.heading("Компания", text="Компания", command=lambda: self._sort_clients("Компания"))
        tree.heading("Статус", text="Статус", command=lambda: self._sort_clients("Статус"))
        tree.heading("Создан", text="Создан", command=lambda: self._sort_clients("Создан"))
        
        tree.column("ID", width=50)
        tree.column("Имя", width=150)
        tree.column("Email", width=200)
        tree.column("Телефон", width=120)
        tree.column("Компания", width=150)
        tree.column("Статус", width=100)
        tree.column("Создан", width=150)
        
        tree.pack(fill=tk.BOTH, expand=True)
        frame.clients_tree = tree
        frame.search_entry = search_entry
        
        return frame
    
    def _create_deals_tab(self) -> tk.Frame:
        """Создать вкладку сделок."""
        frame = tk.Frame(self.notebook)
        
        # Панель управления
        control_frame = tk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(control_frame, text="Обновить", command=self.refresh_deals).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Добавить", command=self.add_deal).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Редактировать", command=self.edit_deal).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Удалить", command=self.delete_deal).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Выгрузить отчет", command=self.export_deals_report, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=5)
        
        # Поиск
        search_frame = tk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_deals(search_entry.get()))
        
        # Таблица
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Название", "Сумма", "Валюта", "Статус", "Клиент ID", "Создана"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        # Настройка заголовков с сортировкой
        tree.heading("ID", text="ID", command=lambda: self._sort_deals("ID"))
        tree.heading("Название", text="Название", command=lambda: self._sort_deals("Название"))
        tree.heading("Сумма", text="Сумма", command=lambda: self._sort_deals("Сумма"))
        tree.heading("Валюта", text="Валюта", command=lambda: self._sort_deals("Валюта"))
        tree.heading("Статус", text="Статус", command=lambda: self._sort_deals("Статус"))
        tree.heading("Клиент ID", text="Клиент ID", command=lambda: self._sort_deals("Клиент ID"))
        tree.heading("Создана", text="Создана", command=lambda: self._sort_deals("Создана"))
        
        tree.column("ID", width=50)
        tree.column("Название", width=200)
        tree.column("Сумма", width=100)
        tree.column("Валюта", width=80)
        tree.column("Статус", width=100)
        tree.column("Клиент ID", width=100)
        tree.column("Создана", width=150)
        
        tree.pack(fill=tk.BOTH, expand=True)
        frame.deals_tree = tree
        frame.search_entry = search_entry
        
        return frame
    
    def _create_tasks_tab(self) -> tk.Frame:
        """Создать вкладку задач."""
        frame = tk.Frame(self.notebook)
        
        # Панель управления
        control_frame = tk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(control_frame, text="Обновить", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Добавить", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Редактировать", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Удалить", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Выгрузить отчет", command=self.export_tasks_report, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=5)
        
        # Поиск
        search_frame = tk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.refresh_tasks(search_entry.get()))
        
        # Таблица
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Название", "Описание", "Срок", "Выполнено", "Клиент ID", "Сделка ID"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.heading("Описание", text="Описание")
        tree.heading("Срок", text="Срок")
        tree.heading("Выполнено", text="Выполнено")
        tree.heading("Клиент ID", text="Клиент ID")
        tree.heading("Сделка ID", text="Сделка ID")
        
        tree.column("ID", width=50)
        tree.column("Название", width=150)
        tree.column("Описание", width=200)
        tree.column("Срок", width=120)
        tree.column("Выполнено", width=100)
        tree.column("Клиент ID", width=100)
        tree.column("Сделка ID", width=100)
        
        tree.pack(fill=tk.BOTH, expand=True)
        frame.tasks_tree = tree
        frame.search_entry = search_entry
        
        return frame
    
    def _create_settings_tab(self) -> tk.Frame:
        """Создать вкладку настроек."""
        frame = GoogleSettingsTab(self.notebook)
        self.google_settings_tab = frame
        return frame
    
    # Методы для работы с клиентами
    def _sort_clients(self, column: str):
        """Сортировать клиентов по колонке."""
        if self.clients_sort_column == column:
            self.clients_sort_reverse = not self.clients_sort_reverse
        else:
            self.clients_sort_column = column
            self.clients_sort_reverse = False
        self.refresh_clients()
    
    def refresh_clients(self, q: Optional[str] = None):
        """Обновить список клиентов."""
        try:
            tree = self.clients_tab.clients_tree
            for item in tree.get_children():
                tree.delete(item)
            
            clients = self.api_client.get_clients(q=q)
            
            # Применить сортировку если указана
            if self.clients_sort_column:
                column_map = {
                    "ID": lambda x: int(x.get('id', 0)),
                    "Имя": lambda x: str(x.get('name', '')).lower(),
                    "Email": lambda x: str(x.get('email', '')).lower(),
                    "Телефон": lambda x: str(x.get('phone', '')),
                    "Компания": lambda x: str(x.get('company', '') or '').lower(),
                    "Статус": lambda x: str(x.get('status', '')).lower(),
                    "Создан": lambda x: str(x.get('created_at', ''))
                }
                if self.clients_sort_column in column_map:
                    clients.sort(key=column_map[self.clients_sort_column], reverse=self.clients_sort_reverse)
            
            for client in clients:
                tree.insert("", tk.END, values=(
                    client.get('id'),
                    client.get('name', ''),
                    client.get('email', ''),
                    client.get('phone', ''),
                    client.get('company', ''),
                    client.get('status', ''),
                    client.get('created_at', '')
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить клиентов: {e}")
    
    def add_client(self):
        """Добавить клиента."""
        dialog = ClientDialog(self.root, "Добавить клиента")
        if dialog.result:
            try:
                self.api_client.create_client(dialog.result)
                self.refresh_clients()
                messagebox.showinfo("Успех", "Клиент добавлен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")
    
    def edit_client(self):
        """Редактировать клиента."""
        tree = self.clients_tab.clients_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования")
            return
        
        item = tree.item(selection[0])
        client_id = item['values'][0]
        
        try:
            client = self.api_client.get_client(client_id)
            
            dialog = ClientDialog(self.root, "Редактировать клиента", client)
            if dialog.result:
                self.api_client.update_client(client_id, dialog.result)
                self.refresh_clients()
                messagebox.showinfo("Успех", "Клиент обновлен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить клиента: {e}")
    
    def delete_client(self):
        """Удалить клиента."""
        tree = self.clients_tab.clients_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите клиента для удаления")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить клиента?"):
            return
        
        item = tree.item(selection[0])
        client_id = item['values'][0]
        
        try:
            self.api_client.delete_client(client_id)
            self.refresh_clients()
            messagebox.showinfo("Успех", "Клиент удален")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {e}")
    
    def export_clients_report(self):
        """Экспортировать отчет по клиентам."""
        try:
            settings = self.google_settings_tab.get_settings()
            if not settings.get('client_secret_path') or not settings.get('folder_id'):
                messagebox.showerror("Ошибка", "Настройте Google интеграцию в разделе Настройки")
                return
            
            clients = self.api_client.get_clients()
            generator = ReportGenerator(
                settings['client_secret_path'],
                settings['folder_id']
            )
            link = generator.export_clients_report(clients)
            messagebox.showinfo("Успех", f"Отчет создан!\nОткрыть в браузере?")
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {e}")
    
    # Методы для работы со сделками
    def _sort_deals(self, column: str):
        """Сортировать сделки по колонке."""
        if self.deals_sort_column == column:
            self.deals_sort_reverse = not self.deals_sort_reverse
        else:
            self.deals_sort_column = column
            self.deals_sort_reverse = False
        self.refresh_deals()
    
    def refresh_deals(self, q: Optional[str] = None):
        """Обновить список сделок."""
        try:
            tree = self.deals_tab.deals_tree
            for item in tree.get_children():
                tree.delete(item)
            
            deals = self.api_client.get_deals(q=q)
            
            # Применить сортировку если указана
            if self.deals_sort_column:
                column_map = {
                    "ID": lambda x: int(x.get('id', 0)),
                    "Название": lambda x: str(x.get('title', '')).lower(),
                    "Сумма": lambda x: float(x.get('amount', 0)),
                    "Валюта": lambda x: str(x.get('currency', '')).lower(),
                    "Статус": lambda x: str(x.get('status', '')).lower(),
                    "Клиент ID": lambda x: int(x.get('client_id', 0)) if x.get('client_id') else 0,
                    "Создана": lambda x: str(x.get('created_at', ''))
                }
                if self.deals_sort_column in column_map:
                    deals.sort(key=column_map[self.deals_sort_column], reverse=self.deals_sort_reverse)
            
            for deal in deals:
                tree.insert("", tk.END, values=(
                    deal.get('id'),
                    deal.get('title', ''),
                    deal.get('amount', 0),
                    deal.get('currency', ''),
                    deal.get('status', ''),
                    deal.get('client_id', ''),
                    deal.get('created_at', '')
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить сделки: {e}")
    
    def add_deal(self):
        """Добавить сделку."""
        dialog = DealDialog(self.root, "Добавить сделку")
        if dialog.result:
            try:
                self.api_client.create_deal(dialog.result)
                self.refresh_deals()
                messagebox.showinfo("Успех", "Сделка добавлена")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить сделку: {e}")
    
    def edit_deal(self):
        """Редактировать сделку."""
        tree = self.deals_tab.deals_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите сделку для редактирования")
            return
        
        item = tree.item(selection[0])
        deal_id = item['values'][0]
        
        try:
            deal = self.api_client.get_deal(deal_id)
            
            dialog = DealDialog(self.root, "Редактировать сделку", deal)
            if dialog.result:
                self.api_client.update_deal(deal_id, dialog.result)
                self.refresh_deals()
                messagebox.showinfo("Успех", "Сделка обновлена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить сделку: {e}")
    
    def delete_deal(self):
        """Удалить сделку."""
        tree = self.deals_tab.deals_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите сделку для удаления")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить сделку?"):
            return
        
        item = tree.item(selection[0])
        deal_id = item['values'][0]
        
        try:
            self.api_client.delete_deal(deal_id)
            self.refresh_deals()
            messagebox.showinfo("Успех", "Сделка удалена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить сделку: {e}")
    
    def export_deals_report(self):
        """Экспортировать отчет по сделкам."""
        try:
            settings = self.google_settings_tab.get_settings()
            if not settings.get('client_secret_path') or not settings.get('folder_id'):
                messagebox.showerror("Ошибка", "Настройте Google интеграцию в разделе Настройки")
                return
            
            deals = self.api_client.get_deals()
            generator = ReportGenerator(
                settings['client_secret_path'],
                settings['folder_id']
            )
            link = generator.export_deals_report(deals)
            messagebox.showinfo("Успех", f"Отчет создан!\nОткрыть в браузере?")
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {e}")
    
    # Методы для работы с задачами
    def _sort_tasks(self, column: str):
        """Сортировать задачи по колонке."""
        if self.tasks_sort_column == column:
            self.tasks_sort_reverse = not self.tasks_sort_reverse
        else:
            self.tasks_sort_column = column
            self.tasks_sort_reverse = False
        self.refresh_tasks()
    
    def refresh_tasks(self, q: Optional[str] = None):
        """Обновить список задач."""
        try:
            tree = self.tasks_tab.tasks_tree
            for item in tree.get_children():
                tree.delete(item)
            
            tasks = self.api_client.get_tasks(q=q)
            
            # Применить сортировку если указана
            if self.tasks_sort_column:
                column_map = {
                    "ID": lambda x: int(x.get('id', 0)),
                    "Название": lambda x: str(x.get('title', '')).lower(),
                    "Описание": lambda x: str(x.get('description', '') or '').lower(),
                    "Срок": lambda x: str(x.get('due_date', '') or ''),
                    "Выполнено": lambda x: (0 if x.get('is_done') else 1),
                    "Клиент ID": lambda x: int(x.get('client_id', 0)) if x.get('client_id') else 0,
                    "Сделка ID": lambda x: int(x.get('deal_id', 0)) if x.get('deal_id') else 0
                }
                if self.tasks_sort_column in column_map:
                    tasks.sort(key=column_map[self.tasks_sort_column], reverse=self.tasks_sort_reverse)
            
            for task in tasks:
                tree.insert("", tk.END, values=(
                    task.get('id'),
                    task.get('title', ''),
                    task.get('description', '')[:50] + '...' if task.get('description') and len(task.get('description', '')) > 50 else task.get('description', ''),
                    task.get('due_date', ''),
                    "Да" if task.get('is_done') else "Нет",
                    task.get('client_id', ''),
                    task.get('deal_id', '')
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")
    
    def add_task(self):
        """Добавить задачу."""
        dialog = TaskDialog(self.root, "Добавить задачу")
        if dialog.result:
            try:
                self.api_client.create_task(dialog.result)
                self.refresh_tasks()
                messagebox.showinfo("Успех", "Задача добавлена")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось добавить задачу: {e}")
    
    def edit_task(self):
        """Редактировать задачу."""
        tree = self.tasks_tab.tasks_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return
        
        item = tree.item(selection[0])
        task_id = item['values'][0]
        
        try:
            task = self.api_client.get_task(task_id)
            
            dialog = TaskDialog(self.root, "Редактировать задачу", task)
            if dialog.result:
                self.api_client.update_task(task_id, dialog.result)
                self.refresh_tasks()
                messagebox.showinfo("Успех", "Задача обновлена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить задачу: {e}")
    
    def delete_task(self):
        """Удалить задачу."""
        tree = self.tasks_tab.tasks_tree
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить задачу?"):
            return
        
        item = tree.item(selection[0])
        task_id = item['values'][0]
        
        try:
            self.api_client.delete_task(task_id)
            self.refresh_tasks()
            messagebox.showinfo("Успех", "Задача удалена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить задачу: {e}")
    
    def export_tasks_report(self):
        """Экспортировать отчет по задачам."""
        try:
            settings = self.google_settings_tab.get_settings()
            if not settings.get('client_secret_path') or not settings.get('folder_id'):
                messagebox.showerror("Ошибка", "Настройте Google интеграцию в разделе Настройки")
                return
            
            tasks = self.api_client.get_tasks()
            generator = ReportGenerator(
                settings['client_secret_path'],
                settings['folder_id']
            )
            link = generator.export_tasks_report(tasks)
            messagebox.showinfo("Успех", f"Отчет создан!\nОткрыть в браузере?")
            webbrowser.open(link)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать отчет: {e}")
    
    def refresh_all(self):
        """Обновить все вкладки."""
        self.refresh_clients()
        self.refresh_deals()
        self.refresh_tasks()


# Диалоги для ввода данных
class ClientDialog:
    """Диалог для добавления/редактирования клиента."""
    
    def __init__(self, parent, title: str, client: Optional[dict] = None):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.transient(parent)
        dialog.grab_set()
        
        tk.Label(dialog, text="Имя:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        if client:
            name_entry.insert(0, client.get('name', ''))
        
        tk.Label(dialog, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        email_entry = tk.Entry(dialog, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        if client:
            email_entry.insert(0, client.get('email', ''))
        
        tk.Label(dialog, text="Телефон:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.grid(row=2, column=1, padx=10, pady=5)
        if client:
            phone_entry.insert(0, client.get('phone', ''))
        
        tk.Label(dialog, text="Компания:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        company_entry = tk.Entry(dialog, width=30)
        company_entry.grid(row=3, column=1, padx=10, pady=5)
        if client:
            company_entry.insert(0, client.get('company', ''))
        
        tk.Label(dialog, text="Статус:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        status_var = tk.StringVar(value=client.get('status', 'active') if client else 'active')
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=["active", "archived"], width=27)
        status_combo.grid(row=4, column=1, padx=10, pady=5)
        
        def save():
            self.result = {
                'name': name_entry.get(),
                'email': email_entry.get() or None,
                'phone': phone_entry.get() or None,
                'company': company_entry.get() or None,
                'status': status_var.get()
            }
            if not self.result['name']:
                messagebox.showerror("Ошибка", "Имя обязательно")
                return
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=5, column=1, pady=10)
        tk.Button(dialog, text="Отмена", command=dialog.destroy).grid(row=5, column=0, pady=10)
        
        dialog.wait_window()


class DealDialog:
    """Диалог для добавления/редактирования сделки."""
    
    def __init__(self, parent, title: str, deal: Optional[dict] = None):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(parent)
        dialog.grab_set()
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        if deal:
            title_entry.insert(0, deal.get('title', ''))
        
        tk.Label(dialog, text="Сумма:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        amount_entry = tk.Entry(dialog, width=30)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)
        if deal:
            amount_entry.insert(0, deal.get('amount', 0))
        
        tk.Label(dialog, text="Валюта:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        currency_var = tk.StringVar(value=deal.get('currency', 'RUB') if deal else 'RUB')
        currency_combo = ttk.Combobox(dialog, textvariable=currency_var, values=["RUB", "USD", "EUR"], width=27)
        currency_combo.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Статус:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        status_var = tk.StringVar(value=deal.get('status', 'new') if deal else 'new')
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=["new", "in_progress", "closed", "cancelled"], width=27)
        status_combo.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Клиент ID:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        client_id_entry = tk.Entry(dialog, width=30)
        client_id_entry.grid(row=4, column=1, padx=10, pady=5)
        if deal and deal.get('client_id'):
            client_id_entry.insert(0, deal.get('client_id'))
        
        def save():
            self.result = {
                'title': title_entry.get(),
                'amount': float(amount_entry.get() or 0),
                'currency': currency_var.get(),
                'status': status_var.get(),
                'client_id': int(client_id_entry.get()) if client_id_entry.get() else None
            }
            if not self.result['title']:
                messagebox.showerror("Ошибка", "Название обязательно")
                return
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=5, column=1, pady=10)
        tk.Button(dialog, text="Отмена", command=dialog.destroy).grid(row=5, column=0, pady=10)
        
        dialog.wait_window()


class TaskDialog:
    """Диалог для добавления/редактирования задачи."""
    
    def __init__(self, parent, title: str, task: Optional[dict] = None):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(parent)
        dialog.grab_set()
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        if task:
            title_entry.insert(0, task.get('title', ''))
        
        tk.Label(dialog, text="Описание:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        description_text = tk.Text(dialog, width=30, height=5)
        description_text.grid(row=1, column=1, padx=10, pady=5)
        if task:
            description_text.insert('1.0', task.get('description', ''))
        
        tk.Label(dialog, text="Срок (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        due_date_entry = tk.Entry(dialog, width=30)
        due_date_entry.grid(row=2, column=1, padx=10, pady=5)
        if task and task.get('due_date'):
            due_date_entry.insert(0, task.get('due_date'))
        
        is_done_var = tk.BooleanVar(value=task.get('is_done', False) if task else False)
        tk.Checkbutton(dialog, text="Выполнено", variable=is_done_var).grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        tk.Label(dialog, text="Клиент ID:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        client_id_entry = tk.Entry(dialog, width=30)
        client_id_entry.grid(row=4, column=1, padx=10, pady=5)
        if task and task.get('client_id'):
            client_id_entry.insert(0, task.get('client_id'))
        
        def save():
            self.result = {
                'title': title_entry.get(),
                'description': description_text.get('1.0', tk.END).strip() or None,
                'due_date': due_date_entry.get() or None,
                'is_done': is_done_var.get(),
                'client_id': int(client_id_entry.get()) if client_id_entry.get() else None
            }
            if not self.result['title']:
                messagebox.showerror("Ошибка", "Название обязательно")
                return
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=5, column=1, pady=10)
        tk.Button(dialog, text="Отмена", command=dialog.destroy).grid(row=5, column=0, pady=10)
        
        dialog.wait_window()

