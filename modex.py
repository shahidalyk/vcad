import os, zipfile

data_extensions  =['csv','xlxs','xlx','txt']
compression_extensions = ['zip']
python_extensions = ['py','pyc','pyw']


def check_zipextensions(filename):
    ext = filename.split(".")[-1]
    if ext in compression_extensions:
        f = open('upload/'+filename, 'rb')
        z = zipfile.ZipFile(f)
        exts= [name.split(".")[-1] for name in z.namelist()]
        for e in exts:
            if e not in python_extensions and e not in data_extensions and e not in compression_extensions:
                return 0
        return 1
    else:
        return 0

def check_extensions(filename):
    if filename.split(".")[-1] in python_extensions:
        return 1
    else:
        return 0

def check_zip(filename):
    if filename.split(".")[-1] in compression_extensions:
        return 1
    else:
        return 0
