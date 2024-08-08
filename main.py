import os
import pandas as pd
from dotenv import load_dotenv
import json
import openai
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph
from pydantic import BaseModel
from typing import List
from google_sheets_service import get_google_services

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Student(BaseModel):
    code: str
    fullName: str
    email: str

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

course_name = input("Course name: ").strip()

def process_csv_to_json(file_path: str) -> str:
    df = pd.read_csv(file_path)
    csv_content = df.to_csv(index=False)
    
    prompt = f"Read the following CSV data and format it into a JSON array of objects with 'code', 'fullName', and 'email'. The 'emails' should be separated by comma :\n\n{csv_content}"
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = llm.invoke(messages)
    
    formatted_data = response.content
    formatted_data = formatted_data.strip('```json').strip('```').strip()

    return formatted_data

def create_google_sheet_with_data(formatted_data: str) -> str:
    try:
        students = json.loads(formatted_data)
        student_objects = [Student(**student) for student in students]
        
        sheets_service, drive_service = get_google_services()

        template_id = '1MXJZ2HQW76Wi9NAQFqrDsT9GEWf27RVnrfZfCjPvYzw'
        copy = drive_service.files().copy(
            fileId=template_id,
            body={'name': course_name}
        ).execute()
        spreadsheet_id = copy['id']

        sheet_names = ['Corte 1', 'Corte 2', 'Corte 3', 'Definitiva']
        
        for sheet_name in sheet_names:
            if sheet_name == 'Corte 1':
                values = []
                for student in student_objects:
                    values.append([student.code, student.fullName, student.email])
            else:
                values = []
                for student in student_objects:
                    values.append([student.code, student.fullName])

            body = {
                'values': values
            }

            sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=f'{sheet_name}!A2',
                valueInputOption='RAW',
                body=body
            ).execute()

        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    except Exception as e:
        print(f"Failed to parse and format data: {e}")
        return ""

workflow = Graph()
workflow.add_node("node_process_csv_to_json", process_csv_to_json)
workflow.add_node("node_create_google_sheet_with_data", create_google_sheet_with_data)

workflow.add_edge("node_process_csv_to_json", "node_create_google_sheet_with_data")

workflow.set_entry_point("node_process_csv_to_json")
workflow.set_finish_point("node_create_google_sheet_with_data")

app = workflow.compile()

file_path = 'data/listaAsistencia.csv'

result = app.invoke(file_path)

print(f"Generated Google Sheet URL: {result}")
