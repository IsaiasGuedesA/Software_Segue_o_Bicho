from flask import Flask,request, render_template, jsonify,redirect,url_for,session
from trackingMap.trackingMap import Start_map
from funcao.funcao import *


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

user_adm = {
    'Username':'admin',
    'Senha':'admin'
}

@app.route('/')
def hello_world():
    return redirect(url_for('login'))


@app.route('/map/<path:topic>',methods=['GET'])
def map(topic):

    if 'username' in session and topic == session['username']:
        result = Start_map(topic)
        if(result):
            return render_template("mapa.html")
        else:
            return 'topico nao existe ou nao informado'
    return redirect(url_for('login'))

    
    


@app.route('/coleira', methods=['POST', 'GET'])
def registra_coleira():
    if request.method == 'POST':
        if request.is_json:
            dados = request.get_json()
            try:
                registro = dados["REGISTRO"]
                nome_animal = dados["NOME_ANIMAL"]
                animal = dados["ANIMAL"]
                senha = dados["SENHA"]
              
                if registro == '' or nome_animal =='' or animal=='' or senha=='':
                    return f"ERRO: ao adiciona a coleira com o registro:{registro}",400
               
                if Registrar_coleira(registro=registro,nome_animal=nome_animal,animal=animal ,senha=senha) != True:
                    return f"ERRO: ao adiciona a coleira com o registro:{registro}",400
                
                
            except:
                return jsonify({"REGISTRO": "registro da coleira","NOME_ANIMAL":"Nome do animal", "ANIMAL":"especie do animal","SENHA":"senha"}), 400
            return redirect(url_for('login'))
        else:
            return jsonify({"REGISTRO": "registro da coleira","NOME_ANIMAL":"Nome do animal", "ANIMAL":"especie do animal", "SENHA":"senha"}), 400

    elif request.method == 'GET':
        registro = request.args.get('registro')
        state = request.args.get('state')

        if registro is None or state is None:
            return "parametro errado: 'registro':'registro da coleira' , 'state':'1 ou 0'", 400
        
        if state == '1' or state == '0':
            if State_coleira(registro=registro, state=state) == True:
                return "OK"
            else:
                return f"erro ao setar o state:{state}, do registro:{registro}", 400
    
        else:
            return f"parametro errado state={state}: 'state':'1 ou 0'", 400     

    else:
        return 400



@app.route('/register', methods=['GET'])
def registra():
    if 'username' in session and "admin" == session['username']:
        return render_template("register.html")
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        dados = request.get_json()
        user = dados["USER"]
        senha = dados["SENHA"]
        if user == user_adm['Username'] and senha == user_adm['Senha']:
            session['username'] = user
            return redirect(url_for('registra'))
        else:
            if vereficar_user(user,senha) == True:
                session['username'] = user
                return redirect(url_for('map',topic=user))
            else:
                return 'ok',400

    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
