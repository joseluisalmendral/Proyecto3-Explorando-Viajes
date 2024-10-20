import pandas as pd
import matplotlib.pyplot as plt




def crear_nombre_vuelo(row, index):
    """
    Genera un nombre de vuelo formateado utilizando la información de origen y destino 
    de una fila del DataFrame.

    Args:
        row (pd.Series): Una fila del DataFrame que contiene los detalles del vuelo.
        index (int): El índice de la fila en el DataFrame.

    Returns:
        str: Una cadena formateada que representa el itinerario del vuelo.
    """
    
    origin_1 = row['origin_1']
    destination_1 = row['destination_1']
    origin_2 = row['origin_2']
    destination_2 = row['destination_2']
    return f"{index} {origin_1} -> {destination_1} / {origin_2} -> {destination_2}"



def crear_dataframe(data):
    """
    Crea un DataFrame de pandas a partir de los datos de vuelos, extrayendo los detalles 
    relevantes como el precio, origen, destino, horas de salida y llegada para cada etapa 
    del itinerario. También calcula la duración total de los vuelos y genera un nombre de 
    vuelo para cada itinerario.

    Args:
        data (dict): Los datos de los vuelos en formato de diccionario, normalmente 
        obtenidos de una respuesta de API.

    Returns:
        pd.DataFrame: Un DataFrame que contiene la información procesada de los vuelos, 
        incluyendo precio, tiempos de vuelo, duración total y nombres generados de los vuelos.
    """

    # Extraemos los itinerarios
    itineraries = data['data']['itineraries']

    # Creamos una lista con los datos que nos interesan de la respuesta
    flight_data = []
    for itinerary in itineraries:
        price = itinerary['price']['raw']
        leg_1 = itinerary['legs'][0]
        leg_2 = itinerary['legs'][1]
        
        flight_info = {
            'id': itinerary['id'],
            'price': price,
            'departure_1': leg_1['departure'],
            'arrival_1': leg_1['arrival'],
            'duration_1': leg_1['durationInMinutes'],
            'origin_1': leg_1['origin']['name'],
            'destination_1': leg_1['destination']['name'],
            'departure_2': leg_2['departure'],
            'arrival_2': leg_2['arrival'],
            'duration_2': leg_2['durationInMinutes'],
            'origin_2': leg_2['origin']['name'],
            'destination_2': leg_2['destination']['name']
        }
        
        flight_data.append(flight_info)

    df = pd.DataFrame(flight_data)

    df['flight_name'] = df.apply(lambda row: crear_nombre_vuelo(row, row.name), axis=1)

    df['total_duration'] = df['duration_1'] + df['duration_2']

    return df


def mostrar_grafica_comparacion_precios(df, ciudad):
    """
    Muestra un gráfico de barras horizontal comparando los precios de los vuelos 
    para una ciudad específica.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos de los vuelos, 
        incluyendo los nombres de los vuelos y los precios.
        ciudad (str): La ciudad o destino para la cual se están comparando los precios de los vuelos.

    Returns:
        None: Muestra la visualización del gráfico de barras.
    """

    plt.figure(figsize=(10, 6))
    plt.barh(df['flight_name'], df['price'], color='blue')
    plt.xlabel('Precio (€)')
    plt.ylabel('Vuelo (Ruta)')
    plt.title(f'Comparacion Precios Vuelos {ciudad}')
    plt.tight_layout()
    plt.show()


def mostrar_grafica_comparacion_duracion(df, ciudad):
    """
    Muestra un gráfico de barras horizontal comparando la duración total de los vuelos 
    para una ciudad específica.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos de los vuelos, 
        incluyendo los nombres de los vuelos y la duración total.
        ciudad (str): La ciudad o destino para la cual se están comparando las duraciones de los vuelos.

    Returns:
        None: Muestra la visualización del gráfico de barras.
    """

    plt.figure(figsize=(10, 6))
    
    plt.barh(df['flight_name'], df['total_duration'], color='green')
    plt.xlabel('Duracion Total (mins)')
    plt.ylabel('Vuelo (Ruta)')
    plt.title(f'Comparacion Duracion Vuelos {ciudad}')
    plt.tight_layout()
    plt.show()



def mostrar_grafica_comparativa(df, ciudad):
    """
    Muestra un gráfico comparativo con dos subgráficos: uno comparando la duración total de los vuelos 
    y otro comparando los precios de los vuelos para una ciudad específica.

    Args:
        df (pd.DataFrame): El DataFrame que contiene los datos de los vuelos, 
        incluyendo nombres de vuelos, precios y duraciones.
        ciudad (str): La ciudad o destino para la cual se están comparando los vuelos.

    Returns:
        None: Muestra la visualización del gráfico comparativo.
    """

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(78, 66))

    # Gráfico 1: Duración Total de los Vuelos
    ax1.bar(df['flight_name'], df['total_duration'], color='orange')
    ax1.set_ylabel('Duración Total (minutos)', fontsize=60)
    ax1.set_xlabel('Vuelos (Ruta)', fontsize=60)
    ax1.set_title(f'Duración Total Vuelos {ciudad}', fontsize=60)
    ax1.tick_params(axis='x', rotation=80, labelsize=50)
    ax1.tick_params(axis='y', labelsize=50)
    ax1.grid(True)

    # Gráfico 2: Precio de los Vuelos
    ax2.bar(df['flight_name'], df['price'], color='purple')
    ax2.set_ylabel('Precio (€)', fontsize=60)
    ax2.set_xlabel('Vuelos (Ruta)', fontsize=60)
    ax2.set_title(f'Precio Vuelos {ciudad}', fontsize=60)
    ax2.tick_params(axis='x', rotation=80, labelsize=50)
    ax2.tick_params(axis='y', labelsize=50) 
    ax2.grid(True)

    plt.tight_layout()
    plt.show()