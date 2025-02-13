
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
RANGE_NAME2 = 'Verificador!v360:AB539'  # Desde W2 hasta AB

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

# Iterar sobre las columnas (por ejemplo: W, X, Y, Z, AA, etc.)
for column_name, column_urls in urls.items():
    results = []  # Asegúrate de que los resultados estén vacíos al empezar cada columna
    for sku_key, url in enumerate(column_urls, 1):  # Iterar sobre las URLs
        driver.get(url)
        precio_oferta = "0"
        precio_normal = "0"
        # time.sleep(3)
     
        try:
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[7]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        except NoSuchElementException:
            pass
        try:
            # Intenta obtener el precio de oferta
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[6]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        except NoSuchElementException:
            pass
        
        try:
            # Intenta obtener el precio de oferta
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[6]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span[1]/span/span[2]') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        except NoSuchElementException:
            pass# Si no se encuentra el precio de oferta, se continúa con el siguiente bloque de código
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[6]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass
        try:
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[5]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/span/span/span[2]') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        except NoSuchElementException:
            pass
        try:
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[5]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span[1]/span/span[2]') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
        except NoSuchElementException:
            pass
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[7]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[5]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[7]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[6]/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/span/span/span[2]')  # Cambiar
            precio_normal = precio_normal_element.text  # Guarda el precio normal
        except NoSuchElementException:
            pass
        

        if precio_oferta == "0" and precio_normal == "0":
            try:
                # Si no se puede encontrar ni el precio de oferta ni el precio normal, intenta con el tercer XPath
                precio_normal_element = driver.find_element("class name", 'andes-money-amount__fraction')  # Cambiar
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
    
   # Calcular el rango basado en la columna actual
    column_index = 1 + (list(urls.keys()).index(column_name) * 3)  # Incrementar cada 3 columnas
    start_col = chr(64 + column_index)  # Convertir índice numérico a letra (ej.: 1 -> A, 2 -> B)
    end_col = chr(64 + column_index + 2)  # Incrementar 2 para abarcar URL, Precio, Precio_oferta

# Escribir datos en las columnas correctas
    range_to_write = f'precios3!{start_col}2:{end_col}'  # Escribir desde la fila 2 en adelante
    values_to_insert = [[item['URL'], item['Precio'], item['Precio_oferta']] for item in results]
    result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID2,
    range=range_to_write,
    valueInputOption='USER_ENTERED',
    body={'values': values_to_insert}
).execute()


driver.quit()

# Calcular el tiempo de ejecución
end_time = time.time()
execution_time = end_time - start_time
print("Tiempo de ejecución: %.2f segundos" % execution_time)

# Fecha de extracción
now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d %H:%M:%S')
data = {"": now_str}
json_data = json.dumps(data)
values = [[json_data]]
result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID2,
    range='precios3!A1',  # Cambiar el rango según tu hoja
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()