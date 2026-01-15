#Função da potencia de um número 
power = lambda num: num ** 2

print(power(5))
print(power(9))

is_even = lambda x: x % 2 == 0

print(is_even(24))
print(is_even(25))

div_num = lambda x,y: x/y

print(div_num(6,2))

reverse_string = lambda s: s[::-1]

print(reverse_string("Amor"))

movies_list = ["Titanic","Indiana Jones","Inception","Star wars"]

ratings = {
  "Titanic" : [8.5,9.0,7.5],
  "Indiana Jones" : [7.5,8.0,9.5],
  "Inception" : [3.5,2.0,1.5],
  "Star wars" : [3.5,8.0,6.5]
}

#Função para calcular média de avaliações de um filme
avg = lambda movie_name: sum(ratings[movie_name]) / len(ratings[movie_name])

print(f"Média de avaliação do filme Titanic: {avg("Titanic")}")


#Função q verifica se um filme está na lista
check_movie = lambda movie: movie in movies_list

print(check_movie("Inception"))

Recomend_movie = lambda movie: f"Recomento assistir {movie} com média de {avg(movie):.2f}"

print(Recomend_movie("Titanic"))