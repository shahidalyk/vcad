import csv, os, operator

def result():
    final = dict()

    for file in os.listdir('results/'):
        with open('results/' + file) as file:
            data = [line.strip() for line in file]

            for row in data:
                key = row.rsplit(',', 1)[0]
                val = row.rsplit(',', 1)[1]
                if final.has_key(key):
                    final[key] += int(val)
                else:
                    final[key] = int(val)

    with open("download/final_results.txt", "w") as f:
        writer = csv.writer(f, delimiter=',')
        for i,j in final.iteritems():
            a = i[:2]
            b = i[-2:]
            print [a,b,j]
            writer.writerow([a,b,j])




