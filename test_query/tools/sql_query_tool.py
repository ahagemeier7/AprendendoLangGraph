from db_connection import get_engine
from sqlalchemy import text
import yaml
import os

# --- Configuração inicial da ferramenta ---
try:
  PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

  MANIFEST_PATH = os.path.join(PROJECT_ROOT, 'manifest.yaml')
  SQL_FILES_PATH = os.path.join(PROJECT_ROOT, 'sql')

  with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    CATALOG = {item['nome_arquivo']: item for item in yaml.safe_load(f)['consultas']}
        
except FileNotFoundError:
    print(f"ERRO CRÍTICO: O arquivo 'manifest.yaml' não foi encontrado em '{MANIFEST_PATH}'.")
    print("A ferramenta de consulta SQL não poderá funcionar.")
    CATALOG = {} # Define o catálogo como vazio para evitar que o programa quebre completamente
except Exception as e:
    print(f"ERRO CRÍTICO: Falha ao carregar ou processar o manifest.yaml: {e}")
    CATALOG = {}

# --- A função principal que o AGENTE irá chamar ---
def run_sql_query(query_name: str, parameters: dict) -> list:
  """
  Executa uma consulta SQL pré-definida a partir do manifesto.

  Args:
    query_name (str): O nome do arquivo .sql a ser executado (ex: 'buscar_usuario.sql').
    parameters (dict): Um dicionário com os parâmetros para a consulta.

  Returns:
    list: Uma lista de dicionários contendo o resultado da consulta,
          ou uma lista com um dicionário de erro em caso de falha.
  """
    
  query_info = CATALOG.get(query_name)
  if not query_info:
    raise ValueError(f"Consulta '{query_name}' não encontrada no manifesto.")

  sql_path = os.path.join(SQL_FILES_PATH, query_name)
  try:
    with open(sql_path, 'r', encoding='utf-8') as f:
      sql_template = f.read()
        
  except FileNotFoundError:
    # Adiciona um erro específico se o arquivo .sql não for encontrado
    error_msg = f"Arquivo SQL '{query_name}' definido no manifesto mas não encontrado em '{SQL_FILES_PATH}'."
    print(f"{error_msg}")
    return [{"error": error_msg}]

  #Busca a engine para a conexão
  db_engine = get_engine()
  try:
    with db_engine.connect() as connection:
      print(f"🔌 Conexão obtida do pool. Executando...")
      stmt = text(sql_template)
      result_proxy = connection.execute(stmt, parameters)
      results = [dict(row._mapping) for row in result_proxy]
      return results
    
  except Exception as e:
    print(f"Erro durante a execução pela ferramenta: {e}")
    return [{"error": str(e)}]