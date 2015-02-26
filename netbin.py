import socket
from multiprocessing.pool import Pool
import pingy

def ping(host):
    # ping = subprocess.Popen(['ping', '-w', '500', host],
    #                         stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # out, error = ping.communicate()
    # return (out, error)
    pingy.verbose_ping(host, 1, 1)
    return host


addresses = ['192.168.0.1', '192.168.0.2', '192.168.0.8'] # etc.
pool = Pool(10) # Increase number to increase speed and resource consumption
ping_results = pool.map(ping, addresses)
print(ping_results)

pool.close()
pool.join()


# def netbin(count, name):

	


# if __name__ == '__main__':
#     netbin()