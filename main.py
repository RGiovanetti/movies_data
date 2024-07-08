from fastapi import FastAPI
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#entorno_p1/SCRIPTS/activate
#uvicorn main:app --reload
#agregado render

csv_file_path = ("./data/df_movie.csv")
csv_file_path3 = ("./data/df_crew.csv")
csv_file_path2 = ("./data/df_cast.csv")
csv_file_path4 = ("./data/df_modelo1.csv")
# Carga el archivo CSV en un DataFrame de Pandas
try:
    df_movie = pd.read_csv(csv_file_path)
    df_cast = pd.read_csv(csv_file_path2)
    df_crew = pd.read_csv(csv_file_path3)
    df_modelo = pd.read_csv(csv_file_path4)

    print("Archivo cargado correctamente.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {csv_file_path} y {csv_file_path2}. Verifica la ruta y asegúrate de que el archivo exista.")

# Define tu aplicación FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenidos a mi API"}

# Ruta para contar películas por mes
@app.get("/cantidad_filmaciones_mes")

def cantidad_filmaciones_mes(month_name):
    # Verifica que la entrada sea un mes válido
    valid_month = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    if month_name.lower() not in valid_month:
        return "El nombre ingresado no corresponde a un mes. Por favor ingrese un nombre válido."

    # Mapea el nombre del mes en español al inglés usando if y elif
    if month_name.lower() == 'enero':
        month_name_en = 'January'
    elif month_name.lower() == 'febrero':
        month_name_en = 'February'
    elif month_name.lower() == 'marzo':
        month_name_en = 'March'
    elif month_name.lower() == 'abril':
        month_name_en = 'April'
    elif month_name.lower() == 'mayo':
        month_name_en = 'May'
    elif month_name.lower() == 'junio':
        month_name_en = 'June'
    elif month_name.lower() == 'julio':
        month_name_en = 'July'
    elif month_name.lower() == 'agosto':
        month_name_en = 'August'
    elif month_name.lower() == 'septiembre':
        month_name_en = 'September'
    elif month_name.lower() == 'octubre':
        month_name_en = 'October'
    elif month_name.lower() == 'noviembre':
        month_name_en = 'November'
    elif month_name.lower() == 'diciembre':
        month_name_en = 'December'
    
    # En caso de que no exista un valor como fecha, convierte 'release_date' a datetime si no está ya en ese formato
    if not pd.api.types.is_datetime64_any_dtype(df_movie['release_date']):
        df_movie['release_date'] = pd.to_datetime(df_movie['release_date'], errors='coerce')
    
    # Añade una columna 'month_name' al DataFrame con el nombre del mes
    df_movie['month_name'] = df_movie['release_date'].dt.month_name()
    
    # Cuenta la cantidad de películas que se estrenaron en el mes especificado
    count = len(df_movie[df_movie['month_name'] == month_name_en])
    resultado = f'Cantidad de películas estrenadas en {month_name} fueron {count}'
    return resultado

