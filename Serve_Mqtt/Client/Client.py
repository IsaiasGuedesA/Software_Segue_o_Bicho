
import paho.mqtt.client as MqttClient

from Database.database import Database

global db
db = Database()

# callback

def on_connect(client, userdata, flags, reason_code , properties,db,qos,Topic_flask):
    if reason_code == 0:
        print("conctado ao broker!")
        tb_regi = db.read("REGI","REGISTRO","STATE=1")
        client.subscribe(topic=Topic_flask, qos=qos)
        print(tb_regi)
        for topic in tb_regi:
            client.subscribe(topic=topic[0],qos=qos)
            print(f"-sub:{topic[0]}")
            
    else:
        print(f"ERRO: fail connect code{reason_code}")

def on_disconnect(client, userdata, reason_code, properties,rc):
    print(f"desconectado do broker! \n reason_code:{reason_code}")

def on_message(client, userdata, message,db,qos,Topic_flask):
    # dado;latitude;longitude;altitude;velocidade;satelite;bateria;Sinal_nbiot;dd/mm/aaaa;hh:mm:ss
    # 1;-16.666661;-16.666661;999;999;999;100;100;11/01/04;13:15:35
    # uns;registro / sub;registro

    print("nova mensagem!")
    print(f"Topic:{message.topic}      msg:{message.payload.decode("utf-8")}     Qos:{str(message.qos)}")
    
    msg = str(message.payload.decode("utf-8"))
    registro = str(message.topic)

    dado = msg.split(';')

    if(registro==Topic_flask):
        print(dado)
        if(dado[0]=="sub"):
            print(f"-sub:{dado[1]}")
            client.subscribe(topic=dado[1],qos=qos)
        elif dado[0]=="uns":
            print(f"-uns:{dado[1]}")
            client.unsubscribe(topic=dado[1])
    else: 
        try:
            db.Inserir_dados(registro,dado[0],dado[1],dado[2],dado[3],dado[4],dado[5],dado[6],dado[7],dado[8],dado[9])
            print("dado adicionado")
        except:
            print("dado no formanto errado")
  


class Client_conect():
    def __init__(self , host:str, port:int, client_id:str ,qos:int, Keepalive:int,topic_flask:str):
        self.__HOST = host
        self.__PORT = port
        self.__CLIENT_ID = client_id
        self.__KEEPALIVE = Keepalive
        self.__Qos = qos
        self.__Topic_flask = topic_flask
        self.__Stt_conection = False
       
    def start(self):
        self.__mqttClient = MqttClient.Client(MqttClient.CallbackAPIVersion.VERSION2, client_id=self.__CLIENT_ID)
        try:
            self.__mqttClient.connect(host=self.__HOST, port=self.__PORT,keepalive=self.__KEEPALIVE)
            
            self.__mqttClient.on_connect =lambda client, userdata, flags, reason_code , properties: on_connect(client, userdata, flags, reason_code , properties,db,self.__Qos,self.__Topic_flask)
            self.__mqttClient.on_disconnect = on_disconnect
            self.__mqttClient.on_message = lambda client, userdata, message:on_message(client, userdata, message,db,self.__Qos,self.__Topic_flask)
            self.__Stt_conection = True
            
        except:
            print("erro ao se conectar!")
            self.__Stt_conection = False


    def loop(self):
        self.__mqttClient.loop_start()

     
    def Subscribe(self,topic:str):
        if self.__Stt_conection :
            try:
                self.__mqttClient.subscribe(topic=topic,qos=self.__Qos)
                print(f"Subscribe:{topic}")
                return True
            except:
                print(f"falha ao se inscrever no topico : {topic} ")
                return False
        else:
            print("nao conctado ao broker!")
            return False
        

    def unsubscribe(self,topic:str):
        try:
            self.__mqttClient.unsubscribe(topic)
            return True
        except:
            return False
   


if __name__ == "__main__":
    pass



