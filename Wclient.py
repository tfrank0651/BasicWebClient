"""
Tyler Frank
zaf455
UTSA CS 6543
Program 2
2/23/2022

Description: Modify the skeleton Web Client to throttle the Web Server when receiving data from a GET request.

Accomplished by:
	- Reducing the Client Receive Window size to 64 bytes (note that UTSA VM has a minimum of 1152)
	- Adding sleep timer when processing data from the Server
	- Adding a for loop when processing data from the Server

Results:
	- When requesting a 1450 byte file, the client receives the first ~1,000 bytes.
	The client then sends a Window Full message. The Server then sends several Keep-Alive messages and receives
	multiple ZeroWindow messages. Once the client has processed the data in the receive buffer, a TCP
	Window Update is sent, and the remainder of the file is sent by the server.
"""


from socket import * # Import socket module
import sys, os, errno, time

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

clientSocket = socket(AF_INET, SOCK_STREAM)
# Use the setsockopt to set the socket's receive buffer to 64 bytes
# Note that the VM has a minimum window size of 1152 bytes, which will be observed in wireshark
clientSocket.setsockopt(SOL_SOCKET, SO_RCVBUF, 64)

# Assign a port number
# serverPort = 6789

if len(sys.argv) < 4:
	print("Usage: python3 " + sys.argv[0] + " serverAddr serverPort filename")
	sys.exit(1)
serverAddr = sys.argv[1]
serverPort = int(sys.argv[2])
fileName = sys.argv[3]

# Connect to the server
try:
	clientSocket.connect((serverAddr,serverPort))
except error as e:
	print("Connection to server failed. " + str(e))
	sys.exit(1)

print('------The client is ready to send--------')
print(str(clientSocket.getsockname()) + '-->' + str(clientSocket.getpeername()))

try:
	getRequest = "GET /" + fileName + " HTTP/1.1\r\nHost: " + serverAddr + "\r\n"
	getRequest = getRequest + "Accept: text/html\r\nConnection: keep-alive\r\n"
	getRequest = getRequest + "User-agent: RoadRunner/1.0\r\n\r\n"
	clientSocket.send(getRequest.encode()) 
	# clientSocket.send(("GET /" + fileName + " HTTP/1.1\r\n").encode()) 
	# clientSocket.send(("Host: " + serverAddr + "\r\n").encode())
	# clientSocket.send("Accept: text/html\r\n".encode())
	# clientSocket.send("Connection: keep-alive\r\n".encode())
	# clientSocket.send("User-agent: RoadRunner/1.0\r\n\r\n".encode())
except error as e:
	print("Error sending GET request: " + str(e))
	clientSocket.close()
	sys.exit(1)

message = ""
while True:
	try:	
		
		newPart = clientSocket.recv(64)
		message = message + newPart.decode()
		# Added .5s sleep to slow the application's processing of data
		time.sleep(0.5)
		if not newPart:
			print(message, flush=True)
			break
		if message[len(message)-1] != "\n":
			# added a loop to slow the application's processing of data
			x = 0
			for i in range(50):
				x = x + 1
			continue
		else:
			print(message, flush=True)
			message = ""
	except error as e:
		print('Error reading socket: ' + str(e))
		sys.exit(1)
	except KeyboardInterrupt:
		print("\nInterrupt signal was received. Client has stopped")
		sys.exit(1)

clientSocket.close()  
sys.exit(0) 
