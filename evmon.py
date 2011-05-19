#!/opt/local/bin/python
# encoding: utf-8

#Master file to be executed so that EvMon starts correct

import os
import Queue
import socket
import base64

from time import sleep
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

    while True:
        #Fetching list of issues
        server.issues = []
        server.getIssues(Filter='?cat=search&status=&hide_closed=1')

        count = 0
        total = 0
        for issue in server.issues:
            if issue.Status == 'open' or issue.Status == 'new':
                print '[' + issue.Issue_ID + '] ' + issue.Status + ' -= ' + issue.Summary + ' =-'
                count+=1

            total+=1
        print '================================================================================='
        print 'Total Issues: ' + str(count) + ' Filtered: ' + str((total - count))

        sleep(20)

else:
    print "Login Failed"
