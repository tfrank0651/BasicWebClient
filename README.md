This program is a basic web client that is modified to demonstrate TCP flow control. This was achieved by using 
```python
clientSocket.setsockopt(SOL_SOCKET, SO_RCVBUF, 64)
``` 
to limit the size of the Receive Buffer and then adding a loop with 
```python 
time.sleep(0.5)
``` 
to increase the time for the client to process the packet.
