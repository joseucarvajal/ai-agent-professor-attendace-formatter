from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import TypedDict, Optional, List


class GraphState(TypedDict):
    """ Represents the state of our graph """
    prompt: str
    nombres_estudiantes: List[str]


# OpenAI api key is stored in .env file
load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


system_prompt_technical_assistant = """
You are a technical informatics assistant expert in csv and data extraction from csv files
"""


technical_assistant = ChatPromptTemplate.from_messages([
    SystemMessage(content=system_prompt_technical_assistant),
    HumanMessage(content="{prompt}")
])


class GeneratedStudents(BaseModel):
    """Students data in this format"""
    students_names: Optional[List[str]] = Field(
        [], description="list of the students extracted from the csv file")
    
technical_assistant_agent = technical_assistant | llm.with_structured_output(GeneratedStudents, method="json_mode")

