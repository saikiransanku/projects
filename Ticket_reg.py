#TrainResFunEx1.py
#It is an seat booking on bus . I had used the threads for develop them.
import threading, time

def reservation(nos):
    # Optional: Input validation for non-positive seat requests
    if nos <= 0:
        print("Hi:{}, Invalid request: Cannot reserve {} seats. Please request a positive number.".format(threading.current_thread().name, nos))
        return

    global totnos
    # Use 'with L:' for safer and more Pythonic lock handling
    with L:
        if nos > totnos:
            print("Hi:{}, {} Seats are Not Available--Try Next Time".format(threading.current_thread().name, nos))
            time.sleep(2) # Simulating a delay for processing the failed attempt
        else:
            totnos = totnos - nos
            print("Hi:{}, {} Seats are Reserved--Happy Journey".format(threading.current_thread().name, nos))
            time.sleep(2) # Simulating a delay for processing the successful reservation
            print("\tNow Available Number of Seats:{}".format(totnos))

# main program
L = threading.Lock()
totnos = 10
print("\tTOTAL NUMBER OF SEATS:{}".format(totnos))

# Define and name threads
p1 = threading.Thread(target=reservation, args=(4,), name="surya")
p2 = threading.Thread(target=reservation, args=(7,), name="chandu")
p3 = threading.Thread(target=reservation, args=(4,), name="shiva")
p4 = threading.Thread(target=reservation, args=(3,), name="Sumanth")
p5 = threading.Thread(target=reservation, args=(2,), name="Vinod")
p6 = threading.Thread(target=reservation, args=(2,), name="mani")

# Dispatch the threads
p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()
