
from shapely import Point,LineString
import pandas as pd
import folium
from Database.database import Database,comand_db

db = Database()
def Start_map(topic:str):
    geometry_line = []
    geometry_point =[]
    icon_image = 'Serve_Flask/trackingMap/point_ball.png'


    resultado =  comand_db(f"SELECT REGISTRO FROM REGI WHERE REGISTRO='{topic}'",True)
    if resultado is None:
        # nao tem essa tabela
        return False
    print(resultado)
    dados = db.read(table=topic)
    dados  = pd.DataFrame(dados, columns=['ID',	'DADO',	'LATITUDE',	'LONGITUDE','ALTITUDE','VELOCIDADE','SATELITE','BATERIA','SINAL_NBIOT','DATA_ORIGIN','HORA_ORIGIN','DATA_DESTINO','HORA_DESTINO'])
    dados_regi = db.read(table='REGI',condition=f"REGISTRO='{topic}'")
    dados_regi = pd.DataFrame(dados_regi, columns=['REGISTRO','NOME_ANIMAL','ANIMAL','STATE','SENHA'])

    
    for i in range(len(dados)):
        if i < len(dados)-1:
            point1 = (dados.loc[i, 'LATITUDE'], dados.loc[i, 'LONGITUDE'])
            point2 = (dados.loc[i+1, 'LATITUDE'], dados.loc[i+1, 'LONGITUDE'])
            geometry_line.append(LineString([point1, point2]))
        

    for i in range(len(dados)):
        geometry_point.append(Point(dados.loc[i, 'LATITUDE'], dados.loc[i, 'LONGITUDE']))

    if(dados['LATITUDE'].empty and dados['LONGITUDE'].empty):
        map = folium.Map(location=[-10, -55], zoom_start=4)

    else:
        map = folium.Map(location=[dados['LATITUDE'][len(dados)-1], dados['LONGITUDE'][len(dados)-1] ], zoom_start=15)

   

    for i in range(len(geometry_line)):
        folium.PolyLine(locations=geometry_line[i].coords, color='green', weight=6, opacity=0.5).add_to(map)

    for i in range(len(geometry_point)):
        icon_point_circle = folium.CustomIcon(
                    icon_image,
                    icon_size=(20, 20),
                    )

        icon_point_pin = folium.Icon(color='green',icon='paw',prefix='fa')

        html_popup = f"""
        <h6>
        Dado: {dados['DADO'][i]}<br>
        Altitude: {dados['ALTITUDE'][i]}<br>
        Velocidade: {dados['VELOCIDADE'][i]}Km/h<br>
        Bateria: {dados['BATERIA'][i]}%<br>
        Satelite: {dados['SATELITE'][i]}<br>
        Sinal_Nbiot: {dados['SINAL_NBIOT'][i]}<br>
        Data: {dados['DATA_ORIGIN'][i]}<br>
        Hora: {dados['HORA_ORIGIN'][i]}<br>
        </h6>
        """

        
        popup = folium.Popup(html_popup, max_width=500)
        
        if i < len(geometry_point)-1:
            folium.Marker([geometry_point[i].x,geometry_point[i].y], popup=popup,icon=icon_point_circle).add_to(map)
        else:
            popup = folium.Popup(f"<h6>(ultimo ponto)<h6>"+html_popup, max_width=500)
            folium.Marker([geometry_point[i].x,geometry_point[i].y], popup=popup,icon=icon_point_pin).add_to(map)

    legend_html = f'''
    <div style="background-color: rgb(255, 255, 255);
    position: fixed;
    bottom: 50px; right: 50px; width: 200px; height: 50px;
        margin:0;
        z-index:9999;
        padding: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-style: normal;
        display: flex;
        flex-direction: column;
        align-items: center;
        -webkit-box-shadow: 6px 9px 23px -9px rgba(0,0,0,0.71);
        -moz-box-shadow: 6px 9px 23px -9px rgba(0,0,0,0.71);
        box-shadow: 6px 9px 23px -9px rgba(0,0,0,0.71);">
            <h1 style="font-size: 20px; margin:0;
            padding: 0;">{dados_regi['NOME_ANIMAL'][0]}</h1>
            <h5 style=" margin:0;
            padding: 0;">{dados_regi['ANIMAL'][0]}</h5>
            <h6 style="font-size: 10px; margin:0;
            padding: 0;">{dados_regi['REGISTRO'][0]}</h6>
        </div>
        '''

    map.get_root().html.add_child(folium.Element(legend_html))


    map.save('Serve_Flask/templates/mapa.html')
    return True
        



if __name__ =='__main__':
    pass