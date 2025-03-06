#TrainResFunEx1.py
#An small code with treads 
import threading,time
def  reservation(nos):
	L.acquire()
	global totnos
	if(nos>totnos):
		print("Hi:{}, {} Seats are Not Available--Try Next Time".format(threading.current_thread().name,nos))
		time.sleep(2)
	else:
		totnos=totnos-nos
		print("Hi:{}, {} Seats are  Reserved--Happy Journey".format(threading.current_thread().name,nos))
		time.sleep(2)
		print("\tNow Available Number of Seats:{}".format(totnos))
	L.release()

#main program
L=threading.Lock()
totnos=10
print("\tTOTAL NUMBER OF SEATS:{}".format(totnos))
p1=threading.Thread(target=reservation,args=(4,))
p1.name="surya"
p2=threading.Thread(target=reservation,args=(7,))
p2.name="chandu"
p3=threading.Thread(target=reservation,args=(4,))
p3.name="shiva"
p4=threading.Thread(target=reservation,args=(3,))
p4.name="Sumanth"
p5=threading.Thread(target=reservation,args=(2,))
p5.name="Vinod"
p6=threading.Thread(target=reservation,args=(2,))
p6.name="mani"
#dispatch the threads
p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()