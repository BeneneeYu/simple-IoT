# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom application protocol
#          used by our smart refrigerator to send grocery order and health status
#          messages. This is our Application Layer used in the Computer Networks
#          course Assignments
#

# import the needed packages
import os  # for OS functions
import sys  # for syspath and system exception
import time  # for sleep
from enum import Enum  # for enumerated types

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")
import serialize_json as sejs
import serialize_flatbuffer as sefb
from transportlayer.CustomTransportProtocol import CustomTransportProtocol as XPortProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage, HealthStatusMessage, ResponseMessage


############################################
#  Serialization Enumeration Type
############################################
class SerializationType(Enum):
    # One can extend this as needed. For now only these two
    UNKNOWN = -1
    JSON = 1
    FBUFS = 2


############################################
#  Bunch of Application Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################
class BadSerializationType(Exception):
    '''Bad Serialization Type'''

    def __init__(self, arg):
        msg = arg + " is not a known serialization type"
        super().__init__(msg)


class BadMessageType(Exception):
    '''Bad Message Type'''

    def __init__(self):
        msg = "bad or unknown message type"
        super().__init__(msg)


############################################
#       Custom Application Protocol class
############################################
class CustomApplnProtocol():
    '''Custom Application Protocol for the Smart Refrigerator'''

    ###############################
    # constructor
    ###############################
    def __init__(self, role):
        self.role = role  # indicates if we are client or server, false => client
        self.ser_type = SerializationType.UNKNOWN
        self.xport_obj = None  # handle to our underlying transport layer object
        self.receive_request_num = 0
        self.receive_request_time = 0.0
        self.receive_response_num = 0
        self.receive_response_time = 0.0

    ###############################
    # configure/initialize
    ###############################
    def initialize(self, config, ip, port):
        ''' Initialize the object '''

        try:
            # Here we initialize any internal variables
            print("Custom Application Protocol Object: Initialize")
            print("serialization type = {}".format(config["Application"]["Serialization"]))

            # initialize our variables
            if (config["Application"]["Serialization"] == "json"):
                self.ser_type = SerializationType.JSON
            elif (config["Application"]["Serialization"] == "fbufs"):
                self.ser_type = SerializationType.FBUFS
            else:  # Unknown; raise exception
                raise BadSerializationType(config["Application"]["Serialization"])

            # Now obtain our transport object
            # @TODO
            print("Custom Appln Protocol::initialize - obtain transport object")
            self.xport_obj = XPortProtoObj(self.role)

            # initialize it
            print("Custom Appln Protocol::initialize - initialize transport object")
            self.xport_obj.initialize(config, ip, port)

        except Exception as e:
            raise e  # just propagate it

    ##################################
    #  send Grocery Order
    ##################################
    def send_grocery_order(self, order):
        try:
            if isinstance(order, GroceryOrderMessage):
                print("Start to serialize a grocery order message")
                start_time = time.time()
                order.ts = start_time
                buf = self.self_serialize(order)
                end_time = time.time()
                print("Serialization is done, took {} secs".format(end_time - start_time))
            else:
                raise BadMessageType()
            self.xport_obj.send_appln_msg(buf, len(buf), False)
        except Exception as e:
            raise e

    ##################################
    #  send Health Status
    ##################################
    def send_health_status(self, status):
        try:
            if isinstance(status, HealthStatusMessage):
                print("Start to serialize a health status message")
                start_time = time.time()
                status.ts = start_time
                buf = self.self_serialize(status)
                end_time = time.time()
                print("Serialization is done, took {} secs".format(end_time - start_time))
            else:
                raise BadMessageType()
            self.xport_obj.send_appln_msg(buf, len(buf), False)
        except Exception as e:
            raise e

    ##################################
    #  send response
    ##################################
    def send_response(self, response):
        try:
            if isinstance(response, ResponseMessage):
                print("Start to serialize a response message")
                start_time = time.time()
                response.ts = start_time
                buf = self.self_serialize(response)
                end_time = time.time()
                print("Serialization is done, took {} secs".format(end_time - start_time))
            else:
                raise BadMessageType()
            self.xport_obj.send_appln_msg(buf, len(buf))
        except Exception as e:
            raise e

    ##################################
    #  receive request
    ##################################
    def recv_request(self):
        try:
            # @TODO@ Implement this
            # receive the message and return it to caller
            #
            # To that end, we ask our transport object to retrieve
            # application level message
            #
            # Note, that in this assignment, we are not worrying about sending
            # transport segments etc and so what we receive from ZMQ is the complete
            # message.
            request = self.xport_obj.recv_appln_msg(0, False)

            # order message or health message
            request_result = self.self_deserialize(request)
            receive_time = time.time() - request_result.ts
            self.receive_request_num += 1
            self.receive_request_time += receive_time
            print("Time Spent to Receive Request is {} secs".format(receive_time))
            print("Average Time Spent to Receive Request is {} secs".format(
                self.receive_request_time / self.receive_request_num))
            return request_result
        except Exception as e:
            raise e

    ##################################
    #  receive response
    ##################################
    def recv_response(self):
        try:
            # @TODO@ Implement this
            # receive the message and return it to caller
            #
            # To that end, we ask our transport object to retrieve
            # application level message
            #
            # Note, that in this assignment, we are not worrying about sending
            # transport segments etc and so what we receive from ZMQ is the complete
            # message.
            response = self.xport_obj.recv_appln_msg()
            # response message instance
            response_result = self.self_deserialize(response)
            receive_time = time.time() - response_result.ts
            self.receive_response_num += 1
            self.receive_response_time += receive_time
            print("Time Spent to Receive Request is {} secs".format(receive_time))
            print("Average Time Spent to Receive Response is {} secs".format(
                self.receive_response_time / self.receive_response_num))
            return response_result
        except Exception as e:
            raise e

    def self_serialize(self, obj):
        if self.ser_type == SerializationType.JSON:
            buf = sejs.serialize(obj)
        else:
            buf = sefb.serialize(obj)
        return buf

    def self_deserialize(self, buf):
        if self.ser_type == SerializationType.JSON:
            obj = sejs.deserialize(buf)
        else:
            obj = sefb.deserialize(buf)
        return obj
