import pandas as pd
from datetime import datetime
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#SetupChromeDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')


#Se cargan las opciones para iniciar el driver
chrome_options = webdriver.ChromeOptions()
#Ubicación del driver

#Main Function
def MainFunction(Link):
    #Instanciamos el driver
    driver = webdriver.Chrome(chrome_options=chrome_options)

    #Maximizar navegador
    driver.maximize_window()

    #Vamos al sitio a scrapear
    driver.get(Link)

    #Se agregaran time sleep en las acciones para evitar el baneo de la página
    time.sleep(3)

    #Funcion para leer las cookies del sitio y evitar el baneo del sitio

    def read_cookies(p = 'cookiesJumbo.txt'):
        cookies = []
        with open(p, 'r') as f:
            for e in f:
                e = e.strip()
                if e.startswith('#'): continue
                k = e.split('\t')
                if len(k) < 3: continue  # not enough data
                # with expiry
                cookies.append({'name': k[-2], 'value': k[-1], 'expiry': int(k[-3])})
        return cookies    

    #Lectura y agregado de las cookies

    cookies = read_cookies("cookiesJumbo.txt") 
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    time.sleep(5)
    # Realizar el scroll hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #Listas para recopilar la información
    products = []


    #Simulación de Scroll para cargar todos los datos
    total_height = int(driver.execute_script("return document.body.scrollHeight"))

    # Hacer scroll poco a poco
    for i in range(0, total_height, 500):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.7)

    time.sleep(2)
    elem = driver.find_element('xpath',"//*")
    soup = BeautifulSoup(elem.get_attribute('innerHTML'),'html.parser')
    #Obtener todos los nombre de los productos
    nameproducts = soup.find_all("span", {"class":"vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body"})
    print('Obteniendo Nombres de los Productos')
    #Obtener todos los precios de los productos
    print('Obteniendo Precios de los Productos')
    priceproducts = soup.find_all("div", {"class":"tiendasjumboqaio-jumbo-minicart-2-x-price"})
    sublist1 = []

    # Busca la lista de productos por la clase "productos" para obtener los links
    lista_productos = soup.find_all("a", {"class":"vtex-product-summary-2-x-clearLink h-100 flex flex-column"})

    for name, price, link in zip(nameproducts, priceproducts, lista_productos):
        producto = {"Name": name.text, "Precio": price.text, "Link":link}
        products.append(producto)

    # Crear un DataFrame
    
    df = pd.DataFrame(products)

    json_str = df.to_json(orient='records')
    print(json_str)

    # abrir el archivo de salida
    with open('Datos Jumbo.json', 'w') as archivo:
        # escribir la lista de diccionarios en el archivo JSON
        json.dump(json_str, archivo)


MainFunction ('https://www.tiendasjumbo.co/supermercado/despensa/arroz-y-granos?order=OrderByBestDiscountDESC')