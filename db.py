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

    def user_exist(self, user):
        list_users = []
        self.mycursor.execute('select user from users')
        for i in self.mycursor: list_users.append(i[0])
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

    def configure_classroom(self, studant, class_):
        classroom = self.return_classroom()
        for i in classroom: self.mycursor.execute('delete from %s where studant = "%s"' %(i, studant))
        self.mycursor.execute('insert into %s (studant, N1, N2, N3) values ("%s", 0, 0, 0)' %(class_, studant))
        self.mydb.commit()

    def return_studants_by_class(self, class_):
        studants = []
        self.mycursor.execute('select studant from %s' %(class_))
        for i in self.mycursor: studants.append(i[0])
        studants.sort()
        return studants

    def return_class_by_studant(self, studant):
        classroom = self.return_classroom()
        for i in classroom:
            studants = []
            self.mycursor.execute('select studant from %s' %(i))
            for l in self.mycursor: studants.append(l[0])
            if studant in studants: return i
        return ''

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

    def return_classroom(self):
        self.mycursor.execute('select class_ from classroom')
        classroom = []
        for i in self.mycursor: classroom.append(i[0])
        return classroom

    def return_studants_to_fix(self):
        studants = self.return_studanst()
        studants_in_class = []
        studants_to_fix = []
        for i in self.return_classroom():
            self.mycursor.execute('select studant from %s' %(i))
            for i in self.mycursor: studants_in_class.append(i[0])
        for i in studants:
            if not i in studants_in_class: studants_to_fix.append(i)
        studants_to_fix.sort()
        return studants_to_fix
    
    def return_grades_to_studant(self, studant):
        class_ = self.return_class_by_studant(studant)
        if class_ == '': return []
        else:
            self.mycursor.execute('select * from %s' %(class_))
            for i in self.mycursor:
                if studant == i[0]: grades = [i[0], i[1], i[2], i[3]]
            return grades
    def return_grades_to_teacher(self, class_):
        grades = []
        self.mycursor.execute('select * from %s' %(class_))
        for i in self.mycursor: grades.append([i[0], i[1], i[2], i[3]])
        return grades

    def create_quiz(self, name, id_):
        self.mycursor.execute('insert into questionnaires (id, name, detais) values ("%s", "%s", "Novo questionário")' %(id_, name))
        self.mycursor.execute('create table detais_%s (position int(2) primary key, question varchar(191), type varchar(50), options varchar(191))' %(id_))
        self.mycursor.execute('create table resp_%s (id int(5) primary key auto_increment, studant varchar(191), position int(2), resp varchar(191))' %(id_))
        self.mycursor.execute('create table submit_%s (studant varchar(191) primary key)' %(id_))
        self.mydb.commit()

    def list_questionnaires(self):
        questionnaires = []
        self.mycursor.execute('select * from questionnaires')
        cont = 0
        for i in self.mycursor:
            questionnaires.append([i[0], i[1], i[2], i[3], cont])
            cont += 1
        return questionnaires

    def is_questionnaires(self, id_):
        questionnaires = []
        self.mycursor.execute('select id from questionnaires')
        for i in self.mycursor: questionnaires.append(i[0])
        if id_ in questionnaires: return True
        else: return False

    def delete_quiz(self, quiz):
        self.mycursor.execute('delete from questionnaires where id = "%s"' %(quiz))
        self.mycursor.execute('drop table detais_%s' %(quiz))
        self.mycursor.execute('drop table resp_%s' %(quiz))
        self.mycursor.execute('drop table submit_%s' %(quiz))
        self.mydb.commit()

    def get_data_by_quiz(self, quiz):
        data = []
        self.mycursor.execute('select * from questionnaires where id = "%s"' %(quiz))
        for i in self.mycursor: data.append([i[1], i[2], i[3]])
        self.mycursor.execute('select * from detais_%s' %(quiz))
        for i in self.mycursor: data.append([i[0], i[1], i[2], i[3]])
        return data

    def save_data_by_quiz(self, quiz, local, data):
        if local == 'meta':
            self.mycursor.execute('update questionnaires set detais = "%s" where id = "%s"' %(data, quiz))
        elif local == 'yes' or local == 'no':
            self.mycursor.execute('update questionnaires set visible = "%s" where id = "%s"' %(data, quiz))
        elif local == 'simple':
            position = []
            self.mycursor.execute('select position from detais_%s' %(quiz))
            for i in self.mycursor: position.append(i[0])
            if position == []: n = 1
            else: n = int(position[-1]) + 1
            self.mycursor.execute('insert into detais_%s (position, question, type) values (%s, "%s", "simple")' %(quiz, n, data))
        self.mydb.commit()

    def save_resp(self, quiz, resp, position, studant):
        jota = False
        id_ = ''
        self.mycursor.execute('select studant, position, id from resp_%s' %(quiz))
        for i in self.mycursor:
            print(i[0], studant, i[1], position)
            if studant == i[0] and str(position) == str(i[1]):
                jota = True
                id_ = str(i[2])
        if jota: self.mycursor.execute('update resp_%s set resp = "%s" where id = "%s"' %(quiz, resp, id_))
        else: self.mycursor.execute('insert into resp_%s (studant, position, resp) values ("%s", "%s", "%s")' %(quiz, studant, position, resp))
        self.mydb.commit()
    
    def return_resp_by_user(self, user, position, quiz):
        resp = ''
        self.mycursor.execute('select resp, position from resp_%s where studant = "%s"' %(quiz, user))
        for i in self.mycursor:
            if position == str(i[1]): resp = i[0]
        return resp

    def return_resp_submit(self, quiz):
        studants = []
        self.mycursor.execute('select studant from submit_%s' %(quiz))
        for i in self.mycursor: studants.append(i[0])
        return studants
    
    def return_resp_by_studant(self, studant, quiz):
        resps = []
        self.mycursor.execute('select resp from resp_%s where studant = "%s"' %(quiz, studant))
        for i in self.mycursor: resps.append(i[0])
        return resps

    def submit_quiz(self, quiz, studant):
        self.mycursor.execute('insert into submit_%s (studant) values ("%s")' %(quiz, studant))
        self.mydb.commit()

    def is_submit(self, studant):
        submits = []
        questionnaires = []
        studants_submit = []
        self.mycursor.execute('select id from questionnaires')
        for i in self.mycursor: questionnaires.append(i[0])
        for i in questionnaires:
            self.mycursor.execute('select studant from submit_%s' %(i))
            for l in self.mycursor: studants_submit.append(l[0])
            if studant in studants_submit: submits.append('yes')
            else: submits.append('no')
        return submits

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
    mycursor.execute('create table questionnaires (id varchar(50) primary key, name varchar(191), detais varchar(191), visible varchar(3) default "no")')
    mydb.commit()
    functions.register_db(user, passwd)
    print('Tudo em dia!')