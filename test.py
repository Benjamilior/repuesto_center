
#No olvidarse del key.json
#Buscar todos los "Cambiar" antes de usar
#En chatgpt cruzar sku_dotu con links. Pedir que te haga el json desde el info del sheets
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

import platform

if platform.system() == "Windows":
    PATH = "C:\\Program Files (x86)\\chromedriver.exe"
elif platform.system() == "Darwin":  # 'Darwin' es el nombre del sistema operativo de macOS
    PATH = "/usr/local/bin/chromedriver"
else:
    raise EnvironmentError("Sistema operativo no compatible")

#Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json' #Cambiar check
SPREADSHEET_ID = '1UNIN1rfq_gkMHttQAvd8LRT9j4mI6QX06coQuu-BsgU' #Cambiar check
creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


# Configuración de Configuración
SCOPES2 = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID2 = '1UNIN1rfq_gkMHttQAvd8LRT9j4mI6QX06coQuu-BsgU'

# Define el rango inicial, en este caso la columna W y puedes continuar con las siguientes columnas.
RANGE_NAME2 = 'Verificador!v2:AB180' # Desde W2 hasta AA (ajústalo como desees)

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES2)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID2, range=RANGE_NAME2).execute()
values = result.get('values', [])

if not values:
    print("No se encontraron datos en la hoja de Google Sheets.")
else:
    # Crear un diccionario que tiene las URLs de todas las columnas.
    urls = {
    f"Columna_{chr(87 + i)}": [
        row[i] if len(row) > i and row[i] != "" else None  # Asegúrate de manejar celdas vacías
        for row in values
    ]
    for i in range(max(len(row) for row in values))  # Calcula el número máximo de columnas
}

# Filtra valores nulos de cada lista para evitar procesar entradas vacías
urls = {key: [url for url in urls_list if url] for key, urls_list in urls.items()}


chrome_options = Options()
chrome_options.add_argument("--headless")  # Sin ver el navegador
chrome_options.add_argument("--window-size=1920x1080")

start_time = time.time()  # Tiempo de inicio de la ejecución
driver = webdriver.Chrome(options=chrome_options)
urls = "https://articulo.mercadolibre.cl/MLC-564993408-optico-izquierdo-chevrolet-sail-2010-2015-_JM"
# Iterar sobre las columnas (por ejemplo: W, X, Y, Z, AA, etc.)
results = []  # Asegúrate de que los resultados estén vacíos al empezar cada columna
for url in urls:
        driver.get(urls)
        precio_oferta = "0"
        precio_normal = "0"
        time.sleep(3)
        try:
            # Intenta obtener el precio de oferta
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[7]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        except NoSuchElementException:
            pass  # Si no se encuentra el precio de oferta, se continúa con el siguiente bloque de código

        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[6]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[6]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass # Si no se encuentra el precio normal, se continúa con el siguiente bloque de código

        if precio_oferta == "0" and precio_normal == "0":
            try:
                # Si no se puede encontrar ni el precio de oferta ni el precio normal, intenta con el tercer XPath
                precio_normal_element = driver.find_element("xpath", '/html/body/main/div[2]/div[5]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
                precio_normal = precio_normal_element.text  # Guarda el precio normal
            except NoSuchElementException as e:
                print(f"No se pudo encontrar el precio en la URL {url} - {e}")

        data = {
            "URL": url,  # Usamos la URL completa como la primera columna
            "Precio": precio_normal,
            "Precio_oferta": precio_oferta
        }
        results.append(data)
        print(data)
        time.sleep(0.5)
    



driver.quit()
