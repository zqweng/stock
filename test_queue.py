import threading
import queue
import animation_thread

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print("worker finish")
        q.task_done()

q = queue.Queue()
threads = []
num_worker_threads = 1

for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

#for item in source():
q.put([1])

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()

animation_thread.my_thread()