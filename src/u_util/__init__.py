def execute(func, msg, *arg, **karg):
    """ informing user before and after executing function """
    print(msg, end=" ", flush=True)
    func(*arg, **karg)
    print("Done")
