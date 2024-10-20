from bs4 import BeautifulSoup

# Requests
import requests

import pandas as pd
import numpy as np

from time import sleep, time

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from src import support_selenium as sup_sel
import random


def sleep_random_time():
    """
    Genera un número aleatorio entre 2 y 5 con un solo decimal, y pausa la ejecución del programa por esa cantidad de segundos.

    Utiliza `random.uniform` para generar el número, y luego lo redondea a un decimal. Finalmente, se usa `time.sleep`
    para pausar la ejecución por la cantidad de segundos generados.

    Returns:
        None
    """

    random_sleep_time = round(random.uniform(2, 5), 1)    
    sleep(random_sleep_time)




def scroll_random(driver):
    """
    Realiza un desplazamiento (scroll) aleatorio hacia abajo en la página actual del navegador Selenium.

    Genera un número aleatorio de píxeles entre 200 y 1000 para hacer el desplazamiento. Luego utiliza `execute_script`
    de Selenium para ejecutar un script de JavaScript que desplaza la ventana de navegación hacia abajo por el número de
    píxeles generados.

    Args:
        driver (webdriver): El controlador de Selenium activo que está interactuando con el navegador.

    Returns:
        None
    """

    random_scroll = random.randint(200, 1000)
    driver.execute_script(f"window.scrollBy(0, {random_scroll});")



def obtener_urls_paginas_principales(ciudades):
    """
    Obtiene las URLs de las páginas principales de búsqueda de TripAdvisor para una lista de ciudades y devuelve un DataFrame con las ciudades y sus URLs.

    La función automatiza el proceso de búsqueda en el sitio web de TripAdvisor para cada ciudad de la lista, realiza un scroll aleatorio
    en la página de resultados y devuelve la URL actual. El resultado final se guarda en un DataFrame que contiene las ciudades y las URLs correspondientes.

    Acciones principales:
    1. Inicializa el navegador en modo incógnito.
    2. Navega a la página principal de TripAdvisor.
    3. Interactúa con el banner de cookies si está presente.
    4. Realiza una búsqueda automática de la ciudad.
    5. Navega a la página de la primera sugerencia de búsqueda.
    6. Realiza un scroll aleatorio en la página.
    7. Almacena la URL actual en una lista.
    8. Devuelve los resultados en un DataFrame.

    Args:
        ciudades (list): Lista de nombres de ciudades para buscar en TripAdvisor.

    Returns:
        pd.DataFrame: Un DataFrame con dos columnas: 'ciudades' y 'urls', donde cada fila corresponde a la URL de búsqueda de la ciudad en TripAdvisor.

    Raises:
        Exception: Si falla la interacción con las cookies o la navegación por la página, el script continúa con la siguiente ciudad.
    """

    urls = []
    codigos_pagina = []
    for ciudad in ciudades:
        chrome_options = Options()
        chrome_options.add_argument("--incognito")

        driver = webdriver.Chrome(options=chrome_options)
        url_wunder = "https://www.tripadvisor.es/"
        driver.get(url_wunder)


        driver.maximize_window()

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("css selector", "#onetrust-reject-all-handler"))).click()
        except:
            print("Fallo al aceptar las cookies")

        sup_sel.sleep_random_time()

        search_box = driver.find_element('css selector', '#lithium-root > main > div:nth-child(4) > div > div > div.ctKgY > div > form > div > div > input')
        search_box.click()
        sup_sel.sleep_random_time()

        search_box.send_keys(ciudad)
        sup_sel.sleep_random_time()

        search_box.send_keys(Keys.ARROW_DOWN)
        sup_sel.sleep_random_time()

        search_box.send_keys(Keys.ENTER)
        sup_sel.sleep_random_time()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(('css selector', '#lithium-root > span > header > span > div > div > div.uNcsI._T.o > div > div.f.M > button:nth-child(3) > span > a'))).click()
        sup_sel.scroll_random(driver)
        sleep(10) #dejamos tiempo a que cargen las cosas

        urls.append(driver.current_url)
        sleep(5)
        codigos_pagina.append(driver.page_source)

        sleep(1)
        driver.quit()

    return pd.DataFrame({'ciudades': ciudades, 'urls': urls, 'codigos_pagina': codigos_pagina})


def obtener_html_de_urls(urls):
    """
    Realiza una solicitud HTTP a una URL de TripAdvisor simulando un navegador real y evitando la detección mediante técnicas de scraping.

    Esta función envía una solicitud `GET` a la URL especificada utilizando encabezados personalizados para simular un navegador real.
    Además, implementa una pausa aleatoria para imitar el comportamiento humano y evitar ser bloqueado por mecanismos de detección de bots.

    Acciones principales:
    1. Genera un User-Agent aleatorio usando la biblioteca `fake_useragent` para simular diferentes navegadores en cada solicitud.
    2. Añade un encabezado que indica que el lenguaje preferido es el español ('es').
    3. Envía la solicitud `GET` a la URL especificada.
    4. Implementa un retraso aleatorio entre 2 y 5 segundos para evitar realizar solicitudes demasiado rápidas, imitando así el comportamiento humano.

    Args:
        url (str): La URL de TripAdvisor (o cualquier otra página) que se desea scrapeer.

    Returns:
        str: El contenido HTML de la página si la solicitud es exitosa (código de estado 200).
        None: Si la solicitud falla, no se devuelve ningún contenido, y se imprime un mensaje de error con el código de estado.

    Raises:
        Exception: Si ocurre algún error durante la solicitud, la función manejará el código de estado con un mensaje adecuado.
    """

    resultado = {'urls': [], 'html': []}
    for url in urls:
        sleep(5)
        headers = {
        # Decirle al server lenguaje español
        'accept-language': 'es', 
        # Simulamos que somos el navegador Chrome
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }

        respuesta = requests.get(url, headers=headers)

        if respuesta.status_code == 200:
            resultado['urls'].append(url)
            resultado['html'].append(BeautifulSoup(respuesta.content, 'html.parser'))

    return pd.DataFrame(resultado)


