from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

#instanciando o modelo
llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = API_KEY)

#Define o prompt do sistema
system_message = SystemMessage(content="""
Você é um assistente. Se o usuario pedir contas, use a ferramente 'somar'. Caso contrario, responda normalmente.
""")

#Definindo a ferramente de soma
@tool("somar")
def somar(valores:str):
  """Soma dois numeros separados por vírgula"""
  try:
    a,b = map(float, valores.split(","))
    return str(a + b)
  except Exception as e:
    return "Erro ao somar os valores: " + str(e)
  
#Criação do agente com LangGraph
tools = [somar]
graph = create_react_agent(model=llm_model,tools=tools,prompt=system_message)

export_graph = graph

#extrair resposta final
def extrair_resposta_final(result):
  ai_message = [m for m in result["messages"] if isinstance(m, AIMessage) and m.content]
  if ai_message:
    return ai_message[-1].content
  else:
    return "Nenhuma resposta gerada."
  
#gerando a imagem do grafo
png_bytes = export_graph.get_graph().draw_mermaid_png(
    draw_method = MermaidDrawMethod.API
)

with open("grafo_exemplo3.png","wb") as f:
    f.write(png_bytes)


#testando o agente
if __name__ == "__main__":
  entrada1 = HumanMessage(content="Quanto é 8 + 5?")
  result1 = export_graph.invoke({"messages": [entrada1]})
  resposta_texto_1 = extrair_resposta_final(result1)
  print("resposta 1:", resposta_texto_1)

  print()

  entrada2 = HumanMessage(content="Quem pintou a monalisa?")
  result2 = export_graph.invoke({"messages": [entrada2]})
  resposta_texto_2 = extrair_resposta_final(result2)
  print("resposta 2:", resposta_texto_2)


  #gerando a imagem do grafo
png_bytes = export_graph.get_graph().draw_mermaid_png(
    draw_method = MermaidDrawMethod.API
)


