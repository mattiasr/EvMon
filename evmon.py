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

    #Fetching list of issues


    server.list_url = str(server.base_url) + '/list.php'
    values = {}
    result = server.FetchURL(server.list_url, giveback='obj', cgi_data=values)
#    print result
    elements = result.findAll(attrs={'class': 'default_white', 'nowrap' : 'nowrap'})

    for element in elements:
        print element

else:
    print "Login Failed"
