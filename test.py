import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Descargar stopwords y recursos de tokenización si aún no están descargados
nltk.download('stopwords')
nltk.download('punkt')

# Cargar el DataFrame df_modelo desde el archivo CSV
df_modelo = pd.read_csv('./data/df_modelo.csv')

app = FastAPI()

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

# Preprocesar las columnas relevantes al inicio de la aplicación
df_modelo = preprocess_columns(df_modelo)

# Definir la función obtener_peliculas_similares aquí
def obtener_peliculas_similares(titulo_pelicula, df_modelo):
    # Código de la función obtener_peliculas_similares

# Endpoint para obtener películas similares
@app.get("/peliculas_similares/")
def peliculas_similares(titulo_pelicula: str):
    try:
        resultados = obtener_peliculas_similares(titulo_pelicula, df_modelo)
        return {"resultados": resultados}
    except Exception as e:
        return {"error": str(e)}

# Ejecutar la aplicación de FastAPI con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
