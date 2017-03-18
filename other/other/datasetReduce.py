file = open("data.csv")
s = file.read()
l = s.strip()
l = l.split("\n")
l = l[2:]
a = [e.split(',') for e in l]



#for e in dist.keys():
 #   print '{axis:"' + e + '", value:' + str(dist[e]) + '},'
