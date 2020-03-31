import multiprocessing
from multiprocessing import Process
import os

def child1():
    print("Child 1",os.getpid())
    os.system("ps fax")


if __name__=="__main__":
    print("Parent ID",os.getpid())
    p1=Process(target=child1)
    p1.run()
    print("========================================================")
    print("Parent ID",os.getpid())
    p1.start()
    p1.join()
	

    print("We're done")
