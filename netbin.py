import socket
from multiprocessing.pool import Pool
import pingy

import sys
import netifaces
import re
from timeit import default_timer as timer

import netbin_host
import netbin_client


import client_function_handler
import host_function_handler

def ping(host):
	return pingy.verbose_ping(host, .5, 1)



start = timer()
pool = Pool(75)
lNodes = {}
pAddress = []
subnet = ""
prompt = ""


##FIND THE SUBNET MASK
enArray = [ x for x in netifaces.interfaces() if x.startswith('en') ]
if(enArray):
	for en in enArray:
		print netifaces.ifaddresses(en).keys()
		bcTuple = netifaces.ifaddresses(en)
		if (2 in bcTuple):
			print bcTuple[2]
			if ('broadcast' in bcTuple[2][0]):
				subnet = re.match("^\d+.\d+.[^.]", bcTuple[2][0]['broadcast']).group(0)+'.'

				break

## IF NO SUBNET FOUND, TERMINATE

if(subnet == ""):
	print("NO SUBNET FOUND!")
	sys.exit()



#PING ALL ADDRESSES IN SUBNET, FIND HOST
pAddress.extend(range(1, 255))
pAddress = [subnet + str(address) for address in pAddress]
PORT = 7878

results = pool.map(ping, pAddress)
pool.terminate()
print [result for result in results if result[0] > 0]

hostAddr = ""
for ip in results:
	if ip[0] > 0:
		print "IP:", ip[0], "Delay:", ip[1], "ms"
		 ##if you take out this check will take 150 seconds to run!!!!
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.5)
			result = sock.connect_ex((ip[0], PORT)) ##7878 random port number
			if result == 0:
				## port open! host found
				hostAddr = ip[0]
				# print "Port {}: \t Open".format(port)
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

# IF WE FIND A HOST, RUN NETBIN CLIENT
if hostAddr: 
	## empty strings falsify
	## another node is already host
	print "host found! at:", hostAddr
	netbin_client.start(hostAddr, 7878)

#ELSE YOURE A HOST, start HOST PROCESS
else:
	netbin_host.start(7878)



print
print "RUNTIME: ", (timer()- start)