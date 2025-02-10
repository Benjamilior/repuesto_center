
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

# RANGE_NAME2 = 'Verificador!v2:AB180' # Desde W2 hasta AA (ajústalo como desees)
RANGE_NAME2 = 'Verificador!v2:AB180'

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
        time.sleep(3)
        
        try:
            precio_oferta_element =  driver.find_element("xpath", '/html/body/main/div[2]/div[7]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span') # Cambiar
            precio_oferta = precio_oferta_element.text  # Guarda el precio de oferta
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
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[7]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span/span/span[2]')  # Cambiar
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
        try:
            # Intenta obtener el precio normal
            precio_normal_element =driver.find_element("xpath", '/html/body/main/div[2]/div[5]/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div[1]/span[1]/span/span[2]')  # Cambiar
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
    range_to_write = f'precios!{start_col}2:{end_col}'  # Escribir desde la fila 2 en adelante
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
    range='precios!A1',  # Cambiar el rango según tu hoja
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()


# competitor = "Mercado Libre"  # Cambiar 
# # Enviar datos a otro Google Sheets
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# KEY = 'key.json'
# NEW_SPREADSHEET_ID = '1ofzsOShcjwZn_lo_yvQhtteoUQfNxPfP8O-4wo-u1vo'  # ID de la nueva hoja de cálculo

# creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
# service = build('sheets', 'v4', credentials=creds)
# sheet = service.spreadsheets()

# # Obtener la última fila con datos en la nueva hoja
# result = sheet.values().get(spreadsheetId=NEW_SPREADSHEET_ID, range='ferre_sur!A:A').execute() #Cambiar donde llega la info
# values = result.get('values', [])
# last_row = len(values) + 1  # Obtener el índice de la última fila vacía

# # Convertir resultados a la lista de valores
# values = [[row['SKU'], competitor, row['Precio'], row['Precio_oferta'], now_str] for _, row in df.iterrows()]

# # Insertar los resultados en la nueva hoja después de la última fila
# update_range = f'ferre_sur!A{last_row}:E{last_row + len(values) - 1}' #Cambiar
# result = sheet.values().update(
#     spreadsheetId=NEW_SPREADSHEET_ID,
#     range=update_range,
#     valueInputOption='USER_ENTERED',
#     body={'values': values}

