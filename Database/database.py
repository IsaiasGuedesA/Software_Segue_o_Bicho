import sqlite3
from datetime import datetime

global Database
Database = "database"

def comand_db(comand:str,fetchone=False,fetchall=False):
    try:
        conn = sqlite3.connect(f'Database/database')
        cur = conn.cursor()
        cur.execute(comand)
        conn.commit()

        if(fetchone and fetchall == False):
            result = cur.fetchone()
            cur.close()
            return result
        if(fetchall and fetchone == False):
            result = cur.fetchall()
            cur.close()
            return result
        
        return True
    except sqlite3.Error as erro:

        return False

def create_table(table):
        '''
        Cria uma tabela no banco de dados com a essa estrutura

        ID INTEGER PRIMARY KEY,
        DADO INT,
        LATITUDE CHAR(10),
        LONGITUDE CHAR(10),
        ALTITUDE CHAR(3),
        VELOCIDADE CHAR(3),
        SATELITE CHAR(3),
        BATERIA CHAR(3),
        SINAL_NBIOT CHAR(3),
        DATA_ORIGIN CHAR(10),
        HORA_ORIGIN CHAR(9),
        DATA_DESTINO CHAR(10),
        HORA_DESTINO CHAR(8)

        '''
        comand = "CREATE TABLE IF NOT EXISTS "+'"'+table+'"' +"""(
                ID INTEGER PRIMARY KEY,
                DADO INT,
                LATITUDE VARCHAR(10),
                LONGITUDE VARCHAR(10),
                ALTITUDE VARCHAR(4),
                VELOCIDADE VARCHAR(4),
                SATELITE VARCHAR(3),
                BATERIA VARCHAR(3),
                SINAL_NBIOT VARCHAR(3),
                DATA_ORIGIN VARCHAR(10),
                HORA_ORIGIN VARCHAR(9),
                DATA_DESTINO VARCHAR(10),
                HORA_DESTINO VArCHAR(8)
                );"""

        if comand_db(comand) != True:
            print(f" Erro ao Criar a tabela:{table}")
    

class Database():
    def __init__(self):
        comand = """CREATE TABLE IF NOT EXISTS REGI(
                REGISTRO VARCHAR(100) PRIMARY KEY,
                NOME_ANIMAL VARCHAR(100),
                ANIMAL VARCHAR(100),
                SENHA VARCHAR(100),
                STATE INTEGER
                );"""
        
        if comand_db(comand) != True:
            print("Erro ao iniciar o Database")
    
    def Registrar_coleira(self,registro,nome,animal,senha):
        '''
        Registra uma nova coleira na tabela registro (REGI)
        '''

        resultado =  comand_db(f"SELECT REGISTRO FROM REGI WHERE REGISTRO='{registro}'",True)
        if resultado is None:
           
            comand = f"INSERT INTO REGI (REGISTRO,NOME_ANIMAL,ANIMAL,SENHA,STATE) VALUES ('{registro}','{nome}','{animal}','{senha}','1');"
            if comand_db(comand) != True:
                print("Erro inserir dado na tabela de REGI")
                return False

            else:
                create_table(table=registro)
                return True
        else:
            print(f"Ja existe o regitro:{registro} na tabela REGI")
            return False
        
    def read_dados(self,registro:str):
        pass

    def state_coleira(self, registro:str , state=True):
        '''
        inscreve ou desecreve do topico cadastrado na tabela registro por meio da coluna state
        '''
        resultado =  comand_db(f"SELECT REGISTRO FROM REGI WHERE REGISTRO='{registro}'",True)
        if resultado is not None:
            comand = f"UPDATE REGI SET STATE='{'1' if state == True else '0'}' WHERE REGISTRO = '{registro}';"
            if comand_db(comand) != True:
                print(f"Erro para aultera a coluna state do Registro:{registro}")
                return False
            return True
        else:
            print(f"Erro o Registro:{registro} nao existe")
            return False


    def Inserir_dados(self,registro:str,Dado:int,Latitude:str,Longitude:str,Altitude:str,Velocidade:str,Satelite:str,Bateria:str,sinalNbiot:str,Data_origin:str,Hora_origin:str):
        '''
        latitude e longitude com 10 caracter ex:-16.666661
        altitude , velocidade, satelite ,bateria,Sinalnbiot ate 3 caracter
        data dd/mm/yy
        hora hh:mm:ss
        '''
        
        comand = """INSERT INTO '{}' (dado,latitude,longitude,altitude,velocidade,satelite,bateria,sinal_nbiot,data_origin,hora_origin,data_destino,hora_destino)
                    VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(registro ,str(Dado),Latitude,Longitude,Altitude,Velocidade,Satelite,Bateria,sinalNbiot,Data_origin,Hora_origin,datetime.now().strftime('%d/%m/%y'),datetime.now().strftime('%H:%M:%S'))
       
        if comand_db(comand) != True:
            print(f"Erro ao Inserir um Dado na tabla:{registro}")

    def read(self, table:str, colum=None , condition:str = None):
        '''
        realiza consultas em uma tabela
        colum (assesar um determinada coluna)
        condition ("colum1 = cond1, colum2 = cond2...")
        '''
        if colum == None:
            if condition == None:
                return comand_db(f"SELECT * FROM '{table}'",fetchall=True)
            else:
                return comand_db(f"SELECT * FROM '{table}' WHERE {condition}",fetchall=True)
            
        else:
            if condition == None:
                return comand_db(f"SELECT {colum} FROM '{table}'",fetchall=True)
            else:
                return comand_db(f"SELECT {colum} FROM '{table}' WHERE {condition}",fetchall=True)


if __name__ == "__main__":

    pass
    
    
