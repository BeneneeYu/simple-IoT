# Client-server Networking

This is a project The client is an Internet of Things (IoT) artifact in the form of an edge-based intelligent/smart refrigerator. It is edge-based because the refrigerator is installed in homes/RVs, which sit at the edge of the network. It is IoT-enabled because it is assumed to include a variety of sensors and networking support. 

Our smart refrigerator periodically sends two different types of messages to two different servers. The first message type that it can send out is a *Grocery Order* to a Grocery Server. The second message type that it can send is a *Health Status* to a Health Status Server. The servers in our assignment are very simple and respond with minimal information. The Grocery Server simply acknowledges with an “Order Placed” reply while the Health Status Server always responds with a “You Are Healthy”  reply. I mimic one such smart refrigerator, one Grocery Server and one Health Status server.

# Operation

Pad serialized buffer of order/status with bytes to make **1MB application-level packet (only for the requests)**

Impose a Maximum Transfer Unit **(MTU) to 16 bytes,** 1MB packet is divided to 64 16-byte chunks, order of which must be guaranteed.

For the **GoBackN and SelectiveRepeat**, the size of sliding window to **8 chunks** at a time. For alternating bit, the size of the window is always 1 chunk. 

Integrate skeleton code with dealer-router scaffolding code

no loss or delay of packets, but set artificial blocks:

## Strategy

In the **network layer** of our skeleton code, when the **REQ** socket on the client or the **DEALER** socket in each intermediate router is ready to forward the chunk to the next hop, using random number logic, either

(a) send the chunk to the next hop

(b) delay it

(c) just don’t send it at all and drop it.

# System

## Structure

/SkeletonCode

applnlayer/ApplnMessageTypes: define data classes and printing function

applnlayer/CustomApplnProtocol: base class of client/server, implements functions to send/receive application objects, send/receive request/response based on network layer

serialize_flatbuffer: (De)serialize based on flatbuffer

serialize_json:(De)serialize based on json

### Refrigerator

generates requests and send to servers

Holds a grocery store server appln object and a health status center appln object (Instance of CustomApplnProtocol).

Appln object holds an instance of CustomTransportProtocolObject.

CustomTransportProtocolObject holds a NWProtoObj, use IP and Port passed from upper layer.

To send appln message, use CustomTransportProtocolObject to send. CustomTransportProtocolObject sends segement using networkObject to send packet. NetworkObj uses socket created when initialized to send.


```
GroceryOrderServer (say 10.0.0.5:5555)
- groc_obj (ApplnProtoObj)
-- xport_obj (XPortProtoObj)
--- nw_obj (NWProtoObj)
---- socket (zmq.DEALER) (should be 10.0.0.2:4444)

HealthStatusServer (say 10.0.0.6:5555)
- health_obj (ApplnProtoObj)
-- xport_obj (XPortProtoObj)
--- nw_obj (NWProtoObj)
---- socket (zmq.DEALER) (should be 10.0.0.2:4444)
```

```
send_grocery_order
- xport_obj.send_appln_msg
-- send_segment
--- nw_obj.send_packet
---- socket.send (say 10.0.0.5:5555)

Order server will respond and send response to 10.0.0.5:5555
recv_response
- xport_obj.recv_appln_msg
-- recv_segment
--- nw_obj.recv_packet
---- socket.recv (say 10.0.0.5:5555)
```

### grocery_server

Instantiate a CustomApplnProtocol to act as server, continuously listening to requests and respond (needs IP and Port).

Holds an instance of ApplnProtoObj, grocery_obj.

To receiver, use method **recv_request** in ApplnProtoObj. 

**Recv_request** will use **recv_appln_msg** in xport_obj, an instance of CustomTransportProtocol.

**Recv_appln_msg** will use **recv_segment**, recv_segment will use recv_packet in nw_obj, an instance of CustomNetworkProtocol.

```
grocery_obj (ApplnProtoObj)
- xport_obj (XPortProtoObj)
-- nw_obj (NWProtoObj)
--- socket (zmq.REP)
```

