from DBConnection import DBConnection
db = DBConnection()
#---Login--------------------------------------------------------------
class Admin(object):

	def __init__(self):
		self.username = ''
		self.name = ''
		self.email = ''		

	def login(self, username, password):
		for admin in db.admins.find({ 'username': username, 'password': password }):
			if not admin:
				return 0
			else:
				self.username = admin['username']
				self.email = admin['email']
				self.name = admin['name']
				return 1


	def logout():
		flash = "You are logged out."
		return redirect(url_for("login"))


	def signup(self, username, password, name, email):

		for admin in db.admins.find({ 'username': username }):
			if not admin:
				admin = db.admins()
				admin['username'] = username
				admin['password'] = password
				admin['name'] = name
				admin['email'] = email
				admin.save()
				return 1
			else:
				return 0
				
		admin = db.admins()
		admin['username'] = username
		admin['password'] = password
		admin['name'] = name
		admin['email'] = email
		admin.save()
		return 1