from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import START,END,StateGraph
from langchain_core.messages import HumanMessage
from langgraph.types import interrupt
from models import models
import logging

#Estados
class StoryState(TypedDict):
  prompt: str
  story: str
  feedback: str
  act: int
  
#nós
def generate_story(state: StoryState):
  """Gera um novo trecho na história, baseado no feedback"""
  feedback = state.get("feedack","")
  story = state.get("story","")
  act = state.get("act",1)
  
  act_descriptions = {
    1: "pimeiro ato, onde apresentamos os personagens e o conflito inicial",
    2: "Segundo ato, onde o conflito se intensifica" ,
    3: "Terceiro ato, onde chegamos ao climax da estoria",
    4: "Quarto ato, onde resolvamos o conflito e concluimos a estoria"
  }

  msg = f"""
    Você é um escritor criativo especializado em criar estorias envolventes.
    Sua tarefa é continuar a estoria no {act_descriptions[act]}
    
    Instruções:
    1- Crie um trecho da estoria que se conecte naturalmente com o que ja foi escrito
    2- Mantenha consistencia com o spersonagens e eventos anteriores
    3- Seja criativo e envolvente
    
    Prompt Inicial:
    {state['prompt']}
    
    Historia até agora:
    {story}
    
    Feedback anterior:
    {feedback}
    
    escreva apenas o novo trecho da estoria, sem explicações adicionais
  """
  
  messages = [HumanMessage(content=msg)]
  response = models["gemini_2.5_flash"].invoke(messages)
  new_story = story + "\n\n" + response.content if story else response.content
  return {
    "story": new_story
  }
  
def get_feedback(state:StoryState):
  """Solicita feedback do usuário sobre a estoria"""
  
  feedback = interrupt(
    {
      "prompt": state["prompt"],
      "story": state["story"],
      "act": state["act"]
    }
  )
  logging.info(feedback)
  return {"feedback":feedback}

def route_Story(state:StoryState):
  """Roteia para o próximo ato, ou finaliza a estoria"""
  f = state.get("feedback")
  act = state.get("act",1)
  
  if f["Feedback"] == 'aprovado':
    if act<4:
      return "next_act"
    return "final"
    
  return "revise"

def next_act(state:StoryState):
  """Avança para po p´roximo ato"""
  current_act = state.get("act",1)
  
  return {"act": current_act + 1}

def final_Story(state:StoryState):
  """Finaliza o workflow e retorna a estória completa"""
  
  return {"story": state["story"]}

builder = StateGraph(StoryState)

builder.add_node("generate_story",generate_story)
builder.add_node("get_feedback",get_feedback)
builder.add_node("next_act",next_act)
builder.add_node("final_story",final_Story)

builder.add_edge(START,"generate_story")
builder.add_edge("generate_story","get_feedback")
builder.add_conditional_edges("get_feedback",route_Story,{
  "revise":"generate_story",
  "next_act" : "next_act",
  "final": "final_story"
})

builder.add_edge("next_act","generate_story")
builder.add_edge("final_story",END)

story_workflow = builder.compile()
