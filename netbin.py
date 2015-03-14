import socket
from multiprocessing.pool import Pool
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
		try:
			sock.sendto("ISHOST", (subnet+str(i), constants.LISTEN_PORT))
		except socket.error:
			print "Socket Error:" + subnet+str(i) 
	
	
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
chunk_size = len(pAddress)/16
address_groups = [pAddress[i:i+chunk_size] for i in range(0, len(pAddress), chunk_size)]
print str(address_groups)
# pAddress = [subnet + str(address) for address in pAddress]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for li in address_groups:
	start_new_thread(send_is_host_query, (subnet, sock, li, ))

sock.settimeout(1)
while 1:
	try:
		result, addr = sock.recvfrom(1024)
		print "Result from host"
		print result
		print str(addr)
		if result == "IAMHOST":
			sock.sendto("ACK", addr)
			hostAddr = addr[0]
			break
		else:
			hostAddr = ""
	except socket.error:
		hostAddr = ""
		break

sock.close()


if hostAddr: 
	## empty strings falsify
	## another node is already host
	print "host found! at:", hostAddr
	netbin_client.start(hostAddr, constants.HOST_PORT)

else:
	netbin_host.start(constants.HOST_PORT)



print
print "RUNTIME: ", (timer()- start)