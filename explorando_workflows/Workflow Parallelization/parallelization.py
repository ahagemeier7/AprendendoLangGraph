from typing_extensions import TypedDict
from langgraph.graph import START,END, StateGraph
from langchain_core.messages import SystemMessage,HumanMessage
from models import models

#1 - SystemMessage
SYSTEM_MESSAGE_LLMS = SystemMessage(content="""
Você é um especialiste em análise de código e boas páticas de programação. Sua tarefa é analisar o código fornecido e sugerir melhorias em termos de:
1. Performance e otimização
2. Boas páticas e padrões de código
3. Segurança e tratamento de erros
4. Legibilidade e manutenibilidade

Forneça suas sugestões de forma estruturada e clara, com exemplos práticos de como implementar as melhorias sugeridas                        
Seja específico e detalhado em suas recomentações
"""
)

# 2 - Definindo estado
class State(TypedDict):
  query: str #código a ser analisado
  llm1: str #analise do 2.5
  llm2: str #analise do 1.5
  best_llm: str #melhor analise escolhida


# 3 - nós 
def call_llm1(state: State):
  """Recebe o códigfo e retorna a analise do modelo gemini 2.5"""
  messages = [ 
    SystemMessage(content=SYSTEM_MESSAGE_LLMS.content),
    HumanMessage(content=f"Analise o seguinte código e forneca sugestões de melhorias: \n\n{state['query']}")
  ]
  response = models["gemini_2.0_flash-lite"].invoke(messages)
  return{"llm1": response.content}

def call_llm2(state: State):
  """Recebe o código e retorna a analise do modelo gemini 1.5"""
  messages = [ 
    SystemMessage(content=SYSTEM_MESSAGE_LLMS.content),
    HumanMessage(content=f"Analise o seguinte código e forneca sugestões de melhorias: \n\n{state['query']}")
  ]
  response = models["gemini_2.0_flash-lite"].invoke(messages)
  return{"llm2": response.content}

def judge(state: State):
  """Avalia qual analise foi mais completa e util"""
  msg = f"""
  Aja como revisor técnico Sênior e avalie a quantidade das análises de código fornecidas por dois especialistas.
  Sua taref é escolher a análise que:
  1. Identifica mais problemas potenciais
  2. Fornece sugestões mais práticas e implementaveis.
  3. Considera aspectos do código, como prformance, segurança, legibilidade, etc.
  4. Explica melhor o raciocinio por tras das sugestões

  [Código analisado]
  {state['query']}

  [modelo1 analisado]
  {state['llm1']}
  
  [Código analisado]
  {state['llm2']}

  Forneça sua avalição comparativa e conclua com seu veredito final usando exatamente um desses formatos:
  '[[A]] se a análise A for melhor'
  '[[B]] se a análise B for melhor'
  '[[C]] em caso de empate'
"""
  messages = [SystemMessage(content=msg), HumanMessage(content=msg)]

  response = models["gemini_2.5_flash"].invoke(messages)
  return {"best_llm": response.content}

#4- Construindo o workflow

code_analysis_builder = StateGraph(State)

#adiciona os nós
code_analysis_builder.add_node("call_llm1", call_llm1)
code_analysis_builder.add_node("call_llm2", call_llm2)
code_analysis_builder.add_node("judge", judge)

#Adiciona as arestas
code_analysis_builder.add_edge(START, "call_llm1")
code_analysis_builder.add_edge(START, "call_llm2")
code_analysis_builder.add_edge("call_llm1", "judge")
code_analysis_builder.add_edge("call_llm2", "judge")
code_analysis_builder.add_edge("judge", END)

code_analysis_workflow = code_analysis_builder.compile()
