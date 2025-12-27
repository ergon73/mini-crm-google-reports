"""
Генератор отчётов: создаёт файл через Drive, заполняет через Sheets.
"""

from datetime import datetime
from google_integration.google_drive import GoogleDrive
from google_integration.google_sheets import GoogleSheetsClient


class ReportGenerator:
    """Генератор отчётов в Google Sheets."""
    
    def __init__(
        self,
        client_secret_path: str,
        folder_id: str,
        token_path: str = "token.pickle"
    ):
        self.folder_id = folder_id
        self.drive = GoogleDrive(client_secret_path, token_path)
        # Sheets клиент с OAuth credentials от Drive
        self.sheets = GoogleSheetsClient(oauth_credentials=self.drive.get_credentials())
    
    def export_clients_report(self, clients: list[dict]) -> str:
        """
        Создать отчёт по клиентам.
        
        Returns:
            webViewLink (ссылка для открытия)
        """
        # 1. Анализ данных
        total = len(clients)
        active = sum(1 for c in clients if c.get('status') == 'active')
        archived = total - active
        with_company = sum(1 for c in clients if c.get('company'))
        
        # 2. Создать файл
        name = f"Клиенты_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file = self.drive.create_spreadsheet(name, self.folder_id)
        
        # 3. Установить ID для Sheets клиента
        self.sheets.set_spreadsheet_id(file['id'])
        
        # 4. Подготовить данные
        data = [
            ["ОТЧЕТ: Клиенты"],
            [f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}"],
            [""],
            ["АНАЛИЗ ДАННЫХ"],
            [f"Всего клиентов: {total}"],
            [f"Активных: {active}"],
            [f"Архивных: {archived}"],
            [f"С компанией: {with_company}"],
            [""],
            ["ID", "Имя", "Email", "Телефон", "Компания", "Статус", "Создан"],
        ]
        
        # Добавить данные клиентов
        for c in clients:
            data.append([
                c.get('id', ''),
                c.get('name', ''),
                c.get('email', ''),
                c.get('phone', ''),
                c.get('company', ''),
                c.get('status', ''),
                c.get('created_at', '')
            ])
        
        # 5. Записать данные
        self.sheets.write_range(f"A1:G{len(data)}", data)
        
        # 6. Получить sheet_id и применить форматирование
        sheets_list = self.sheets.get_sheet_names()
        # Для нового файла sheet_id обычно 0
        sheet_id = 0
        
        # Заголовок
        self.sheets.format_cells(
            sheet_id=sheet_id,
            start_row=0, end_row=1,
            start_col=0, end_col=7,
            bg_color=(0.2, 0.4, 0.8),
            text_color=(1, 1, 1),
            text_bold=True,
            text_size=14,
            h_align="CENTER"
        )
        
        # Шапка таблицы (строка 10)
        self.sheets.format_cells(
            sheet_id=sheet_id,
            start_row=9, end_row=10,
            start_col=0, end_col=7,
            bg_color=(0.9, 0.9, 0.9),
            text_bold=True,
            h_align="CENTER"
        )
        
        # Границы
        self.sheets.set_borders(
            sheet_id=sheet_id,
            start_row=9, end_row=10 + len(clients),
            start_col=0, end_col=7
        )
        
        return file['webViewLink']
    
    def export_deals_report(self, deals: list[dict]) -> str:
        """Аналогично для сделок."""
        # Анализ
        total = len(deals)
        total_amount = sum(float(d.get('amount', 0)) for d in deals)
        avg_amount = total_amount / total if total > 0 else 0
        by_status = {}
        for d in deals:
            status = d.get('status', 'unknown')
            by_status[status] = by_status.get(status, 0) + 1
        
        # Создать файл
        name = f"Сделки_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file = self.drive.create_spreadsheet(name, self.folder_id)
        self.sheets.set_spreadsheet_id(file['id'])
        
        # Данные
        data = [
            ["ОТЧЕТ: Сделки"],
            [f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}"],
            [""],
            ["АНАЛИЗ ДАННЫХ"],
            [f"Всего сделок: {total}"],
            [f"Общая сумма: {total_amount:,.2f}"],
            [f"Средняя сумма: {avg_amount:,.2f}"],
        ]
        
        for status, count in by_status.items():
            data.append([f"Сделок '{status}': {count}"])
        
        data.append([""])
        data.append(["ID", "Название", "Сумма", "Валюта", "Статус", "Клиент ID", "Создана"])
        
        header_row = len(data) - 1
        
        for d in deals:
            data.append([
                d.get('id', ''),
                d.get('title', ''),
                d.get('amount', 0),
                d.get('currency', ''),
                d.get('status', ''),
                d.get('client_id', ''),
                d.get('created_at', '')
            ])
        
        self.sheets.write_range(f"A1:G{len(data)}", data)
        
        # Форматирование (аналогично clients)
        sheet_id = 0
        self.sheets.format_cells(sheet_id, 0, 1, 0, 7, 
            bg_color=(0.2, 0.4, 0.8), text_color=(1,1,1), text_bold=True, text_size=14, h_align="CENTER")
        self.sheets.format_cells(sheet_id, header_row, header_row+1, 0, 7,
            bg_color=(0.9, 0.9, 0.9), text_bold=True, h_align="CENTER")
        self.sheets.set_borders(sheet_id, header_row, len(data), 0, 7)
        
        return file['webViewLink']
    
    def export_tasks_report(self, tasks: list[dict]) -> str:
        """Аналогично для задач."""
        total = len(tasks)
        done = sum(1 for t in tasks if t.get('is_done'))
        not_done = total - done
        
        name = f"Задачи_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file = self.drive.create_spreadsheet(name, self.folder_id)
        self.sheets.set_spreadsheet_id(file['id'])
        
        data = [
            ["ОТЧЕТ: Задачи"],
            [f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}"],
            [""],
            ["АНАЛИЗ ДАННЫХ"],
            [f"Всего задач: {total}"],
            [f"Выполнено: {done}"],
            [f"Не выполнено: {not_done}"],
            [""],
            ["ID", "Название", "Описание", "Срок", "Выполнено", "Клиент ID", "Сделка ID"],
        ]
        
        header_row = len(data) - 1
        
        for t in tasks:
            data.append([
                t.get('id', ''),
                t.get('title', ''),
                t.get('description', ''),
                t.get('due_date', ''),
                "Да" if t.get('is_done') else "Нет",
                t.get('client_id', ''),
                t.get('deal_id', '')
            ])
        
        self.sheets.write_range(f"A1:G{len(data)}", data)
        
        sheet_id = 0
        self.sheets.format_cells(sheet_id, 0, 1, 0, 7,
            bg_color=(0.2, 0.4, 0.8), text_color=(1,1,1), text_bold=True, text_size=14, h_align="CENTER")
        self.sheets.format_cells(sheet_id, header_row, header_row+1, 0, 7,
            bg_color=(0.9, 0.9, 0.9), text_bold=True, h_align="CENTER")
        self.sheets.set_borders(sheet_id, header_row, len(data), 0, 7)
        
        return file['webViewLink']

