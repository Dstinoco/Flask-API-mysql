import mysql.connector
from passlib.hash import pbkdf2_sha256

mydb = mysql.connector.connect(user='root', 
                               password='bart1234',
                               host='localhost',
                               database='db_carros')

email = input("Digite o Email :")
senha1 = input("Digite sua senha: ")
senha2 = input("Repita sua senha: ")


if senha1 == senha2:
    password = pbkdf2_sha256.hash(senha1)

    query = f"INSERT INTO users_model (email, password) VALUES ('{email}', '{password}')"
    cursor = mydb.cursor()
    cursor.execute(query)
    mydb.commit()

else:
    print('Senhas incorretas')


print("Sucesso!")
