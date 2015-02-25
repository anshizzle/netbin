import click
import sys
import socket

def printError(error):
	print "ERROR: " + error + '\nTerminating.'
	sys.exit()




@click.command()
@click.option('--port', default=8000, help='Port that host server should run on.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')


def netbin_host(port):
	s = socket.socket()
	host = socket.gethostname()
	# Bind socket to port
	try:
	    s.bind((host, port))
	except socket.error, msg:
		printError('Could not bind port.')

	s.listen(5)
	print 'Now listening '

	while 1:

		#Accept the connection
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

		#Variable that indicates the connection should be closed
		should_close = 0

		while not should_close:
			data = conn.recv(1024)
			#Handle input
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
					 


			else:
				response = 'ERROR: Invalid command.'

			conn.sendall(response)
			print "Response sent: "
			print response
			response = ""
		 
		print 'Closing connection with ' + addr[0] + ':' + str(addr[1])
		conn.close()

	s.close()



if __name__ == '__main__':
    netbin_host()