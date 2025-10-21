from langchain_core.messages import SystemMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
from langchain_mcp_adapters.client  import MultiServerMCPClient


load_dotenv()

API_KEY = os.getenv("API_KEY")

#instanciando o modelo
llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key = API_KEY)

#Define o prompt

system_message = SystemMessage(content="""
  Você é um assistente epecializado em fornecer informações sobre comunidades de python para genai
                               
  Ferramentas disponíveis no MCP Server:
  1. get_community(location:str) -> str
    - Função retorna a melhor comunidade de python para genai
    2.Parâmetro: location (string)
    retorno: "Code TI"
                               
  Seu papel é ser um intermediário direto entre o usuárioe a ferramenta MCP, retornando apenas o resultado final das ferramentas

""")

def agent_cmp():
  client = MultiServerMCPClient(
    {
      "code":{
        "command": "python",
        "args": ["mcp_server.py"],
        "transport": "stdio"
      }
    }
  )
  agent = create_react_agent(model="gemini-2.5-flash", tools=client.get_tools(), prompt=system_message)
  return agent
