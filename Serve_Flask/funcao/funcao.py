from Database.database import Database
import paho.mqtt.client as Mqtt
import time 
from Config_Broker.Config_Broker import Config


cliente = Mqtt.Client(Mqtt.CallbackAPIVersion.VERSION2, client_id="Flask_serve")
db = Database()


def publi_mqtt(mensagem:str):
    

    cliente.connect(host=Config["HOST"],port=Config["PORT"],keepalive=Config["KEEPALIVE"])

    resultado = cliente.publish(Config["TOPIC_FLASK"], mensagem)
  
    time.sleep(1)
    status = resultado.rc
    if status == 0:
        print(f"Mensagem '{mensagem}' publicada no tópico '{Config["TOPIC_FLASK"]}'")
        cliente.disconnect()
        return True
    else:
        print(f"Falha ao publicar mensagem no tópico '{Config["TOPIC_FLASK"]}'")
        cliente.disconnect()
        return False




def Registrar_coleira(registro:str, nome_animal:str, animal:str, senha:str):
    if db.Registrar_coleira(registro=registro,nome=nome_animal,animal=animal,senha=senha) == True:
        publi_mqtt(f"sub;{registro}")
        return True
    else:
        return False

def State_coleira(registro:str, state:str):
    if state == '1':
        if db.state_coleira(registro ,state=True) == True :
            publi_mqtt(f"sub;{registro}")
            return True
        return False 
    else:
        if db.state_coleira(registro ,state=False) == True :
            publi_mqtt(f"uns;{registro}")
            return True
        return False

def vereficar_user(user,senha):
    usuario = db.read(table='REGI',condition=f"REGISTRO= '{user}'")
    if usuario == None:
        return False
    
    if db.read(table='REGI',colum="SENHA",condition=f"REGISTRO= '{user}'")[0][0] == senha:
        return True
    
    