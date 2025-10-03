from parallelization import code_analysis_workflow

#código de exemplo para analise
codigo_teste = """
def calcular_media(lista):
  soma =0 
  for i in range(len(lista)):
    soma = soma + lista[i]
    
  media = soma / len(lista)
  return media
  
#testando a funcao
numeros = [1,2,3,4,5]
resultado = calcular_media(numeros)
print(f'A media e: {resultado}')
"""

#Executando o wofklow
resultado = code_analysis_workflow.invoke({
  "query": codigo_teste
})

#exibindo os resultados
print("\n === Analise do gemini 2.5 ===")
print(resultado["llm1"])

print("\n === Analise do gemini 1.5 ===")
print(resultado["llm2"])

print("\n === Avaliacao final ===")
print(resultado["best_llm"])