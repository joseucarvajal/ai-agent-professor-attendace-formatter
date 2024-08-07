from dotenv import load_dotenv
from langgraph.graph import Graph

def function_1(input_1):
    return input_1 + " Hi"

def function_2(input_2):
    return input_2 + " there"

workflow = Graph()
workflow.add_node("node_1", function_1)
workflow.add_node("node_2", function_2)

workflow.add_edge("node_1", "node_2")

workflow.set_entry_point("node_1")
workflow.set_finish_point("node_2")

# Compilar el grafo
app = workflow.compile()

# Ejecutar el flujo de trabajo
result = app.invoke("Hello")
print(result)