from mongokit import Connection,Document
import datetime

con=Connection()

@connection.register
class Project(Document):
    __collection__ = 'projects'
    __database__= 'VCAD'

    structure={
        'projectId': long,
        'projectName': basestring,
        'fileSize':int,
        'uploadedBy': int,
        'startDate': datetime.datetime,
        'endStart': datetime.datetime,
        'contributers': list,
        'clusters':[{
            'clusterId': long,
            'projectId': long,
            'status': basestring,
            'isdone': int,
            'createdOn': datetime.datetime,
            'jobs':[]
            }
            ]}
        
    gridfs = {
        'containers':['files','clusters'],
        }

@connection.register
class projectfiles(Document):
    structure={
    'referenceId': basestring
    }
    gridfs = {
    'containers':['file']
    }

@connection.register
class user(Document):
    __collection__ = 'users'
    __database__= 'VCAD'

    structure = {
        'userId':long,
        'name': basestring,
        'username': basestring,
        'password': basestring,
        'device':{
            'deviceId': long,
            'userId': long,
            'ram': basestring,
            }
        }

@connection.register
class Admin(Document):
    __collection__ = 'admin'
    __database__ = 'VCAD'

    structure = {
        'username': basestring,
        'password': basestring,
        'name': basestring,
        'email': basestring
        }
    
@connection.register
class logs(Document):
    __collection__ = 'logs'
    __database__= 'VCAD'

    structure = {
        'logId': long,
        'logType': basestring,
        }
    gridfs = {
        'containers': ['logs']
        }

