"""
*args - Utilizamos quando não temos certeza quantos argumentos queremos ter em uma função
  os argumentos são passadas como uma tupla
**kargs - além dos valores podemos passar também as chaves de cada argumento
  os argumentos são passadas como um dicionario
"""

#args
def sum(*num):
  sum_total = 0
  for n in num:
    sum_total += n

  print(f"A soma é {sum_total}")

sum(7,8,6,54,3,53,45,6)

#**kargs
def presentation(**data):
  for key,value in data.items():
    print(f"{key} - {value}")
  
presentation(name="Python", category="Backend",nivel="Iniciante")
