#Grafos e lógica para IA

from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START,END,StateGraph
from langgraph.types import Send

from schemas import *
from prompts import *
from dotenv import load_dotenv
import os
from tavily import TavilyClient
import streamlit as st

load_dotenv()

OPENAPI_KEY = os.getenv("GOOGLE_API_KEY")

#Modelos
llm = ChatGoogleGenerativeAI(api_key=OPENAPI_KEY, model="gemini-2.0-flash-lite")
reasoning_llm = ChatGoogleGenerativeAI(api_key=OPENAPI_KEY, model="gemini-2.5-flash")


#Nós
def build_first_queries(state: ReportState):
  class QueryList(BaseModel):
    queries: List[str]
  
  user_input = state.user_input
  prompt = build_queries.format(user_input=user_input)
  query_llm = llm.with_structured_output(QueryList)
  result = query_llm.invoke(prompt)

  return {"queries": result.queries}

def search_tavily(query: str):
  tavily_client = TavilyClient()
  
  results = tavily_client.search(query, max_results=1,include_raw_content=False)
  url = results["results"][0]["url"]
  
  url_extraction = tavily_client.extract(url)
  if (len(url_extraction["results"]) > 0):
    raw_content = url_extraction["results"][0]["raw_content"]
    prompt = resume_search.format(user_input=user_input,search_results=raw_content)
    llm_result = llm.invoke(prompt)
    query_results = QueryResult(
      title = results["results"][0]["title"],
      url = url,
      resume = llm_result.content
    )
  return {"queries_results": query_results}
  
def researcher(state: ReportState):
  return [Send("search_tavily", {"query": query}) for query in state.queries]
  
def final_writer(state: ReportState):
  search_results = ""
  references = ""
  for i, result in enumerate(state.queries_results):
    search_results += f"[{i+1}]\n\n"
    search_results += f"Título: {result.title}\n"
    search_results += f"URL: {result.url}\n"
    search_results += f"Resumo: {result.resume}\n"
    search_results += "============================="
    
    references += f"[{i+1}] - [{result.title}]({result.url})\n"
    
    prompt = build_final_response.format(user_input=user_input,search_results=search_results)
    llm_result = reasoning_llm.invoke(prompt)
    final_reponse = llm_result.content + "\n\n References: \n " + references
  return {"final_response": final_reponse}

#Grafo
builder = StateGraph(ReportState)
builder.add_node("build_first_queries", build_first_queries)
builder.add_node("search_tavily", search_tavily, loop_over="queries")
builder.add_node("final_writer", final_writer)

builder.add_edge(START, "build_first_queries")
builder.add_conditional_edges("build_first_queries", researcher, ["search_tavily"])
builder.add_edge("search_tavily", "final_writer")
builder.add_edge("final_writer", END)

graph = builder.compile()

#Execução
if __name__ == "__main__":
  st.title("App Langgraph")
  user_input = st.text_input("Qual a sua pergunta?",value="Me explique o processo para construir um agente de IA")
  if st.button("Pesquisar"):
    with st.status("Processando..."):
      response = graph.invoke({"user_input": user_input})
      st.write(response["final_response"])