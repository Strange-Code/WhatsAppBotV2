#DESARROLLADO POR COMUNIDAD DE PROGRAMADORES STRANGE CODE
from selenium import webdriver
import time

browser = webdriver.Edge(executable_path="./driver/edgedriver")


def seleccionarChat():
    elements = browser.find_elements_by_tag_name("span")
    for element in elements:
        if element.text == 'strngrwrld':
            element.click()
            return True
    return False


def validaQR():
    try:
        element = browser.find_element_by_tag_name("canvas")
    except:
        return False
    return True

def leerArchivo():
    archivo = open('./resource/leer.txt',mode="r")
    
    print("SELECCIONAR LA CAJA DE TEXTO")
    cajitaDeTexto = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

    for linea in archivo.readlines():
        print("LINEA LEIDA : " + linea)
        cajitaDeTexto.send_keys(linea)
    archivo.close()

def bootWhatsapp():
    browser.get("https://web.whatsapp.com/")
    time.sleep(5)

    ##variable de espera
    espera = True

    while espera:
        print("ESTOY ESPERADO")
        espera = validaQR()
        time.sleep(2)
        if espera == False:
            print("QUE SE AUTENTICO")
            break
    
    time.sleep(2)
    print("BUSCANDO CHAT")
    btnChat = seleccionarChat()
    time.sleep(2)
    
    leerArchivo()
 

bootWhatsapp()