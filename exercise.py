import pickle
a = [[1], [2, 3]]
# f = open('output.txt', 'wb')
# pickle.dump(a, f)

f = open('outpro.txt', 'rb')
data = pickle.load(f)
print(data)