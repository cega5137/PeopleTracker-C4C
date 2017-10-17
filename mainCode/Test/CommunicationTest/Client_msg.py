from socket import * import time import subprocess import signal

def init_client(host, port):
    # Initializes the client
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    
    #
    # Perform anything you need to to set up the clients here, i.e.. ultra sonic sensor code
    #
    
    return connectToServer(host, port)

def connectToServer(host, port):
    # Connects to Server
    s=socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            s.connect((host, port))
            print "socket connected!!"
            time.sleep(2)
            break
        except:
            print "not connection found will try again in 2 seconds..."
            time.sleep(2)
    return s


def runClient(soc):
    #Main Loop
    while True:
        # Take Measurment
        data = 'Station Current Total'#getdata()
        
        if len(data) == 0:
            continue
        
        # Attempt to send to server
        bits_written = soc.send(data)#write(data)

        if bits_written == 0: # Assume Server closed connection, close socket and attempt to connect to server again
            soc.close()
            soc = connectToServer(host, port)


def cleanup(soc):
    # Close Socket
    if (soc > 0):
        soc.close()
    # Shutdown pi
    shutdownRPi()

def shutdownRPi():
    print "Shutting down"
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


######################################################################
################################### Main #############################
######################################################################
host = "10.0.0.150" #ip address of the server
port = 2004
print "hostname: ", host, " Portnumber: ", port

# Initalize Client
soc = init_client(host, port)
runClient(soc)
cleanup(soc)





