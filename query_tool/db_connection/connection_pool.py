import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError

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
      return f"mssql+pyodbc://{user}:{password}@{host}:{port}/{name}?driver={driver}"#&TrustServerCertificate=yes"
    
    elif db_type.upper() == 'POSTGRES':
      return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    
    else:
      raise ValueError(f"Tipo de banco de dados '{db_type}' não é suportado. Use 'MSSQL' ou 'POSTGRES'.")

# --- FLUXO PRINCIPAL ---

# Constrói a URL usando a função helper, mantendo o código principal limpo.
DATABASE_URL = _build_database_url()

def _create_engine_with_retries(url: str, retries: int = 5, delay: int = 5) -> Engine:
    """
    Tenta criar a Engine do SQLAlchemy com um mecanismo de retentativa.
    """
    for i in range(retries):
        try:
            engine = create_engine(
                url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800
            )
            # Tenta conectar para verificar se a engine foi criada com sucesso
            with engine.connect() as connection:
                connection.close()
            print(f"✅ Engine do banco de dados criada e conectada com sucesso após {i+1} tentativa(s).")
            return engine
        except OperationalError as e:
            print(f"❌ Falha na conexão (tentativa {i+1}/{retries}): {e}")
            if i < retries - 1:
                print(f"Tentando reconectar em {delay} segundos...")
                time.sleep(delay)
            else:
                raise
        except Exception as e:
            print(f"❌ Erro inesperado ao criar a Engine: {e}")
            raise

# Cria a Engine do SQLAlchemy com retentativas
engine: Engine = _create_engine_with_retries(DATABASE_URL)

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
