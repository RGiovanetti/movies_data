from fastapi import FastAPI
from fastapi import HTTPException
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

try:
    df_movie = pd.read_csv(csv_file_path)
    df_cast = pd.read_csv(csv_file_path2)
    df_crew = pd.read_csv(csv_file_path3)
    df_modelo = pd.read_csv(csv_file_path4)

    print("Archivo cargado correctamente.")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {csv_file_path} y {csv_file_path2}. Verifica la ruta y asegúrate de que el archivo exista.")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenidos a MovieData"}


@app.get("/cantidad_filmaciones_mes")

def cantidad_filmaciones_mes(month_name):
    """
    Retorna la cantidad de películas estrenadas en el mes especificado.

    Parameters:
    month_name (str): Nombre del mes en español.

    Returns:
    str: Cantidad de películas estrenadas en el mes especificado.
    """
    valid_month = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    if month_name.lower() not in valid_month:
        return f"El nombre ingresado no corresponde a un mes. Por favor ingrese un nombre válido."

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
    
    if not pd.api.types.is_datetime64_any_dtype(df_movie['release_date']):
        df_movie['release_date'] = pd.to_datetime(df_movie['release_date'], errors='coerce')
    
    df_movie['month_name'] = df_movie['release_date'].dt.month_name()
    
    count = len(df_movie[df_movie['month_name'] == month_name_en])
    resultado = f'Cantidad de películas estrenadas en {month_name} fueron {count}'
    return resultado

