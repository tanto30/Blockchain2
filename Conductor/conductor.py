from socket import socket
from subprocess import Popen, CREATE_NEW_CONSOLE
from queue import Queue, Empty
from threading import Thread


def find_free_port():
    s = socket()
    s.bind(('', 0))
    return s.getsockname()[1]


processes = []

# def enqueue_output(out, queue):
#     for line in iter(out.readline, b''):
#         queue.put(line)
#     out.close()

while (True):
    cmd = input()
    cmd = [a.strip() for a in cmd.split()]
    if not cmd:
        continue
    if cmd[0] == "run":
        num = int(cmd[1])
        for i in range(num):
            port = find_free_port()
            # processes.append()
            processes.append(Popen("python ../Node " + str(port), shell=True, creationflags=CREATE_NEW_CONSOLE))
            # q = Queue()
            # t = Thread(target=enqueue_output, args=(processes[i].stdout, q))
            # t.daemon = True
            # t.start()
            print("Started node instance on port " + str(port))
            # while True:
            #     print(processes[i].stdout.readline())
    elif cmd[0] == "stop":
        for process in processes:
            process.terminate()
    # elif cmd[0] == "debug":
    #     try:
    #         output = q.get_nowait()
    #     except Empty:
    #         pass
    #     else:
    #         print(output)
