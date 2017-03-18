file = open("data.txt")
s = file.read()
l = s.strip()
l = l.split("\n")
l = l[1:]
ls = [e.split('\t') for e in l]
