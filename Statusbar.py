# encoding: utf-8

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

