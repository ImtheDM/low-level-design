import threading, time

resourceA = threading.Lock()
resourceB = threading.Lock()

def func1():
    
    with resourceA:
        print("Executing func1...")
        time.sleep(0.05)
        print("Fetchin lock b")

        with resourceB:
            print("Got both locks, exec completed")

    print("func1 completed")

def func2():

    with resourceB:
        print("Executing func2...")
        time.sleep(0.05)
        print("Fetchin lock a")

        with resourceA:
            print("Got both locks, exec completed")

    print("func1 completed")

def main():
    
    t1 = threading.Thread(target=func1)
    t2 = threading.Thread(target=func2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    main()