from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re
from unicodedata import normalize

filepath = './resource/whatsapp_session.txt'
driver = webdriver

def crear_driver_session():

    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
                
    org_command_execute = RemoteWebDriver.execute

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver

def buscar_chats():
    print("BUSCANDO CHATS")

    if len(driver.find_elements_by_class_name("_2zkCi")) == 0:
        print("CHAT ABIERTO")
        message = identificar_mensaje()
        if message != None:
            return True

    chats = driver.find_elements_by_class_name("_2aBzC")

    for chat in chats:
        print("DETECTANDO MENSAJES SIN LEER")

        chats_mensajes = chat.find_elements_by_class_name("_38M1B")

        if len(chats_mensajes) == 0:
            print("CHATS ATENDIDOS")
            continue

        element_name = chat.find_elements_by_class_name('_3Dr46')
        name = element_name[0].text.upper().strip()
        name = name.lstrip()

        print("IDENTIFICANDO CONTACTO")
        
        with open("./resource/contactos_autorizados.txt", mode='r', encoding='utf-8') as archivo:
            contactos = [linea.rstrip() for linea in archivo]
            if name not in contactos:
                print("CONTACTO NO AUTORIZADO:", name)
                continue
        
        print(name, "AUTORIZADO PARA SER ATENDIDO POR BOT")
        
        chat.click()
        return True
    return False

def normalizar(message: str):
    # -> NFD y eliminar diacríticos
    message = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", message), 0, re.I
    )

    # -> NFC
    return normalize( 'NFC', message)

def identificar_mensaje():
    element_box_message = driver.find_elements_by_class_name("_3XpKm")
    posicion = len(element_box_message) -1

    color =  element_box_message[posicion].value_of_css_property("background-color")

    if color == "rgba(220, 248, 198, 1)" or color == "rgba(5, 97, 98, 1)":
        print("CHAT ATENDIDO")
        return
    
    element_message = element_box_message[posicion].find_elements_by_class_name("_3ExzF")
    message = element_message[0].text.upper().strip()
    print("MENSAJE RECIBIDO :", message)
    return normalizar(message)

def preparar_respuesta(message :str):
    print("PREPARANDO RESPUESTA")

    if message.__contains__("QUE ES STRANGECODE"):
        response = "StrangeCode es una comunidad de informaticos que les apasiona aprender y compartir conocimiento :-D \n" \
                        "Puedes visitar nuestra pagina web: https://strange-code.github.io/Links \n"
    elif message.__contains__("CUAL ES SU CANAL DE YOUTUBE"):
        response = "Puedes visitarnos en: https://www.youtube.com/channel/UCl24Q__MfUNDMhNWBluHcTg \n"
    elif message.__contains__("QUIERO UNIRME A LA COMUNIDAD"):
        response = "Puedes unirte a la comunidad ingresando al siguiente link: https://discord.com/invite/26ptv6URXY \n"
    elif message.__contains__("QUE PUEDES HACER"):
        text1 = open("./resource/respuesta1.txt", mode='r', encoding='utf-8')
        response = text1.readlines()
        text1.close()
    elif message.__contains__("GRACIAS"):
        response = "Ha sido un place ayudarte ;-)  \n"
    elif message.__contains__("DONDE ESTA EL DINERO"):
        response = "Ni k Decirte  \n"
    elif message.__contains__("XD"):
        response = "xdd \n"
    elif message.__contains__("HOLA"):
        response = "Hola, Como estas?  ;-)  \n"
    elif message.__contains__("PRECIO"):
        if message.__contains__("CODIGO"): 
            response = "Es gratis:( \n "
        elif message.__contains__("CALCETINES"): 
            response = "VALEN 30 EL PAR (y) \n "
    elif message.__contains__("COMO ESTAS"):
        if message.__contains__("MAL"): 
            response = "Por que estas mal :( \n "
        elif message.__contains__("BIEN"): 
            response = "Que me alegro que estes bien :) (Y) \n"
        else: 
            response = "Como estas? PUTA (Y) \n"
    else:        
        response = "Hola, soy a Eva un bot creado por StrangeCode, preguntame ¿Qué puedo hacer? :-D \n"

    return response

def procesar_mensaje(message :str):
    chatbox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    response = preparar_respuesta(message)
    chatbox.send_keys(response)

def whatsapp_boot_init():
    global driver
    driver = crear_driver_session()

    while True:
        if not buscar_chats():
            sleep(10)
            continue
        
        message = identificar_mensaje()

        if message == None:
            continue

        procesar_mensaje(message)


whatsapp_boot_init()