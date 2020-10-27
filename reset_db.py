import mysql.connector, functions

user = functions.user_db()
mydb = mysql.connector.connect(user = user[0], passwd = user[1])
mycursor = mydb.cursor()
mycursor.execute('drop database notificador')
mycursor.execute('create database notificador')
mycursor.execute('use notificador')
mycursor.execute('create table users (user varchar(25) primary key, name varchar(25), passwd varchar(25), type_account varchar(25))')
mydb.commit()

print('Pronto!')