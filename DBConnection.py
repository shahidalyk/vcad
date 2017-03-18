from mongokit import Document, Connection
#from pymongo import MongoClient
import config
import datetime

# Schema-----------------------------------------------------------------------
class Project(Document):
    __collection__ = 'projects'
    __database__= 'vcad'

    structure = {
        'id': int,
        'name': basestring,
        'fileSize': long,
        'admin': basestring,
        'startDate': datetime.datetime,
        'endDate': datetime.datetime,
        'volunteers': list,
        'state' : basestring,
        'fragments': list,
        }
        
    gridfs = {
        'containers':['file'],
        }

class Files(Document):
    __collection__ = 'files'
    __database__= 'vcad'

    structure = {
        'projectid': int,
        'name': basestring,
        'docid' : basestring,
        'type' : basestring
    }
    gridfs = {
        'containers':['file']
    }

class Job(Document):
    __collection__ = 'jobs'
    __database__= 'vcad'

    structure = {
        'projectid': int,
        'name': basestring,
        'status': basestring,
        'docid' : basestring
    }

class User(Document):
    __collection__ = 'users'
    __database__= 'vcad'

    structure = {
        'id':int,
        'name': basestring,
        'email': basestring,
        'status': basestring,
        'androidos': basestring,
        'ram': basestring,
        }

class Admin(Document):
    __collection__ = 'admins'
    __database__ = 'vcad'

    structure = {
        'username': basestring,
        'password': basestring,
        'name': basestring,
        'email': basestring
        }
    
class Log(Document):
    __collection__ = 'logs'
    __database__= 'vcad'

    structure = {
        'logId': long,
        'logType': basestring,
    }
    #gridfs = {
    #    'containers': ['logs']
    #}

class Server(Document):
    __collection__ = 'server'
    __database__= 'vcad'

    structure = {
        'state': basestring,
    }


# DBConnection class---------------------------------------------------------------
class DBConnection(object):

    def __init__(self):
        #mongodb_uri = "mongodb://13.76.244.22:27017"
        #mongolab_uri = "mongodb://shahid:sakmongo054@ds062818.mlab.com:62818/MongoLab-25"
        connectionString = 'insert mongodb uri here'
        #self.client = MongoClient(mongolab_uri,
        #             connectTimeoutMS=30000,
        #             socketTimeoutMS=None,
        #             socketKeepAlive=True)
        #self.db = self.client.get_default_database()
        #self.con = Connection(mongodb_uri)
        self.con = Connection()

        self.con.register([Project])
        self.con.register([Files])
        self.con.register([Job])
        self.con.register([User])
        self.con.register([Admin])
        self.con.register([Log])
        self.con.register([Server])

        self.projects = self.con.Project
        self.files = self.con.Files
        self.jobs = self.con.Job
        self.users = self.con.User
        self.admins = self.con.Admin
        self.logs = self.con.Log
        self.server = self.con.Server

    def __del__(self):
        self.con.close()
        self.con.disconnect()

    def connect():        
        con = Connection()
        projects = con.vcad.projects
        admins = con.vcad.admin
        con.register([Project])
        return

    def disconnect():
        return

