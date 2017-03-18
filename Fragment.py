from DBConnection import DBConnection
import zipfile, os, csv
import datetime
import modex


db = DBConnection()

#---Fragment--------------------------------------------------------------
class Fragment(object):

	@staticmethod
	def fragments(filename):
	    ext = filename.split(".")[-1]
	    flag = 0
	    if ext in modex.python_extensions:
	        Fragment.simple_files(filename)
	    elif ext in modex.compression_extensions:
	        zipfilename = open('upload/'+filename,'r')
	        z = zipfile.ZipFile(zipfilename)
	        exts= [name.split(".")[-1] for name in z.namelist()]
	        for e in modex.data_extensions:
	            if e in exts:
	                flag = 1
	        if flag==1:
	            Fragment.dataFragments(filename)
	        else:
	            Fragment.simple(filename)

	@staticmethod
	def simple_files(filename):
		return
    
	#---------------------------------------------------------------------
	@staticmethod
	def simple(filename):
	    with zipfile.ZipFile('upload/'+filename, "r") as z:
	    	z.extractall("temp/")
	    return
	
	#----------------------------------------------------------------------
	@staticmethod
	def dataFragments(filename):
	    with zipfile.ZipFile('upload/'+filename, "r") as z:
	        pyfile = ""
	        z.extractall("temp/")
	        for files in os.listdir("temp/"):
	        	if files.split(".")[-1] in modex.python_extensions:
	           		pyfile = files

	      	for a in os.listdir("temp/"):
	            if a.split(".")[-1] in modex.data_extensions:
	            	with open("temp/"+a, "r") as datafile:
		                reader = csv.reader(datafile,delimiter = ',', quoting=csv.QUOTE_NONE, quotechar='')
		                data = list(reader)
		                row_count = len(data)
		                row_limit = int((row_count*20)/100)
		                org_row_limit = row_limit
		                starting_row = 0
		                limit = int(row_count/row_limit)
		                for d in range(1,limit+1):
			                myfile = open("fragments/"+filename.split('.')[0]+str(d)+".csv" , "w")
			                wr = csv.writer(myfile,quoting = csv.QUOTE_NONE, quotechar='')
			                wr.writerows(data[starting_row:row_limit])
			                starting_row = row_limit
			                row_limit = row_limit+org_row_limit
			                myfile.close()
			                z = zipfile.ZipFile("fragments/"+filename.split('.')[0]+"_Fragment_"+str(d)+".zip",'w')
			                z.write("temp/"+pyfile)
			                z.write("fragments/"+filename.split('.')[0]+str(d)+".csv")
			                z.close()
			                os.remove("fragments/"+filename.split('.')[0]+str(d)+".csv")
	              	for a in os.listdir("temp/"):
	                	os.remove("temp/"+a)
	    return
	#---------------------------------------------------------------------------------

	@staticmethod
	def saveFragmentsDb():
		for file in os.listdir('fragments/'):
			f = open('fragments/' + file)
			newfile = db.projectfiles.ProjectFiles()
			newfile['referenceId'] = file
			newfile.save()
			newfile.fs.file.put(f)

		return #for file in os.listdir('fragments/'):

	@staticmethod
	def getFragmentsList():
		for file in db.projectfiles.find():
			print file
		return

	@staticmethod
	def getFragments():
		for file in db.projectfiles.ProjectFiles.fs.find():
			print file

		for f in db.projectfiles.ProjectFiles.find({'referenceId' : 'Codes_Cluster_1.zip'}):
			ff =  f.fs.file.get_last_version()
			print ff.read()

		return

	def __init__(self):
		self.size = 0
		self.time = datetime.datetime.now()
		self.state = ''		

	def login(self, username, password):
		for admin in db.admins.find({ 'username': username, 'password': password }):
			if admin is None:
				return 0
			else:
				self.username = admin['username']
				self.email = admin['email']
				self.name = admin['name']
				return 1


	def logout():
		flash = "You are logged out."
		return redirect(url_for("login"))