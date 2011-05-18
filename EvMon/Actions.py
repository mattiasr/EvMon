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
        self.project_id = None
        self.project_name = None


    def FetchURL(self, url, giveback="raw", cgi_data=None):
        """
        Get Contents from Eventum server
        """
        urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.Cookie))
        request = urllib2.Request(url, urllib.urlencode(cgi_data))
        response = urlopener.open(request)
        result = response.read()
        response.close()

        del response

        if giveback == "raw":
            return result

        if giveback == "obj":
            soup = BeautifulSoup(result, convertEntities=BeautifulSoup.ALL_ENTITIES)
            return soup

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
        #print result
        soup = BeautifulSoup(result)
        option = soup.findAll('option')

        project = []
        for element in option:
            opt = [element['value'], element['label']]
            project.append(opt)
            print "[" + element['value'] + "] " + element['label']

        # Selecting project
        self.project_id = 1
        self.project_name = 'op5 Support'

        return self.goto_project()


    def get_project_id(self):
        return str(self.project_id)


    def get_project_name(self):
        return str(self.project_name)


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


    def goto_project(self):
        """
        Go to the project you want to login to.
        """
        print "Fetching Project: [" + self.get_project_id() + "] " + self.get_project_name()
        self.select_project_url = self.base_url + '/select_project.php'
        values = {
                  'cat' : 'select',
                  'url' : '',
                  'project' : self.get_project_id(),
                  'remember' : '1',
                  'Submit' : 'Login',
         }

        result = self.FetchURL(self.select_project_url, cgi_data=values)
        soup = BeautifulSoup(result)
        elements = soup.findAll('a')
        for url in elements:
            if url['href'] == '/logout.php':
                return True

        return False

