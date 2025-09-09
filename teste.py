from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

#Configuracoes iniciais
load_dotenv()
API_KEY=os.getenv("API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=API_KEY)

#prompt do sistema
system_message = SystemMessage(content="""
Voce e um pesquisador muito sarcastico e ironico,
use ferramenta 'search' sempre que necessario,
especialmente para perguntas que exigem informacoes da web
                               """)

#Criando a ferramenta search
@tool('search')
def search_web(query:str = "") -> str:
    """
    Busca informacoes na web baseada na consulta fornecida
    
    Args: 
        query: termos para buscar dados na web
    
    Returns: 
        As informacoes encontradas na web ou uma mensagem indicando que nenhuma informacao foi encontrada
    """
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(query)
    return search_docs

#Criacao do agente react
tools = [] # Temporarily remove search_web to debug
graph = create_react_agent(model=model,tools=tools,prompt=system_message)

export_graph = graph

app = export_graph
