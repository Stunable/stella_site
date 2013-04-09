import urllib2
import mimetools
from StringIO import StringIO

from bs4 import BeautifulSoup


DEBUG = False # Set to True for debugging output.

class VolusionAPIError(Exception):
    pass

class VolusionLogonError(VolusionAPIError):
    pass

class VolusionConnectionError(VolusionAPIError):
    pass

class API_CONNECTION(object):
    creds ={
        'email': 'gdamon@gmail.com',
        'pw':'volusionsucksA$$'
    }

class API:
    def __init__(self, url=None, api_connection=None):
        self.__handlerCache = {}
        if not url:
            url = 'http://v1339437.pdmowhsxm5o2.demo1.volusion.com/net/WebService.aspx?'
        if not api_connection:
            api_connection = API_CONNECTION()


        url+= '?Login=%(email)s&EncryptedPassword=%(pw)s&API_Name=Generic'%api_connection.creds




        self._opener = urllib2.build_opener()

        print url
        self._opener.open(url)


        try:
           self.soup = BeautifulSoup(self._opener.open(url))
        except (urllib2.URLError, urllib2.HTTPError), e:
            raise VolusionConnectionError("Library could not connect to the Volusion API.  Either this installation of Volusion does not support the API, or the url, %s, is incorrect.\n\nError: %s" % (self._url, e))
        self.data = self.soup.response

