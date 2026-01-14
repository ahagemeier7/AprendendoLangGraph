filmInception = {
  "title": "Inception",
  "Year": 2010,
  "imdbRating": 8.8
}

print(filmInception)

print(len(filmInception))

print(type(filmInception))

#Recuperar elemento do dicionário

print(filmInception["title"])
print(filmInception.get("year"))

#Buscar apenas as chaves
print(filmInception.keys())

#Buscar apenas valores
print(filmInception.values())

print(filmInception.items())


#adicionar itens ao dicionario
filmInception["director"] = "Christopher Nolan"

#atualizar itens no dicionario
filmInception.update({"imdbRating": 8.5})
print(filmInception)

filmInception.pop("director")

filmesDict = {
  "inception": {
    "title": "Inception",
    "Year": 2010,  
    "imdbRating": 8.8
  }
}