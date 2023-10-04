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
        


@app.route("/vendas", methods=['POST'])
def incluir_carro():
    data = request.get_json()
    my_cursor = mydb.cursor()
    query = 'INSERT INTO carro (id, marca, modelo, ano) VALUES (%s, %s, %s, %s)'
    values = (data['id'], data['marca'], data['modelo'], data['ano'] )
    my_cursor.execute(query, values)
    mydb.commit()
    return jsonify({'message': 'Carro adicionado com sucerro'}), 201





app.run(debug=True)    