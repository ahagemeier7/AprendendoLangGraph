from typing import Annotated
from typing_extensions import TypedDict
from operator import or_
import random
from langgraph.graph import START, END, StateGraph
from langchain_core.messages import HumanMessage
from Parallelization.models import models

#Estados
class State(TypedDict):
  detective: str
  crime: str
  location: str
  clue: str
  story: Annotated[dict[str, str], or_]
  
  
#Nós
def first_act(state:State):
  """Escreve o primeiro ato"""
  detective = random.choice([
    "Um detetive excentrico com memória fotográfica",
    "Um investigador que resolve casos atraves de analise de padrões",
    "Um detetive aposentado que não consegue resistir a um bom mistério"
  ])
  
  crime = random.choice([
    "Desaparecimento de um bjeto valioso",
    "Uma mensagem codificada deixada na cena do crime",
    "Um Assassinato aparentemente impossível"
  ])
  
  location = random.choice([
    "Uma mansão vitoriana isolada",
    "Um museu de antiguidades",
    "Clube exclusivo de alta sociedade"
  ])
  clue = random.choice([
    "Uma marca de cigarro rara",
    "Um relógio parado em um hrário específico",
    "Uma carta de baralho manchada"
  ])
  
  
  msg = f"""
  Você é um esxritor de mistério experiente, encarregado de escrever o primeiro ato de uma história de detetive.
  
  Instruções:
  Baseado nas seguintes informações iniciais:
  * **Detetive** {detective}
  * **crime** {crime}
  * **local** {location}
  * **Pista inicial** {clue}
  
  Escreve o primeiro ato dessa histórioa, esse ato deve:
  1- Apresentar o detetive: Mostre quem é o detetive e suas caracteristicas unicas
  2- ESabelecer o contexto: Descreva o local e a situação antes do crime ser descoberto
  3- Introduzir o Mistério: O momento em que o detetive é chamado para investigar {crime}
  4- Terminar com o primeiro ponto de virada: O detetive encontra {clue} e decide aceitar o caso
  
  O primeiro ato deve ter entre 1 e 2 paragrafos.
  Ao final, sinalize claramente:
  Fim do primeiro Ato
  Primeiro ponto de virada [Descreva brevemente o ponto de virada]
  
  
  """
  
  messages = [HumanMessage(content=msg)]
  response = models["gemini_2.5_flash"].invoke(messages)
  
  return {
    "story": {"act_1": response.content},
    "detective": detective,
    "crime": crime,
    "location": location,
    "clue": clue
  }
  
def second_act(state:State):
  """Escreve o segundo ato"""
  msg = f"""
  Você é um escritor de mistério continuando uma história de detetive
  Abaixo está o primeiro ato da história:
  ---- Inicio do primeiro ato ----
  {state['story']["act_1"]}
  ---- Fim do primeiro ato ----
  
  Instruções:
  Agora escreve o Segundo ato desta história, cotinuando diretamente de onde o primeiro ato parou.
  Este ato deve ter:
  1- investigações iniciais: Como o detetive começa a coletar evidencias e entrevistar suspeitos
  2- Novas pistas: Descobertas que parecem levar em direções diferentes
  3- Complicações: Suspeitos que mentem, pistas que se contradizem
  4- Ponto médio: Uma revelação surpreendente que muda a direção da investigação
  
  O segundo ato deve ter entre 1 e 2 paragrafos.
  Ao fina sinalze claramente
  Fim do segundo Ato
  Ponto médio [Descreva brevemente o ponto médio]
  """
  messages = [HumanMessage(content=msg)]
  response = models["gemini_2.5_flash"].invoke(messages)
  
  return {
    "story": {"act_2": response.content},
  }
  
def third_act(state:State):
  """Escreve o terceiro ato"""
  msg = f"""
  Você é um escritor de mistério continuando uma história de detetive
  Abaixo está o primeiro e o segundo ato da história:
  ---- Inicio do primeiro ato ----
  {state['story']["act_1"]}
  ---- Fim do primeiro ato ----
  ---- Inicio do segundo ato ----
  {state['story']["act_2"]}
  ---- Fim do segundo ato ----
  
  Instruções:
  Agora escreve o terceiro ato desta história, cotinuando diretamente de onde o segundo ato parou.
  Este ato deve ter:
  1- Crise: Momento em que todas as teorias parecem estar eradas
  2- Revelação: Uma conexão inesperada com as pistas
  3- Decisão final: O detetive percebe a verdade e se prepara para o confronto
  
  O terceito ato deve ter entre 1 e 2 paragrafos.
  Ao fina sinalze claramente
  Fim do terceiro Ato
  Segundo ponto de virada [Descreva brevemente o segundo ponto de virada]
  """
  messages = [HumanMessage(content=msg)]
  response = models["gemini_2.5_flash"].invoke(messages)
  
  return {
    "story": {"act_3": response.content},
  }
  
def fourth_act(state:State):
  """Escreve o quarto ato"""
  msg = f"""
  Você é um escritor de mistério continuando uma história de detetive
  Abaixo está o primeiro, o segundo e terceiro ato da história:
  ---- Inicio do primeiro ato ----
  {state['story']["act_1"]}
  ---- Fim do primeiro ato ----
  ---- Inicio do segundo ato ----
  {state['story']["act_2"]}
  ---- Fim do segundo ato ----
  ---- Inicio do terceiro ato ----
  {state['story']["act_3"]}
  ---- Fim do tercero ato ----
  
  
  Instruções:
  Agora escreve o quarto ato desta história, cotinuando diretamente de onde o terceiro ato parou.
  Este ato deve ter:
  1- Climax: Momento em que o detetive revela a soluçaõ do misterio
  2- Explicação: Como todas as pistas se encaixam na solução final
  3- Conclusão: Impacto da resolução do caso, e o que o detetive aprendeu
  O quarto ato deve ter entre 1 e 2 paragrafos.
  Ao fina sinalze claramente
  Fim do quarto Ato
  Climax [texto do climax]
  Resolução: [Texto da resolução]
  Fim da história
  """
  messages = [HumanMessage(content=msg)]
  response = models["gemini_2.5_flash"].invoke(messages)
  
  return {
    "story": {"act_4": response.content},
  }
  
#workflow
detective_builder = StateGraph(State)
  
detective_builder.add_node("first_act",first_act)
detective_builder.add_node("second_act",second_act)
detective_builder.add_node("third_act",third_act)
detective_builder.add_node("fourth_act",fourth_act)

detective_builder.add_edge(START,"first_act")
detective_builder.add_edge("first_act","second_act")
detective_builder.add_edge("second_act","third_act")
detective_builder.add_edge("third_act","fourth_act")
detective_builder.add_edge("fourth_act",END)

detective_workflow = detective_builder.compile()
