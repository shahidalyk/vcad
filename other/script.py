import csv

with open('data.csv') as file:
    data = [line.strip().split(',') for line in file]

nodes = dict()

for row in data:
    key = "%s %s" % (row[1],row[2])
    if nodes.has_key(key):
        nodes[key] += 1
    else:
        nodes[key] = 1

with open("myfile.txt", "w") as f:
    writer = csv.writer(f, delimiter=',')
    for i,j in nodes.iteritems():
        a = i[:2]
        b = i[-2:]
        writer.writerow([a,b,j])

print 'done'





