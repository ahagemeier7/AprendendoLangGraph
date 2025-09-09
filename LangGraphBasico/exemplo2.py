#--------------------------------------
#Desenhando o grafo
#--------------------------------------
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from pydantic import BaseModel
from langchain_core.runnables.graph import MermaidDrawMethod
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

#instanciando o modelo
llm_model = GoogleGenerativeAI(model="gemini-2.5-flash",api_key = API_KEY)

#definição do graph state
class GraphState(BaseModel):
    input: str
    output: str
    
#Função de resposta
def responder(state):
    input_message = state.input
    response = llm_model.invoke([HumanMessage(content=input_message)])
    return GraphState(input=state.input, output=response)

#Criando o graph
graph = StateGraph(GraphState)
graph.add_node("responder",responder)
graph.set_entry_point("responder")
graph.set_finish_point("responder")

#compilando o grafo
export_graph = graph.compile()

#gerando a imagem do grafo
png_bytes = export_graph.get_graph().draw_mermaid_png(
    draw_method = MermaidDrawMethod.API
)

with open("grafo_exemplo1.png","wb") as f:
    f.write(png_bytes)

#testando o agente
if __name__ == "__main__":
    result = export_graph.invoke(GraphState(input="Quem descobriu a américa",output=""))
    print(result)

