import os, sys
import urllib
import urllib2
import cookielib
import base64
import md5
import ConfigParser

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
        self.base_filters = '?cat=search&status=&hide_closed=1&nosave=1&keywords='
        self.assined = None
        self.filter_status = None
        self.filter_assigned = None
        self.issues = []
        self.firstRun = None
        self.debug = False
        self.poll_interval = 60
        self.config_hash = None


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
            if issue.Assigned == '':
                issue.Assigned = 'Unassigned'
            self.addIssue(issue)


    def FetchURL(self, url, giveback="raw", cgi_data=None):
        """
        Get Contents from Eventum server
        """
        if self.debug: print 'Fetching: ' + url
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
            if self.project_id == None:
                print "[" + element['value'] + "] " + element['label']
            if self.project_id == element['value']:
                self.project_name = element['label']

        if self.project_id == None:
            print "Warning: No project selected, update your config with"
            print "         project_id from one of the above."
            sys.exit(1)

        if len(option) == 1:
            if self.debug: print "Only one project, lets continue"
            goto_url = str(self.base_url) + '/list.php' + str(self.base_filters)
            result = self.FetchURL(goto_url, giveback='obj', cgi_data=values)
            csv_list = result.find(attrs={'name':'csv_data'})['value']
            self.getIssues(csv_list=csv_list)
            return True
        else:
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
        if self.debug: print "Fetching Project: [" + self.get_project_id() + "] " + self.get_project_name()

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

    def validate_status(self, issue):
        """
        Return true if a status should be filtered in.
        """
        if not self.filter_status or self.filter_status[0] == "":
            return True

        for filter_status in self.filter_status:
            if filter_status == issue.Status:
                return True
        return False

    def validate_assigned(self, issue):
        if not self.filter_assigned or self.filter_assigned[0] == "":
            return True

        import re

        for filter_assigned in self.filter_assigned:
            if re.match(filter_assigned, issue.Assigned):
                return True
        return False

    def filter_issue(self, issue):
        """
        Return true if all is good.
        """

        filtered_in = False

        # Should we filter based on assigned?
        if self.validate_assigned(issue) and self.validate_status(issue):
            filtered_in = True

        return filtered_in

    def reload_config(self):
        """
        Reload the config file.
        """

        try:
            config_hash = md5.new(file(os.path.expanduser('~/.evmon.conf')).read())
        except IOError:
            print "Error: Couldn't find configuration file ~/.evmon.conf, please read README"
            sys.exit(1)

        if self.debug:
            print "Last Hash   : " + str(self.config_hash)
            print "Current Hash: " + str(config_hash.hexdigest())

        if self.config_hash != str(config_hash.hexdigest()):
            default = GenericServer()
            if self.debug:
                print "Config changed, reloading..."

            config = ConfigParser.SafeConfigParser()
            config.read(os.path.expanduser('~/.evmon.conf'))

            try:
                self.username = config.get('Server', 'username')
                self.password = config.get('Server', 'password')
                self.base_url = config.get('Server', 'base_url')
            except:
                print "ERROR: Required variables not found, please read README"

            try: self.project_id = config.get('Server', 'project_id')
            except: pass

            try: self.filter_assigned = config.get('Server', 'filter_assigned').split(",")
            except: self.filter_assigned = default.filter_assigned

            try: self.debug = int(config.get('Server', 'debug'))
            except: self.debug = default.debug

            try: self.poll_interval = int(config.get('Server', 'poll_interval'))
            except: self.poll_interval = default.poll_interval

            try: self.filter_status = config.get('Server', 'filter_status').split(",")
            except: self.filter_status = default.filter_status

            self.config_hash = config_hash.hexdigest()
            del config_hash, default

