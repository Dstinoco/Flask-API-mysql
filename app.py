from flask import Flask, jsonify, request
import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(user='root', password='bart1234',
                              host='localhost',
                              database='db_carros')
app = Flask(__name__)


@app.route('/carros', methods=['GET'])
def consultar_carros():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM carro')
    todas_vendas = my_cursor.fetchall()
    columns = [column[0] for column in my_cursor.description]
    pandas_df = pd.DataFrame(todas_vendas, columns=columns)
    pandas_df = pandas_df.to_dict(orient='records')
    return jsonify(pandas_df[:5])
    
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
def atualizar_carro(id):
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