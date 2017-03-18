from DBConnection import DBConnection
import zipfile, shutil, os, csv
import datetime
import modex
import imp


db = DBConnection()

#---Log--------------------------------------------------------------
class Result(object):


	def validateResults(self):

		jobs = 0
		results = 0

		for job in db.jobs.find():
                        jobs = jobs + 1

                for file in os.listdir('results/'):
                        results = results + 1
                print jobs
                print results
                
                if jobs == results:
                        return 1
                else:
                        return 0


	def compileResults(self, filename):

		from resultScript import result

		result()


		return

