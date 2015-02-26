import socket
from multiprocessing.pool import Pool
import pingy
from timeit import default_timer as timer

def ping(host):
	return pingy.verbose_ping(host, .5, 1)



start = timer()
pool = Pool(75)
lNodes = {}
pAddress = []
subnet = "192.168.0"
pAddress.extend(range(1, 255))
pAddress = [subnet + str(address) for address in pAddress]

results = pool.map(ping, pAddress)

for ip in results:
	if ip[0] > 0:
		print ip[0]
		if not ip[0] != "192.168.0.01":
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				result = sock.connect_ex((ip[0], 7878)) ##7878 random port number
				if result == 0:
				    print "Port {}: \t Open".format(port)
				sock.close()

			except KeyboardInterrupt:
			    print "You pressed Ctrl+C"
			    sys.exit()

			except socket.gaierror:
			    print 'Hostname could not be resolved. Exiting'
			    sys.exit()

			except socket.error:
			    print "Couldn't connect to server"
			    sys.exit()

print(timer()- start)