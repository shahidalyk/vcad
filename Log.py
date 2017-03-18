from DBConnection import DBConnection
import zipfile, shutil, os, csv
import datetime
import modex


db = DBConnection()

#---Log--------------------------------------------------------------
class Log(object):


	

	def logProjectStart(self, project):
	
		file = open('logs/projects.csv', 'a')
		file.write(str(project.id) + "," + str(project.name) + "," + str(project.fileSize) + "," + str(project.admin) + "," + str(project.startDate) + "," + str(project.state) + "," + str(datetime.datetime.now()) + "\n")
		file.close()

		return


	def logFragments(self, projectId, fragments):
	
		file = open('logs/fragments.csv', 'a')

		for fragment in fragments:
			file.write(str(fragment['id']) + "," + str(projectId) + "," + str(fragment['size']) + "," + str(fragment['time']) + "," + str(datetime.datetime.now()) + "\n")
		file.close()

		return


	def logProjectUsers(self, user):

		file = open('logs/users.csv', 'a')
		file.write(str(user['id']) + "," + str(user['name']) + "," + str(user['email']) + "," + str(user['androidos']) + "," + str(user['ram']) + "," + str(datetime.datetime.now()) + "\n")
		file.close()

		return


	def logJob(self, job):
			
		file = open('logs/jobs.csv', 'a')
		file.write(str(job['projectId']) + "," + str(job['name']) + "," + str(job['status']) + "," + str(job['user']) + "," + str(datetime.datetime.now()) + "\n")
		file.close()

		return


	def logDevices(self, user, status):
			
		file = open('logs/devices.csv', 'a')

		if status == 'online':
			file.write(str(status) + "," + str(user['id']) + "," + str(user['name']) + "," + str(user['androidos']) + "," + str(user['ram']) + "," + str(datetime.datetime.now()) + "\n")

		elif status == 'offline':
			file.write(str(status) + "," + str(user['id']) + "," + str(user['name']) + "," + str(user['androidos']) + "," + str(user['ram']) + "," + str(datetime.datetime.now()) + "\n")
			
		file.close()

		return