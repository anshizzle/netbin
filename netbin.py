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
from thread import *



def send_is_host_query(subnet, sock, m_range):
	for i in m_range:
		sock.sendto("ISHOST", (subnet+str(i), constants.LISTEN_PORT))	
	




start = timer()
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
chunk_size = len(pAddress)/15
address_groups = [pAddress[i:i+chunk_size] for i in range(0, len(pAddress), chunk_size)]
# pAddress = [subnet + str(address) for address in pAddress]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for li in address_groups:
	start_new_thread(send_is_host_query, (subnet, sock, li, ))

sock.settimeout(1)
try:
	hostAddr = sock.recv(1024)
except socket.error:
	hostAddr = ""


if hostAddr: 
	## empty strings falsify
	## another node is already host
	print "host found! at:", hostAddr
	netbin_client.start(hostAddr, constants.HOST_PORT)

else:
	netbin_host.start(constants.HOST_PORT)



print
print "RUNTIME: ", (timer()- start)