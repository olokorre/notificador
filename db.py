import mysql.connector

class Data_Base(object):
    def __init__(self, user, passwd):
        self.mydb = mysql.connector.connect(user = user, passwd = passwd)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("use notificador")

    def create_user(self, user, real_name, passwd, type_account):
        self.mycursor.execute('insert into users (user, name, passwd, type_account) values ("%s", "%s", "%s", "%s")' %(user, real_name, passwd, type_account))
        self.mydb.commit()
        return True

    def user_check(self, user, passwd):
        self.mycursor.execute('select * from users')
        list_of_users = []
        list_passwd = []
        for i in self.mycursor:
            list_of_users.append(i[0])
            list_passwd.append(i[1])
        for i in list_of_users:
            for l in list_passwd:
                if user == i and passwd == l: return True
        return False