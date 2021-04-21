from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import os

#browser = webdriver.Edge(executable_path='./driver/edgedriver')

filepath = './resource/whatsapp_session.txt'
with open(filepath) as fp:
    for cnt, line in enumerate(fp):
        if cnt == 0:
            executor_url = line
        if cnt == 1:
            session_id = line


def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver


browser = create_driver_session(session_id, executor_url)
print("browser URL: " + browser.current_url)


def enviar():
    element = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span')
    element.click()
    print("MENSAJE ENVIADO")
            
def enviar_mensaje(mensaje: str):
    chatbox = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    chatbox.send_keys(mensaje)
    time.sleep(2)
    enviar()


while True:
        print("BUSCANDO CHAT")
        #SE BUSCA POR LA CLASE _2aBzC POR QUE SE DETECTO QUE TODOS LOS CHATS TIENEN ESA ATRIBUTO
        chats = browser.find_elements_by_class_name("_2aBzC")
        if len(chats) > 0:
            for chat in chats:
                print("DETECTANDO MENSAJES SIN LEER")
                #SE BUSCA POR LA CLASE _38M1B POR QUE SE DETECTO QUE SOLO LOS QUE SON ETIQUETADOS CON MENSAJES SIN LEER TIENEN ESA CLASE
                chats_mensajes = chat.find_elements_by_class_name("_38M1B")
                
                #SE BUSCA POR LA CLASE _3Dr46 PARA COMPROBAR NOMBRE
                name = chat.find_elements_by_class_name('_3Dr46')
                
                if len(chats_mensajes) == 0:
                    print("CHAT", name[0].text, "SIN MENSAJES POR ATENDER")
                    sleep(1)
                    continue

                for chats_mensaje in chats_mensajes:
                        try:
                            print("IDENTIFICANDO CONTACTO")
                            #SE BUSCA NOMBRE DEL CONTACTO
                            #Valida si el boot puede atender a este contacto
                            contactos = open("./resource/contactos_autorizados.txt", mode='r', encoding='utf-8')
                            
                            if name[0].text not in contactos.readlines():
                                print("Contacto no autorizado : ", name[0].text)
                                continue

                            #Abre chat de contacto
                            chat.click()
                            #SE BUSCA DETECTA EL MENSAJE
                            message = browser.find_elements_by_class_name("_24wtQ")
                            
                            #Valida si mensaje se encuentra en el diccionario de acciones
                            diccionario = open("./resource/diccionario_bot.txt", mode='r', encoding='utf-8')
                            if message[0].text.upper() not in diccionario.readlines():
                                print("Mensaje no reconocido, Enviando mensaje de bienvenida")

                                response = "Hola, soy un boot en entrenamiento y solo puedo atender preguntas exactas :-( \n" \
                                                           "Indícame en que te puedo ayudar :-) : \n"\
                                                            "SALUDAR \n"\
                                                            "RESPONDER \n"\
                
                                chatbox = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                                chatbox.send_keys(response)
                            
                            diccionario.close()
                                
                        except Exception as e:
                            print("EXCEPTION : ",e)
        else:
            print("NO TIENE CONTACTOS EN LISTA")
            sleep(30)

