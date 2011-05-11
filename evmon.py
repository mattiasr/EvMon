#!/opt/local/bin/python
# encoding: utf-8

#Master file to be executed so that EvMon starts correct

import os
import Queue
import socket

from EvMon import Actions

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

# Create Server Object and set config options for the server
server = Actions.GenericServer()
server.username = ""
server.password = ""
server.base_url = "https://tickets.op5.com"

if server.Login() == True:
    print "Login Successful"
else:
    print "Login Failed"
