from Client.Client import Client_conect
import time
from Config_Broker.Config_Broker import Config


    

if __name__ == "__main__":
    a = Client_conect(
    host=Config["HOST"],
    port=Config["PORT"],
    client_id=Config["CLIENT_ID"],
    Keepalive= Config["KEEPALIVE"],
    qos=Config["QOS"],
    topic_flask=Config["TOPIC_FLASK"]
    )

    a.start()
    a.loop()
    
    try:
        while True: time.sleep(0.001)
    except:
        pass
    pass
