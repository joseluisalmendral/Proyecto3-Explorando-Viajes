import pandas as pd
from bs4 import BeautifulSoup
import requests

import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


def distance_conversion(x):
    """
    Converts a distance string to kilometers.

    The input string is expected to contain a numeric distance followed by a unit ('km' or 'm'). The function converts the string to a float value representing the distance in kilometers.

    Parameters:
    - x (str): A string representing the distance (e.g., '2.5 km' or '500 m'), with commas optionally used as decimal separators.

    Returns:
    - (float or None): The distance in kilometers, or None if the unit is not recognized.
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
    Cleans and formats specific columns in a DataFrame.

    This function processes the 'Distance to center', 'Score', 'Price (€)', and 'Location score' columns by applying necessary conversions and formatting, such as extracting numeric values, handling units, and converting strings to floats.

    Parameters:
    - df (pandas.DataFrame): The input DataFrame containing the columns to be cleaned.

    Returns:
    - (pandas.DataFrame): The cleaned DataFrame with formatted columns.
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
    Extracts property data from a BeautifulSoup object and returns it as a cleaned DataFrame.

    The function scrapes property details such as name, address, distance to the center, score, location score, price, and link from HTML elements identified by specific data-test IDs. The extracted data is then cleaned using the `clean_df` function.

    Parameters:
    - soup (BeautifulSoup): A BeautifulSoup object containing the HTML of the property listings.

    Returns:
    - (pandas.DataFrame): A cleaned DataFrame with the extracted property data.
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
    Opens a URL in a browser to scrape property data from Booking.com, scrolls to load more results, and returns the page source as a BeautifulSoup object.

    The function navigates to a specific search result page for a city on the Booking.com website based on the provided destination ID, check-in, and check-out dates. It continuously scrolls to load more results, clicks the "load more results" button, and finally returns the page's HTML content.

    Parameters:
    - dest_id (str): The destination ID used to search for the city.
    - checkin (str): The check-in date in 'YYYY-MM-DD' format.
    - checkout (str): The check-out date in 'YYYY-MM-DD' format.

    Returns:
    - (BeautifulSoup): A BeautifulSoup object containing the HTML of the search results page.
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

