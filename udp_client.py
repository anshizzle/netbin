import sys
import socket
import math


# I used http://www.binarytides.com/programming-udp-sockets-in-python/
# to build and understand basic socket architecture
# 
# So the basics of creating the socket, connecting/binding it to a port, and sending and receiving data
# was copied from the site.
#
# The bulk of everything else was both research, Python documentation, and various stack overflow questions (usually for one or two minor lines like math.ceil)


PACKET_LENGTH  = 100.


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def send_message(msg, addr):
    # DETERMINE LENGTH OF MESSAGE
    try :
        #send the whole command
        s.sendto(msg, addr)
         
        # Get ACK from client
        package_acked = 0
        count = 1 #

        s.settimeout(.500)

        while not package_acked and count < 3:
            # print "Waiting for ACK for " + msg 
            try:
                d = s.recvfrom(1024)
                reply = d[0]
                if reply == "ACK":
                    package_acked = 1
            except socket.error:
                s.sendto(msg, addr)
                count = count + 1

        if count >= 3:
            contants.printError("Failed to send message.")


    except socket.error, msg:
        constants.printError("Failed to send message.")
        sys.exit() 

def receive_message():
    try:
        s.settimeout(None)
        length, addr = s.recvfrom(1024)
        try:
            length = int(length[1:])
        except ValueError:
            contants.printError("Invalid packet from server.")

        s.sendto("ACK", addr)
        

    except socket.error:
        contants.printError("Failed to receive message.")

    count = 0
    counter = 0
    message = ""
    s.settimeout(2.)

    while count < length:
        try:
            d = s.recvfrom(1024)
            data = d[0]
            addr = d[1]

            # If this is a resend of the length packet or a different packet,
            # Resend the ACK
            if data[0:1] == "l" or not int(data[0:1]) == counter:
                s.sendto("ACK", addr)
            else:
                message = message + data[1:]
                counter = (counter+1)%2
                count = count + 1
                s.sendto("ACK", (host, port))
                # print "PACKAGE ACKED"
        except socket.error:
            contants.printError("Failed to receive message.")

    return [message, addr]



#Check the number of arguments
if len(sys.argv) != 3:
	contants.printError("Invalid number of args.")

# Check if port is valid.
if not is_number(sys.argv[2]) or 1 > int(sys.argv[2]) or int(sys.argv[2]) > 65535:
	contants.printError("Invalid port.")


host = sys.argv[1]
port = int(sys.argv[2])
# print "Sending packets to" + host + ":" + `port`

# Create socket with UDP connection
try:
    # create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
 
print "Connected."

should_continue = 1
while should_continue:
    user_input = raw_input()
    command = ""
    send = 1
    if user_input == "exit":
        command = user_input
        should_continue = 0
        send = 0
    elif user_input == "help":
        print "I'm helping you"
    elif user_input.startswith("?"):
        command = user_input
        #TODO - CHECK IF KEY IS VALID
    elif user_input.startswith("list"):
        command = user_input
    elif "=" in user_input:
        #TODO - CHECK IF KEY IS VALID
        command = user_input
    else:
        print "ERROR: Invalid command."
        send = 0

    if send: 

        # Send Length
        length = int(math.ceil(len(command)/PACKET_LENGTH))
        # print "Packet length is " + `length`

        send_message("l" + `length`, (host, port))

        # Send the user command
        count = 0
        while count < length:
            send_message(`count%2` + command[count*int(PACKET_LENGTH):(count+1)*int(PACKET_LENGTH)], (host, port))
            count = count + 1

        response = receive_message()

        print response[0]




    