@app.get("/votos_titulo")
def votos_titulo(titulo_de_la_filmacion: str):
    """
    Retorna la cantidad de valoraciones y promedio de una película específica.

    Parameters:
    titulo_de_la_filmacion (str): Título de la película.

    Returns:
    str: Detalles sobre las valoraciones de la película.
    """
    df_filtrado = df_movie[df_movie['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    
    if len(df_filtrado) == 0:
        raise HTTPException(status_code=404, detail=f'No se encontró la película {titulo_de_la_filmacion}')
    
    df_filtrado = df_filtrado[['title', 'vote_count', 'vote_average', 'release_year']]
    
    titulo = df_filtrado['title'].values[0]
    release_year = df_filtrado['release_year'].values[0]
    vote_count = df_filtrado['vote_count'].values[0]
    vote_average = df_filtrado['vote_average'].values[0]
    
    if vote_count > 2000:
        resultado = f'La película {titulo} fue estrenada en el año {release_year} cuenta con {vote_count} valoraciones, con un promedio de {vote_average}'
    else:
        resultado = f'{titulo_de_la_filmacion} no cuenta con la cantidad de valoraciones necesarias'

    return resultado

@app.get("/cantidad_filmaciones_dia")
def cantidad_filmaciones_dia(day_name):
    """
    Retorna la cantidad de películas estrenadas en un día específico de la semana.

    Parameters:
    day_name (str): Nombre del día de la semana en español.

    Returns:
    str: Cantidad de películas estrenadas en el día especificado.
    """
    valid_days = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo', 'sabado', 'miercoles']
    
    if day_name.lower() not in valid_days:
        return f"El valor ingresado no corresponde a un día de la semana. Por favor ingrese un nombre válido."

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

    if not pd.api.types.is_datetime64_any_dtype(df_movie['release_date']):
        df_movie['release_date'] = pd.to_datetime(df_movie['release_date'], errors='coerce')

    df_movie['weekday'] = df_movie['release_date'].dt.day_name()

    count = len(df_movie[df_movie['weekday'] == day_name1])
    resultado = f'Cantidad de películas estrenadas un dia {day_name} fueron {count}'
    return resultado

@app.get("/score_titulo")
def score_titulo(titulo_de_la_filmación):
    """
    Retorna la popularidad de una película específica.

    Parameters:
    titulo_de_la_filmación (str): Título de la película.

    Returns:
    str: Popularidad de la película.
    """
    df_filtrado = df_movie[df_movie['title'].str.contains(titulo_de_la_filmación, case=False, na=False)]
    
    df_filtrado = df_filtrado[['title', 'release_date', 'popularity', 'release_year']]
    
    if df_filtrado.empty:
        return f'No se encontró la película "{titulo_de_la_filmación}"'

    else:
        titulo = df_filtrado.iloc[0]['title']
        release_year = df_filtrado.iloc[0]['release_year']
        popularity = df_filtrado.iloc[0]['popularity']
        
        resultado = f'La película {titulo} fue estrenada en el año {release_year} con un score/popularidad de {popularity}'
        
        return resultado

@app.get("/get_actor")
def get_actor(nombre_actor: str):
    """
    Retorna información sobre un actor específico y sus filmaciones.
    Si se busca un apellido/nombre común trae la cantidad de actores con ese apellido.

    Parameters:
    nombre_actor (str): Nombre del actor.

    Returns:
    str: Información sobre las filmaciones del actor.
    """
    actores_filtrados = df_cast[df_cast['castname'].str.contains(nombre_actor, case=False, na=False)]
    
    cantidad_actores_unicos = actores_filtrados['castname'].nunique()
    
    if cantidad_actores_unicos > 1:
        return f'El nombre "{nombre_actor}" corresponde a {cantidad_actores_unicos} actores diferentes. Por favor, sea más específico.'
    
    if cantidad_actores_unicos == 0:
        return f'No se encontró ningún actor con el nombre "{nombre_actor}".'
    
    actor_nombre = actores_filtrados.iloc[0]['castname']
    
    peliculas_actor = df_movie.merge(actores_filtrados, on='id', how='inner')
    
    cantidad_filmaciones = len(peliculas_actor)
    retorno_total = peliculas_actor['return'].sum()
    promedio_retorno = retorno_total / cantidad_filmaciones if cantidad_filmaciones > 0 else 0
    
    resultado = (f'El actor {actor_nombre} ha participado en {cantidad_filmaciones} filmaciones '
                f'y ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación.')
    
    return resultado   

@app.get("/get_actor_sindirector")
def contar_actoressindirector(nombre_actor: str): #buscar Mel Brooks en get_actor_sindirector y en get_acto para ver diferencia
    """
    Retorna información sobre un actor que no es director en sus filmaciones.

    Parameters:
    nombre_actor (str): Nombre del actor.

    Returns:
    str: Información sobre las filmaciones del actor sin ser director.
    """
    actores_filtrados = df_cast[df_cast['castname'].str.contains(nombre_actor, case=False, na=False)]
    directores_filtrados = df_crew[(df_crew['crewname'].str.contains(nombre_actor, case=False, na=False)) & (df_crew['crewjob'] == 'Director')]
    cantidad_actores_unicos = actores_filtrados['castname'].nunique()

    if cantidad_actores_unicos > 1:
        return f'El nombre "{nombre_actor}" corresponde a {cantidad_actores_unicos} actores diferentes, por favor sea más específico. Actores encontrados: {actores_filtrados["castname"].drop_duplicates().tolist()}'
        #por si sabemos solo el apellido/nombre puede servir como orientador
    if cantidad_actores_unicos == 0:
        raise HTTPException(status_code=404, detail=f'No se encontró al actor {nombre_actor}')

    actor_nombre = actores_filtrados.iloc[0]['castname']
    peliculas_actor = df_movie.merge(actores_filtrados, on='id', how='inner')
    peliculas_director = df_movie.merge(directores_filtrados, on='id', how='inner')
    peliculas_actor_solo = peliculas_actor[~peliculas_actor['id'].isin(peliculas_director['id'])]

    cantidad_filmaciones = len(peliculas_actor_solo)
    retorno_total = peliculas_actor_solo['return'].sum()
    promedio_retorno = retorno_total / cantidad_filmaciones if cantidad_filmaciones > 0 else 0
    
    resultado = f'El actor {actor_nombre} ha participado en {cantidad_filmaciones} filmaciones (solo como actor) y ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación.'
    
    return resultado

@app.get("/director")
def get_director(nombre_director):
    """
    Retorna información sobre un director específico y sus filmaciones.

    Parameters:
    nombre_director (str): Nombre del director.

    Returns:
    str: Información sobre las filmaciones del director.
    """
    directores_filtrados = df_crew[(df_crew['crewname'].str.contains(nombre_director, case=False, na=False)) & (df_crew['crewjob'] == 'Director')]
    
    if len(directores_filtrados) == 0:
        raise HTTPException(status_code=404, detail=f'No se encontró al director {nombre_director}')
    peliculas_director = df_movie.merge(directores_filtrados, on='id', how='inner')
    
    retorno_total = peliculas_director['return'].sum()
    peliculas = peliculas_director['title'].tolist()
    costo_total = peliculas_director['budget'].sum()
    ganancia_total = peliculas_director['revenue'].sum()
    peliculas_str = ', '.join(peliculas)

    resultado = f'El director {nombre_director} ha conseguido un retorno total de {retorno_total} con un costo total de {costo_total} y una ganancia total de {ganancia_total} y dirigió las siguientes películas: {peliculas_str}'
    
    return resultado



###ADAPTACIONES NECESARIAS PARA PODER CORRER EL MODELO### 

df_modelo['title'] = df_modelo['title'].str.lower()
df_modelo['top_5_actors'] = df_modelo['top_5_actors'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
df_modelo['top_5_actors'] = df_modelo['top_5_actors'].str.lower()
nltk.download('stopwords')
nltk.download('punkt')
stopwords_english = set(stopwords.words('english'))
stopwords_spanish = set(stopwords.words('spanish'))

def tokenize_and_remove_stopwords(text, language='english'):
    """
    Preprocesa el texto eliminando signos de puntuación y palabras vacías.

    Parameters:
    texto (str): Texto a preprocesar.

    Returns:
    str: Texto preprocesado.
    """
    tokens = word_tokenize(text)
    if language == 'english':
        tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords_english]
    elif language == 'spanish':
        tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords_spanish]
    return ' '.join(tokens)

def preprocess_columns(df, columns=['overview', 'genres_names', 'top_5_actors', 'director'], language='english'):
    for col in columns:
        df[col] = df[col].apply(lambda x: tokenize_and_remove_stopwords(str(x), language))
    return df

df_modelo = preprocess_columns(df_modelo)

df_modelo['genres_names'] = df_modelo['genres_names'].apply(lambda x: x.split(', '))
df_modelo['top_5_actors'] = df_modelo['top_5_actors'].apply(lambda x: x.split(', '))
df_modelo['director'] = df_modelo['director'].apply(lambda x: x.split(', '))

vectorizer = TfidfVectorizer(stop_words='english')

X_overview = vectorizer.fit_transform(df_modelo['overview'].fillna('').values.astype('U'))
X_genres = vectorizer.fit_transform(df_modelo['genres_names'].apply(lambda x: ' '.join(x)).fillna('').values.astype('U'))
X_actors = vectorizer.fit_transform(df_modelo['top_5_actors'].apply(lambda x: ' '.join(x)).fillna('').values.astype('U'))
X_director = vectorizer.fit_transform(df_modelo['director'].apply(lambda x: ' '.join(x)).fillna('').values.astype('U'))



### SISTEMA DE RECOMENDACIÓN
@app.get("/recomendar_peliculas")
def obtener_peliculas_similares(titulo_pelicula):
    """
    Recomienda películas similares a partir de un título dado.

    Parameters:
    titulo (str): Título de la película de referencia.

    dict: Diccionario en formato de lista con los títulos de las películas recomendadas.
    """
    index_pelicula_objetivo = df_modelo[df_modelo['title'].str.lower() == titulo_pelicula.lower()].index[0]
    
    similarity_overview = cosine_similarity(X_overview[index_pelicula_objetivo], X_overview).flatten()
    similarity_genres = cosine_similarity(X_genres[index_pelicula_objetivo], X_genres).flatten()
    similarity_actors = cosine_similarity(X_actors[index_pelicula_objetivo], X_actors).flatten()
    similarity_director = cosine_similarity(X_director[index_pelicula_objetivo], X_director).flatten()

    similarity_combined = (similarity_overview + similarity_genres + similarity_actors + similarity_director) / 4.0

    similarity_scores_sorted_indices = similarity_combined.argsort()[::-1]

    top_n = 5
    top_n_indices = similarity_scores_sorted_indices[1:top_n + 1]

    lis=[]
    peliculas_similares = df_modelo.iloc[top_n_indices]['title'].values
    for elemento in peliculas_similares:
        lis.append(str(elemento))
        
    resultados = f"Películas más similares a '{titulo_pelicula}': {lis}"

    return resultados 
