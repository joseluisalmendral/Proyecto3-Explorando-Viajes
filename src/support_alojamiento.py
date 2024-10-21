import pandas as pd
from bs4 import BeautifulSoup
import requests

import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


def distance_conversion(x):
    """
    Convierte una cadena de texto que representa una distancia en kilómetros.

    La cadena de entrada debe contener un valor numérico seguido de una unidad ('km' o 'm'). La función convierte la cadena en un valor flotante que representa la distancia en kilómetros.

    Parámetros:
    - x (str): Una cadena de texto que representa la distancia (por ejemplo, '2.5 km' o '500 m'), con comas opcionalmente usadas como separadores decimales.

    Retorna:
    - (float o None): La distancia en kilómetros, o None si la unidad no es reconocida.
    """

    x = x.replace(',', '.')
    
    if x.split()[1] == 'km':
        return float(x.split()[0])
    
    elif x.split()[1] == 'm':
        return float(x.split()[0]) / 1000
    
    else:
        return None


def clean_df(df):
    """
    Limpia y formatea columnas específicas de un DataFrame.

    Esta función procesa las columnas 'Distance to center', 'Score', 'Price (€)', y 'Location score', aplicando las conversiones y formatos necesarios, tales como la extracción de valores numéricos, el manejo de unidades y la conversión de cadenas a valores flotantes.

    Parámetros:
    - df (pandas.DataFrame): El DataFrame de entrada que contiene las columnas a limpiar.

    Retorna:
    - (pandas.DataFrame): El DataFrame limpio con las columnas formateadas.
    """

    # Formatting 'Distance to center'
    df['Distance to center'] = df['Distance to center'].str.extract(r'(\d+\,?\d*\s\w{1,2})')
    df['Distance to center'] = df['Distance to center'].apply(distance_conversion)

    # Formatting 'Score'
    df['Score'] = df['Score'].str.replace(',', '.').astype(float)
    # Formatting 'Price (€)'
    df['Price (€)'] = df['Price (€)'].str.replace('€','').str.replace(' ','').str.replace('.','').astype(float)
    # Formatting 'Location score'
    df['Location score'] = df['Location score'].str.replace(r'\w+\s','', regex=True).str.replace(',','.').astype(float)

    return df


def soup_to_df(soup):
    """
    Extrae datos de propiedades de un objeto BeautifulSoup y los devuelve como un DataFrame limpio.

    La función obtiene detalles de propiedades como nombre, dirección, distancia al centro, puntuación, puntuación de la ubicación, precio y enlace desde elementos HTML identificados por IDs de datos específicos. Los datos extraídos luego se limpian usando la función `clean_df`.

    Parámetros:
    - soup (BeautifulSoup): Un objeto BeautifulSoup que contiene el HTML de los listados de propiedades.

    Retorna:
    - (pandas.DataFrame): Un DataFrame limpio con los datos de las propiedades extraídas.
    """

    # Get every item from the soup
    items = soup.find_all('div', {'data-testid': 'property-card'})

    # Defining a dictionary with the funcions that capture the information
    keys = {'Name': lambda x: x.find('div', {"data-testid": "title"}).text,
            'Address': lambda x: x.find('span', {"data-testid": "address"}).text, 
            'Distance to center': lambda x: x.find('span', {"data-testid": "distance"}).text, 
            'Score': lambda x: x.find('div', {"data-testid": "review-score"}).text[11:15], 
            'Location score': lambda x: x.find('a', {"data-testid": "secondary-review-score-link"}).text, 
            'Price (€)': lambda x: x.find('span', {"data-testid": "price-and-discounted-price"}).text, 
            'Link': lambda x: x.find("a", {'data-testid': 'title-link'}).get('href')
            }
    
    # Empty list to store items
    data = []

    for item in items:
        # Empty dictionary to store data for every item
        dc = {}
        # Fill dictionary
        for key in keys:
            try:
                dc[key] = keys[key](item)
            except:
                dc[key] = None

        data.append(dc)

    df = clean_df(pd.DataFrame(data))

    return df


def scrap_url(dest_id, checkin, checkout):
    """
    Abre una URL en un navegador para hacer scraping de datos de propiedades en Booking.com, realiza desplazamiento para cargar más resultados y devuelve el código fuente de la página como un objeto BeautifulSoup.

    La función navega a una página de resultados de búsqueda específica en Booking.com para una ciudad, según el ID de destino y las fechas de check-in y check-out proporcionadas. Desplaza continuamente la página para cargar más resultados, hace clic en el botón de "cargar más resultados" y finalmente retorna el contenido HTML de la página.

    Parámetros:
    - dest_id (str): El ID de destino usado para buscar la ciudad.
    - checkin (str): La fecha de check-in en formato 'YYYY-MM-DD'.
    - checkout (str): La fecha de check-out en formato 'YYYY-MM-DD'.

    Retorna:
    - (BeautifulSoup): Un objeto BeautifulSoup que contiene el HTML de la página de resultados de búsqueda.
    """
    
    # Open a window
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    # Get the proper URL
    url = f"https://www.booking.com/searchresults.es.html?lang=es&dest_id={dest_id}&dest_type=city&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0"
    driver.get(url)
    driver.maximize_window()
    
    while True:
        # Scroll to the end
        sleep(random.uniform(3,5))
        driver.execute_script('window.scrollBy(0, 20000)')
        sleep(random.uniform(3,5))
        # Scroll a bit up to fin the button to load more items
        driver.execute_script('window.scrollBy(0, -400)')
        sleep(random.uniform(3,5))

        try:
            # Press 'load more results'
            driver.find_element('css selector', '#bodyconstraint-inner > div:nth-child(8) > div > div.af5895d4b2 > div.df7e6ba27d > div.bcbf33c5c3 > div.dcf496a7b9.bb2746aad9 > div.d4924c9e74 > div.c82435a4b8.f581fde0b8 > button').click()

        except:
            print('No more loading available')
            break
    
    sleep(random.uniform(3,5))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Cerrar navegador
    driver.close()

    # Print the URL in case we want to test it manually
    print(url)

    return soup

