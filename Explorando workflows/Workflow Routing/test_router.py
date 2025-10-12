from router import workflow_router

def test_workflow():
  resultado_tecnico = workflow_router.invoke({
    "query": 'como posso aprender python'
  })
  print('===  Consulta técnica ===')
  print(f'Pergunta: Como posso aprender python?')
  print(f"reposta: {resultado_tecnico['answer']}")
  
  
  resultado_saude = workflow_router.invoke({
    "query": 'QUais sao os beneficios de uma alimentação saudavel?'
  })
  print('===  Consulta técnica ===')
  print(f'Pergunta: Quais sao os beneficios de uma alimentação saudável?')
  print(f"reposta: {resultado_saude['answer']}")
  
  
  resultado_geral = workflow_router.invoke({
    "query": 'Qual a capital do Brasil?'
  })
  print('===  Consulta técnica ===')
  print(f'Pergunta: Qual a capital do Brasil?')
  print(f"reposta: {resultado_geral['answer']}")
  
if __name__ == '__main__':
  test_workflow()