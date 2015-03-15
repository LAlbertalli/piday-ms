import pickle

data = [pickle.load(open("%d.db"%i,"rb")) for i in xrange(1,5)]
d = data[0]+data[1][1:]+data[2][2:]+data[3][2:]
with open("0.db","wb") as f:
    pickle.dump(d,f)
