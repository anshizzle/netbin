import socket
from multiprocessing.pool import Pool
import pingy
import netbin_host
import netbin_client
import sys
import netifaces
import re
import constants
from timeit import default_timer as timer


def ping(host):
	return pingy.verbose_ping(host, .5, 1)



start = timer()
pool = Pool(75)
lNodes = {}
pAddress = []

##FIND THE SUBNET MASK
subnet = ""
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


pAddress.extend(range(1, 255))
pAddress = [subnet + str(address) for address in pAddress]

results = pool.map(ping, pAddress)

print [result for result in results if result[0] > 0]
hostAddr = ""
for ip in results:
	if ip[0] > 0:
		print "IP:", ip[0], "Delay:", ip[1], "ms"
		 ##if you take out this check will take 150 seconds to run!!!!
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.5)
			result = sock.connect_ex((ip[0], constants.HOST_PORT))
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






if hostAddr: 
	## empty strings falsify
	## another node is already host
	print "host found! at:", hostAddr
	netbin_client.start(hostAddr, constants.HOST_PORT)

else:
	netbin_host.start(constants.HOST_PORT)



print
print "RUNTIME: ", (timer()- start)