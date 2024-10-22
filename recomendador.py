import streamlit as st
import analise as an


st.title("Escolhedor de Filmes 3000")


st.text("Escolha o ano de lançamento do filme")
ano_selecionado = st.selectbox('Selecione um número:', range(1916, 2018))

st.text("Escolha a quantidade de minutos do seu filme")
minutos = st.selectbox('Selecione um número:', range(0, 338))

# Filtros para o gênero
st.text("Escolha o gênero do seu filme")
lista_genero = st.multiselect(
    "gêneros:",
    ["Crime", "Fantasy", "Thriller", "TV Movie", "Music", "Animation", "Action", "Documentary", "History", 
     "Romance", "Family", "War", "Mystery", "Foreign", "Comedy", "Horror", "Drama", "Science Fiction", 
     "Adventure", "Western"]
)
st.write("Você escolheu:", lista_genero)

st.text("Escolha a nota mínima de avaliação do seu filme")
nota_min = st.selectbox('Selecione um número:', [p/10 for p in range(0, 101)])

if st.button("Recomendar", type="primary"):
    filmes_recomendados = an.recomendar_filmes(ano_selecionado,nota_min,lista_genero,minutos)
    st.write(filmes_recomendados)




