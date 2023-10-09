from flask import Flask, jsonify, request
import mysql.connector
import pandas as pd
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, exceptions
from model import UsersModel
from db import db 





mydb = mysql.connector.connect(user='root', 
                               password='bart1234',
                               host='localhost',
                               database='db_carros')
app = Flask(__name__)



app.config['JWT_SECRET_KEY'] = 'teste-key-tinoco'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bart1234@localhost/db_carros'
app.config['JWT_ERROR_MESSAGE'] = 'Token de autorização ausente'


db.init_app(app)
JWTManager(app)




with app.app_context():
    db.create_all()
    db.session.commit()



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = UsersModel.query.filter_by(email=data.get('email')).first()

    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401



@app.route('/carros', methods=['GET'])
@jwt_required()
def consultar_carros():
    current_user_id = get_jwt_identity()

    user = UsersModel.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM carro')
    todas_vendas = my_cursor.fetchall()
    columns = [column[0] for column in my_cursor.description]
    pandas_df = pd.DataFrame(todas_vendas, columns=columns)
    pandas_df = pandas_df.to_dict(orient='records')
    return jsonify(pandas_df)

    
@app.route("/carros/<int:id>", methods=['GET'])
def obter_carros(id):
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM carro')
    todas_vendas = my_cursor.fetchall()
    columns = [column[0] for column in my_cursor.description]
    pandas_df = pd.DataFrame(todas_vendas, columns=columns)
    pandas_df = pandas_df.to_dict(orient='records')
    for carro in pandas_df:
        if carro.get('id') == id:
            return jsonify(carro)
        
@app.route("/carros", methods=['POST'])
def incluir_carro():
    data = request.get_json()
    my_cursor = mydb.cursor()
    query = 'INSERT INTO carro (id, marca, modelo, ano) VALUES (%s, %s, %s, %s)'
    values = (data['id'], data['marca'], data['modelo'], data['ano'] )
    my_cursor.execute(query, values)
    mydb.commit()
    return jsonify({'message': 'Carro adicionado com sucesso'}), 201

@app.route("/carros/<int:id>", methods=['DELETE'])
def excluir_carro(id):
    my_cursor = mydb.cursor()
    query = 'DELETE FROM carro WHERE id = %s'
    my_cursor.execute(query, (id,))
    mydb.commit()
    return jsonify({'message': f'Carro de ID {id} removido com sucesso.'})

@app.route('/carros/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_carro(id):
    current_user_id = get_jwt_identity()

    user = UsersModel.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404


    data = request.json
    marca = data.get('marca')
    modelo = data.get('modelo')
    ano = data.get('ano')

    if modelo is None or marca is None or ano is None:
        return jsonify({'message': 'Campos: marca, modelo e ano são Obrigatorios'})
    my_cursor = mydb.cursor()
    query = 'UPDATE carro SET modelo = %s, marca = %s, ano = %s WHERE id = %s'
    values = (modelo, marca, ano, id)
    my_cursor.execute(query, values)
    mydb.commit()
    return jsonify({'message': f'Carro com o ID {id} atualizado!'})






app.run(debug=True)    