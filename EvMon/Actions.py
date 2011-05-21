import urllib
import urllib2
import cookielib
import base64

from EvMon.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

class GenericIssue(object):
    def __init__(self, kwds):
        self.__dict__ = dict(((x.replace(' ', '_'), y) for x, y in kwds.items()))


    def __repr__(self):
        str = ''
        for x in self.__dict__:
            str += "%s: %s\n" % (x, self.__dict__[x] or '')
        return str

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
        self.base_filters = '?cat=search&status=&hide_closed=1'
        self.issues = []
        self.firstRun = None


    def addIssue(self, object):
        self.issues.append(object)


    def getIssues(self, csv_list=None, Filter=None):
        if not csv_list:
            if not Filter:
                self.list_url = str(self.base_url) + '/list.php' + self.base_filters
            else:
                self.list_url = str(self.base_url) + '/list.php' + Filter
            values = {}

            result = self.FetchURL(self.list_url, giveback='obj', cgi_data=values)
            csv_list = result.find(attrs={'name':'csv_data'})['value']

        issues = base64.b64decode(csv_list).split('\n')

        colnames = issues.pop(0)
        colnames = colnames.split('\t')

        i = 1
        for row in issues:
            issue = GenericIssue(dict([(colnames[i], x) for i, x in enumerate(row.split('\t'))]))
            self.addIssue(issue)


    def FetchURL(self, url, giveback="raw", cgi_data=None):
        """
        Get Contents from Eventum server
        """
        print 'Fetching: ' + url
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

        goto_url = str(self.base_url) + '/list.php' + str(self.base_filters)
        self.select_project_url = self.base_url + '/select_project.php'
        values = {
                  'cat' : 'select',
                  'url' : goto_url,
                  'project' : self.get_project_id(),
                  'remember' : '1',
                  'Submit' : 'Login',
         }

        result = self.FetchURL(self.select_project_url, giveback='obj', cgi_data=values)

        if result.find(attrs={'href':'/logout.php'}) is not None:
            csv_list = result.find(attrs={'name':'csv_data'})['value']
            self.getIssues(csv_list=csv_list)
            return True

        return False

