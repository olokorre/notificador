import mysql.connector, functions

class Data_Base(object):
    def __init__(self, user, passwd):
        self.mydb = mysql.connector.connect(user = user, passwd = passwd)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("use notificador")

    def create_user(self, user, real_name, passwd_text, type_account):
        passwd = functions.md5_hash(passwd_text)
        self.mycursor.execute('insert into users (user, name, passwd, type_account) values ("%s", "%s", "%s", "%s")' %(user, real_name, passwd, type_account))
        self.mydb.commit()
        return True

    def user_check(self, user, passwd_text):
        passwd = functions.md5_hash(passwd_text)
        list_users = []
        list_passwd = []
        self.mycursor.execute('select user, passwd from users')
        for i in self.mycursor:
            list_users.append(i[0])
            list_passwd.append(i[1])
        for i in range(len(list_users)):
            if list_users[i] == user and list_passwd[i] == passwd: return True
        return False
    
    def get_type_account(self, user):
        list_users = []
        list_types = []
        self.mycursor.execute('select user, type_account from users')
        for i in self.mycursor:
            list_users.append(i[0])
            list_types.append(i[1])
        for i in range(len(list_users)):
            if user == list_users[i]: return list_types[i]
        return None

    def get_name(self, user):
        list_users = []
        list_names = []
        self.mycursor.execute('select user, name from users')
        for i in self.mycursor:
            list_users.append(i[0])
            list_names.append(i[1])
        for i in range(len(list_users)):
            if user == list_users[i]: return list_names[i]
        return None

    def store_menssage(self, room, message):
        self.mycursor.execute('insert into chat (room, menssage) values ("%s", "%s")' %(room, message))
        self.mydb.commit()

    def get_menssage(self, room):
        menssage = ''
        self.mycursor.execute('select menssage from chat where room = "%s"' %(room))
        for i in self.mycursor:
            menssage += '%s\n' %(i)
        return menssage

if __name__ == "__main__":
    user = input("Usuario MySQL\n$ ")
    passwd = input("Senha do usuario MySQL\n$ ")
    mydb = mysql.connector.connect(user = user, passwd = passwd)
    mycursor = mydb.cursor()
    mycursor.execute('create database notificador')
    mycursor.execute('use notificador')
    mycursor.execute('create table users (user varchar(50) primary key, name varchar(50), passwd varchar(50), type_account varchar(50))')
    mycursor.execute('create table chat (id int(80) primary key auto_increment, room varchar(25), menssage varchar(80))')
    mydb.commit()
    functions.register_db(user, passwd)
    print('Tudo em dia!')