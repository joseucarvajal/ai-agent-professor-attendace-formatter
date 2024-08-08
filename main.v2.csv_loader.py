import os
import pandas as pd
from dotenv import load_dotenv
import openai
import json
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph
from pydantic import BaseModel, Field
from typing import List, Optional

# Cargar variables de entorno desde .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Definir la clase Student
class Student(BaseModel):
    code: str
    fullName: str
    email: str

# Configurar ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Definir function_1 para leer el archivo CSV y enviar el prompt a ChatGPT
def function_1(file_path: str) -> str:
    # Leer el archivo CSV
    df = pd.read_csv(file_path)
    csv_content = df.to_csv(index=False)
    
    # Crear el prompt
    prompt = f"Read the following CSV data and format it into a JSON array of objects with 'code', 'fullName', and 'email'. The 'emails' should be separated by comma :\n\n{csv_content}"
    
    # Enviar el prompt a ChatGPT
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = llm.invoke(messages)
    
    # Acceder al contenido de la respuesta de manera adecuada
    formatted_data = response.content


    print('formatted data ' + formatted_data)

    return formatted_data

# Definir function_2 para formatear la respuesta en una lista de objetos Student
def function_2(formatted_data: str) -> List[Student]:
    try:
        students = json.loads(formatted_data)
        student_objects = [Student(**student) for student in students]
        return student_objects
    except Exception as e:
        print(f"Failed to parse and format data: {e}")
        return []

# Crear el grafo
workflow = Graph()
workflow.add_node("node_1", function_1)
workflow.add_node("node_2", function_2)

# Conectar los nodos
workflow.add_edge("node_1", "node_2")

# Establecer punto de entrada y punto de finalización
workflow.set_entry_point("node_1")
workflow.set_finish_point("node_2")

# Compilar el grafo
app = workflow.compile()

# Ejecutar el flujo de trabajo
file_path = 'data/listaAsistencia.xls - Programacion II.csv'  # Reemplaza con la ruta real
result = app.invoke(file_path)

# Imprimir el resultado
for student in result:
    print(student)