# SECCION OBTENER INFO

funciones_primera_celda = {
    'get_subcategoria': lambda item:  item.find('span',{'class': 'biGQs _P fiohW hmDzD'}).getText(),
    'get_nombre': lambda item:  item.find('h3',{'class': 'biGQs _P fiohW alXOW EEXWj GzNcM BYtua UTQMg alvrA fOtGX'}).getText(),
    'get_precio': lambda item:  item.find('div',{'class': 'biGQs _P fiohW fOtGX'}).getText().replace('\xa0€',''),
    'get_puntuacion': lambda item:  item.find('div',{'class': 'jVDab W f u w JqMhy'}).get('aria-label', 'Desconocido').split(' ')[0].replace(',','.'),
    'get_n_reviews': lambda item:  item.find('div',{'class': 'jVDab W f u w JqMhy'}).get('aria-label', 'Desconocido').split(' ')[-2],
    'get_url_detalles': lambda item:  item.find('a',{'class': 'BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS'})['href'],
}

funciones_celdas = {
    'get_subcategoria': lambda item:  item.find('div',{'class': 'biGQs _P pZUbB hmDzD'}).getText(),
    'get_nombre': lambda item:  item.find('div',{'class': 'biGQs _P fiohW alXOW NwcxK GzNcM ytVPx UTQMg RnEEZ ngXxk'}).getText(),
    'get_precio': lambda item:  item.find('div',{'class': 'biGQs _P fiohW avBIb fOtGX'}).getText().replace('\xa0€',''),
    'get_puntuacion': lambda item:  item.find('div',{'class': 'jVDab W f u w JqMhy'}).get('aria-label', 'Desconocido').split(' ')[0].replace(',','.'),
    'get_n_reviews': lambda item:  item.find('div',{'class': 'jVDab W f u w JqMhy'}).get('aria-label', 'Desconocido').split(' ')[-2],
    'get_url_detalles': lambda item:  item.find('a',{'class': 'BMQDV _F Gv wSSLS SwZTJ hNpWR'})['href'],
}


def obter_info(funcion, item):
    try:
        return funcion(item)
    except:
        return 'Desconocido'


def obtener_actividades(df):
    categorias = ['INPRESCINDIBLES', 'GASTRONOMIA', 'ARTE Y CULTURA', 'ATRACCIONES PRINCIPALES', 'OTRAS ATRACCIONES PRINCIPALES', 'VISITAS GUIADAS']
    resultado = {"ciudad": [], "categoria": [], "subcategoria": [], "nombre": [], "precio": [], "puntuacion": [], "n_reviews": [], "url_detalles": []}

    for i, fila in df.iterrows():
        ciudad = fila['ciudades']
        html = BeautifulSoup(fila['codigos_pagina'], 'html.parser')

        celdas = html.find_all('div', {'class': 'BYvbL A'})[:6]

        for i, celda in enumerate(celdas):
            for item in celda.find_all('li')[:4]:

                if i == 0:
                    resultado['ciudad'].append(ciudad)
                    resultado['categoria'].append(categorias[i])
                    resultado['subcategoria'].append(obter_info(funciones_primera_celda['get_subcategoria'], item))
                    resultado['nombre'].append(obter_info(funciones_primera_celda['get_nombre'], item))
                    resultado['precio'].append(obter_info(funciones_primera_celda['get_precio'], item))
                    resultado['puntuacion'].append(obter_info(funciones_primera_celda['get_puntuacion'], item))
                    resultado['n_reviews'].append(obter_info(funciones_primera_celda['get_n_reviews'], item))
                    resultado['url_detalles'].append(obter_info(funciones_primera_celda['get_url_detalles'], item))
                else:
                    resultado['ciudad'].append(ciudad)
                    resultado['categoria'].append(categorias[i])
                    resultado['subcategoria'].append(obter_info(funciones_celdas['get_subcategoria'], item))
                    resultado['nombre'].append(obter_info(funciones_celdas['get_nombre'], item))
                    resultado['precio'].append(obter_info(funciones_celdas['get_precio'], item))
                    resultado['puntuacion'].append(obter_info(funciones_celdas['get_puntuacion'], item))
                    resultado['n_reviews'].append(obter_info(funciones_celdas['get_n_reviews'], item))
                    resultado['url_detalles'].append(obter_info(funciones_celdas['get_url_detalles'], item))

    return pd.DataFrame(resultado)                
        