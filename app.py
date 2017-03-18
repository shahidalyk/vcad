from flask import Flask, render_template, redirect, url_for, request, make_response, send_from_directory, abort, flash, session
#from flask.ext.login import LoginManager
from werkzeug import secure_filename
from bson import ObjectId
from gridfs import GridFS
from gridfs.errors import NoFile
import os
import time
import shutil
import requests
import zipfile
from mongokit import Connection

#Project Files---------------------------------------------------------
from DBConnection import DBConnection
from Authentication import Admin
from Project import Project
from Result import Result
from Log import Log
import modex
import clustering


# initialize application
app = Flask(__name__)
app.config.from_object('config')
wsgi_app = app.wsgi_app

admin = Admin()
projectid = 0


#----------------------------------------------------------------------
#--- Views ------------------------------------------------------------
#----------------------------------------------------------------------

#--- Root -------------------------------------------------------------

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


#--- Dashboard --------------------------------------------------------

@app.route("/dashboard", methods = ['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = DBConnection()

    projects = 0
    files = 0
    jobs = 0
    users = 0
    completed = 0
    progress = 0
    #state = 'deactivated'

    for project in db.projects.find():
        projects = projects + 1

    for file in db.files.find({ 'type': 'fragment' }):
        files = files + 1

    for job in db.jobs.find():
        jobs = jobs + 1

    for user in db.users.find():
        users = users + 1

    for server in db.server.find():
        state = server['state']

    for job in db.jobs.find({ 'status': 'completed' }):
        completed = completed + 1

    try:
        progress = int((completed*100)/jobs)
    except:
        pass

    return render_template("dashboard.html", admin = admin, projects = projects, files = files, jobs = jobs, users = users, state = state, progress = progress)


#--- Project ------------------------------------------------------------

@app.route("/project", methods = ['GET', 'POST'])
def project():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = DBConnection()

    projects = 0
    files = 0
    jobs = 0
    users = 0
    
    for project in db.projects.find():
        projects = projects + 1

    for file in db.files.find({ 'type': 'fragment' }):
        files = files + 1

    for job in db.jobs.find():
        jobs = jobs + 1

    for user in db.users.find():
        users = users + 1

    return render_template("project.html", admin = admin, projects = projects, files = files, jobs = jobs, users = users)


#--- Statistics ---------------------------------------------------------

@app.route("/statistics", methods = ['GET'])
def statistics():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = DBConnection()

    projects = 0
    files = 0
    jobs = 0
    users = 0
    
    for project in db.projects.find():
        projects = projects + 1

    for file in db.files.find({ 'type': 'fragment' }):
        files = files + 1

    for job in db.jobs.find():
        jobs = jobs + 1

    for user in db.users.find():
        users = users + 1

    return render_template("statistics.html", admin = admin, projects = projects, files = files, jobs = jobs, users = users)


#--- Users --------------------------------------------------------------

@app.route("/users", methods = ['GET'])
def users():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = DBConnection()

    projects = 0
    files = 0
    jobs = 0
    users = 0
    
    for project in db.projects.find():
        projects = projects + 1

    for file in db.files.find({ 'type': 'fragment' }):
        files = files + 1

    for job in db.jobs.find():
        jobs = jobs + 1

    for user in db.users.find():
        users = users + 1
 
    def get_users():
        users = list()
        for user in db.users.find():
            users.append(user)
        return users

    return render_template("users.html", get_users = get_users, admin = admin, projects = projects, files = files, jobs = jobs, users = users)



#----------------------------------------------------------------------
#--- Admin Controls ---------------------------------------------------
#----------------------------------------------------------------------                       

#--- Start Project ----------------------------------------------------

@app.route("/startProject")
def startProject():
    global projectid
    db = DBConnection()

    # create new project

    for f in os.listdir('upload/'):
        filename = f
    project = Project(filename, admin.name)
    projectid = project.id

    # set server state
    server = db.server()
    server['state'] = 'activated'
    server.save()

    # create Logs
    
    log = Log()
    log.logProjectStart(project)
    log.logFragments(project.id, project.fragments)

    # request start middleware
    request = requests.post("http://localhost:8000/start/"+ str(projectid))
        

    #flash("clustering done")
    return redirect(url_for('dashboard'))



#--- Activate Project ----------------------------------------------------

@app.route("/activate")
def activateProject():

    db = DBConnection()

    for server in db.server.find():
        server['state'] = 'activated'
        server.save()

    # request activate project middleware
    request = requests.post("http://localhost:8000/activate/"+ str(projectid))
    print projectid

    flash('Project is activated.')

    return redirect(url_for('dashboard'))


#--- Deactivate Project ----------------------------------------------------

@app.route("/deactivate")
def deactivateProject():

    db = DBConnection()

    for server in db.server.find():
        server['state'] = 'deactivated'
        server.save()

    # request deactivate project middleware
    request = requests.post("http://localhost:8000/deactivate/"+ str(projectid))

    flash('Project is deactivated.')

    return redirect(url_for('dashboard'))



#--- Upload Data ------------------------------------------------------

@app.route("/upload", methods = ['GET', 'POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            if modex.check_extensions(filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      # file uploaded
            else:
                if modex.check_zip(filename):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))      # file uploaded
                    
                    if modex.check_zipextensions(filename):
                        flash('Project Uploaded.')
                        startProject()
                        return redirect(url_for('dashboard'))
                    else:
                        flash("Incompatible Files in ZIP")
                        
                else:
                    print "Incompatible files"
                    flash("Incompatible files")
            
            return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

#--- Download Fragments -------------------------------------------

@app.route("/download")
def download():
    #try:
    #    print"hello"
    #    db = con.VCAD
    #    gfs = GridFS(db)
    #    f1 = gfs.find_one({'filename': "hello.py"})
    #    #f1 = gfs.get(ObjectId('56bba794a7bfe8f122dfbc89'))
    #    response = make_response(f1.read())
    #    response.headers['Content-Type'] = 'application/octet-stream'
    #    response.headers["Content-Disposition"] = "attachment; filename={}".format("hello.py")
    #    #response.mimetype = f1.content_type
    #    return response
    #except:
    #    print "error"
    #return
    #for file in os.listdir('fragments/'):
        #response = make_response('fragments/'+file)
        #response.headers['Content-Type'] = 'application/octet-stream'
        #response.headers["Content-Disposition"] = "attachment; filename={}".format("hello.py")
        #return response

    shutil.make_archive('upload/final_results', 'zip', 'download/')
    #os.remove('download/final_results.txt')
    return send_from_directory('upload/', 'final_results.zip', as_attachment=True)


#--- Admin Login ------------------------------------------------------

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
        flash('Already Logged in.')

    error = None
    user = {}
    if request.method == 'POST':
        
        if admin.login( request.form['username'], request.form['password'] ):
            session['username'] = request.form['username']
            flash("Logged in")
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed")
            return render_template("publicbase.html")
    return render_template("publicbase.html")


#--- Admin Logout -----------------------------------------------------

@app.route("/logout")
def logout():
    if 'username' not in session:
        return redirect(url_for('login'))
    session.pop('username', None)
    
    flash('Logged out.')

    return redirect(url_for("login"))


#--- Admin Registration -----------------------------------------------

@app.route("/signup", methods = ['POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        if admin.signup( request.form['username'], request.form['password'], request.form['name'], request.form['email'] ):
            flash("Signed up")
            return redirect(url_for('login'))
        else:
            flash("User exists")
            request.form['username']
            return redirect(url_for('login'))
    #return render_template("publicbase.html")




#----------------------------------------------------------------------
#--- Web Services (Requests to Middleware) ----------------------------
#----------------------------------------------------------------------

#--- Get State --------------------------------------------------------

@app.route("/getState", methods = ['GET'])
def getState():
    db = DBConnection()
    state = 'none'
    for server in db.server.find():
        state = server['state']
    return state


#--- Delete -----------------------------------------------------------

@app.route("/delete", methods = ['GET'])
def delete():
    db = DBConnection()
    
    for file in os.listdir('upload/'):
        os.remove('upload/' + file)

    for file in os.listdir('download/'):
        os.remove('download/' + file)

    for file in os.listdir('fragments/'):
        os.remove('fragments/' + file)

    for file in os.listdir('results/'):
        os.remove('results/' + file)

    request = requests.post("http://localhost:8000/delete")

    db.con.vcad.drop_collection('projects')
    db.con.vcad.drop_collection('files')
    db.con.vcad.drop_collection('jobs')

    flash('Project Deleted.')

    return redirect(url_for('dashboard'))                     



#----------------------------------------------------------------------
#--- Web Services (Requests from Middleware) ----------------------------
#----------------------------------------------------------------------

#--- Get State --------------------------------------------------------

@app.route("/result/<int:id>", methods = ['GET', 'POST'])
def result(id):

    db = DBConnection()

    for index, file in enumerate(db.files.find({'projectid': id, 'type': 'result'})):
        docid = file['_id']
        for result in db.con.vcad.fs.files.find({'docid' : docid}):
            f = db.files.fs.get(result['_id'])
            filename = 'results/' + str(file['name']) + '.zip'
            zipResults = open(filename, 'wb')
            zipResults.write(f.read())
            zipResults.close()

    with zipfile.ZipFile(filename, "r") as z:
        z.extractall("results/")
        #z.close()
        
    os.remove(filename)

    result = Result()

    # Validate Results
    if result.validateResults():
        
        # Compile Results
        result.compileResults(filename)

        # Send Final Results to user
        download()

    else:
        print 'incomplete results sent from the middleware.'
        flash('incomplete results sent from the middleware.')


    return redirect(url_for('dashboard')) 



#----------------------------------------------------------------------
#--- Utility Functions ------------------------------------------------
#---------------------------------------------------------------------- 

#--- Download Data ----------------------------------------------------

@app.route('/uploads/<path:filename>')
def download_file(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


#--- Clustering -------------------------------------------------------

def is_clustered(filename):
    for a in proj.find({'projectName':filename}):
        if a['fragments'] == []:
            return 1
    return 0



#----------------------------------------------------------------------
#--- Application Settings ---------------------------------------------
#---------------------------------------------------------------------- 

if __name__ == '__main__':
    app.config.from_object('config')
    app.run(debug=True)


