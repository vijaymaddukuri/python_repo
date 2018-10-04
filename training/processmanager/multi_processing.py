import multiprocessing

def task_set():
    p_id = multiprocessing.current_process().ident
    p_name=multiprocessing.current_process().name

    print ("child {} : {}".format(p_name, p_id))


def main():
    p_id = multiprocessing.current_process().ident
    print("Parent process id : {}".format(p_id))

    for item in range(1,6):
        p = multiprocessing.Process(target=task_set)
        p.start()
    for child in multiprocessing.active_children():
        child.join()
    print("{} terminates".format((multiprocessing.current_process().name)))
if __name__ == '__main__':
    main()