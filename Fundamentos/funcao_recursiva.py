def fatorial(n: int):

  if n == 1:
    return 1
  else:
    return (n * fatorial(n - 1))

number = int(input("Digite um numero para o fatorial:\n"))
print(f"O fatrorial de {number} é {fatorial(number)}")