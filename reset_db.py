import mysql.connector, functions

user = functions.user_db()
mydb = mysql.connector.connect(user = user[0], passwd = user[1])
mycursor = mydb.cursor()
mycursor.execute('drop database notificador')
mycursor.execute('create database notificador')
mycursor.execute('use notificador')
mycursor.execute('create table users (user varchar(50) primary key, name varchar(50), passwd varchar(50), type_account varchar(50))')
mydb.commit()

print('Pronto!')