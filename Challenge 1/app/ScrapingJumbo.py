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

#Instanciamos el driver
driver = webdriver.Chrome(chrome_options=chrome_options)

#Maximizar navegador
driver.maximize_window()

#Vamos al sitio a scrapear
driver.get('https://www.tiendasjumbo.co')

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

time.sleep(3)


#Ubicamos el elemento donde están los departamentos 
departamentos = driver.find_element(By.XPATH, '//*[@id="menu-item-music-store"]/div')
acciones = ActionChains(driver)
acciones.move_to_element(departamentos).perform()
time.sleep(3)
#Iterar elementos por departamento'
Serie2 = range(1, 20, 1)

#Listas para recopilar datos
Departamento = []
Link = []
Categorias = []
Subcategorias = []

#Iteración para los departamentos existentes
for i in Serie2:
    try:
        print('----') 
        #elementodepar = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div/div[2]/div/div[2]/section/div/div[1]/div/div/nav/ul/li/div[2]/div/section/div/div/div/div/div/div/div[1]/div/ul/div[{i}]/div/li'.format(i=i))
        elementodepar = driver.find_element(By.XPATH, ' /html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/section/div/div[1]/div/div/nav/ul/li/div[2]/div/section/div/div/div/div/div/div/div[1]/div/ul/div[{i}]/div/li/span/a'.format(i=i))

        Departamento.append(elementodepar.text) 
        print(elementodepar.text)
        acciones.move_to_element(elementodepar).perform()
        time.sleep(2)
        # Obtener el valor del atributo href
        elementolink = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/section/div/div[1]/div/div/nav/ul/li/div[2]/div/section/div/div/div/div/div/div/div[2]/div/div[1]/a')
        href = elementolink.get_attribute("href")
        print(href)
        Link.append(href)
        time.sleep(2)
        Catego = []

        #Iteración para obtener las diferentes categorias
        for i in Serie2:
            try:
                elementocategoria = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/section/div/div[1]/div/div/nav/ul/li/div[2]/div/section/div/div/div/div/div/div/div[2]/div/div[2]/ul/li[{i}]/div/span/a'.format(i=i))
                #print(elementocategoria.text) 
                cate = elementocategoria.text
                Catego.append(cate)
                time.sleep(.1)
            except Exception as e:
                print(e)

        numcategorias = len(Catego)
        listanumcategorias = range(1,numcategorias,1)
        Subcatego = []
        time.sleep(2)
        #Iteración para obtener las diferentes sub categorias
        for i in listanumcategorias:
            for j in Serie2:
                try:
                    #elementosubcategoria = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div/div[2]/div/div[2]/section/div/div[1]/div/div/nav/ul/li/div[2]/div/section/div/div/div/div/div/div/div[2]/div/div[2]/ul/li[{i}]/div/div/ul/li[{j}]/a'.format(i=i, j=j))
                    elementosubcategoria = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/section/div/div[1]/div/div/nav/ul/li/div[2]/div/section/div/div/div/div/div/div/div[2]/div/div[2]/ul/li[{i}]/div/div/ul/li[{j}]/a'.format(i=i, j=j))

                    #print(elementosubcategoria.text)
                    Subcatego.append(elementosubcategoria.text)
                    time.sleep(.1)
                except:
                    pass
        print('-----')
        Subcategorias.append(Subcatego)
        Categorias.append(Catego)
    except Exception as e:
        print(e)


# creamos un DataFrame de ejemplo
df = pd.DataFrame({
    'Departamento': Departamento,
    'Link': Link,
    'Categorias': Categorias,
    'Subcategorias': Subcategorias
})

# convertimos el DataFrame en un diccionario
diccionario = df.to_dict(orient='records')

json_string = json.dumps(diccionario)

# abrir el archivo de salida
with open('Datos.json', 'w') as archivo:
    # escribir la lista de diccionarios en el archivo JSON
    json.dump(json_string, archivo)
