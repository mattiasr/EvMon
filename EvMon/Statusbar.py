# encoding: utf-8
import gtk
import os
import platform

class StatusBar(object):
    """
        Statusbar object
    """

    def __init__(self, **kwds):
        # add all keywords to object, every mode searchs inside for its favorite arguments/keywords
        for k in kwds: self.__dict__[k] = kwds[k]

        self._CreateFloatingStatusbar()

        # image for logo in statusbar
        self.nagstamonLogo = gtk.Image()
        self.nagstamonLogo.set_from_file(self.output.Resources + os.sep + "evmon_small" + self.output.BitmapSuffix)

        # 2 versions of label text for notification
        self.statusbar_labeltext = ""
        self.statusbar_labeltext_inverted = ""
        self.Flashing = False

        # Label for display
        self.Label = gtk.Label()

        # statusbar hbox container for logo and status label
        self.HBox = gtk.HBox()

        # Use EventBox because Label cannot get events
        self.LogoEventbox = gtk.EventBox()
        self.LogoEventbox.add(self.nagstamonLogo)
        self.EventBoxLabel = gtk.EventBox()
        self.EventBoxLabel.add(self.Label)
        self.HBox.add(self.LogoEventbox)
        self.HBox.add(self.EventBoxLabel)
        self.StatusBar.add(self.HBox)

        self.StatusBar.show_all()

        try:
            fontsize = 7000
            self.Label.set_markup('<span size="%s" bgcolor="white" color="black"> Loading... </span>' % (fontsize))
            # compare heights, height of logo is the important one
            while self.LogoEventbox.size_request()[1] > self.Label.size_request()[1]:
                self.Label.set_markup('<span size="%s" bgcolor="white" color="black"> Loading... </span>' % (fontsize))
                fontsize += 250
            self.output.fontsize = fontsize
        except:
            # in case of error define fixed fontsize
            self.output.fontsize = 10000


    def _CreateFloatingStatusbar(self):
        """
        create statusbar as floating window
        """
        # TOPLEVEL seems to be more standard compliant
        #self.StatusBar = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # WINDOWS_POPUP works
        self.StatusBar = gtk.Window(gtk.WINDOW_POPUP)
        self.StatusBar.set_decorated(False)
        self.StatusBar.set_keep_above(True)
        self.StatusBar.stick()
        # at http://www.pygtk.org/docs/pygtk/gdk-constants.html#gdk-window-type-hint-constants
        # there are some hint types to experiment with
        if platform.system() == "Windows":
            self.StatusBar.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        else:
            self.StatusBar.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
        self.StatusBar.set_property("skip-taskbar-hint", True)
        self.StatusBar.set_skip_taskbar_hint(True)


