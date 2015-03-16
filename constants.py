import sys

GEN_PACKET_LENGTH = 1024

HOST_PORT = 7878
LISTEN_PORT = 7900
COMMUNICATE_PORT = 7899
HOST_LISTEN_PORT = 6969
HOST_COMMUNICATE_PORT =6970


DOWNLOAD_CMDS = ["download", "dl"]
LIST_CMDS = ["list", "ls"]
UPLOAD_CMDS = ["upload", "up"]
EXIT_CMDS = ["exit", "quit", "q"]

FILE_END_SIGNAL = "EOFAFD12039!!^^"
LIST_ITEM_DELIMITER = "|,.|"

NETBIN_DIR = "Netbin/"

INVALID_FILE_UPLOAD = "File not found"

HOST_COMM_ERROR = "There was an error communicating with the host"
NO_FILES_STRING =  "No files currently on netbin"


def list_file_num_string(num):
	return str(num) + " files on netbin currently"



def printError(error):
	print "ERROR: " + error + '.\n'
	sys.exit()

