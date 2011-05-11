import urllib
import urllib2
import cookielib

from EvMon.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup


class GenericServer(object):

    def __init__(self, **kwds):
        # add all keywords to object, every mode searchs inside for its favorite arguments/keywords
        for k in kwds: self.__dict__[k] = kwds[k]

        self.Cookie = cookielib.CookieJar()
        self.urlopener = None


    def FetchURL(self, url, giveback="raw", cgi_data=None):
        """
        Get Contents from Eventum server
        """
        urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.Cookie))
        request = urllib2.Request(url, urllib.urlencode(cgi_data))
        response = urlopener.open(request)

        print urlopener

        # give back pure HTML or XML in case giveback is "raw"
        if giveback == "raw":
            result = response.read()
            response.close()
            del response
            return result
