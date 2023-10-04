from flask import Flask, jsonify, request
import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(user='root', password='bart1234',
  host='localhost',
  database='empresa')





my_cursor = mydb.cursor()
my_cursor.execute('SELECT * FROM vendas')
todas_vendas = my_cursor.fetchall()
columns = [column[0] for column in my_cursor.description]
pandas_df = pd.DataFrame(todas_vendas, columns=columns)
