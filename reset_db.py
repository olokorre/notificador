import mysql.connector, functions

user = functions.user_db()
mydb = mysql.connector.connect(user = user[0], passwd = user[1])
mycursor = mydb.cursor()
mycursor.execute('drop database notificador')
mycursor.execute('create database notificador')
mycursor.execute('use notificador')
mycursor.execute('create table users (user varchar(50) primary key, name varchar(50), passwd varchar(50), type_account varchar(50))')
mycursor.execute('create table chat (id int(80) primary key auto_increment, room varchar(25), menssage varchar(80))')
mycursor.execute('create table classroom (class_ varchar(2) primary key)')
for turma in range(3):
    mycursor.execute('insert into classroom (class_) values ("%sF")' %(turma + 1))
    mycursor.execute('create table %sF (studant varchar(80) primary key, N1 int(2), N2 int(2), N3 int(2))' %(turma + 1))
mycursor.execute('create table questionnaires (id varchar(50) primary key, name varchar(80), detais varchar(100), visible varchar(3) default "no")')
mydb.commit()

print('Pronto!')