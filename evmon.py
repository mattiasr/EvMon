#!/usr/bin/env python
# encoding: utf-8

#Master file to be executed so that EvMon starts correct

import os
import Queue
import socket
import base64
import ConfigParser

from time import sleep
from EvMon import Actions

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)
config = ConfigParser.SafeConfigParser()
config.read(os.path.expanduser('~/.evmon.conf'))

# Create Server Object and set config options for the server
server = Actions.GenericServer()
server.username = config.get('Server', 'username')
server.password = config.get('Server', 'password')
server.base_url = config.get('Server', 'base_url')

if server.Login() == True:
    print "Login Successful"

    # Since we got the first result during login, we just parse the data first time
    server.firstRun = True
    os.system('clear')
    while True:
        if not server.firstRun:
            #Fetching list of issues
            server.issues = []
            server.getIssues()
            os.system('clear')

        count = 0
        total = 0
        print '===================================== EvMon ====================================='
        for issue in server.issues:
            #if issue.Status == 'open' or issue.Status == 'new':
            if issue.Status == 'new':
                if issue.Assigned == '':
                    issue.Assigned = 'Unassigned'

                print '[' + issue.Issue_ID + '] ' + issue.Status + ' [' + issue.Assigned + '] ' + ' -= ' + issue.Summary + ' =-'
                count+=1

            total+=1
        if count == 0:
            print "No issues"

        print '================================================================================='
        print 'Total Issues: ' + str(count) + ' Filtered: ' + str((total - count))

        sleep(60)
        server.firstRun = False

else:
    print "Login Failed"
