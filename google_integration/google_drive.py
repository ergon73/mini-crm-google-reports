"""
Модуль для работы с Google Drive API через OAuth2.
Создание файлов от имени пользователя.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]


class GoogleDrive:
    """Клиент для создания файлов в Google Drive через OAuth2."""
    
    def __init__(
        self,
        client_secret_path: str,
        token_path: str = "token.pickle"
    ):
        """
        Args:
            client_secret_path: Путь к client_secret.json (OAuth Desktop)
            token_path: Путь для сохранения токена
        """
        self.client_secret_path = client_secret_path
        self.token_path = token_path
        self.credentials = None
        self._authenticate()
        
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
    
    def _authenticate(self):
        """OAuth2 аутентификация с сохранением токена."""
        # Загрузить существующий токен
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Если токена нет или он невалиден
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_path,
                    SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            
            # Сохранить токен
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.credentials, token)
    
    def create_spreadsheet(self, name: str, folder_id: str) -> dict:
        """
        Создать Google Spreadsheet в указанной папке.
        
        Args:
            name: Название файла
            folder_id: ID папки на Drive
            
        Returns:
            {"id": str, "name": str, "webViewLink": str}
        """
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }
        
        file = self.drive_service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()
        
        return {
            'id': file['id'],
            'name': file['name'],
            'webViewLink': file['webViewLink']
        }
    
    def get_credentials(self):
        """Получить credentials для передачи в GoogleSheetsClient."""
        return self.credentials

