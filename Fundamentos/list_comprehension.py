listnumbers = [i for i in range(10) if i < 4]

print(listnumbers)

movieslist = ["titanic","star wars","indiana jones"]

movieswithe = [movie for movie in movieslist if 'e' in movie.lower()]

watchedMovies = [movie for movie in movieslist if movie != "titanic"]

while True:
  searchName = input("Digite o nome do filme para buscar na lista ou sair para encerrar:\n")
  if searchName.lower() == "sair":
    print("Encerrado")
    break

  foundMovies = [movie for movie in movieslist if searchName.lower() in movie.lower()]

  if foundMovies:
    print(foundMovies)
    for foundmovie in foundMovies:
      print(foundmovie)
  else:
    print(f"Nenhumk filme foi encontrado com o nome {searchName}")