import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import missingno as msno
import ast
from sklearn.preprocessing import MinMaxScaler  # Importação do MinMaxScaler
from sklearn.neighbors import NearestNeighbors  # Importação para o KNN

# Importando um CSV do Google Drive
url = 'https://drive.google.com/file/d/1NKuLY2nh4le25ff_RFvQWxtRTgXN0OEI/view?usp=sharing'
# Pegando o ID do arquivo a partir da URL
file_id = url.split('/')[-2]
# Criando a URL para download direto no ambiente
pogo = 'https://drive.google.com/uc?id=' + file_id

# Carregando os dados
dados = pd.read_csv(pogo)

# Removendo duplicatas
dados = dados.drop_duplicates(subset=['original_title', 'release_date'], keep='first')

# Exibir o número de filmes antes e depois da remoção
print(f"Número de filmes após a remoção de duplicatas: {len(dados)}")

df_clean = dados.drop(columns=['budget', 'homepage', 'id', 'keywords', 'popularity',
                                'production_companies', 'production_countries',
                                'revenue', 'spoken_languages', 'status',
                                'tagline', 'title', 'vote_count'])

df_clean = df_clean.dropna(subset=['release_date', 'overview', 'runtime'])

# Criar um dicionário de mapeamento de idiomas para números
language_mapping = {language: idx for idx, language in enumerate(df_clean['original_language'].unique())}

# Substituir os idiomas pelos números correspondentes
df_clean['original_language_numeric'] = df_clean['original_language'].replace(language_mapping)

df_clean['release_date'] = pd.to_datetime(df_clean['release_date']).dt.year

df_clean = df_clean.drop('original_language', axis=1)

# Converte a coluna 'genres' de string para uma lista de dicionários, se for necessário
df_clean['genres'] = df_clean['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Extrai apenas os valores do campo 'name' em cada dicionário da lista
df_clean['genres'] = df_clean['genres'].apply(lambda x: [genre['name'] for genre in x])

# Cria um conjunto com todos os gêneros únicos presentes no dataset
all_genres = set(genre for sublist in df_clean['genres'] for genre in sublist)

# Para cada gênero, cria uma coluna binária (0 ou 1)
for genre in all_genres:
    df_clean[genre] = df_clean['genres'].apply(lambda x: 1 if genre in x else 0)

# Remove a coluna original 'genres' se não for mais necessária
df_clean = df_clean.drop('genres', axis=1)

# Normalizando a coluna 'runtime'
scaler = MinMaxScaler()
df_clean['runtime_normalized'] = scaler.fit_transform(df_clean[['runtime']])

# Preparação do modelo KNN
feature_columns = [genre for genre in all_genres] + ['runtime_normalized', 'vote_average']
X = df_clean[feature_columns].values
knn = NearestNeighbors(n_neighbors=15, algorithm='auto')
knn.fit(X)

def calcular_pontuacao_genero(filme, generos_desejados):
    """Calcula uma pontuação baseada na presença dos gêneros desejados."""
    pontuacao = sum(filme[genero] for genero in generos_desejados if genero in filme)
    return pontuacao

def recomendar_filmes(ano_lancamento, nota_min, generos, tempo_min, top_n=5):
    # Filtra filmes com base nos critérios fornecidos
    candidatos = df_clean[
        (df_clean['release_date'] >= ano_lancamento) &
        (df_clean['vote_average'] >= nota_min) &
        (df_clean['runtime'] >= tempo_min)
    ]

    # Se não encontrar candidatos, retorne uma lista vazia
    if candidatos.empty:
        return []

    # Cria a matriz de características para o KNN
    candidatos_matrix = candidatos[feature_columns].values

    # Encontra os filmes mais próximos usando o KNN
    distances, indices = knn.kneighbors(candidatos_matrix)

    recomendados = []
    for i in range(len(indices)):
        for idx in indices[i][1:]:  # Começa do segundo índice para evitar o próprio filme
            if idx < len(candidatos):  # Verifica se o índice está dentro do DataFrame filtrado
                filme = candidatos.iloc[idx]
                pontuacao = calcular_pontuacao_genero(filme, generos)  # Usar a nova função de pontuação
                if pontuacao > 0:  # Só adicionar filmes que têm pontuação de gênero
                    runtime_original = filme['runtime']  # Pega a duração original do filme
                    recomendados.append((pontuacao, filme, runtime_original))
                    if len(recomendados) >= top_n:  # Para assim que atingir o número desejado de recomendações
                        break
        if len(recomendados) >= top_n:
            break

    # Ordena os filmes pela pontuação e seleciona os mais próximos
    recomendados = sorted(recomendados, key=lambda x: x[0], reverse=True)[:top_n]

    # Retorna os filmes recomendados com a minutagem correta
    return [
        {
            'title': filme['original_title'],
            'overview': filme['overview'],
            'release_date': filme['release_date'],
            'runtime': runtime,  # Usa a duração original correta
            'vote_average': filme['vote_average']  # Nota original
        }
        for _, filme, runtime in recomendados
    ]


# Exemplo de uso: recomendando filmes
recomendacoes = recomendar_filmes(
    ano_lancamento=2000, nota_min=6.5, generos=['Animation', 'Action'], tempo_min=65, top_n=5
    #adicionem os parametros seguindo este modelo; podem colocar mais generos separados por virgula
)

# Exibe as recomendações
for filme in recomendacoes:
    print(f"Título: {filme['title']}, Ano: {filme['release_date']}, Duração: {filme['runtime']} min, Nota: {filme['vote_average']}")

