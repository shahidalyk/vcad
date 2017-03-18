import vcaddb
db = con.VCAD.projects
class clusters:
    clusterNum
    clusterOf
    clusterState

    def create_cluster(path,project):
        for e in db.find({filename:project}):
            



        return

    def get_cluster(clusterNum):
        #getCluster from db
        return
    def get_cluster_State(clusterNum):
        #get state from db
        return

    def is_done(cluster):
        #check if done
        return
    
        
        



class Transitioner:
    serverState

    def setServerState():
        return

    def getServerState():
        return

    def getMiddlewareState():
        return


class Admin:
    username
    password
    email

    def login():
    return

    def logout():
    return        