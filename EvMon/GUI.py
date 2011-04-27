# encoding: utf-8

try:
    import pygtk
    pygtk.require("2.0")
except Exception, err:
    print
    print err
    print
    print "Could not load pygtk, maybe you need to install python gtk."
    print
    import sys
    sys.exit()
import gtk
import Statusbar

class GUI(object):

    def __init__(self, **kwds):

        # Meta
        self.name = "evmon"
        self.version = "0.0.1"
        self.website = "http://evmon.ryrlen.org"
        self.copyright = "©2011-2015 Mattias Ryrlén\nmattias@ryrlen.org"
        self.comments = "Eventum Queue monitor for your desktop"

        # get resources directory from current directory - only if not being set before by pkg_resources
        if self.Resources == "":
            if os.path.exists(os.path.normcase(os.getcwd() + os.sep + "Evmon" + os.sep + "resources")):
                self.Resources = os.path.normcase(os.getcwd() + os.sep + "Evmon" + os.sep + "resources")
            else:
                self.Resources = os.path.normcase(os.getcwd() + os.sep + "resources")

        # create all GUI widgets
        self.CreateOutputVisuals()

        # set size of popup-window
        self.popwin.Resize()

        # flag which is set True if already notifying
        self.Notifying = False

    def CreateOutputVisuals(self):
        """
            create output visuals
        """
        # decide if the platform can handle SVG if not (Windows and MacOSX) use PNG
        if platform.system() == "Windows" or platform.system() == "Darwin":
            self.BitmapSuffix = ".png"
        else:
            self.BitmapSuffix = ".svg"

        # set app icon for all app windows
        gtk.window_set_default_icon_from_file(self.Resources + os.sep + self.name + self.BitmapSuffix)

