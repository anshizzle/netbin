#!/usr/bin/python

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



# I MADE THE PACKET LENGTH 100 characters because that's pretty much guaranteed to be under 1024 bytes.
# It may not be the most efficient, but it works, which is what we're being graded on :)
PACKET_LENGTH = 100.


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_valid_key(key):
    if len(key) == 0 or "?" in key or "=" in key or "\n" in key:
        return False
    else:
        return True
        

def is_valid_value(value):
    if "\n" in value:
        return False
    else:
        return True


def send_message(msg, addr):
    # DETERMINE LENGTH OF MESSAGE
    print "SENDING " + msg
    try :
        #send the whole command
        s.sendto(msg, addr)
         
        # Get ACK from client
        package_acked = 0
        count = 1 #message has already been sent once

        s.settimeout(.500)

        while not package_acked and count < 3:
            print "Waiting for ACK " + msg
            try:
                d = s.recvfrom(1024)
                reply = d[0]
                if reply == "ACK":
                    package_acked = 1
                    print "PACKAGE WAS ACKED"
            except socket.error:
                s.sendto(msg, addr)
                count = count + 1

        if count >= 3:
            printError("Failed to send message.")


    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit() 

def receive_message():
    try:
        s.settimeout(None)
        length, addr = s.recvfrom(1024)
        try:
            length = int(length[1:])

        except ValueError:
            printError("Invalid packet from server.")


        s.sendto("ACK", addr)

    except socket.error:
        printError("Failed to receive message.")


    print "INCOMING MESSAGE OF LENGTH " + `length`
    count = 0
    counter = 0
    message = ""
    s.settimeout(2)

    while count < length:
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

            s.sendto("ACK", addr)

    return [message, addr]


# Used http://www.binarytides.com/programming-udp-sockets-in-python/ to
# Build basic socket architecture.

if len(sys.argv) != 2:
    printError("Invalid number of args.")
    sys.exit()
if not is_number(sys.argv[1]) or 1 > int(sys.argv[1]) or int(sys.argv[1]) > 65535:
    printError("Invalid port.")
    sys.exit()

# Empty dictionary to implement the key value store
my_dictionary = {}


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
port = int(sys.argv[1])


# Bind socket to port
try:
    s.bind((host, port))
except socket.error, msg:
    printError('Could not bind port.')

print "Listening on " + host + ":" + `port`


#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    data, addr = receive_message()
    print "RECEIVED MESSAGE: " + data

    #####
    # The densest block of code - also present in server_python_tcp.py
    # 
    #   Checks the received input and sends back the appropriate response from the server
    #   
    #####


    if data == "exit":
        print "RECEIVED CLOSE CONNECTION REQUEST"
        should_close = 1
        break
    elif data.startswith('?'):
        # User is querying for a key
        print "RECEIVED QUERY KEY VALUE REQUEST"
        key = data[1:]
        if is_valid_key(key):
            if key in my_dictionary:
                response = key + '=' + my_dictionary[key]
            else:
                response = key + '='
        else:
            response = "ERROR: Invalid command."
    elif '=' in data:
        print 'RECEIVED MODIFY KEY VALUE REQUEST'
        key, value = data.split('=', 1)
        print 'key: ' + key
        print 'value: ' + value
        if is_valid_key(key) and is_valid_value(value):
            my_dictionary[key] = value
            response = 'OK'
        else:
            response = "ERROR: Invalid command."
    # Called list
    elif data == 'list':
        print 'RECEIVED LIST REQUEST'
        response = ""
        for key, value in my_dictionary.iteritems():
            response = response + key + '=' + value + '\n'
        response = response[:-1]
    # Called listc
    elif data.startswith('listc'):
        print 'RECEIVED LISTC REQUEST'
        print data
        command = data.split(' ', 2)
        if len(command) > 1 and len(command) <= 3 and is_number(command[1]):
            print "Valid listc command"
            num_to_print = int(command[1])
            print "Num to Print = " + `num_to_print`
            start_index = -1
            if len(command) == 3:
                # Handle continuation key
                continuation_key = command[2]

                # If the continuation key is valid, start index is the continuation key
                if is_number(continuation_key) and int(continuation_key) < len(my_dictionary):
                    start_index = int(continuation_key)
                else:
                    response = "BAD KEY"

            # If there is no continuation key, then start at 0
            else: 
                start_index = 0
            # Get dictionary of items to print, starting from the estart index

            if start_index != -1:
                response = ""
                items_to_print = my_dictionary.items()[start_index:]
                print "Start Index: " + `start_index`
                print "Printing " + `num_to_print` + " items"
                print items_to_print
                for key, value in items_to_print[:num_to_print]:
                    response = response + key + '=' + value + '\n'

                if num_to_print >= len(items_to_print):
                    response = response + 'END'
                else:
                    response = response + `start_index+num_to_print`
        else:
            response = "ERROR: Invalid command"

    #####
    #
    # SEND THE RESPONSE.
    # 1. Figure out the number of packets it would take
    # 2. Send that
    # 3. Break up the response and send the packets
    #
    #####


    #SEND THE LENGTH
    length = int(math.ceil(len(response)/PACKET_LENGTH))

    # print "SENDING LENGTH VALUE " + `length`

    send_message("l" + `length`, addr)

    # print "SENDING RESPONSE:\n" + response
    # Send the RESPONSE
    count = 0
    while count < length:
        # print "SENDING PACKET " + `count` + ": " + `count%2` + response[count*PACKET_LENGTH:(count+1)*PACKET_LENGTH]
        send_message(`count%2` + response[count*int(PACKET_LENGTH):(count+1)*int(PACKET_LENGTH)], addr)
        count = count + 1



s.close()