sku={
    "Ferresurdotu1": "https://articulo.mercadolibre.cl/MLC-1463415569-cementos-bio-bio-_JM",
    "Ferresurdotu2": "https://articulo.mercadolibre.cl/MLC-998714861-tornillo-autoperforante-hexagonal-cg-12x34-zincado-100-u-_JM",
    "Ferresurdotu5": "https://articulo.mercadolibre.cl/MLC-1135761461-tornillo-autoperforante-hex-techo-pta-fina-10x2-12-100und-_JM",
    "Ferresurdotu6": "https://articulo.mercadolibre.cl/MLC-1711579718-tornillo-10x2-12-hex-punta-espada-autoperforante-x-100-unds-_JM",
    "Ferresurdotu7": "https://listado.mercadolibre.cl/tornillo-autoperforante#D[A:tornillo%20autoperforante]",
    "Ferresurdotu8": "https://articulo.mercadolibre.cl/MLC-1370057941-tornillo-autoperforante-hex-techo-pta-espada-10-x-3-500-_JM",
    "Ferresurdotu9": "https://articulo.mercadolibre.cl/MLC-1999633288-tornillo-autoperforante-hex-techo-pta-fina-10-x-1-100und-_JM",
    "Ferresurdotu10": "https://articulo.mercadolibre.cl/MLC-1318753225-5-sacos-bolsas-construccion-arena-escombros-drywall-90-x-60-_JM",
    "Ferresurdotu11": "https://articulo.mercadolibre.cl/MLC-1427363303-tornillo-autoperforante-hexagonal-techo-12x2-12-100und-_JM",
    "Ferresurdotu14": "https://articulo.mercadolibre.cl/MLC-1912561232-placas-volcanita-yeso-carton-10x1200x2400mm-rf-res-fuego-_JM",
    "Ferresurdotu16": "https://www.mercadolibre.cl/discos-de-corte-para-fierro-4-12-krafter-50-unidades-color-negro/p/MLC22808266",
    "Ferresurdotu18": "https://articulo.mercadolibre.cl/MLC-2278678864-tornillo-autoperforante-hexagonal-techo-12x34-100und-_JM",
    "Ferresurdotu21": "https://articulo.mercadolibre.cl/MLC-2160078152-plancha-zinc-5v-035x895x2000-az80-_JM",
    "Ferresurdotu22": "https://articulo.mercadolibre.cl/MLC-1840218848-terciado-estructural-pino-18-mm-122-244-para-retiro-_JM",
    "Ferresurdotu23": "https://articulo.mercadolibre.cl/MLC-1296956405-camara-para-rueda-carretilla-350-x-8-_JM",
    "Ferresurdotu24": "https://articulo.mercadolibre.cl/MLC-1093704646-frague-weber-mendoza-1-kg-_JM",
    "Ferresurdotu26": "https://articulo.mercadolibre.cl/MLC-2100987606-pack-10-unidades-teflon-12-66mt-amarillo-gas-_JM",
    "Ferresurdotu27": "https://articulo.mercadolibre.cl/MLC-570702012-abrazadera-20-mm-pvc-conduit-100-uni-_JM",
    "Ferresurdotu29": "https://articulo.mercadolibre.cl/MLC-1044372693-tornillo-madera-crs-zincado-6-x-1-58-1000-und-_JM",
    "Ferresurdotu31": "https://articulo.mercadolibre.cl/MLC-1399469127-osb-estructural-95-mm-122-x-244-cm-_JM",
    "Ferresurdotu33": "https://articulo.mercadolibre.cl/MLC-920998168-terciado-pino-estructural-18mm122mt244mt-_JM",
    "Ferresurdotu34": "https://articulo.mercadolibre.cl/MLC-1044353527-tornillo-madera-crs-zincado-6-x-2-pulgadas-1000-unidades-_JM",
    "Ferresurdotu35": "https://articulo.mercadolibre.cl/MLC-1293179465-pack-15codos-ppr-90-polifusion-termofusion-20mm-_JM",
    "Ferresurdotu36": "https://articulo.mercadolibre.cl/MLC-1308027930-osb-95mm-244x122-_JM",
    "Ferresurdotu38": "https://articulo.mercadolibre.cl/MLC-1269397891-pino-cepillado-seco-1x3x32-mts-_JM",
    "Ferresurdotu39": "https://articulo.mercadolibre.cl/MLC-1268894299-pino-bruto-seco-2x3x32-mts-_JM",
    "Ferresurdotu40": "https://articulo.mercadolibre.cl/MLC-610283173-tarugo-paloma-plastico-vulcanita-empaque-de-100-_JM",
    "Ferresurdotu41": "https://articulo.mercadolibre.cl/MLC-1661087992-pino-seco-cepillado-1-x-4-x-320-mt-_JM",
    "Ferresurdotu42": "https://articulo.mercadolibre.cl/MLC-1269397891-pino-cepillado-seco-1x3x32-mts-_JM",
    "Ferresurdotu43": "https://articulo.mercadolibre.cl/MLC-1053135050-plancha-yeso-carton-120-x-240-x-15-mm-_JM",
    "Ferresurdotu44": "https://articulo.mercadolibre.cl/MLC-600450409-brocha-para-pintar-3-pulgadas-mango-madera-_JM",
    "Ferresurdotu46": "https://articulo.mercadolibre.cl/MLC-1922144384-brocha-mango-plastico-4-pulgadas-101mm-pretul-truper-_JM",
    "Ferresurdotu48": "https://articulo.mercadolibre.cl/MLC-1659571374-bolsa-de-pellet-de-madera-15kg-_JM",
    "Ferresurdotu50": "https://articulo.mercadolibre.cl/MLC-1420910791-tarugo-clavo-tornillo-punta-cruz-8x80mm-100-pcs-_JM",
    "Ferresurdotu51": "https://articulo.mercadolibre.cl/MLC-2288718570-codo-40-x-875-grados-gris-hoffens-_JM",
    "Ferresurdotu52": "https://articulo.mercadolibre.cl/MLC-1873955484-tubo-sanitario-gris-40mm-1mt-hoffens-ferrepernos-_JM",
    "Ferresurdotu54": "https://articulo.mercadolibre.cl/MLC-1460466747-tubo-pvc-sanitario-gris-75mm-x-6m-_JM",
    "Ferresurdotu55": "https://articulo.mercadolibre.cl/MLC-978502154-gas-butano-doite-227-gr-_JM",
    "Ferresurdotu57": "https://articulo.mercadolibre.cl/MLC-2156043996-plancha-zinc-acanalada-035x851x3660-az80-_JM",
    "Ferresurdotu58": "https://articulo.mercadolibre.cl/MLC-2216250876-brocha-58x2-cerda-natural-mango-madera-hela-_JM",
    "Ferresurdotu59": "https://articulo.mercadolibre.cl/MLC-1383795425-pino-impregnado-2-x-2-x-320-mt-_JM",
    "Ferresurdotu61": "https://articulo.mercadolibre.cl/MLC-1044821285-pack-50-unidades-codos-pvc-hidraulico-20-mm-so-so-_JM",
    "Ferresurdotu62": "https://articulo.mercadolibre.cl/MLC-1241654727-aguarras-mineral-1-lt-_JM",
    "Ferresurdotu66": "https://www.mercadolibre.cl/pilas-duracell-alcalinas-aaa-16-unidades/p/MLC24887947",
    "Ferresurdotu69": "https://articulo.mercadolibre.cl/MLC-1268952025-pino-cepillado-seco-1x2x32-mts-pack-de-10-unidades-_JM",
    "Ferresurdotu72": "https://articulo.mercadolibre.cl/MLC-1071289706-osb-estructural-111mm-certificado-ce-iso-_JM",
    "Ferresurdotu73": "https://articulo.mercadolibre.cl/MLC-978289979-tubo-sanitario-gris-50mm-1mt-hoffens-ferrepernos-_JM",
    "Ferresurdotu75": "https://articulo.mercadolibre.cl/MLC-631710463-silicona-blanca-sellador-acrilico-sellotec-300-ml-_JM",
    "Ferresurdotu76": "https://articulo.mercadolibre.cl/MLC-1444108857-clavo-corriente-de-3-pulgadas-paquete-de-1kg-_JM",
    "Ferresurdotu77": "https://articulo.mercadolibre.cl/MLC-1383795351-pino-seco-cepillado-2-x-2-x-320-mt-_JM",
    "Ferresurdotu78": "https://articulo.mercadolibre.cl/MLC-1665298580-abrazadera-conduit-abrazadera-omega-16mm-100-unidades-_JM",
    "Ferresurdotu82": "https://articulo.mercadolibre.cl/MLC-1326209133-tirafondo-hexagonal-14x1-12-pulgadas-100-unidades-_JM",
    "Ferresurdotu83": "https://articulo.mercadolibre.cl/MLC-1374157337-pellet-de-madera-premium-15kg-entrega-en-santiago-_JM",
    "Ferresurdotu84": "https://articulo.mercadolibre.cl/MLC-917729581-rodillo-para-pintar-hela-corta-gota-18-cm-_JM",
    "Ferresurdotu85": "https://articulo.mercadolibre.cl/MLC-1462012053-pack-3u-codo-sanitario-pvc-875-50-mm-gris-_JM",
    "Ferresurdotu86": "https://articulo.mercadolibre.cl/MLC-969597596-guante-cabritilla-sforro-_JM",
    "Ferresurdotu87": "https://articulo.mercadolibre.cl/MLC-1013012915-salida-caja-pvc-conduit-58-16mm-10-unidades-_JM",
    "Ferresurdotu89": "https://articulo.mercadolibre.cl/MLC-1840218848-terciado-estructural-pino-18-mm-122-244-para-retiro-_JM",
    "Ferresurdotu90": "https://articulo.mercadolibre.cl/MLC-621455265-salida-de-caja-p-conduit-20mm-pack-5-unidades--_JM",
    "Ferresurdotu92": "https://articulo.mercadolibre.cl/MLC-1407904597-terciado-estructural-pino-9-mm-122-244-para-retiro-_JM",
    "Ferresurdotu95": "https://articulo.mercadolibre.cl/MLC-1402987669-abrazadera-conduit-abrazadera-omega-20mm-50-unidades-_JM",
    "Ferresurdotu97": "https://www.mercadolibre.cl/pegamento-para-pvc-240-cc-tradicional-caplicador-vinilit/p/MLC32387483#wid=MLC2271993840",
    "Ferresurdotu98": "https://articulo.mercadolibre.cl/MLC-1053170634-plancha-yeso-carton-120x240x125mm-rf-resistente-fuego-k-_JM",
    "Ferresurdotu99": "https://articulo.mercadolibre.cl/MLC-1337884217-piso-terraza-deck-impregnado-1-12x4-en-320-metros-_JM",
    "Ferresurdotu100": "https://articulo.mercadolibre.cl/MLC-1133364954-terminal-ppr-polifusion-termofusion-20x12-he-gris-_JM",
    "Ferresurdotu103": "https://articulo.mercadolibre.cl/MLC-2308032420-codo-75-x-87-cgoma-sanitario-blanco-_JM",
    "Ferresurdotu105": "https://www.mercadolibre.cl/rodillo-chiporro-lizcal-7-18-cm/p/MLC27717159?pdp_filters=category:MLC180856#wid=MLC2065868480",
    "Ferresurdotu111": "https://articulo.mercadolibre.cl/MLC-993111848-tuberia-conduit-emt-20mmx10mmx3mts-iec-61386-21-certificada-_JM#position=3",
    "Ferresurdotu113": "https://articulo.mercadolibre.cl/MLC-1458718685-terciado-estructural-pino-15-mm-122-244-para-retiro-_JM",
    "Ferresurdotu114": "https://articulo.mercadolibre.cl/MLC-1270736318-fibrocemento-liso-4mm-120-240-para-retiro-_JM",
    "Ferresurdotu116": "https://articulo.mercadolibre.cl/MLC-1661075338-pino-seco-cepillado-1-x-5-x-320-mt-_JM",
    "Ferresurdotu120": "https://articulo.mercadolibre.cl/MLC-2123354898-plancha-zinc-alum-acanalada-035x851x3000-economica-az-80-_JM",
    "Ferresurdotu121": "https://articulo.mercadolibre.cl/MLC-993823203-diluyente-sintetico-bot-1-lt-quimica-universal-_JM",
    "Ferresurdotu124": "https://articulo.mercadolibre.cl/MLC-1396718065-adhesivo-pvc-tradicional-60cc-pomo-vinilit-_JM",
    "Ferresurdotu126": "https://articulo.mercadolibre.cl/MLC-1459204059-plancha-acanalada-zinc-alum-de-2000-x-850-x-035-_JM",
    "Ferresurdotu128": "https://articulo.mercadolibre.cl/MLC-977866505-tapa-tornillo-pvc-hidraulico-12-he-pvc-_JM",
    "Ferresurdotu131": "https://articulo.mercadolibre.cl/MLC-2216465398-adhesivo-porcelanato-da-polvo-saco-25kg-weber-_JM",
    "Ferresurdotu132": "https://articulo.mercadolibre.cl/MLC-1426988197-guante-multiflex-power-lite-steelpro-_JM",
    "Ferresurdotu133": "https://articulo.mercadolibre.cl/MLC-2123383698-diluyente-pxl-400-duco-1-lt-dideval-_JM",
    "Ferresurdotu134": "https://articulo.mercadolibre.cl/MLC-1270449263-fibrocemento-liso-6mm-120-240-para-retiro-_JM",
    "Ferresurdotu135": "https://articulo.mercadolibre.cl/MLC-1237023752-manguera-mallaflex-para-jardin-34-por-metro-_JM",
    "Ferresurdotu138": "https://articulo.mercadolibre.cl/MLC-1840218848-terciado-estructural-pino-18-mm-122-244-para-retiro-_JM",
    "Ferresurdotu140": "https://articulo.mercadolibre.cl/MLC-1362664443-osb-9mm-multiplac-122x244cm-lp-nacional-_JM",
    "Ferresurdotu141": "https://articulo.mercadolibre.cl/MLC-1049452344-cartucho-gas-butano-con-valvula-de-seguridad-190-yanes-_JM",
    "Ferresurdotu146": "https://articulo.mercadolibre.cl/MLC-1030231053-tee-20-mm-12-pvc-hidraulico-_JM",
    "Ferresurdotu149": "https://www.mercadolibre.cl/pasta-muro-interior-1-kilo-f-6-terminacion-blanca/p/MLC23604408?",
    "Ferresurdotu151": "https://articulo.mercadolibre.cl/MLC-1042064366-valvula-bola-12-stretto-_JM",
    "Ferresurdotu158": "https://articulo.mercadolibre.cl/MLC-1957670800-codo-sanitario-pvc-gris-110mm-x-45-fitting-_JM",
    "Ferresurdotu161": "https://articulo.mercadolibre.cl/MLC-1012441953-copla-pvc-gris-sanitario-110mm-_JM",
    "Ferresurdotu163": "https://www.mercadolibre.cl/serrucho-barracuda-550mm-22-bahco/p/MLC24750720",
    "Ferresurdotu164": "https://www.mercadolibre.cl/repuesto-hoja-de-cartonero-10-piezas-18x100mm-total/p/MLC25292713",
    "Ferresurdotu165": "https://www.mercadolibre.cl/electrodo-soldadura-krafter-e60111-kg-diametro-332-25-mm/p/MLC23884712?",
    "Ferresurdotu168": "https://articulo.mercadolibre.cl/MLC-1270590420-fibrocemento-liso-5mm-120-240-para-retiro-_JM",
    "Ferresurdotu170": "https://articulo.mercadolibre.cl/MLC-1531361800-punta-cruz-phillips-industrial-ph2x25mm-_JM",
    "Ferresurdotu172": "https://articulo.mercadolibre.cl/MLC-1143564178-llave-bola-jardin-lavadero-bronzzo-12-_JM",
    "Ferresurdotu176": "https://www.mercadolibre.cl/regulador-gas-cemco-cilindros-2-5-11-15kg-color-gris/p/MLC22858991",
    "Ferresurdotu178": "https://articulo.mercadolibre.cl/MLC-1459204059-plancha-acanalada-zinc-alum-de-2000-x-850-x-035-_JM",
    "Ferresurdotu179": "https://articulo.mercadolibre.cl/MLC-956876876-sifon-loa-1-12-1-14-salcurva-standard-hoffens-_JM",
    "Ferresurdotu181": "https://articulo.mercadolibre.cl/MLC-1351964047-tapa-asiento-para-bano-wc-blanca-universal-fanaloza-_JM",
    "Ferresurdotu182": "https://articulo.mercadolibre.cl/MLC-1461018979-pasta-muro-interior-tajamar-f-15-blanca-15-kilos-_JM",
    "Ferresurdotu183": "https://articulo.mercadolibre.cl/MLC-1053177015-plancha-yeso-carton-120-x-240-x-10-mm-knauf-volcanita-_JM",
    "Ferresurdotu186": "https://articulo.mercadolibre.cl/MLC-1250083539-esmalte-al-agua-blanco-semibrillo-1-gl-_JM",
    "Ferresurdotu188": "https://articulo.mercadolibre.cl/MLC-939557102-silicona-bano-cocina-agorex-700-300ml-blanca-_JM",
    "Ferresurdotu189": "https://articulo.mercadolibre.cl/MLC-1331426079-clavo-corriente-2-12-x-11-bwg-caja-1-kg-_JM",
    "Ferresurdotu191": "https://articulo.mercadolibre.cl/MLC-1531430492-pila-d-grande-duracell-_JM",
    "Ferresurdotu195": "https://articulo.mercadolibre.cl/MLC-1026738000-guante-steelpro-multiflex-power-lite-_JM",
    "Ferresurdotu201": "https://www.mercadolibre.cl/electrodo-soldadura-6011-18-1kg-indura/p/MLC29818521?pdp_filters=category:MLC414387",
    "Ferresurdotu202": "https://articulo.mercadolibre.cl/MLC-1368806837-plancha-zincalum-lisa-04-mm-3x1-_JM",
    "Ferresurdotu207": "https://articulo.mercadolibre.cl/MLC-1305523602-electrodo-e-6011-18-32mm-1-kg-krafter-_JM",
    "Ferresurdotu209": "https://articulo.mercadolibre.cl/MLC-999436736-enchufe-macho-volante-10a-250vac-negro-fanton-_JM",
    "Ferresurdotu210": "https://articulo.mercadolibre.cl/MLC-2160078350-plancha-zinc-5v-035x895x3000-az80-_JM",
    "Ferresurdotu212": "https://www.mercadolibre.cl/tornillo-turbo-torx-1460x10060-caja-de-100u-tuhaus/p/MLC34060934",
    "Ferresurdotu213": "https://articulo.mercadolibre.cl/MLC-1891430118-tubo-pvc-sanitario-gris-110mm-x-6m-_JM",
    "Ferresurdotu215": "https://www.mercadolibre.cl/tornillo-turbo-146-x-8060-x-100-und/p/MLC28897942",
    "Ferresurdotu216": "https://articulo.mercadolibre.cl/MLC-1382128013-tubo-pvc-presion-azul-20mm-pn-16-x-1mt-hoffens-ferrepernos-_JM",
    "Ferresurdotu219": "https://articulo.mercadolibre.cl/MLC-1416150781-tubo-pvc-hidraulico-32mm-x-6m-_JM",
    "Ferresurdotu221": "https://articulo.mercadolibre.cl/MLC-2188014458-saco-tipo-papero-rojo-50-kilos-x-100-unid-60x90cm-qrubber-_JM",
    "Ferresurdotu223": "https://articulo.mercadolibre.cl/MLC-2134969996-tubo-pvc-hidraulico-25mm-x-6m-_JM",
    "Ferresurdotu224": "https://articulo.mercadolibre.cl/MLC-1268894299-pino-bruto-seco-2x3x32-mts-_JM",
    "Ferresurdotu227": "https://articulo.mercadolibre.cl/MLC-992480568-tornillo-6x1-14-crs-zincado-rosca-gruesa-x-100-unidades-_JM",
    "Ferresurdotu229": "https://articulo.mercadolibre.cl/MLC-1041506272-electrodo-soldadura-e7018-18-32mm-1-kg-_JM",
    "Ferresurdotu230": "https://articulo.mercadolibre.cl/MLC-1661088024-pino-seco-cepillado-2-x-5-x-320-mt-_JM",
    "Ferresurdotu233": "https://articulo.mercadolibre.cl/MLC-1331904191-clavo-corriente-2-x-12-bwgcaja-1-kg-_JM",
    "Ferresurdotu236": "https://www.mercadolibre.cl/llave-paso-gas-12-hi-he-stretto/p/MLC28906026",
    "Ferresurdotu239": "https://articulo.mercadolibre.cl/MLC-2156037452-llave-bola-jardin-lavadero-34-_JM",
    "Ferresurdotu241": "https://sodimac.falabella.com/sodimac-cl/product/110248401/Sifon-plastico-1-1-4-x1-1-2-/110248405",
    "Ferresurdotu243": "https://articulo.mercadolibre.cl/MLC-1015801962-pasta-muro-interior-f-15-1-galon-tajamar-_JM",
    "Ferresurdotu250": "https://articulo.mercadolibre.cl/MLC-1320638657-guante-steelpro-multiflex-power-lite-_JM",
    "Ferresurdotu251": "https://articulo.mercadolibre.cl/MLC-1042654457-galon-oleo-brillante-pinta-facil-tajamar-ferrepernos-_JM",
    "Ferresurdotu252": "https://articulo.mercadolibre.cl/MLC-1076026717-cinta-de-embalaje-transparente-marca-3m-_JM",
    "Ferresurdotu254": "https://articulo.mercadolibre.cl/MLC-1320644625-lente-de-seguridad-us-eagle-tech-plus-gris-as-_JM",
    "Ferresurdotu255": "https://articulo.mercadolibre.cl/MLC-2273299544-malla-acma-c92-5x26-_JM",
    "Ferresurdotu256": "https://articulo.mercadolibre.cl/MLC-1180188129-flexible-hi-hi-12-40-cms-agua-caliente-y-fria-_JM",
    "Ferresurdotu257": "https://articulo.mercadolibre.cl/MLC-1368090789-ampolleta-wellmax-led-11w-e27-sec-luz-fria-6500k-premium-_JM",
    "Ferresurdotu258": "https://articulo.mercadolibre.cl/MLC-1741655614-electrodo-soldadura-6011-332-1kg-indura-punto-azul-_JM",
    "Ferresurdotu259": "https://www.mercadolibre.cl/huincha-de-medir-5-metros-x-25mm-knight-doble-cara/p/MLC23884511",
    "Ferresurdotu266": "https://articulo.mercadolibre.cl/MLC-950769429-latex-extracubriente-blanco-galon-pinturasonlinecl-_JM",
    "Ferresurdotu267": "https://articulo.mercadolibre.cl/MLC-1606294588-esmalte-sintetico-tajamar-litro-_JM",
    "Ferresurdotu269": "https://articulo.mercadolibre.cl/MLC-2285253364-guante-multiprotect-flex-l-1700-force-talla-9-_JM",
    "Ferresurdotu270": "https://articulo.mercadolibre.cl/MLC-2240610152-electrodo-7018-18-indura-1-kilo-_JM",
    "Ferresurdotu271": "https://articulo.mercadolibre.cl/MLC-1053157964-plancha-alistonado-fibrocemento-1200x2400x60mm-_JM",
    "Ferresurdotu272": "https://articulo.mercadolibre.cl/MLC-1459369094-pegamento-adhesivo-de-contacto-multiuso-agorex-60-120-ml-_JM",
    "Ferresurdotu274": "https://articulo.mercadolibre.cl/MLC-2273930364-yeso-carton-standard-borde-rebajado-15mm-120x240-cm-_JM",
    "Ferresurdotu275": "https://articulo.mercadolibre.cl/MLC-937134347-kit-flexible-12-x-30-cm-con-llave-angular-de-paso-_JM",
    "Ferresurdotu276": "https://articulo.mercadolibre.cl/MLC-535759721-jgo-fitting-wc-silencioso-fanalozafas-_JM",
    "Ferresurdotu277": "https://www.mercadolibre.cl/pila-duracell-aaa/p/MLC21204961",
    "Ferresurdotu278": "https://articulo.mercadolibre.cl/MLC-519611969-vitrolux-63-vitrificante-para-piso-interior-brillante-nat-_JM",
    "Ferresurdotu279": "https://articulo.mercadolibre.cl/MLC-1401679097-soquete-portalampara-de-loza-conector-rosca-e27-250v-4a-sec-_JM",
    "Ferresurdotu280": "https://articulo.mercadolibre.cl/MLC-2212283972-punta-corriente-2-pulgadas-1-kilo-_JM",
    "Ferresurdotu281": "https://articulo.mercadolibre.cl/MLC-912958615-acrizinc-pintura-galon-colores-de-cartilla-pinturasonlinecl-_JM",
    "Ferresurdotu284": "https://articulo.mercadolibre.cl/MLC-2001116942-interruptor-simple-912-blanco-genesis-schneider-electric-_JM",
    "Ferresurdotu285": "https://articulo.mercadolibre.cl/MLC-2106663412-policarbonato-ondulado-081x30mts-05mm-transparente-dvp-_JM",
    "Ferresurdotu286": "https://articulo.mercadolibre.cl/MLC-2209249860-rodillo-espuma-poliester-7cm-hela-_JM",
    "Ferresurdotu287": "https://articulo.mercadolibre.cl/MLC-1977119918-esmalte-al-agua-iris-galon-varios-colores-_JM",
    "Ferresurdotu290": "https://articulo.mercadolibre.cl/MLC-536968005-disco-lija-flap-para-madera-115mm-60-uyu-pack-5-unidades-_JM",
    "Ferresurdotu291": "https://articulo.mercadolibre.cl/MLC-1416562777-tapagoteras-agorex-gris-cartucho-440-gramos-_JM",
    "Ferresurdotu292": "https://articulo.mercadolibre.cl/MLC-920299804-flexible-agua-metalico-m10-x-hi-12-40cm-_JM",
    "Ferresurdotu293": "https://articulo.mercadolibre.cl/MLC-1291196574-flexible-de-gas-12hi-x-38hi-iz-1mt-para-regulador-_JM",
    "Ferresurdotu294": "https://articulo.mercadolibre.cl/MLC-1443313543-pasta-muro-exterior-a-1-tajamar-terminacion-blanca-bolsa-1kg-_JM",
    "Ferresurdotu295": "https://articulo.mercadolibre.cl/MLC-1460493193-piso-flotante-aspen-191x1200-mm-_JM",
    "Ferresurdotu297": "https://articulo.mercadolibre.cl/MLC-1017552647-tomacorriente-triple-2p-tierra-10a-250v-certificacion-sec-_JM",
    "Ferresurdotu298": "https://www.mercadolibre.cl/rodillo-chiporro-lizcal-5-12-cm/p/MLC27503475",
    "Ferresurdotu299": "https://articulo.mercadolibre.cl/MLC-1798432182-clavos-corrientes-4-x-caja-25kg-bighouse-_JM",
    "Ferresurdotu300": "https://articulo.mercadolibre.cl/MLC-2193317390-electrodo-soldadura-krafter-e7018-diam-332-24mm-1-kg-_JM",
    "Ferresurdotu302": "https://articulo.mercadolibre.cl/MLC-980923198-display-soldadura-estano-50-1-mt-pasta-soldar-10-gr-_JM",
    "Ferresurdotu303": "https://articulo.mercadolibre.cl/MLC-2303917968-flexible-agua-calefont-hi-hi-25-cms-_JM",
    "Ferresurdotu304": "https://articulo.mercadolibre.cl/MLC-1464478867-tapa-ciega-placa-genesis-7424-color-blanco-pack-5-unidades-_JM",
    "Ferresurdotu305": "https://articulo.mercadolibre.cl/MLC-476301275-latex-al-agua-extracubriente-sipa-blanco-pinturasonlinecl-_JM",
    "Ferresurdotu306": "https://articulo.mercadolibre.cl/MLC-1058005425-lapiz-carpintero-ovalado-madera-albanil-construccion-12-pcs-_JM",
    "Ferresurdotu307": "https://articulo.mercadolibre.cl/MLC-536042053-kit-instalacion-wc-sello-flexibles-etc-_JM",
    "Ferresurdotu308": "https://articulo.mercadolibre.cl/MLC-1861612260-latex-antihongos-fast-colores-galon-_JM",
    "Ferresurdotu309": "https://articulo.mercadolibre.cl/MLC-1193739556-rodillo-pintar-chiporro-natural-18cm-pelo-largo-_JM",
    "Ferresurdotu311": "https://articulo.mercadolibre.cl/MLC-1423271109-cobertor-para-piscina-rectangular-39-m-x-18-m-intex-azul-_JM",
    "Ferresurdotu313": "https://articulo.mercadolibre.cl/MLC-1053151643-plancha-yeso-carton-120-x-240-x125-mm-_JM",
    "Ferresurdotu314": "https://articulo.mercadolibre.cl/MLC-473703457-rodillo-hela-110mm-espuma-poliester-alta-densidad-hela-_JM",
    "Ferresurdotu316": "https://articulo.mercadolibre.cl/MLC-1031050273-abrazadera-caddy-cd-zincada-20mm-pack-10-unidades-_JM",
    "Ferresurdotu318": "https://articulo.mercadolibre.cl/MLC-971114232-esmalte-al-agua-semibrillo-pintamax-1-gl-perla-revor-_JM",
    "Ferresurdotu320": "https://articulo.mercadolibre.cl/MLC-1819672784-caneria-de-cobre-12-tipo-m-para-agua-3mt-_JM",
    "Ferresurdotu321": "https://articulo.mercadolibre.cl/MLC-1430803589-2-barras-de-soldadura-plata-en-varilla-al-15-_JM",
    "Ferresurdotu322": "https://www.mercadolibre.cl/barniz-vitrificante-poliuretano-sipa-1-litro-secado-rapido/p/MLC22940194",
    "Ferresurdotu324": "https://articulo.mercadolibre.cl/MLC-1048811740-buzo-desechable-blanco-dupont-tyvek-original-txl-y-xxl-_JM",
    "Ferresurdotu325": "https://articulo.mercadolibre.cl/MLC-1674748992-esmalte-al-agua-sipa-satinado-tecno-blanco-5gl-_JM",
    "Ferresurdotu326": "https://articulo.mercadolibre.cl/MLC-2303971628-flexible-hi-hi-12-50-cms-agua-_JM",
    "Ferresurdotu328": "https://articulo.mercadolibre.cl/MLC-1405715505-caneria-de-cobre-12-tipo-l-para-gas-3mt-_JM",
    "Ferresurdotu329": "https://articulo.mercadolibre.cl/MLC-1621476608-soldadura-estano-50-1-mt-_JM",
    "Ferresurdotu327": "https://www.mercadolibre.cl/aceite-mezcla-stihl-500-cc/p/MLC28322722",
    "Ferresurdotu332": "https://articulo.mercadolibre.cl/MLC-953829623-soldadura-indepp-estano-50-carrete-500-gr-_JM",
    "Ferresurdotu333": "https://www.mercadolibre.cl/cerradura-cilindrica-odis-201-dormitorio-inox-35-55blister/p/MLC28904395",
    "Ferresurdotu337": "https://articulo.mercadolibre.cl/MLC-1270590441-fibrocemento-liso-8mm-120-240-para-retiro-_JM",
    "Ferresurdotu338": "https://articulo.mercadolibre.cl/MLC-580695053-pack-2-flexible-agua-he-hi-m10-largo-x1-x-12-35-cm-_JM",
    "Ferresurdotu339": "https://www.mercadolibre.cl/disco-sierra-circular-7-14-x-24-truper-st-724-ferrenet-color-acero/p/MLC22516859",
    "Ferresurdotu340": "https://www.mercadolibre.cl/disco-sierra-714-x-24-dientes-makita-widia/p/MLC22735094",
    "Ferresurdotu341": "https://articulo.mercadolibre.cl/MLC-1382540686-masking-tape-18-mm-x-40-mt-_JM",
    "Ferresurdotu345": "https://articulo.mercadolibre.cl/MLC-1395057423-silicona-sellatodo-universal-1100-transparente-300ml-agorex-_JM",
    "Ferresurdotu346": "https://articulo.mercadolibre.cl/MLC-1683160460-cola-fria-madera-pritt-pegafix-225gr-_JM",
    "Ferresurdotu349": "https://articulo.mercadolibre.cl/MLC-912958615-acrizinc-pintura-galon-colores-de-cartilla-pinturasonlinecl-_JM",
    "Ferresurdotu350": "https://articulo.mercadolibre.cl/MLC-912958615-acrizinc-pintura-galon-colores-de-cartilla-pinturasonlinecl-_JM",
    "Ferresurdotu351": "https://articulo.mercadolibre.cl/MLC-2218265496-malla-eco-sol-tipo-5014-rollo-150-x-25-metros-inchalam-_JM",
    "Ferresurdotu352": "https://articulo.mercadolibre.cl/MLC-1124562945-malla-cg-5050-de-2-x-1-10-usos-varios-_JM",
    "Ferresurdotu353": "https://sodimac.falabella.com/sodimac-cl/product/110298802/2.60-x-5m.-Malla-Acma-C-139-Sin-economia-de-borde/110298816",
    "Ferresurdotu354": "https://articulo.mercadolibre.cl/MLC-1048124204-malla-cerco-1-g-x-38-de-185-x-3-mts-_JM",
    "Ferresurdotu355": "https://articulo.mercadolibre.cl/MLC-532658738-monomando-ducha-tina-mixa-mallorca-_JM",
    "Ferresurdotu357": "https://articulo.mercadolibre.cl/MLC-1021958515-remaches-pop-de-4-x-10-mm-100-unidades-_JM",
    "Ferresurdotu361": "https://www.mercadolibre.cl/regulador-gas-cemco-cilindro-45kg-j-ravera-color-plateado/p/MLC32086159",
    "Ferresurdotu364": "https://articulo.mercadolibre.cl/MLC-1467168707-llave-lavatorio-eco-miami-_JM",
    "Ferresurdotu365": "https://articulo.mercadolibre.cl/MLC-2109843250-hoffens-desague-1-12-lavap-ccola-_JM",
    "Ferresurdotu367": "https://www.mercadolibre.cl/desague-tina-1-12-con-rebalse-y-sifon-plastico/p/MLC28956490",
    "Ferresurdotu368": "https://articulo.mercadolibre.cl/MLC-541120185-combinacion-lavaplatos-isabella-plumber-_JM",
    "Ferresurdotu369": "https://www.mercadolibre.cl/foco-proyector-led-telco-flat-50w-megabright-color-de-la-carcasa-negro-color-de-la-luz-blanco-frio/p/MLC22198217",
    "Ferresurdotu371": "https://articulo.mercadolibre.cl/MLC-950589641-panel-led-circular-empotrado-18w-luz-blanco-neutro-_JM",
    "Ferresurdotu378": "https://www.mercadolibre.cl/enchufe-hembra-2pt-10a-250v-fanton-negro/p/MLC32052684",
    "Ferresurdotu380": "https://articulo.mercadolibre.cl/MLC-992566544-adaptador-macho-enchufe-americano-2p-_JM",
    "Ferresurdotu384": "https://articulo.mercadolibre.cl/MLC-2162682418-esmalte-al-agua-pieza-y-fachada-galon-blanco-ceresita-_JM",
    "Ferresurdotu386": "https://articulo.mercadolibre.cl/MLC-971172390-latex-pintamax-1-gl-blanco-lino-revor-_JM",
    "Ferresurdotu388": "https://articulo.mercadolibre.cl/MLC-1606294588-esmalte-sintetico-tajamar-litro-_JM",
    "Ferresurdotu389": "https://articulo.mercadolibre.cl/MLC-1375685683-esmalte-sintetico-tajamar-galon-_JM",
    "Ferresurdotu392": "https://articulo.mercadolibre.cl/MLC-1425951167-esmalte-sintetico-brillante-14-gl-negro-tricolor-_JM",
    "Ferresurdotu393": "https://articulo.mercadolibre.cl/MLC-1354608598-oleo-opaco-profesional-tricolor-blanco-galon-_JM",
    "Ferresurdotu394": "https://www.mercadolibre.cl/removedor-de-pintura-1lt-quimica-universal/p/MLC27916120",
    "Ferresurdotu397": "https://articulo.mercadolibre.cl/MLC-2053541710-cerestain-1gl-castano-ceresita-protector-de-madera-_JM",
    "Ferresurdotu399": "https://articulo.mercadolibre.cl/MLC-2109766028-tricolor-pintura-spray-blanco-_JM",
    "Ferresurdotu400": "https://articulo.mercadolibre.cl/MLC-2109766028-tricolor-pintura-spray-blanco-_JM",
    "Ferresurdotu401": "https://articulo.mercadolibre.cl/MLC-1565651350-spray-esmalte-acrilico-negro-sr-400ml-passol-mimbral-_JM",
    "Ferresurdotu402": "https://articulo.mercadolibre.cl/MLC-1565651350-spray-esmalte-acrilico-negro-sr-400ml-passol-mimbral-_JM",
    "Ferresurdotu404": "https://articulo.mercadolibre.cl/MLC-1386889037-candado-oister-e20-20mm-oister-serie-e-_JM",
    "Ferresurdotu406": "https://articulo.mercadolibre.cl/MLC-1809812036-buzo-desechable-blanco-tipo-tyvek-topsafe-_JM",
    "Ferresurdotu408": "https://articulo.mercadolibre.cl/MLC-1053183416-plancha-yeso-carton-120x240x15mm-rh-resistente-humedad-_JM",
    "Ferresurdotu409": "https://articulo.mercadolibre.cl/MLC-1775533686-piso-flotante-efloor-8mm-roble-montana-mod-1003094631-_JM",
    "Ferresurdotu411": "https://www.mercadolibre.cl/gas-doite-230-grs-pro-gas-camping/p/MLC23421637",
    "Ferresurdotu412": "https://articulo.mercadolibre.cl/MLC-1565651350-spray-esmalte-acrilico-negro-sr-400ml-passol-mimbral-_JM",
    "Ferresurdotu413": "https://articulo.mercadolibre.cl/MLC-1565651350-spray-esmalte-acrilico-negro-sr-400ml-passol-mimbral-_JM",
    "Ferresurdotu414": "https://articulo.mercadolibre.cl/MLC-2031752158-rodillo-chiporro-sintetico-ancho-18-cms-valprik-_JM",
    "Ferresurdotu416": "https://articulo.mercadolibre.cl/MLC-1307976286-combinacion-lavaplatos-standard-cc7-1001-fas-jravera-_JM",
    "Ferresurdotu418": "https://articulo.mercadolibre.cl/MLC-956876910-desague-1-14-lavatorio-con-rebalse-y-cola-hoffens-_JM",
    "Ferresurdotu419": "https://articulo.mercadolibre.cl/MLC-993439548-cinta-aislante-huincha-aisladora-3m-temflex-1500-18mmx10m-_JM",
    "Ferresurdotu421": "https://articulo.mercadolibre.cl/MLC-1395035025-silicona-sellatodo-universal-1100-negra-300ml-agorex-_JM",
    "Ferresurdotu423": "https://www.mercadolibre.cl/enchufe-doble-10a-emb-marisio-ngenesis-blanco-n0327036/p/MLC24336256",
    "Ferresurdotu425": "https://www.mercadolibre.cl/candado-oister-xtra-30mm/p/MLC28726235",
    "Ferresurdotu426": "https://articulo.mercadolibre.cl/MLC-978256527-candado-de-bronce-pulido-40mm-lioi-_JM",
    "Ferresurdotu427": "https://articulo.mercadolibre.cl/MLC-2256814570-flexible-hi-he-12-25-cms-agua-caliente-y-fria-_JM",
    "Ferresurdotu429": "https://www.mercadolibre.cl/candado-odis-b40-40mm/p/MLC28329304",
    "Ferresurdotu430": "https://www.mercadolibre.cl/grapas-516-x-1000un-et-50-truper-ferrenet/p/MLC24404402",
    "Ferresurdotu431": "https://articulo.mercadolibre.cl/MLC-952883503-mascarilla-3m-n95-8210v-nueva-1-unidad-_JM",
    "Ferresurdotu433": "https://articulo.mercadolibre.cl/MLC-554416589-candado-oister-de-fierro-40mm-_JM",
    "Ferresurdotu435": "https://www.mercadolibre.cl/enchufe-hembra-2pt-10a-250v-fanton-negro/p/MLC32052684",
    "Ferresurdotu436": "https://articulo.mercadolibre.cl/MLC-936399392-barniz-marino-sipa-galon-pinturasonlinecl-_JM",
    "Ferresurdotu437": "https://www.mercadolibre.cl/cerestain-roble-galon-ceresita-11380201-color-marron/p/MLC28746285",
    "Ferresurdotu438": "https://articulo.mercadolibre.cl/MLC-1419426195-carbolineo-1-galon-37-lts-prox-_JM",
    "Ferresurdotu443": "https://www.mercadolibre.cl/eslinga-de-amarre-5-mts-limite-de-carga-800-kg-con-rachet/p/MLC28962467",
    "Ferresurdotu444": "https://articulo.mercadolibre.cl/MLC-641944212-ampolleta-wellmax-11-watts-1000lm-certificada-sec-e27-11w-_JM",
    "Ferresurdotu446": "https://articulo.mercadolibre.cl/MLC-965060987-desague-lavamanoslavatorio-1-14-fas-_JM",
    "Ferresurdotu447": "https://articulo.mercadolibre.cl/MLC-956322262-hisopo-2-para-caldera-marca-hela-_JM",
    "Ferresurdotu448": "https://articulo.mercadolibre.cl/MLC-1354814850-esmalte-sintetico-tricolor-profesional-blanco-gln-_JM",
    "Ferresurdotu449": "https://articulo.mercadolibre.cl/MLC-972696716-pala-punta-de-huevo-mango-metalico-lioi-_JM",
    "Ferresurdotu451": "https://articulo.mercadolibre.cl/MLC-993841106-diluyente-sintetico-bidon-5-lt-quimica-universal-_JM",
    "Ferresurdotu452": "https://articulo.mercadolibre.cl/MLC-540716507-desague-para-tina-1-12-con-rebalse-_JM",
    "Ferresurdotu453": "https://articulo.mercadolibre.cl/MLC-1565651350-spray-esmalte-acrilico-negro-sr-400ml-passol-mimbral-_JM",
    "Ferresurdotu454": "https://www.mercadolibre.cl/esmeril-angular-4-12-600w-krafter-hdd452-color-negro/p/MLC34277806",
    "Ferresurdotu455": "https://www.mercadolibre.cl/proyector-de-area-led-30w-smd-4500k-mega-color-de-la-carcasa-negro/p/MLC21025411",
    "Ferresurdotu456": "https://articulo.mercadolibre.cl/MLC-1424597140-interruptor-simple-912-de-sobreponer-16-a-md274275-_JM",
    "Ferresurdotu457": "https://articulo.mercadolibre.cl/MLC-1442895643-hilo-albanil-lienza-carpintera-100m-uyustools-_JM",
    "Ferresurdotu458": "https://articulo.mercadolibre.cl/MLC-580331818-enchufe-industrial-macho-volante-16a-amp-2pt-220v-ip44-_JM",
    "Ferresurdotu459": "https://articulo.mercadolibre.cl/MLC-2295782454-carretilla-estandar-90-lt-azul-rueda-pantanera-350x8-lioi-_JM",
    "Ferresurdotu460": "https://articulo.mercadolibre.cl/MLC-1431885133-camara-pretul-truper-pneumatico-rueda-carretilla-_JM",
    "Ferresurdotu461": "https://www.mercadolibre.cl/panel-led-sobrepuesto-redondo-12w-6000k-vkb-ferremax-color-blanco/p/MLC29088337",
    "Ferresurdotu464": "https://articulo.mercadolibre.cl/MLC-1119373759-enchufe-macho-convert-2p-negro-mec-_JM",
    "Ferresurdotu466": "https://articulo.mercadolibre.cl/MLC-1467747663-eslinga-de-amarre-25mts-limite-de-carga-200-kg-con-hebilla-_JM",
    "Ferresurdotu467": "https://articulo.mercadolibre.cl/MLC-1431957039-grapa-truper-38-pulgadas-et-50-38-caja-1000-pzas-_JM",
    "Ferresurdotu469": "https://articulo.mercadolibre.cl/MLC-1441842403-cloro-para-piscina-5ltrs-_JM",
    "Ferresurdotu472": "https://articulo.mercadolibre.cl/MLC-1442464789-hilo-albanil-lienza-carpintera-50m-uyustools-_JM",
    "Ferresurdotu474": "https://articulo.mercadolibre.cl/MLC-1453547379-serrucho-de-mano-profesional-bahco-600mm-2500-24-xt7-hp-ergo-_JM",
    "Ferresurdotu475": "https://articulo.mercadolibre.cl/MLC-1464480385-balde-concretero-12-lt-_JM",
    "Ferresurdotu476": "https://www.mercadolibre.cl/huincha-medir-75mt-knightmimbral/p/MLC24102816",
    "Ferresurdotu477": "https://articulo.mercadolibre.cl/MLC-1809810712-escobilla-acero-5-filas-mango-madera-uyustools-_JM",
    "Ferresurdotu478": "https://articulo.mercadolibre.cl/MLC-2109830604-espatula-hela-hela-espatula-york-50-mm-_JM",
    "Ferresurdotu480": "https://articulo.mercadolibre.cl/MLC-985104374-barre-hojas-truper-22dtes-cmango-cod-em-22-_JM",
    "Ferresurdotu481": "https://articulo.mercadolibre.cl/MLC-1448195355-cloro-piscina-tableta-triple-accion-1-kg-pote-5-unid-dideval-_JM",
    "Ferresurdotu482": "https://articulo.mercadolibre.cl/MLC-985104374-barre-hojas-truper-22dtes-cmango-cod-em-22-_JM",
    "Ferresurdotu483": "https://articulo.mercadolibre.cl/MLC-574417800-esmeril-angular-4-12-700w-dewalt-dwe4010-env-gratis-_JM",
    "Ferresurdotu484": "https://www.mercadolibre.cl/huincha-de-medir-kinight-10mx25mm/p/MLC24258196",
    "Ferresurdotu486": "https://articulo.mercadolibre.cl/MLC-1032669138-monomando-lavamanos-almagro-afj-_JM",
    "Ferresurdotu487": "https://articulo.mercadolibre.cl/MLC-1032669138-monomando-lavamanos-almagro-afj-_JM",
    "Ferresurdotu488": "https://articulo.mercadolibre.cl/MLC-1030888622-barrehojas-22dtes-plast-con-mango-ep-22r-truper-mimbral-_JM",
    "Ferresurdotu489": "https://www.mercadolibre.cl/tineta-pintura-soquina-latex-constructor-blanco/p/MLC27233882",
    "Ferresurdotu490": "https://www.mercadolibre.cl/tijera-para-podar-8-curva-truper/p/MLC27511032#wid=MLC1444611599",
    "Ferresurdotu492": "https://www.mercadolibre.cl/tijera-para-cortar-pasto-10-t-17-truper-color-cafe/p/MLC23843378#wid=MLC2113979050",
    "Ferresurdotu493": "https://articulo.mercadolibre.cl/MLC-1465662642-esmalte-al-agua-satinado-fachada-1gln-blanco-nacar-tricolor-_JM",
    "Ferresurdotu494": "https://articulo.mercadolibre.cl/MLC-1438687847-puerta-terciado-45cm-x-80-cm-x-2-mt-_JM",
    "Ferresurdotu495": "https://articulo.mercadolibre.cl/MLC-554194122-cola-fria-agorex-profesional-pote-1kg-_JM",
    "Ferresurdotu496": "https://articulo.mercadolibre.cl/MLC-493335596-caja-estanca-pvc-100x100x70mm-6-conos-conexion-electrica-_JM",
    "Ferresurdotu499": "https://articulo.mercadolibre.cl/MLC-1009851220-enchufe-macho-3p-convertible-_JM",
    "Ferresurdotu500": "https://articulo.mercadolibre.cl/MLC-1713948806-interruptor-volante-paso-clasico-pera-6a-castillo-95-blanco-_JM",
    "Ferresurdotu501": "https://articulo.mercadolibre.cl/MLC-497193647-galon-cerestain-protector-de-madera-caoba-pinturasonlinecl-_JM",
    "Ferresurdotu503": "https://www.mercadolibre.cl/enchufe-triple-2pt-10a-250v-blanco-emb-bticino-1308bn/p/MLC28969145",
    "Ferresurdotu504": "https://articulo.mercadolibre.cl/MLC-1827465120-esmalte-al-agua-iris-semi-brillo-lavable-colores-galon-_JM",
    "Ferresurdotu505": "https://articulo.mercadolibre.cl/MLC-1853602572-latex-acrilico-tajamar-galon-colores-_JM",
    "Ferresurdotu507": "https://articulo.mercadolibre.cl/MLC-1914540168-combinacion-lavaplato-al-muro-fas-cc8-1001-_JM",
    "Ferresurdotu508": "https://articulo.mercadolibre.cl/MLC-1346566605-monomando-ducha-linea-galia-plus-_JM",
    "Ferresurdotu509": "https://articulo.mercadolibre.cl/MLC-979489267-corta-carton-cartonero-exacto-cuchillo-marca-truper-cut-6x-_JM",
    "Ferresurdotu510": "https://articulo.mercadolibre.cl/MLC-1036369655-enchufe-hembra-volante-negro-10a-250v-1500w-2pt-sec-_JM",
    "Ferresurdotu511": "https://articulo.mercadolibre.cl/MLC-948726231-enchufe-hembra-doble-embutido-10a-negro-rema-_JM",
    "Ferresurdotu513": "https://articulo.mercadolibre.cl/MLC-2240610152-electrodo-7018-18-indura-1-kilo-_JM",
    "Ferresurdotu514": "https://articulo.mercadolibre.cl/MLC-2109766028-tricolor-pintura-spray-blanco-_JM",
    "Ferresurdotu516": "https://articulo.mercadolibre.cl/MLC-640710404-desague-receptaculo-cromado-1-14-con-rebalse-_JM",
    "Ferresurdotu518": "https://articulo.mercadolibre.cl/MLC-2216439488-huincha-aisladora-34x30mx20mi-autofundente-3m-_JM",
    "Ferresurdotu519": "https://articulo.mercadolibre.cl/MLC-902422526-alambre-mig-flux-para-soldar-sin-gas-rollo-08-de-1-kilo-_JM",
    "Ferresurdotu520": "https://articulo.mercadolibre.cl/MLC-1400285715-remache-tipo-pop-4x8-100-unidades-_JM",
    "Ferresurdotu521": "https://articulo.mercadolibre.cl/MLC-1461301029-cartucho-filtro-piscina-tipo-a-intex-29000-_JM",
    "Ferresurdotu523": "https://articulo.mercadolibre.cl/MLC-1565651350-spray-esmalte-acrilico-negro-sr-400ml-passol-mimbral-_JM",
    "Ferresurdotu524": "https://www.mercadolibre.cl/candado-odis-b50-gancho-largo-54mm-50mm-serie-",
    "Ferresurdotu525": "https://articulo.mercadolibre.cl/MLC-1311141650-overol-tipo-piloto-tela-poplin-_JM",
    "Ferresurdotu526": "https://www.mercadolibre.cl/disco-sierra-pmadera-714-40-dientes-truper/p/MLC22607231?",
    "Ferresurdotu527": "https://www.mercadolibre.cl/soplete-a-gas-yanes-cmetal-cpiezo-prof-400p/p/MLC26694544?",
    "Ferresurdotu531": "https://articulo.mercadolibre.cl/MLC-2240603924-pintura-alta-temperatura-aerosol-specialty-_JM",
    "Ferresurdotu533": "https://www.mercadolibre.cl/candado-odis-b60-60mm-serie-b/p/MLC22619866",
    "Ferresurdotu536": "https://articulo.mercadolibre.cl/MLC-1027456961-alargador-5-mts-5-posicion-con-usb-negrogris-mec-mimbral-_JM",
    "Ferresurdotu539": "https://www.mercadolibre.cl/soplete-a-gas-yanes-cpiezo-prof-4001k/p/MLC27454271",
    "Ferresurdotu540": "https://articulo.mercadolibre.cl/MLC-1042654457-galon-oleo-brillante-pinta-facil-tajamar-ferrepernos-_JM",
    "Ferresurdotu541": "https://articulo.mercadolibre.cl/MLC-1352956534-spray-tricolor-pintura-metalizada-aluminio-485-ml-_JM",
    "Ferresurdotu542": "https://articulo.mercadolibre.cl/MLC-1759340206-calefon-gas-licuado-7-litros-tiro-natural-splendid-ionizado-_JM",
    "Ferresurdotu543": "https://www.mercadolibre.cl/martillo-carpintero-mango-fibra-20-oz-bahco-428f-20/p/MLC24751352?",
    "Ferresurdotu544": "https://articulo.mercadolibre.cl/MLC-1072526828-martillo-carpintero-una-curva-truper-16oz-mango-fibra-_JM",
    "Ferresurdotu546": "https://www.mercadolibre.cl/disco-de-sierra-circular-pmad-714in180-mm-para-78-222-mm-40d/p/MLC22625018",
    "Ferresurdotu547": "https://articulo.mercadolibre.cl/MLC-1096330952-rueda-carretilla-pantanera-350x8-llanta-naranja-_JM",
    "Ferresurdotu548": "https://articulo.mercadolibre.cl/MLC-594395931-cable-alargador-simple-lexo-10a-2p-10mts-naranjo-_JM",
    "Ferresurdotu549": "https://articulo.mercadolibre.cl/MLC-995367828-alargador-multiple-gris-6-tomas-cled-5mts-_JM",
    "Ferresurdotu551": "https://articulo.mercadolibre.cl/MLC-581811559-serrucho-truper-podar-16-cgancho-3-filos-stp-16x-_JM",
    "Ferresurdotu556": "https://www.mercadolibre.cl/disco-para-sierra-circular-7-pulgada-de-60-dientes-uyustools/p/MLC22606963",
    "Ferresurdotu559": "https://articulo.mercadolibre.cl/MLC-1395487901-combinacion-llave-grifo-para-lavaplatos-tipo-v-bogen-stretto-_JM",
    "Ferresurdotu562": "https://articulo.mercadolibre.cl/MLC-543918149-desmalezadora-43cc-17hp-incluye-arnes-wulkan-_JM",
    "Ferresurdotu564": "https://articulo.mercadolibre.cl/MLC-1809812036-buzo-desechable-blanco-tipo-tyvek-topsafe-_JM",
    "Ferresurdotu565": "https://articulo.mercadolibre.cl/MLC-2220104310-malla-eco-sol-5014-10-x-25-metros-inchalam-_JM",
    "Ferresurdotu566": "https://articulo.mercadolibre.cl/MLC-1465390709-sifon-trampa-multiuso-tipo-s-y-p-40mm-_JM",
    "Ferresurdotu568": "https://www.mercadolibre.cl/serrucho-bahco-prizecut-22-pulg-professional-244p-carpintero/p/MLC24304871",
    "Ferresurdotu570": "https://articulo.mercadolibre.cl/MLC-2240610152-electrodo-7018-18-indura-1-kilo-_JM",
    "Ferresurdotu574": "https://articulo.mercadolibre.cl/MLC-625821407-tubo-led-t8-9w-60cm-iluminaled-6500k-ld-_JM",
}

sku2= {
"Ferresurdotu280":"https://articulo.mercadolibre.cl/MLC-542552972-bateria-gdlite-agm-12v-7ah-nuevas-_JM",
"Ferresurdotu254":"https://articulo.mercadolibre.cl/MLC-941108413-bateria-12v-7a-ultracell-solo-retiro-en-local-_JM",
"Ferresurdotu253":"https://articulo.mercadolibre.cl/MLC-527215020--bateria-recargable-12v-7ah-axxtec-por-ultracell--_JM",
"Ferresurdotu252":"https://articulo.mercadolibre.cl/MLC-1004879502-bateria-agm-12v-7ah-ciclo-profundo-ups-lampara-factura-_JM"} #Cambiar check
# ).execute()

# print(f"Datos insertados correctamente en la nueva hoja de Google Sheets en el rango {update_range}")