from queue import Queue
pq = Queue(maxsize=10000)
pq.put(1)
print(pq.qsize())
pq.put(2)
t1 = pq.get()
print(t1)
t2 = pq.get()
print(t2)