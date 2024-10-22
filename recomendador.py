import streamlit as st

st.title("Escolhedor de Filmes 3000")

st.text("Escolha o ano de lançamento do filme")

#col1, col2 = st.columns(2)
#with col1:
#    year_start = st.selectbox("De", range(1916, 2018), key=0)
#with col2:
#    year_end = st.selectbox("Até", range(1916, 2018), key=1)

numero_selecionado = st.selectbox('Selecione um número:', range(1916, 2018))

st.text("Escolha o intervalo de minutos do seu filme")

minutos = st.selectbox('Selecione um número:', range(0, 338))

#col1, col2 = st.columns(2)
#with col1:
#    duration_min = st.selectbox("De", range(0, 338), key=2)
#with col2:
#    duration_max = st.selectbox("Até", range(0, 338), key=3)

# Filtros para o gênero
st.text("Escolha o gênero do seu filme")

options = st.multiselect(
    "gêneros:",
    ["Crime", "Fantasy", "Thriller", "TV Movie", "Music", "Animation", "Action", "Documentary", "History", 
     "Romance", "Family", "War", "Mystery", "Foreign", "Comedy", "Horror", "Drama", "Science Fiction", 
     "Adventure", "Western"]
)

st.write("Você escolheu:", options)

st.text("Escolha os idiomas do seu filme")

options = st.multiselect(
    "idiomas:",
    ["English", "Japanese", "French", "Chinese", "Spanish", "German", "Hindi", "Russian", "Korean", 
     "Telugu", "Cantonese", "Italian", "Dutch", "Tamil", "Swedish", "Thai", "Danish", "Unknown", 
     "Hungarian", "Czech","Portuguese","Icelandic","Turkish","Norwegian Bokmål","Afrikaans","Polish",
     "Hebrew","Arabic","Vietnamese","Kyrgyz","Indonesian","Romanian","Persian","Norwegian","Slovenian","Pashto","Greek",]
)

st.write("Você escolheu:", options)

st.text("Escolha a nota mínima de avaliação do seu filme")
nota = st.selectbox('Selecione um número:', ["{:.2f}".format(x * 0.1) for x in range(10, 101)])



#col1, col2 = st.columns(2)
#with col1:
#    min_value = st.selectbox("Escolha o limite inferior do intervalo", [x * 0.1 for x in range(10, 101)])
#with col2:
#    max_value = st.selectbox("Escolha o limite superior do intervalo", [x * 0.1 for x in range(10, 101)])


