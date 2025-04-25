'''''
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = Chrome(service=service, options=option)
    url = "https://app.midis.gob.pe/Infomidis/#/"
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    # Quitar splash screen
    ActionChains(driver).move_by_offset(10, 10).click().perform()
    wait.until(EC.invisibility_of_element_located((By.ID, "splashScreen")))

    # Cerrar modal inicial
    close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='myModalInicio']//button[contains(text(),'Cerrar')]")))
    close_btn.click()
    wait.until(EC.invisibility_of_element_located((By.ID, "myModalInicio")))

    # Ir a la sección de Padrón de Hogares
    btnPGH = wait.until(EC.element_to_be_clickable((By.ID, "lipgh")))
    btnPGH.find_element(By.TAG_NAME, "a").click()

    wait.until(EC.presence_of_element_located((By.ID, "selDepartamento")))
    print("¡Select encontrado!")
    data_total = []

    departamento = "LIMA"
    print(f"Procesando: {departamento}")
    Select(driver.find_element(By.ID, "selDepartamento")).select_by_visible_text(departamento)
    time.sleep(1)

    wait.until(EC.presence_of_element_located((By.ID, "selProvincia")))
    print("¡Provincias cargadas!")
    select_prov = Select(driver.find_element(By.ID, "selProvincia"))
    provincias = [opt.text for opt in select_prov.options if opt.text != 'Seleccione provincia']

    for provincia in provincias:
        Select(driver.find_element(By.ID, "selProvincia")).select_by_visible_text(provincia)
        time.sleep(1)
        print(f"    Provincia: {provincia} - esperando distritos...")
        wait.until(EC.presence_of_element_located((By.ID, "selDistrito")))
        print("¡Distritos cargados!")
        select_dist = Select(driver.find_element(By.ID, "selDistrito"))
        distritos = [opt.text for opt in select_dist.options if opt.text != 'Seleccione distrito']

        for distrito in distritos:
            Select(driver.find_element(By.ID, "selDistrito")).select_by_visible_text(distrito)
            time.sleep(2)
            print(f"    Distrito: {distrito} - esperando tabla...")
            wait.until(EC.presence_of_element_located((By.ID, "tblServicios")))
            print("    ¡Tabla cargada!")

            valores = []
            try:
                for i in range(3):
                    fila = driver.find_elements(By.CSS_SELECTOR, "#tblServicios tbody tr")[i]
                    columnas = fila.find_elements(By.TAG_NAME, "td")
                    if len(columnas) == 2:
                        nombre = columnas[0].text.strip()
                        cantidad = columnas[1].text.strip().replace(',', '')
                        valores.append(int(cantidad) if cantidad.isdigit() else 0)
            except Exception as e:
                print(f"    Error procesando fila en {distrito}: {e}")
                continue

            if len(valores) == 3:
                data_total.append({
                    "Departamento": departamento,
                    "Provincia": provincia,
                    "Distrito": distrito,
                    "No Pobre": valores[0],
                    "Pobre": valores[1],
                    "Pobre extremo": valores[2]
                })
            print(f"Datos almacenados de: {distrito}")

    time.sleep(3)
    driver.quit()

    df = pd.DataFrame(data_total)
    nombre_archivo = "pgh_lima.csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado como: {nombre_archivo}")

if __name__ == '__main__':
    main()

 '''   
#el de arriba es de lima noma, el de abajo si es de cerru
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

def main():
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    #option.add_argument("--window-size=1920,1080")
    driver = Chrome(service=service,options=option)
    url="https://app.midis.gob.pe/Infomidis/#/"
    driver.get(url)
    wait = WebDriverWait(driver,5)

    #Quitar el splashScreen que aparece al cargar la pagina
    ActionChains(driver).move_by_offset(10, 10).click().perform()
    wait.until(EC.invisibility_of_element_located((By.ID, "splashScreen")))

    #Cerrar la pantalla que bloque las opciones de interactuar con la pagina
    close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='myModalInicio']//button[contains(text(),'Cerrar')]")))
    close_btn.click()
    wait.until(EC.invisibility_of_element_located((By.ID, "myModalInicio")))

    #Acceder a la ruta de Padrón de Hogares
    btnPGH = wait.until(EC.element_to_be_clickable((By.ID,"lipgh")))
    btnPGH.find_element(By.TAG_NAME,"a").click()

    #Obtener información por Distrito
    #Esperamos a que el menú de departamentos esté visible
    wait.until(EC.presence_of_element_located((By.ID, "selDepartamento")))
    print("¡Select encontrado!")
    #inicializar lista
    data_total = []
    select_depto = Select(driver.find_element(By.ID, "selDepartamento"))
    departamentos = [opt.text for opt in select_depto.options if opt.text != 'Todos los departamentos']
    for departamento in departamentos:
        print(f"Procesando: {departamento}")
        Select(driver.find_element(By.ID, "selDepartamento")).select_by_visible_text(departamento)
        time.sleep(1)
        #esperar a que cargue el menu de provincias
        wait.until(EC.presence_of_element_located((By.ID, "selProvincia")))
        print("¡Provincias cargadas!")
        select_prov = Select(driver.find_element(By.ID, "selProvincia"))
        pronvincias = [opt.text for opt in select_prov.options if opt.text != 'Seleccione provincia']

        for provincia in pronvincias:
            Select(driver.find_element(By.ID, "selProvincia")).select_by_visible_text(provincia)
            time.sleep(1)
            print(f"    Provincia: {provincia} - esperando distritos...")
            wait.until(EC.presence_of_element_located((By.ID, "selDistrito")))
            print("¡Distritos cargados!")
            select_dist = Select(driver.find_element(By.ID, "selDistrito"))
            distritos = [opt.text for opt in select_dist.options if opt.text != 'Seleccione distrito']

            for distrito in distritos:
                Select(driver.find_element(By.ID, "selDistrito")).select_by_visible_text(distrito)
                time.sleep(2)
                #esperar a que cargue la tabla
                print(f"    Distrito: {distrito} - esperando tabla...")
                wait.until(EC.presence_of_element_located((By.ID, "tblServicios")))
                print("    ¡Tabla cargada!")
                #extraer filas de la tabla
                filas = driver.find_elements(By.CSS_SELECTOR, "#tblServicios tbody tr")[:3]  # Solo las 3 primeras
                print(f"    Filas encontradas: {len(filas)} (usando solo las 3 primeras)")
                valores = []
                for i in range(min(3, len(filas))):
                    # Re-obtén las filas directamente cada vez
                    fila = driver.find_elements(By.CSS_SELECTOR, "#tblServicios tbody tr")[i]
                    columnas = fila.find_elements(By.TAG_NAME, "td")
                    if len(columnas) == 2:
                        try:
                            nombre = columnas[0].text.strip()
                            cantidad = columnas[1].text.strip().replace(',', '')
                            valores.append(int(cantidad) if cantidad.isdigit() else 0)
                        except Exception as e:
                            print(f"    Error al procesar fila {i+1}: {e}")
                if len(valores)== 3:
                    data_total.append({
                        "Departamento": departamento,
                        "Provincia": provincia,
                        "Distrito": distrito,
                        "No Pobre": valores[0],
                        "Pobre": valores[1],
                        "Pobre extremo": valores[2]
                        })
                print(f"Datos almacenados de: {distrito}")
    time.sleep(5)
    #cerrar navegador
    driver.quit()
    df = pd.DataFrame(data_total)
    nombre_archivo = "pgh_data.csv"
    # Guardar en CSV
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado como: {nombre_archivo}")

if __name__=='__main__':
    main()