@app.get("/votos_titulo")
def votos_titulo(titulo_de_la_filmacion: str):
    # Filtrar el DataFrame por títulos que contienen la cadena especificada
    df_filtrado = df_movie[df_movie['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    
    # Verificar si se encontraron resultados
    if len(df_filtrado) == 0:
        raise HTTPException(status_code=404, detail=f'No se encontró la película {titulo_de_la_filmacion}')
    
    # Seleccionar las columnas deseadas
    df_filtrado = df_filtrado[['title', 'vote_count', 'vote_average', 'release_year']]
    
    # Obtener el primer resultado encontrado
    titulo = df_filtrado['title'].values[0]
    release_year = df_filtrado['release_year'].values[0]
    vote_count = df_filtrado['vote_count'].values[0]
    vote_average = df_filtrado['vote_average'].values[0]
    
    # Verificar la cantidad de valoraciones
    if vote_count > 2000:
        resultado = f'La película {titulo} fue estrenada en el año {release_year} cuenta con {vote_count} valoraciones, con un promedio de {vote_average}'
    else:
        resultado = f'{titulo_de_la_filmacion} no cuenta con la cantidad de valoraciones necesarias'

    return resultado

@app.get("/cantidad_filmaciones_dia")
def cantidad_filmaciones_dia(day_name):
    # Verifica que la entrada sea un día de la semana válido
    valid_days = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo', 'sabado', 'miercoles']
    
    if day_name.lower() not in valid_days:
        return "El nombre ingresado no corresponde a un día de la semana. Por favor ingrese un nombre válido."

    # Mapea el nombre del día de la semana en español al inglés usando if y elif
    if day_name.lower() == 'lunes':
        day_name1 = 'Monday'
    elif day_name.lower() == 'martes':
        day_name1 = 'Tuesday'
    elif day_name.lower() == 'miércoles' or day_name.lower() == 'miercoles':
        day_name1 = 'Wednesday'
    elif day_name.lower() == 'jueves':
        day_name1 = 'Thursday'
    elif day_name.lower() == 'viernes':
        day_name1 = 'Friday'
    elif day_name.lower() == 'sábado' or day_name.lower() == 'sabado':
        day_name1 = 'Saturday'
    elif day_name.lower() == 'domingo':
        day_name1 = 'Sunday'

    # En caso de que no exista un valor como fecha pasa 'release_date' a datetime si no está ya en ese formato
    if not pd.api.types.is_datetime64_any_dtype(df_movie['release_date']):
        df_movie['release_date'] = pd.to_datetime(df_movie['release_date'], errors='coerce')

    # Añade una columna 'weekday' al DataFrame con el nombre del día de la semana
    df_movie['weekday'] = df_movie['release_date'].dt.day_name()

    # Cuenta la cantidad de películas que se estrenaron en el día de la semana especificado
    count = len(df_movie[df_movie['weekday'] == day_name1])
    resultado = f'Cantidad de películas estrenadas un dia {day_name} fueron {count}'
    return resultado

@app.get("/score_titulo1")
def score_titulo(titulo_de_la_filmación):
    # Filtrar el DataFrame por títulos que contienen la cadena especificada
    df_filtrado = df_movie[df_movie['title'].str.contains(titulo_de_la_filmación, case=False, na=False)]
    
    # Seleccionar las columnas deseadas
    df_filtrado = df_filtrado[['title', 'release_date', 'popularity', 'release_year']]
    
    # Verificar si se encontraron resultados
    if df_filtrado.empty:
        return {"mensaje": f'No se encontró la película "{titulo_de_la_filmación}"'}
    else:
        # Obtener el primer resultado encontrado
        titulo = df_filtrado.iloc[0]['title']
        release_year = df_filtrado.iloc[0]['release_year']
        popularity = df_filtrado.iloc[0]['popularity']
        
        # Preparar el resultado
        resultado = f'La película {titulo} fue estrenada en el año {release_year} con un score/popularidad de {popularity}'
        
        return resultado

    

@app.get("/get_actor")
def get_actor(nombre_actor):
    # Filtrar el DataFrame de actores por nombres que contengan la cadena especificada
    actores_filtrados = df_cast[df_cast['castname'].str.contains(nombre_actor, case=False, na=False)]
    
    # Contar la cantidad de actores únicos encontrados
    cantidad_actores_unicos = actores_filtrados['castname'].nunique()
    
    if cantidad_actores_unicos > 1:
        print(f'el nombre "{nombre_actor}" corresponde a  {cantidad_actores_unicos} actores difrentes por favor sea mas especifico')
        print(actores_filtrados[['castname']].drop_duplicates())
    else:
        actor_nombre = actores_filtrados.iloc[0]['castname']
        
        # Filtrar películas donde participó el actor específico
        peliculas_actor = df_movie.merge(actores_filtrados, on='id', how='inner')
        
        cantidad_filmaciones = len(peliculas_actor)
        retorno_total = peliculas_actor['return'].sum()
        promedio_retorno = retorno_total / cantidad_filmaciones
        
        resultado = (f'El actor {actor_nombre} ha participado en {cantidad_filmaciones} filmaciones y Ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación.')
    
    return resultado

@app.get("/get_actorsindirector")
def contar_actoressindirector(nombre_actor):
    # Filtrar el DataFrame de actores por nombres que contengan la cadena especificada
    actores_filtrados = df_cast[df_cast['castname'].str.contains(nombre_actor, case=False, na=False)]

    # Filtrar el DataFrame de directores por nombres que contengan la cadena especificada
    directores_filtrados = df_crew[(df_crew['crewname'].str.contains(nombre_actor, case=False, na=False)) & (df_crew['crewjob'] == 'Director')]

    cantidad_actores_unicos = actores_filtrados['castname'].nunique()

    if cantidad_actores_unicos > 1:
        print(f'El nombre "{nombre_actor}" corresponde a {cantidad_actores_unicos} actores diferentes, por favor sea más específico.')
        print(actores_filtrados[['castname']].drop_duplicates())
    else:
        actor_nombre = actores_filtrados.iloc[0]['castname']
        
        # Filtrar películas donde participó el actor específico
        peliculas_actor = df_movie.merge(actores_filtrados, on='id', how='inner')
        
        # Filtrar películas donde el actor también es director
        peliculas_director = df_movie.merge(directores_filtrados, on='id', how='inner')
        
        # Obtener las películas donde el actor solo actúa y no dirige
        peliculas_actor_solo = peliculas_actor[~peliculas_actor['id'].isin(peliculas_director['id'])]

        cantidad_filmaciones = len(peliculas_actor_solo)
        retorno_total = peliculas_actor_solo['return'].sum()
        promedio_retorno = retorno_total / cantidad_filmaciones if cantidad_filmaciones > 0 else 0
        
        resultado = f'El actor {actor_nombre} ha participado en {cantidad_filmaciones} filmaciones (solo como actor) y Ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación.'
    
    return resultado

@app.get("/director1")
def get_director1(nombre_director):
    # Filtrar el DataFrame de directores por nombres que contengan la cadena especificada
    directores_filtrados = df_crew[(df_crew['crewname'].str.contains(nombre_director, case=False, na=False)) & (df_crew['crewjob'] == 'Director')]
    
    # Filtrar las películas dirigidas por el director especificado
    peliculas_director = df_movie.merge(directores_filtrados, on='id', how='inner')
    
    retorno_total = peliculas_director['return'].sum()
    peliculas = peliculas_director['title'].tolist()
    costo_total = peliculas_director['budget'].sum()
    ganancia_total = peliculas_director['revenue'].sum()
    peliculas_str = ', '.join(peliculas)

    resultado = f'El director {nombre_director} ha conseguido un retorno total de {retorno_total} con un costo total de {costo_total} y una ganancia total de {ganancia_total} y dirigió las siguientes películas: {peliculas_str}'
    
    return resultado
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
import numpy as np
import ast
pd.set_option('display.max_columns', None)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Extraer los 5 primeros actores
df_cast['cast'] = df_cast.groupby('id').cumcount() + 1
df_cast_top5 = df_cast[df_cast['cast'] <= 3]
df_cast_top5 = df_cast_top5.groupby('id')['castname'].apply(list).reset_index()
df_cast_top5.columns = ['id', 'top_5_actors']

# Extraer el director
df_directors = df_crew[df_crew['crewjob'] == 'Director']
df_directors = df_directors.groupby('id')['crewname'].first().reset_index()
df_directors.columns = ['id', 'director']

# Merge con df_movie
df_modelo = df_movie.merge(df_cast_top5, on='id', how='left')
df_modelo = df_modelo.merge(df_directors, on='id', how='left')

df_modelo = df_modelo[['id','title', 'overview', 'genres_names', 'top_5_actors', 'director']]

df_modelo['title'] = df_modelo['title'].str.lower()
# Unir los nombres de actores si están en una lista
df_modelo['top_5_actors'] = df_modelo['top_5_actors'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)

df_modelo['top_5_actors'] = df_modelo['top_5_actors'].str.lower()

# Descargar stopwords y recursos de tokenización si aún no están descargados
nltk.download('stopwords')
nltk.download('punkt')

# Definir stopwords en inglés y español
stopwords_english = set(stopwords.words('english'))
stopwords_spanish = set(stopwords.words('spanish'))

# Función para tokenizar y eliminar stopwords manteniendo nombres completos de actores
def tokenize_and_remove_stopwords(text, language='english'):
    tokens = word_tokenize(text)
    if language == 'english':
        tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords_english]
    elif language == 'spanish':
        tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords_spanish]
    return ' '.join(tokens)

