# Proyecto de Machine Learning Operations - Modelos de Recomendación de Películas

### Introducción

Este proyecto tiene como objetivo desarrollar un sistema de recomendación de películas (MVP) utilizando técnicas avanzadas de machine learning como la vectorización de texto y la similitud del coseno. Desde la limpieza de datos (ETL) hasta el despliegue de una API con FastAPI en la plataforma de Render, el proyecto abarca varias etapas cruciales dentro del mundo de los datos (procesos de data engineer, análisis de datos, hasta el desarrollo de un modelo de ML) para su implementación efectiva.

# links de interés
## Enlaces

- [Video Explicación del Proyecto](https://drive.google.com/drive/u/0/folders/11IpWNN-hSfqtHBvODh3UdX_MUjzRYVkv)
- [FastAPI en Render](https://movies-data-sj8r.onrender.com/docs)
- [Dataset Original](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5)
- [Mi Repositorio](https://github.com/RGiovanetti?tab=repositories)


### Tabla de Contenidos

- Descripción del Proyecto
- Proceso de ETL (Extracción, Transformación y Carga) de los Datos
- Creación de la API con FastAPI
- Análisis Estadístico de los Datos (EDA)
- Explicación del Modelo de Recomendación
- Conclusión
- Descripción del Proyecto

Este proyecto implica la implementación de un modelo de recomendación de películas utilizando machine learning, utilizando dos conjuntos de datos en formato CSV: movies_dataset.csv y credits.csv, cada uno con aproximadamente 45,000 filas de datos en bruto. El objetivo principal es realizar una adecuada limpieza y preparación de los datos (ETL) para su posterior consulta a través de una API, proporcionando detalles sobre películas, directores y elenco. Además, se incluye un análisis estadístico de los datos (EDA) para apoyar la selección, entrenamiento e implementación del modelo final.

### Proceso de ETL (Extracción, Transformación y Carga) de los Datos

En los archivos etl_movies.ipynb y etl_Credit.ipynb del repositorio se detallan los pasos para transformar los datos iniciales en bruto. Se aplicaron diversas técnicas y herramientas para normalizar los datos, eliminar duplicados, manejar valores nulos y crear estructuras de datos optimizadas para consultas eficientes.

### Creación de la API con FastAPI

La carpeta del proyecto API contiene los detalles sobre la configuración y desarrollo de la API utilizando FastAPI. Esta API se conecta directamente a los datos procesados durante el ETL y ofrece 8 endpoints principales para consultas específicas como películas por mes, puntajes, votos, detalles de actores y directores.

- Películas por mes: get_movies_by_month (escribimos el 'mes' y nos devuelve la cantidad de títulos hechos en ese mes)
- Películas por día: get_movies_by_day (escribimos el 'día' y nos devuelve la cantidad de títulos hechos en ese día)
- Score de película: get_movie_score (escribimos el título y nos devuelve su puntaje)
- Votación de película: get_movie_votes_average (escribimos el título y nos devuelve su número de votos y promedio)
- Consulta de actor: get_actor_info (retorna información sobre un actor específico y sus filmaciones. Si se busca un apellido/nombre común trae la cantidad de actores con ese apellido)
- Consulta de actorsindirecto: get_non_director_actor_info (retorna información sobre un actor que no es director en sus filmaciones)
- Consulta de director: get_director_info (retorna información sobre un director específico y sus filmaciones)
- Sistema de recomendación: get_recomendacion (ponemos el titulo de una funcion y nos retorna una lista con 5 peliculas recomendadas, basada en el titulo, genero, actor y director)


### Análisis exploratorio de los Datos (EDA)

El archivo 'eda y preparacion_modelo.ipynb' muestra en detalle el análisis estadístico aplicado después del ETL. Se evaluaron datos numéricos, se generaron nubes de palabras y se analizaron patrones relevantes para preparar los datos adecuadamente para el modelo de recomendación.

### Explicación del Modelo de Recomendación

Se optó por utilizar TfidfVectorizer y cosine_similarity para implementar el modelo de recomendación, utilizando los datos preparados en el EDA. El código se encuentra en main.py configurado para entrenar automáticamente el modelo al iniciar el servidor de la API y proporcionar recomendaciones precisas basadas en similitud de contenido.

### Conclusión

El proyecto de Machine Learning Operations - Modelos de Recomendación de Películas representa un desafío integral que abarca múltiples aspectos del desarrollo en Data Science. Desde la implementación de técnicas de ingeneria de datos como un correcto ETL o la creación de una API, hasta tecnicas el desarrollo de un modelo de machine learning.
 El sistema modelo no solo cumple con los objetivos iniciales de proporcionar recomendaciones precisas, sino que también establece una base sólida para futuras expansiones y mejoras. La metodología empleada en el ETL, EDA y modelado puede ser adaptada fácilmente para incorporar nuevos datos y técnicas avanzadas en el futuro.

###### Requisitos Previos

- Antes de comenzar, asegúrate de tener instalados los siguientes programas y librerías:

Git
Python 3.8 o superior
Pip (gestor de paquetes de Python)
Librerías de Python: pandas, nltk, sklearn, scipy, fastapi