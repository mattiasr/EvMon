# encoding: utf-8

import os
import gtk

from EvMon import GUI
conf = ''
servers = ''
debug_queue = ''

print "EvMon, the eventum monitor program"

output = GUI.GUI(conf=conf, servers=servers, debug_queue=debug_queue)

gtk.main()