# Función para tokenizar y preprocesar múltiples columnas
def preprocess_columns(df, columns=['overview', 'genres_names', 'top_5_actors', 'director'], language='english'):
    for col in columns:
        df[col] = df[col].apply(lambda x: tokenize_and_remove_stopwords(str(x), language))
    return df

# Ejemplo de uso:
# Suponiendo que tienes un DataFrame df_modelo con las columnas 'overview', 'genres_names', 'top_5_actors', 'director'

# Preprocesar las columnas relevantes
df_modelo = preprocess_columns(df_modelo)


df_modelo['genres_names'] = df_modelo['genres_names'].apply(lambda x: x.split(', '))
df_modelo['top_5_actors'] = df_modelo['top_5_actors'].apply(lambda x: x.split(', '))
df_modelo['director'] = df_modelo['director'].apply(lambda x: x.split(', '))



# Vectorización y cálculo de similitudes (fuera de la función del endpoint)
vectorizer = TfidfVectorizer(stop_words='english')

X_overview = vectorizer.fit_transform(df_modelo['overview'].fillna('').values.astype('U'))
X_genres = vectorizer.fit_transform(df_modelo['genres_names'].apply(lambda x: ' '.join(x)).fillna('').values.astype('U'))
X_actors = vectorizer.fit_transform(df_modelo['top_5_actors'].apply(lambda x: ' '.join(x)).fillna('').values.astype('U'))
X_director = vectorizer.fit_transform(df_modelo['director'].apply(lambda x: ' '.join(x)).fillna('').values.astype('U'))

