import hashlib

def user_db():
	user = open('user.txt', 'r')
	return_user = user.readlines()
	user.close()
	return return_user

def register_db(user, passwd):
	file_user = open('user.txt', 'w')
	file_user.write(user + '\n' + passwd)
	file_user.close()
	print('Pronto!')

def md5_hash(text):
	resp = hashlib.md5(text.encode()).hexdigest()
	return resp