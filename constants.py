import sys
LIST_INIT_PACKET_LENGTH = 64
LIST_FILE_PACKET_LENGTH = 1024
GEN_PACKET_LENGTH = 4096

HOST_PORT = 7878
LISTEN_PORT = 7900
COMMUNICATE_PORT = 7899
HOST_LISTEN_PORT = 6969
HOST_COMMUNICATE_PORT =6970


DOWNLOAD_CMDS = ["download", "dl"]
LIST_CMDS = ["list", "ls"]
UPLOAD_CMDS = ["upload", "up"]
EXIT_CMDS = ["exit", "quit", "q"]

FILE_END_SIGNAL = "ABCEOF12039!!^^"

INVALID_FILE_UPLOAD = "File not found"



def printError(error):
	print "ERROR: " + error + ' Terminating.\n'
	sys.exit()

