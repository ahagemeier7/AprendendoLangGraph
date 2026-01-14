lista = ["1","2","3","5"]

for number in lista:
  print(number)


for number in lista:
  if number == "5":
    break

for number in lista:
  if number == "5":
    continue
  print("outro numero")
    