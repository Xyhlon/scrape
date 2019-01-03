import multiprocessing


def multiprocess(func):
    print('processing')

    def wrapper(*args, **kwargs):
        processes = []
        for i in range(multiprocessing.cpu_count()):
            p = multiprocessing.Process(target=func, args=[args], kwargs=kwargs)
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        return func(*args, **kwargs)

    return wrapper
