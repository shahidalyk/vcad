#clustering Module
import modex
import zipfile,os,csv
def clustering(filename):
    ext = filename.split(".")[-1]
    flag = 0
    if ext in modex.python_extensions:
        simple_files(filename)
    elif ext in modex.compression_extensions:
        zipfilename = open('upload/'+filename,'rb')
        z = zipfile.ZipFile(zipfilename)
        exts= [name.split(".")[-1] for name in z.namelist()]
        for e in modex.data_extensions:
            if e in exts:
                flag = 1
        if flag==1:
            data_clustering(filename)
        else:
            simple(filename)
#--------------------------------------------------------------------
def simple_files(filename):
    return
    
#---------------------------------------------------------------------
def simple(filename):
    with zipfile.ZipFile('upload/'+filename, "r") as z:
      z.extractall("temp/")
    return
#----------------------------------------------------------------------
def data_clustering(filename):
    with zipfile.ZipFile('upload/'+filename, "r") as z:
      pyfile = ""
      z.extractall("temp/")
      for files in os.listdir("temp/"):
        if files.split(".")[-1] in modex.python_extensions:
          pyfile = files

      for a in os.listdir("temp/"):
            if a.split(".")[-1] in modex.data_extensions:
              with open("temp/"+a, "r") as datafile:
                reader = csv.reader(datafile,delimiter = ',')
                data = list(reader)
                row_count = len(data)
                row_limit = (row_count*20)/100
                org_row_limit = row_limit
                starting_row = 0
                limit = row_count/row_limit
                for d in range(1,limit+1):
                  myfile = open("clusters/"+filename.split('.')[0]+str(d)+".csv" , "wb")
                  wr = csv.writer(myfile,quoting = csv.QUOTE_ALL)
                  wr.writerows(data[starting_row:row_limit])
                  starting_row = row_limit
                  row_limit = row_limit+org_row_limit
                  z = zipfile.ZipFile("clusters/"+filename.split('.')[0]+"_Cluster_"+str(d)+".zip",'w')
                  z.write("temp/"+pyfile)
                  z.write("clusters/"+filename.split('.')[0]+str(d)+".csv")
                  myfile.close()
                  z.close()
                  os.remove("clusters/"+filename.split('.')[0]+str(d)+".csv")
              for a in os.listdir("temp/"):
                os.remove("temp/"+a)
                  


    return
#---------------------------------------------------------------------------------