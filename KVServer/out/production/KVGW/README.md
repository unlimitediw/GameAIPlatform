# KV Store

KV store is implemented with Java. It consists of 4 parts:
 - KVStoreServer is the server side
 - KVStoreClient is the client side
 - PerformanceEveluate is the performance test client side 
 - Common is the shared library used by all above  

KVStoreServer uses blocking TCP sockets, multiple threads to receive the requests from the clients and execute the requests, then responses to the clients. The
current supported operations/commands are: SET, GET, STATS, MULTISET, MULTIGET. Every accepted client will be processed by a new single thread. The server supports 
binary based protocols and text based protocols. For binary based protocols, the server listen 6666 port; for test based protocols, the server listen 5555. To start
the server, use  ./Server

KVStoreClient uses blocking TCP sockets, single thread to send request and receive the response. It also supports binary based protocols and text based protocols.
The client starting command is:
	./Client <server_ip> <server_port> <operation> <key> <value> 
server_port is 5555 or 6666. operation supports SET, GET, MULTISET, MULTIGET. <key> are at most 64 characters long, <value> are at most 1KB long. key, value 
are strings used depending on whether it is a GET, SET, MULTIGET, or MULTISET. For example: 
	./Client 127.0.0.1 5555 SET "xiaoming" "hello" 
will set "xiaoming" as the key, "hello" as the value to the KV storer with the text based protocols.
	./Client 127.0.0.1 6666 GET "xiaoming" 
will get the value of "xiaoming" from the KV storer with the binary based protocols
	./Client 127.0.0.1 5555 MULTIGET "xiaoming" "lilei" "hanmeimei" 
will get the value of "xiaoming", "lilei", "hanmeimei" from the KV storer with the text based protocols.
	./Client 127.0.0.1 6666 MULTISET "xiaoming" "hello" "lilei" "how are you" "hanmeimei" "nice to meet you"
will set "xiaoming", "lilei", "hanmeimei" with their value "hello", "how are you", "hanmeimei" to the KV storer respectively.
	./Client 127.0.0.1 5555 STATS
will return the count of objects currently stored in the KV storer

Group Members:
 - Xiaosu Lyu
 - Xingyu Zhang
 - Wentao Li
 - Xu Mo

Extra Features:
 - feature 1
	Support MULTISET operation that allows several key/value pairs to be added in a single connection
 - feature 2
	Support MULTIGET operation that allows several key/value pairs to be retrieved in a single connection
 - feature 3
	Support binary based protocols by listenning 6666 port on server side
	
 ## Protocol Description
 - Text based protocols format
	operation + whitespace + key + whitespace + value + whitespace + key + whitespace + value + ... + "\n"
	All segments are represented by ASCII characters seperated with a whitespace, ending with "\n". 
	Since we use whitespace to be a delimiter, the value content cannot contain whitespace if use MULTISET operation. 
	
 - Binary based protocols format
	Each communication package is formatted with (2 bytes package length + package content), in which each package content is formatted with (2 bytes content length + content + 2 bytes content length + content + ...
	In binary based protocols, there is no limitation of value part cannot contain whitespace. Any content in binary based protocols is formatted with 2 bytes content length + content.
 
 ## Performance Evaluation
 
