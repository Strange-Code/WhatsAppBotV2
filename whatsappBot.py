from selenium import webdriver
import time

browser = webdriver.Edge(executable_path='./driver/msedgedriver')

def seleccionarChat(nombre : str):
    buscando = True

    while buscando:
        print("BUSCANDO CHAT")
        elements = browser.find_elements_by_tag_name("span")
        for element in elements:
            if element.text == nombre:
                print("ENCONTRAMOS AL IMPOSTOR")
                element.click()
                buscando = False
                break

def enviar():
    element = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span')
    element.click()
    print("MENSAJE ENVIADO")

def enviarMensaje(mensaje: str):
    chatbox = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    chatbox.send_keys(mensaje)
    time.sleep(2)
    enviar()

def leerArchivo(ruta:str):
    archivo = open(ruta, mode='r', encoding='utf-8')
    chatbox = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

    for linea in archivo.readlines():
        print ("MENSAJE : ", linea)
        chatbox.send_keys(linea)

    archivo.close()

def validaQR():
    try:
        browser.find_element_by_tag_name("canvas")
    except:
        return False
    return True

def botWhatsapp():
    browser.get("https://web.whatsapp.com/")
    time.sleep(5)

    espera = True

    while espera:
        print("ESTOY ESPERANDO")
        espera = validaQR()
        time.sleep(2)
        if espera == False:
            print("SE AUTENTICO")
            break
    
    seleccionarChat("RPONCE")
    time.sleep(2)
    leerArchivo('./resource/pruebaBot.txt')

botWhatsapp()