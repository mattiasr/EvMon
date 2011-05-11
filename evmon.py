#!/opt/local/bin/python
# encoding: utf-8

#Master file to be executed so that EvMon starts correct

import os
import Queue
import socket

from EvMon import Actions
########## Config
#
email = ""
passwd = ""
base_url = "http://tickets.op5.com"
login_url = base_url + "/login.php"

values = {
          'cat' : 'login',
          'url' : '',
          'email' : email,
          'passwd' : passwd,
          'Submit' : 'Login',
         }


# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)


server = Actions.GenericServer()

result = server.FetchURL(login_url, cgi_data=values)


print result

