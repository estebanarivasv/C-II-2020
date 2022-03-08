## System design decisions
### Table of contents
- [Setting server socket's ip address as 0.0.0.0](#setting-server-socket-s-ip-address-as-0000)
- [Authentication mechanism](#authentication-mechanism)
- [Data model and data persistence](#data-model-and-data-persistence)
- [Why threads and not processes?](#why-threads-and-not-processes-)
- [Threads as demons](#threads-as-demons)
- [Manager().list() vs multiprocessing.Queue](#manager--list---vs-multiprocessingqueue)
- [Pipes](#pipes)

### Setting server socket's ip address as 0.0.0.0
Setting local server IPv4 address as 0.0.0.0, lets the server listen to all IPv4 addresses on the local machine. This helps to achieve a distributed and scalable system where you can even connect with your phone.

### Authentication mechanism

The server asks the operator for the username and password. Once it has those values, the server checks if the operator exists in the database. If the user does exist, it compares that entity's password with the given password. If those variables match, the server sends an "OK" message. Otherwise, the server sends an error.

### Data model and data persistence

In the file located in `server/main/models/operator.py`, I defined the table to be created when the connection with the database is made if it doesn't exist.

I used a MySQL server in a Docker container because of its simplicity and its lack of a local server configuration.  

### Why threads and not processes?

As processes implement the true parallelism, because the jobs are executed simultaneously, and their execution is orchestrated by the OS, they can be heavyweight.

I chose to work with threads because I don't need parallelism. I just need the server admits users implementing concurrency, letting each thread process connections and finish at the same time other users connect to the server. 

When I run the system with `threading.Thread` and `multiprocessing.Process`, I noticed the threads were requiring less memory space.

### Threads as demons
I also preferred to work with threads as demons too. Every time I terminate the server `app.py`, the threads handling the socket connections stop.

### Manager().list() vs multiprocessing.Queue

First, I implemented a `multiprocessing.Queue` to share sockets. I couldn't get it to work because socket instances are not pickable. For more info, check: https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled

Then, I tried to simulate a FIFO Queue with a plain `List`. The problem was that it wasn't being shared between threads. So I had to implement a `multiprocessing.Manager().list()` where its `Manager()` object controls a server process that holds Python objects and allows other processes to manipulate them using proxies. This last item let me append and consume PipeService instances which were used between threads to communicate messages.

### Pipes

I used pipes to communicate threads and establish a synchronic communication between them. These pipes are the body of the chat.