### health_server

Very alike to grocery_server

### **Client**

**appln_obj.send_order**=>**xport_obj.send_appln_smg**=>**send_segment**=>**nw_obj.send_packet**=>**socket.send**

### **Server**

**appln_obj.recv_request**=>**xport_obj.recv_appln_msg**=>**recv_segment**=>**nw_obj.recv_packet**=>**socket.recv**

## Unit

**Segment**: A segment is the unit of end-to-end transmission in the TCP protocol. A segment consists of a TCP header followed by application data. A segment is transmitted by encapsulation inside an IP datagram.

**IP Datagram**: An IP datagram is the unit of end-to-end transmission in the IP protocol.

**Packet**: A packet is the unit of data passed across the interface between the internet layer and the link layer.

**Frame**: A frame is the unit of transmission in a link layer protocol.

data=>segment=>packet=>frame

## Implementation

### Collect end-to-end latency data

Create field `ts` for message, when server receive a message, get the time for receving it by get the time difference between time now and `ts`.

# Flatbuffers

## Data structure

Struct, Table, root_type, union

## Use steps

1. Use CMake to compile FlatBuffers and generate flatc
2. Define data structure using Schema, use flatc to compile Schema and get source code
3. Use API of source code to manipulate data

two types of message types: ORDER and HEALTH (just like GET, PUT etc in http)

ORDER - grocery_server - Order Placed
Health Status - health_server - You Are Healthy

- Extend the message formats as required by the writeup
- Define Flatbuffer schema and generated serialization code for the schema
- JSON dictionary for the same message format

Pass specific type message parameters to functions directly, do not try to wrap.
Wrapping is the implementation in serialization/deserialization.

## Schema

1. Define enums for the message type in a separate fbs file.
2. Include that fbs file in three separate files,
3. One each for the grocery order, health status and response table definitions where each of those are their own root types.
4. All of them use the same namespace. Then give all these files as arguments to a single invocation of flatc --python.

# Work Done

implement reliable transfer in transport layer using different policies

no flow/congestion control

Use REQ socket at client, REQ socket at server, and DEALER-ROUTER socket at router.

Every node append it's host name at front for 

network layer: append addr, dst IP,

transport layer: append ack

ZMQ packet: identity, null, payload

payload: [n/w adr dst IP] [transport seq] [appln payload]

In CustomTransportProtocol:

In send_appln_msg, append the original message, break chunks and use send_segment

request: [zmq.IDENTITY, _ , message]

ZMQ_REQ: when sending message, ZMQ inserts an empty frame at the front of message, when receiving the message, it removes the empty frame at front, return the message to appln layer

ZMQ_REP: when receiving message, save the envelope frames before the null frame, return the content after the null frame. When appln layer responds, the envelope frame abd null frame will be added.

ZMQ_ROUTER: when receiving a message, an envelope frame will be added at the front to mark the origin of message. It's specified by zmq_setsockopt(ZMQ_IDENTITY), also can be generated by receiver. When sending message, sends the content after envelope frame to the address marked as envelope frame.

ZMQ_DEALER: fair-queue the message received

# How to test

1. **sudo mn --topo=single,7 --link=tc**

2. **mininet> source commands_auto.txt**

   This command deploys two routers on h2 and h4, and a server on h6.

3. **xterm h1**

   Open xterm to see the output.

4. Under Node:h1, **python3 refrigerator.py -g 10.0.0.6 -p 4444**

   This command deploys a client on h1, sets the IP address of grocery store as 10.0.0.6, which is the IP address of h6, and sets the port as 4444.

After that, the client will consult the routing table, find next hop, and waits for the response.

Routers between the client and server will act in DEALER-ROUTER mode.

```
H1 10.0.0.5 H2
H1 10.0.0.6 H2
H2 10.0.0.5 H3
H2 10.0.0.6 H4
H3 10.0.0.5 H5
H3 10.0.0.6 H6
H4 10.0.0.5 H5
H4 10.0.0.6 H6
```

