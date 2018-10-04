"""
Intercommunication: Communication btw two process
"""
import multiprocessing

def pipe_handler(rd, wt):
    data=rd.recv()
    wt.send(data.upper())

def main():
    rd1, wt1 = multiprocessing.Pipe()
    rd2, wt2 = multiprocessing.Pipe()
    child = multiprocessing.Process(target=pipe_handler, args=(rd1, wt2))
    child.start()

    #Parent process, writes into the pipe
    payload = 'This is a sample string'
    wt1.send(payload)
    response = rd2.recv()

    print("sent : {}".format(payload))
    print("recv : {}".format(response))

if __name__ == '__main__':
    main()