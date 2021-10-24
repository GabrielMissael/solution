# Solution

- Solución propuesta para el reto BBVA Contigo del Hackathon BBVA 2021. Equipo Mexdapy. Integrantes: 
    - David Pedroza Segoviano
    - Regina Priscila Badillo
    - Zaid de Anda Mariscal
    - Gabriel Missael Barco

## Descripción

![flow](https://i.imgur.com/ALN0eOn.png)

Nuestro proyecto realizará escucha activa por batches diarios o semanales (A definir) de opiniones en Twitter. Se escuchará en 5 regiones geográficas diferentes:

- España
- México
- Perú
- Argentina
- Colombia.

Se obtendrán los tweets usando la API de Twitter por medio de Tweepy (Librería de Python) usando consultas con palabras claves de las 4 prioridades estratégicas de BBVA:

- Mejorar la salud financiera de los clientes.
- Ayudar a los clientes hacia un futuro sostenible.
- Crecer en clientes.
- Buscar la excelentica operativa.

![geolisten](https://i.imgur.com/4NKgquL.png)

Posterior a la recolección por zona y prioridad, se analizarán los Tweets usando modelos pre-entrenados de Natural Lenguaje Processing para identificar clusters (conjuntos) de tweets con temas e ideas similares (similitud semántica). Luego, se realizará análisis de sentimientos, extracción de palabras clave de cada conjunto, esto lo puede ver de manera sintetizada en el flowchart anexado. 

Finalmente, utilizando las palabras clave y el sentimiento asociado a cada conjunto, se generará una oración, idealmente en forma de sugerencia, que resuma el contenido del conjunto.

## Recursos de apoyo:

- [Entregable 2](https://drive.google.com/drive/folders/1LLXhP6zizKcj66pxeyk3fE7fwyq1uueD?usp=sharing)

- [Entregable 1](https://drive.google.com/drive/folders/12ef3BHbgejSfPqrziVR6YRWbqrKDcID5?usp=sharing)

## Análisis de tweets.

Todo el análisis se usa utilizando Python y múltiples librerías (ver requirements.txt en el repositorio). La representación gráfica del pipeline completo de recolección y análisis de tweets se encuentra en la carpeta de drive, con el nombre de "Solution pipeline.png". El proceso es el siguiente: 

1. Recolectamos tweets usando **Tweepy**, por zona geográfica en los **5 países** de interés. Para esto, se especifica un centro con coordenadas y un radio, tal que se recolectan tweets de dicho circulo (que incluye al país en cuestión y a sus vecinos). Para obtener los tweets, se generan querys diferentes para cada una de las **4 prioridades**, y esto se hace con palabras clave relacionadas con dicha prioridad. Por ejemplo, para la prioridad de salud financiera, se buscan palabras clave como "ahorro" e "inversión. Se recolectan un total de 5000 tweets por país y prioridad, obteniendo un total de 20 datasets de 5000 tweets cada uno. 
2. Realizamos clustering dentro de cada uno de estos 20 datasets para obtener los temas de los que se habla, para esto: 
    1. Creamos **embeddings de los tweets**, esto es, pasamos cada tweet a un punto en el espacio. En particular, usamos un modelo pre-entrenado llamado **Siamese BERT-Network**, distiluse-base-multilingual-cased-v2, que pasa cada tweet a un punto en el espacio de 512 dimensiones. Esto tiene la propiedad de que los puntos cercanos (tweets) hablan de temas similares, y los puntos lejanos de temas diferentes.
    2. Aplicamos una técnica de **reducción de dimensionalidad** de los datos ya que 512 son demasiadas dimensiones para varias técnicas de clustering (particularmente de la que usamos). Para esto, usamos **UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction**, un algoritmo de clustering eficiente y que preserva las características de los datos de manera eficiente. Reducimos a 15 dimensiones. 
    3. Finalmente, aplicamos un algoritmo de **clustering** sobre estos puntos para obtener grupos de tweets que hablen de lo mismo y/o de manera similar. Para esto, usamos **HDBSCAN: Hierarchical density-based spatial clustering of applications with noise.** Este algoritmo determina por si mismo el número de clusters y manda los tweets irrelevantes a ruido (sin cluster asignado. 
3. Una vez con los clusters dentro de cada dataset, tomamos únicamente los que tengan más de 100 tweets, y analizamos cada uno de estos clusters. Hacemos un análisis de sentimientos sobre los tweets y también obtenemos las palabras que mejor representan la información de los clusters.
4. Finalmente, realizamos varias visualizaciones de los clusters con este análisis y se genera la recomendación.

![pipeline](https://i.imgur.com/pTdBtkc.png)

## AWS

En una instancia de AWS, se ejecutará primero nuestro scrapper de información de twitter (cuya información se detalla más a profundidad en la sección **análisis de tweets**, que guardaremos en la misma instancia, para posterior ingreso a el módulo de análisis de tweets. Después, de manera secuencial, se ejecutará un análisis de sentimiento sobre cada cluster, para procesar todos los datos y obtener todos los estadísticos, que se almacenarán en un servicio S3. Estos datos posteriormente se pondrán a disposición de la página web mediante una API, que siempre estará expuesta para que la página web la pueda consumir. Cuando reciba un request, la API cargará los datos de S3, y los cambiará a un formato json para que la página web los pueda consumir.

## Página Web

Todos los datos obtenidos y procesados, serán desplegados en una página web, que consumirá la API antes implementada en la instancia de AWS (Ver sección anterior). Esta página contendrá una vista inicial, donde se podrán elegir entre distintos países: España, México, Perú, Argentina, Colombia, (Ver maqueta de página en la carpeta). Por cada país, existirá una página donde se mostrará un Dashboard de los estadísticos, mapas, wordclouds, y demás indicadores que ayuden a la comprensión de los datos procesados.

Esta página está siendo escrita con HTML, CSS y JavaScript puro, por el momento no hay necesidad de utilizar ninguna otra tecnología, se plantea que para el MVP, esta página pueda ser alojada en GitHub Pages.