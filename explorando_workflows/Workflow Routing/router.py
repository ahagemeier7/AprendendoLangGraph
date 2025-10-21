from typing_extensions import TypedDict
from langgraph.graph import START, END,StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from Parallelization.models import models

#System messages
SYSTEM_MESSAGE_ASSISTENTE = SystemMessage(content="""
Você é um assistente virtual especializado em ajudar com diferentes tipos de consulta, seja educado e prestativo em suas respostas
                                        
""")

SYSTEM_MESSAGE_TECNICO = SystemMessage(content="""
Você é um especialista técnico que fornece respostas detalhadas e precisa sobre tecnologia, use linguagem técnica apropriada e forneça exemplos práticos
quando possível                                      
                                       
""")

SYSTEM_MESSAGE_SAUDE = SystemMessage(content="""
Você é um consultor de saúde que fornece informações gerais sobre bem estar e saude, lembre-se de sempre enfatizar que suas respostas são apenas informativas
e não substituem consultas médicas                                     
                        
""")

class State(TypedDict):
  query: str
  category: str
  answer: str
  
def router(state: State):
  """Roteia a consulta para diferentes categorias baseadas no conteudo"""
  query = state['query'].lower()
  palavras_tecnologia = ['python','programação','código','desenvolvimento', 'software','tecnologia']
  palavras_saude = ['saude','exercício','alimentação','bem estar','medicina','dieta']
  if any(palavra in query for palavra in palavras_tecnologia):
    return {'category': "tecnico"}
  elif  any(palavra in query for palavra in palavras_saude):
    return {'category': 'saude'}
  else:
    return {'category': 'assistente'}
  
def assistente(state:State):
  """Processa consultas gerais"""
  messages = [SYSTEM_MESSAGE_ASSISTENTE, HumanMessage(content=state['query'])]
  response = models['gemini_2.5_flash'].invoke(messages)
  return {'answer': response.content}


  
def tecnico(state:State):
  """Processa consultas tecnicas"""
  messages = [SYSTEM_MESSAGE_TECNICO, HumanMessage(content=state['query'])]
  response = models['gemini_2.5_flash'].invoke(messages)
  return {'answer': response.content}

  
def saude(state:State):
  """Processa consultas sobre saúde"""
  messages = [SYSTEM_MESSAGE_SAUDE, HumanMessage(content=state['query'])]
  response = models['gemini_2.5_flash'].invoke(messages)
  return {'answer': response.content}

workflow_builder = StateGraph(State)
workflow_builder.add_node('router',router)
workflow_builder.add_node('tecnico',tecnico)
workflow_builder.add_node('assistente',assistente)
workflow_builder.add_node('saude',saude)

workflow_builder.set_entry_point('router')
workflow_builder.add_conditional_edges('router',lambda state : state['category'],
{
  'assistente': 'assistente',
  'tecnico': 'tecnico',
  'saude': 'saude'
})

workflow_builder.add_edge('assistente',END)
workflow_builder.add_edge('tecnico',END)
workflow_builder.add_edge('saude',END)

workflow_router = workflow_builder.compile()