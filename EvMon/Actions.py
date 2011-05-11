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
        self.username = None
        self.password = None
        self.base_url = None


    def FetchURL(self, url, giveback="raw", cgi_data=None):
        """
        Get Contents from Eventum server
        """
        urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.Cookie))
        request = urllib2.Request(url, urllib.urlencode(cgi_data))
        response = urlopener.open(request)

        if giveback == "raw":
            result = response.read()
            response.close()
            del response
            return result

    def Login(self):
        """
        Login to Eventum webserver
        """

        self.login_url = str(self.base_url) + "/login.php"
        values = {
                  'cat' : 'login',
                  'url' : '',
                  'email' : self.get_username(),
                  'passwd' : self.get_password(),
                  'Submit' : 'Login',
         }

        result = self.FetchURL(self.login_url, cgi_data=values)
        return True


    def get_username(self):
        """
        Return the config username in str format
        """

        return str(self.username)


    def get_password(self):
        """
        Return the config username in str format
        """

        return str(self.password)


    def ListProjects():
        """
        Get a list of the projects avaible for the user
        """

