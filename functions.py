def user_db():
	user = open('user.txt', 'r')
	return_user = user.readlines()
	user.close()
	return return_user