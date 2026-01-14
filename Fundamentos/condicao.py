name = input("Digite o nome do filme:\n")
year = int(input("Digite o ano de lançamento:\n"))
rating = float(input("Digite a nota de avaliação do filme:\n"))

if rating > 8.0 and year > 2015:
  print(f"O filme {name} é muito bom")
else:
  print("Ruim")