@app.get("/recomendacion232")
def obtener_peliculas_similares(titulo_pelicula):
    # Obtener el índice de la película objetivo por el título
    index_pelicula_objetivo = df_modelo[df_modelo['title'].str.lower() == titulo_pelicula.lower()].index[0]
    
    # Calcular la similitud del coseno para cada característica por separado
    similarity_overview = cosine_similarity(X_overview[index_pelicula_objetivo], X_overview).flatten()
    similarity_genres = cosine_similarity(X_genres[index_pelicula_objetivo], X_genres).flatten()
    similarity_actors = cosine_similarity(X_actors[index_pelicula_objetivo], X_actors).flatten()
    similarity_director = cosine_similarity(X_director[index_pelicula_objetivo], X_director).flatten()

    # Calcular la similitud combinada (promedio de las similitudes)
    similarity_combined = (similarity_overview + similarity_genres + similarity_actors + similarity_director) / 4.0

    # Obtener los índices ordenados por similitud (excluyendo la película objetivo)
    similarity_scores_sorted_indices = similarity_combined.argsort()[::-1]

    # Top N películas más similares (excluyendo la propia película)
    top_n = 5
    top_n_indices = similarity_scores_sorted_indices[1:top_n + 1]

    # Obtener los títulos de las películas más similares
    peliculas_similares = df_modelo.iloc[top_n_indices]['title'].values

    # Formatear el resultado como texto
    resultados = f"Películas más similares a '{titulo_pelicula}':"
    for i, titulo in enumerate(peliculas_similares, start=1):
        resultados += f"las recomendaciones son {i}- {titulo}"

    return resultados
