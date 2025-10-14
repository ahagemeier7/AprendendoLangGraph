import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool

load_dotenv()

#Constroi a URL de conexao
def _build_database_url() -> str:
    """
    Função interna para construir a URL de conexão com base nas variáveis de ambiente.
    Valida a existência das variáveis necessárias.
    """
    db_type = os.getenv('DB')
    
    if not db_type:
      raise ValueError("A variável de ambiente 'DB' não foi definida. Especifique 'MSSQL' ou 'POSTGRES'.")

    # Valida que as variáveis de ambiente comuns existem
    required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    for var in required_vars:
      if not os.getenv(var):
        raise ValueError(f"A variável de ambiente obrigatória '{var}' não foi encontrada.")

    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    name = os.getenv('DB_NAME')

    if db_type.upper() == 'MSSQL':
      driver = os.getenv('DB_DRIVER', 'ODBC+Driver+17+for+SQL+Server').replace(' ', '+')
      # AVISO DE SEGURANÇA: TrustServerCertificate=yes é um risco em produção.
      # Considere tornar isso configurável.
      return f"mssql+pyodbc://{user}:{password}@{host}:{port}/{name}?driver={driver}"#&TrustServerCertificate=yes"
    
    elif db_type.upper() == 'POSTGRES':
      return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    
    else:
      raise ValueError(f"Tipo de banco de dados '{db_type}' não é suportado. Use 'MSSQL' ou 'POSTGRES'.")

# --- FLUXO PRINCIPAL ---

# Constrói a URL usando a função helper, mantendo o código principal limpo.
DATABASE_URL = _build_database_url()
  
#Cria a Engine do SQLAlchemy
#Esse objeto e o ponto central de acesso ao banco e gerencia de pool
#Ele e criado apenas uma vez, quando o modulo e importado
engine: Engine = create_engine(
  DATABASE_URL,
  poolclass=QueuePool,         # Usa o QueuePool, que é o padrão e o mais recomendado.
  pool_size=5,                 # Número de conexões a manter abertas no pool.
  max_overflow=10,             # Conexões extras que podem ser abertas sob carga pesada (5 + 10 = 15 total).
  pool_timeout=30,             # Segundos para aguardar por uma conexão antes de dar erro.
  pool_recycle=1800            # Recicla conexões após 1800s (30 min) para evitar conexões fechadas pelo DB.
)

def get_engine() -> Engine:
  """
  Retorna a instância única do Engine.
  O agente usará esta função para obter acesso ao pool de conexões.
  """
  return engine

def test_connection():
  try:
      connection = engine.connect()
      connection.close()
      print("✅ Conexão com o banco de dados estabelecida com sucesso!")
  except Exception as e:
      print(f"❌ Falha ao conectar com o banco de dados: {e}")

# Testa a conexão quando este módulo é executado diretamente
if __name__ == '__main__':
  test_connection()