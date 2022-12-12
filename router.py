#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   router.py    
@Contact :   zhengyu.shen@vanderbilt.edu

@Modify Time      @Author         @Version    @Desciption
------------      ------------    --------    -----------
2022/10/25 15:10   Shen Zhengyu      1.0         None
'''
# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
#
# Code taken from ZeroMQ's sample code for the HelloWorld
# program, but modified to use DEALER-ROUTER sockets to showcase
# TCP. Plus, added other decorations like comments, print statements,
# argument parsing, etc.
#
# This code is for the intermediate router.
#
# Note: my default indentation is now set to 2 (in other snippets, it
# used to be 4)

# import the needed packages
import os  # for OS functions
import sys  # for syspath and system exception
import time  # for sleep
import argparse  # for argument parsing
import configparser  # for configuration parsing
import zmq  # actually not needed here but we are printing zmq version and hence needed
import random

# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert(0, os.getcwd())

# this is our application level protocol and its message types
from applnlayer.CustomApplnProtocol import CustomApplnProtocol as ApplnProtoObj
from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from applnlayer.ApplnMessageTypes import HealthStatusMessage
from applnlayer.ApplnMessageTypes import ResponseMessage


class Router():
    '''Custom Transport Protocol'''

    ###############################
    # constructor
    ###############################
    def __init__(self):
        self.router_obj = None
        self.nextip = None
        self.nextport = None

    ###############################
    # configure/initialize
    ###############################
    def initialize(self, args):
        ''' Initialize the object '''

        try:
            # Here we initialize any internal variables
            print("Router Object: Initialize")

            # Now obtain our network layer object
            print("Router Protocol::initialize - obtain network object")
            self.router_obj = NWProtoObj()

            # # Now, get the configuration object
            config = configparser.ConfigParser()
            config.read(args.config)

  
            # In this assignment, we let network layer (which holds all the ZMQ logic) to
            # directly talk to the remote peer. In future assignments, this will be the
            # next hop router to whom we talk to.
            print("Custom Transport Protocol::initialize - initialize network object")
            # self.router_obj.driver (args, self.nextip, self.nextport)
            self.router_obj.initialize_router(config, args.myaddr, args.myport)

        except Exception as e:
            raise e  # just propagate it


##################################
# Command line parsing
##################################
def parseCmdLineArgs():
    # parse the command line
    parser = argparse.ArgumentParser()

    # add optional arguments]
    parser.add_argument("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
    parser.add_argument("-a", "--myaddr", default="*", help="Interface to bind to (default: *)")
    parser.add_argument("-p", "--myport", type=int, default=4444, help="Port to bind to (default: 4444)")
    args = parser.parse_args()

    return args


# ------------------------------------------
# main function
def main():
    """ Main program """

    print("Demo program for TCP Router with ZeroMQ")

    # first parse the command line args
    parsed_args = parseCmdLineArgs()

    router = Router()
    # start the driver code
    router.initialize(parsed_args)


# ----------------------------------------------
if __name__ == '__main__':
    # here we just print the version numbers
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current pyzmq version is %s" % zmq.pyzmq_version())

    main()
