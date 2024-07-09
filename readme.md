# Proyecto de Machine Learning Operations - Modelos de Recomendación de Películas

### Introducción

Este proyecto tiene como objetivo desarrollar un sistema de recomendación de películas utilizando técnicas avanzadas de machine learning como la vectorización de texto y la similitud del coseno. Desde la limpieza de datos (ETL) hasta el despliegue de una API con FastAPI en la plataforma de Render, el proyecto abarca varias etapas cruciales dentro del mundo de los datos (procesos de data engineer, análisis de datos, hasta el desarrollo de un modelo de ML) para su implementación efectiva.

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

La carpeta del proyecto API contiene los detalles sobre la configuración y desarrollo de la API utilizando FastAPI. Esta API se conecta directamente a los datos procesados durante el ETL y ofrece 6 endpoints principales para consultas específicas como películas por mes, puntajes, votos, detalles de actores y directores.

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