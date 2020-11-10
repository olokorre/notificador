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

    def whats_class(self, studant, classroom):
        class__ = []
        for i in range(len(classroom)):
            studants = []
            self.mycursor.execute('select studant from %s' %(classroom[i]))
            for l in self.mycursor: studants.append(l[0])
            if studant in studants: class__.append(classroom[i])
            else: class__.append('N/A')
        return class__

    def user_exist(self, user):
        list_users = []
        self.mycursor.execute('select user from users')
        for i in self.mycursor:
            list_users.append(i[0])
        if user in list_users: return False
        else: return True

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

    def return_studanst(self):
        name = []
        type_account = []
        self.mycursor.execute('select name, type_account from users;')
        for i in self.mycursor:
            if i[1] == 'Aluno':
                name.append(i[0])
                type_account.append(i[1])
        name.sort()
        return name

    def configure_classroom(self, studant, class_):
        pass

    def return_classroom(self):
        self.mycursor.execute('select class_ from classroom')
        classroom = []
        for i in self.mycursor: classroom.append(i[0])
        return classroom

if __name__ == "__main__":
    user = input("Usuario MySQL\n$ ")
    passwd = input("Senha do usuario MySQL\n$ ")
    mydb = mysql.connector.connect(user = user, passwd = passwd)
    mycursor = mydb.cursor()
    mycursor.execute('create database notificador')
    mycursor.execute('use notificador')
    mycursor.execute('create table users (user varchar(50) primary key, name varchar(50), passwd varchar(50), type_account varchar(50))')
    mycursor.execute('create table chat (id int(80) primary key auto_increment, room varchar(25), menssage varchar(80))')
    mycursor.execute('create table classroom (class_ varchar(2) primary key)')
    for turma in range(3):
        mycursor.execute('insert into classroom (class_) values ("%sF")' %(turma + 1))
        mycursor.execute('create table %sF (studant varchar(80) primary key, N1 int(2), N2 int(2), N3 int(2))' %(turma + 1))
    mydb.commit()
    functions.register_db(user, passwd)
    print('Tudo em dia!')