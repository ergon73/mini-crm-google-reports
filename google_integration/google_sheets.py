"""
Модуль для работы с Google Sheets API.
Поддерживает как Service Account, так и OAuth2 credentials.
"""

import os
from typing import Optional, List, Tuple
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def sanitize_value(value) -> str:
    """
    Защита от formula injection.
    Преобразует значения, начинающиеся с '=', '+', '-', '@' в строки.
    """
    if value is None:
        return ""
    
    str_value = str(value)
    if str_value and str_value[0] in ('=', '+', '-', '@'):
        return "'" + str_value
    return str_value


class GoogleSheetsClient:
    """Клиент для работы с Google Sheets API."""
    
    def __init__(
        self, 
        credentials_path: Optional[str] = None, 
        spreadsheet_id: Optional[str] = None,
        oauth_credentials = None  # НОВОЕ: принимает готовые OAuth credentials
    ):
        """
        Args:
            credentials_path: Путь к JSON-ключу Service Account
            spreadsheet_id: ID таблицы
            oauth_credentials: Готовые OAuth2 credentials (от GoogleDrive)
        """
        self.spreadsheet_id = spreadsheet_id or os.getenv("GSHEETS_SPREADSHEET_ID")
        
        # Приоритет: OAuth credentials > Service Account
        if oauth_credentials:
            self.credentials = oauth_credentials
        elif credentials_path or os.getenv("GSHEETS_CREDENTIALS_PATH"):
            creds_path = credentials_path or os.getenv("GSHEETS_CREDENTIALS_PATH")
            self.credentials = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        else:
            raise ValueError("Нужны credentials: oauth_credentials или credentials_path")
        
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheets = self.service.spreadsheets()
    
    def set_spreadsheet_id(self, spreadsheet_id: str):
        """Установить ID таблицы (для работы с только что созданной)."""
        self.spreadsheet_id = spreadsheet_id
    
    def get_sheet_names(self) -> List[str]:
        """Получить список названий листов."""
        try:
            spreadsheet = self.sheets.get(spreadsheetId=self.spreadsheet_id).execute()
            return [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
        except HttpError as error:
            raise Exception(f"Ошибка при получении списка листов: {error}")
    
    def create_sheet(self, title: str) -> int:
        """
        Создать новый лист.
        
        Returns:
            sheet_id созданного листа
        """
        try:
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': title
                        }
                    }
                }]
            }
            response = self.sheets.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=request_body
            ).execute()
            return response['replies'][0]['addSheet']['properties']['sheetId']
        except HttpError as error:
            raise Exception(f"Ошибка при создании листа: {error}")
    
    def write_range(self, range_name: str, values: List[List]):
        """
        Записать данные в диапазон.
        
        Args:
            range_name: Диапазон (например, "A1:C3")
            values: Список списков значений
        """
        try:
            # Санитизировать значения
            sanitized_values = [
                [sanitize_value(cell) for cell in row] 
                for row in values
            ]
            
            body = {
                'values': sanitized_values
            }
            self.sheets.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
        except HttpError as error:
            raise Exception(f"Ошибка при записи данных: {error}")
    
    def format_cells(
        self,
        sheet_id: int,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        bg_color: Optional[Tuple[float, float, float]] = None,
        text_color: Optional[Tuple[float, float, float]] = None,
        text_bold: bool = False,
        text_size: Optional[int] = None,
        h_align: Optional[str] = None
    ):
        """
        Форматировать ячейки.
        
        Args:
            sheet_id: ID листа
            start_row: Начальная строка (0-based)
            end_row: Конечная строка (не включительно)
            start_col: Начальная колонка (0-based)
            end_col: Конечная колонка (не включительно)
            bg_color: RGB цвет фона (0.0-1.0)
            text_color: RGB цвет текста (0.0-1.0)
            text_bold: Жирный текст
            text_size: Размер шрифта
            h_align: Горизонтальное выравнивание ("LEFT", "CENTER", "RIGHT")
        """
        try:
            requests = []
            
            # Форматирование ячеек
            cell_format = {}
            
            if bg_color:
                cell_format['backgroundColor'] = {
                    'red': bg_color[0],
                    'green': bg_color[1],
                    'blue': bg_color[2]
                }
            
            text_format = {}
            if text_color:
                text_format['foregroundColor'] = {
                    'red': text_color[0],
                    'green': text_color[1],
                    'blue': text_color[2]
                }
            if text_bold:
                text_format['bold'] = True
            if text_size:
                text_format['fontSize'] = text_size
            
            if text_format:
                cell_format['textFormat'] = text_format
            
            if h_align:
                cell_format['horizontalAlignment'] = h_align
            
            if cell_format:
                requests.append({
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': start_row,
                            'endRowIndex': end_row,
                            'startColumnIndex': start_col,
                            'endColumnIndex': end_col
                        },
                        'cell': {
                            'userEnteredFormat': cell_format
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
                    }
                })
            
            if requests:
                self.sheets.batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body={'requests': requests}
                ).execute()
        except HttpError as error:
            raise Exception(f"Ошибка при форматировании ячеек: {error}")
    
    def merge_cells(
        self,
        sheet_id: int,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int
    ):
        """Объединить ячейки."""
        try:
            self.sheets.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    'requests': [{
                        'mergeCells': {
                            'range': {
                                'sheetId': sheet_id,
                                'startRowIndex': start_row,
                                'endRowIndex': end_row,
                                'startColumnIndex': start_col,
                                'endColumnIndex': end_col
                            },
                            'mergeType': 'MERGE_ALL'
                        }
                    }]
                }
            ).execute()
        except HttpError as error:
            raise Exception(f"Ошибка при объединении ячеек: {error}")
    
    def set_borders(
        self,
        sheet_id: int,
        start_row: int,
        end_row: int,
        start_col: int,
        end_col: int,
        style: str = "SOLID",
        width: int = 1,
        color: Tuple[float, float, float] = (0, 0, 0)
    ):
        """
        Установить границы для диапазона ячеек.
        
        Args:
            sheet_id: ID листа
            start_row: Начальная строка (0-based)
            end_row: Конечная строка (не включительно)
            start_col: Начальная колонка (0-based)
            end_col: Конечная колонка (не включительно)
            style: Стиль границы ("SOLID", "DASHED", etc.)
            width: Толщина границы
            color: RGB цвет границы (0.0-1.0)
        """
        try:
            border = {
                'style': style,
                'width': width,
                'color': {
                    'red': color[0],
                    'green': color[1],
                    'blue': color[2]
                }
            }
            
            self.sheets.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    'requests': [{
                        'updateBorders': {
                            'range': {
                                'sheetId': sheet_id,
                                'startRowIndex': start_row,
                                'endRowIndex': end_row,
                                'startColumnIndex': start_col,
                                'endColumnIndex': end_col
                            },
                            'top': border,
                            'bottom': border,
                            'left': border,
                            'right': border,
                            'innerHorizontal': border,
                            'innerVertical': border
                        }
                    }]
                }
            ).execute()
        except HttpError as error:
            raise Exception(f"Ошибка при установке границ: {error}")

