# google_sheets_tool.py
from langgraph.core import Graph  # Ajusta esta importación según la estructura de langgraph
from google_sheets_service import get_google_sheets_service
import json

class Tool:
    def __init__(self, name):
        self.name = name

    def run(self, input_data: str) -> str:
        raise NotImplementedError("Subclasses should implement this!")

class GoogleSheetsTool(Tool):
    def __init__(self):
        super().__init__("google_sheets_tool")

    def run(self, input_data: str) -> str:
        students = json.loads(input_data)
        
        service = get_google_sheets_service()
        template_id = '1THaO5CZzHXyirjWB__nk7bUqw9UcOZIA'  # Reemplaza con el ID de tu plantilla
        copy_title = 'Lista de Estudiantes Generada'
        copy = service.files().copy(
            fileId=template_id,
            body={'name': copy_title}
        ).execute()
        spreadsheet_id = copy['id']

        values = [['Code', 'FullName', 'Email']]
        for student in students:
            values.append([student['code'], student['fullName'], student['email']])

        body = {
            'values': values
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
