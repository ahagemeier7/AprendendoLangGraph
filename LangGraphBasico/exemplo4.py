#--------------------------------------
#trabalhando com logica condicional
#--------------------------------------
from langchain_core.messages import HumanMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

#instanciando o modelo
llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key = API_KEY)

#Define o estado do Graph
class GraphState(BaseModel):
    input: str
    output: str
    tipo: str = None
    
#função de calculo
def realizar_calculo(state: GraphState) -> GraphState:
    return GraphState(input=state.input, output="Resposta de calculo ficticio: 42")

#Função para responder perguntas normais
def responder_curiosidade(state: GraphState) -> GraphState:
    response = llm_model.invoke([HumanMessage(content=state.input)])
    return GraphState(input=state.input,output=response.content)

#Função para tratar perguntas não reconhecidas
def responder_erro(state: GraphState) -> GraphState:
    return GraphState(input=state.input,output="Desculpe, não entendi sua pergunta")

#Função de classificação dos nodes
def classificar(state:GraphState)-> GraphState:
    pergunta = state.input.lower()
    if any(palavra in pergunta for palavra in ["Soma","quanto é","mais","calcular"]):
        tipo = "calculo"
    elif any(palavra in pergunta for palavra in ["quem","onde","quando","porque"]):
        tipo = "curiosidade"
    else:
        tipo = "desconhecido"
    return GraphState(input=state.input,output="",tipo=tipo)

#Criando o Grafo
graph = StateGraph(GraphState)
graph.add_node("classificar",classificar)
graph.add_node("realizar_calculo",realizar_calculo)
graph.add_node("responder_curiosidade",responder_curiosidade)
graph.add_node("responder_erro",responder_erro)

#Adicionando condicionais
graph.add_conditional_edges(
    "classificar",
    lambda state: {
        "calculo":"realizar_calculo",
        "curiosidade":"responder_curiosidade",
        "desconhecido": "responder_erro"
    }[state.tipo]
)

#Definindo entrada e saida e compilação
graph.set_entry_point("classificar")
graph.set_finish_point(["realizar_calculo","responder_curiosidade","responder_erro"])
export_graph = graph.compile()

#gerando a imagem do grafo
png_bytes = export_graph.get_graph().draw_mermaid_png(
    draw_method = MermaidDrawMethod.API
)

with open("grafo_exemplo4.png","wb") as f:
    f.write(png_bytes)


#testando o projeto
if __name__ == "__main__":
    exemplos =[
        "Quanto é 10+5",
        "QUem inventou a lampada",
        "Me diga um comando especial"
    ]
    for exemplo in exemplos:
        result = export_graph.invoke(GraphState(input=exemplo,output=""))
        print(f"Pergunta: {exemplo}\nResposta: {result["output"]}\n ")