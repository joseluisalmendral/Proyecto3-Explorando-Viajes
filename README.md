
# Proyecto de Planificación de Viajes

![Imagen del Proyecto](./imagenes/imagen_readme.webp)

Este proyecto se ha enfocado en ofrecer una solución personalizada para una pareja que busca una escapada romántica durante el Día de San Valentín en 2025. El objetivo es proporcionar una experiencia de viaje inolvidable, combinando vuelos, alojamiento y actividades cuidadosamente seleccionadas en ciudades como París y Barcelona. Utilizamos herramientas de scraping y procesamiento de datos para obtener información actualizada de las mejores opciones, permitiendo elegir vuelos económicos, alojamientos bien ubicados y actividades destacadas para disfrutar en pareja.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas y archivos:

```
├── .gitignore
├── datos
├── html
├── jsons
├── respuestas
├── urls
├── imagenes
├── notebooks
├── src
├── __pycache__
```

### Descripción de Carpetas y Archivos

- **datos**: Contiene archivos CSV que almacenan información estructurada sobre actividades, alojamientos y vuelos. Los datos incluyen detalles de ciudades como Barcelona, París y Madrid, además de fechas relevantes para los viajes planificados.
- **html**: Archivos HTML de actividades para las ciudades de Barcelona y París, posiblemente resultado de scraping web.
- **jsons**: Información relacionada con aeropuertos y respuestas JSON para vuelos entre Madrid, Barcelona y París para el año 2025.
- **urls**: Almacena CSVs con URLs de páginas web utilizadas para el scraping o análisis.
- **imagenes**: Contiene una imagen para el README.
- **notebooks**: Contiene tres notebooks Jupyter que analizan las actividades, alojamientos y vuelos.
- **src**: Scripts de Python que soportan los notebooks, con funciones específicas para actividades, alojamiento y vuelos.

## Requisitos

Este proyecto requiere Python 3.12 y las siguientes bibliotecas:

- pandas 2.2.3
- numpy 2.1.2
- matplotlib 3.9.2
- selenium 4.25.0
- requests 2.32.3
- beautifulsoup4 4.12.3
- tqdm 4.66.5
- webdriver-manager 4.0.2
- python-dotenv 1.0.1

Para instalar estas dependencias, ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

## APIs Utilizadas

En este proyecto hemos utilizado las siguientes APIs para obtener información de vuelos y otras fuentes de datos:

1. **Sky-Scrapper**: Se utilizó para obtener información sobre los aeropuertos de las ciudades y sobre los vuelos.

## Webs Scrapeadas

Hemos decidido utilizar el web scrapping para obtener cierta información como:

1. **TripAdvisor.es**: Se utilizó para obtener las mejores cosas que hacer en cada ciudad en varias categorías.

2. **Booking.es**: Se utilizó para obtener información sobre los alojamientos más centricos de cada ciudad.



## Descripción de los Notebooks

1. **actividades.ipynb**: Este notebook analiza las actividades disponibles en ciudades como Barcelona y París, extrayendo información sobre las actividades más populares y visualizando datos relevantes para los viajeros.
2. **alojamiento.ipynb**: Analiza opciones de alojamiento para varias ciudades, proporcionando comparativas de precios, ubicación y disponibilidad entre Barcelona y otras ciudades.
3. **vuelos.ipynb**: Evalúa diferentes opciones de vuelos entre Madrid, Barcelona y París, basándose en datos de precios, disponibilidad y fechas específicas.

## Fechas de Vuelos, Alojamientos y Actividades

- **Vuelos**:
  - Vuelo Madrid - París: El mejor vuelo identificado es desde Madrid a París (Charles de Gaulle o París Orly) con un precio de 315.94€ y una duración total de 9h 40min. Fecha: 2025.
  - Vuelo Madrid - Barcelona: El mejor vuelo es Madrid -> Barcelona y Barcelona -> Madrid, con un precio total de 86€ y una duración de 2h 40min. Fecha: 2025.

- **Alojamientos**:
  - Alojamientos en Barcelona: 13-16 de febrero de 2025. Se han evaluado diferentes opciones para alojamientos en Barcelona, comparando precios y disponibilidad.

- **Actividades**:
  - Actividades en ciudades como París y Barcelona, obtenidas a través de scraping desde TripAdvisor. Las actividades seleccionadas están entre las mejores categorías ya filtradas por TripAdvisor.

