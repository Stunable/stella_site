# profile_middleware - a middleware that profiles views
#
# Inspired by udfalkso's http://www.djangosnippets.org/snippets/186/
# and the Shwagroo Team's http://www.djangosnippets.org/snippets/605/
#
# Install this by adding it to your MIDDLEWARE_CLASSES.  It is active
# if you are logged in as a superuser, or always when settings.DEBUG
# is True.
#
# To use it, pass 'profile=1' as a GET or POST parameter to any HTTP
# request.

from base64 import b64decode, b64encode
import cPickle
from cStringIO import StringIO
from decimal import Decimal
import hotshot, hotshot.stats
import pprint
import sys
import tempfile

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection, reset_queries
from django.http import HttpResponse
from django.utils import html

from django.http import HttpResponsePermanentRedirect

# from django.core.exceptions import MiddlewareNotUsed
# from django.conf import settings
import cProfile
import pstats
import marshal
# from cStringIO import StringIO


import re
 
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
 
from django import http
 
''' 
EXAMPLE USAGE:
    Put this file in a directory called, eg, 'middleware,' inside your django
    project. Make sure to create an __init__.py file in the directory so it can
    be included as a module. 
    Set the values for 
        settings.XS_SHARING_ALLOWED_ORIGINS
        settings.XS_SHARING_ALLOWED_METHODS 
        settings.XS_SHARING_ALLOWED_HEADERS
    in settings.py. Then include 
        'modernomad.middleware.crossdomainxhr.CORSMiddleware' 
    in MIDDLEWARE_CLASSES in settings.py.
'''
 
try:
    import settings 
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = []
 
class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
 
        eg.         
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
        Access-Control-Allow-Methods: ["Content-Type"]
 
    """
    def process_request(self, request):
 
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            response['Access-Control-Allow-Headers']  = ",".join( XS_SHARING_ALLOWED_HEADERS ) 
            return response
 
        return None
 
    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
 
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
 
        return response

class StdoutWrapper(object):
    """Simple wrapper to capture and overload sys.stdout"""
    def __init__(self):
        self.stdout = sys.stdout
        self.stream = StringIO()
        sys.stdout = self.stream

    def __del__(self):
        if self.stdout is not None:
            sys.stdout = self.stdout

    def __str__(self):
        return self.stream.getvalue()


def render_stats(stats, sort, format):
    """
    Returns a StringIO containing the formatted statistics from _statsfile_.

    _sort_ is a list of fields to sort by.
    _format_ is the name of the method that pstats uses to format the data.
    """
    output = StdoutWrapper()
    if hasattr(stats, "stream"):
        stats.stream = output.stream
    stats.sort_stats(*sort)
    getattr(stats, format)()
    return output.stream

def render_queries(queries, sort):
    """
    Returns a StringIO containing the formatted SQL queries.

    _sort_ is a field to sort by.
    """
    output = StringIO()
    if sort == 'order':
        print >>output, "     time query"
        for query in queries:
            print >>output, " %8s %s" % (query["time"], query["sql"])
        return output
    if sort == 'time':
        def sorter(x, y):
            return cmp(x[1][1], y[1][1])
    elif sort == 'queries':
        def sorter(x, y):
            return cmp(x[1][0], y[1][0])
    else:
        raise RuntimeError("Unknown sort: %s" % sort)
    print >>output, "  queries     time query"
    results = {}
    for query in queries:
        try:
            result = results[query["sql"]]
            result[0] += 1
            result[1] += Decimal(query["time"])
        except KeyError:
            results[query["sql"]] = [1, Decimal(query["time"])]
    results = sorted(results.iteritems(), cmp=sorter, reverse=True)
    for result in results:
        print >>output, " %8d %8.3f %s" % (result[1][0],
                                           result[1][1],
                                           result[0])
    return output


def pickle_stats(stats):
    """Pickle a pstats.Stats object"""
    if hasattr(stats, "stream"):
        del stats.stream
    return cPickle.dumps(stats)

def unpickle_stats(stats):
    """Unpickle a pstats.Stats object"""
    stats = cPickle.loads(stats)
    stats.stream = True
    return stats


class RadioButton(object):
    """Generate the HTML for a radio button."""
    def __init__(self, name, value, description=None, checked=False):
        self.name = name
        self.value = value
        if description is None:
            self.description = value
        else:
            self.description = description
        self.checked = checked

    def __str__(self):
        checked = ""
        if self.checked:
            checked = "checked='checked'"
        return ("<input "
                "type='radio' "
                "name='%(name)s' "
                "value='%(value)s' "
                "%(checked)s>"
                "%(description)s"
                "</input><br />" %
                {'name': self.name,
                 'value': self.value,
                 'checked': checked,
                 'description': self.description})


class RadioButtons(object):
    """Generate the HTML for a list of radio buttons."""
    def __init__(self, name, checked, values):
        self.result = []
        for v in values:
            description = None
            if isinstance(v, (list, tuple)):
                value = v[0]
                description = v[1]
            else:
                value = v
            select = False
            if value == checked:
                select = True
            self.result.append(RadioButton(name, value, description, select))

    def __str__(self):
        return "\n".join([str(button) for button in self.result])


stats_template = """
<html>
    <head><title>Profile for %(url)s</title></head>
    <body>
        <form method='post' action='?profile=1'>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>Sort by</legend>
                %(sort_first_buttons)s
            </fieldset>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>then by</legend>
                %(sort_second_buttons)s
            </fieldset>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>Format</legend>
                %(format_buttons)s
            </fieldset>
            <div style='clear: both'></div>
            <input type='hidden' name='queries' value='%(rawqueries)s' />
            <input type='hidden' name='stats' value='%(rawstats)s' />
            <input type='hidden' name='show_stats' value='1' />
            <input type='submit' name='show_queries' value='Show Queries' />
            <input type='submit' name='sort' value='Sort' />
        </form>
        <hr />
        <pre>%(stats)s</pre>
    </body>
</html>
"""

sort_categories = (('time', 'internal time'),
                   ('cumulative', 'cumulative time'),
                   ('calls', 'call count'),
                   ('pcalls', 'primitive call count'),
                   ('file', 'file name'),
                   ('nfl', 'name/file/line'),
                   ('stdname', 'standard name'),
                   ('name', 'function name'))

def display_stats(request, stats, queries):
    """
    Generate a HttpResponse of functions for a profiling run.

    _stats_ should contain a pstats.Stats of a hotshot session.
    _queries_ should contain a list of SQL queries.
    """
    sort = [request.REQUEST.get('sort_first', 'time'),
            request.REQUEST.get('sort_second', 'calls')]
    format = request.REQUEST.get('format', 'print_stats')
    sort_first_buttons = RadioButtons('sort_first', sort[0],
                                      sort_categories)
    sort_second_buttons = RadioButtons('sort_second', sort[1],
                                       sort_categories)
    format_buttons = RadioButtons('format', format,
                                  (('print_stats', 'by function'),
                                   ('print_callers', 'by callers'),
                                   ('print_callees', 'by callees')))
    output = render_stats(stats, sort, format)
    output.reset()
    output = [html.escape(unicode(line)) for line in output.readlines()]
    response = HttpResponse(mimetype='text/html; charset=utf-8')
    response.content = (stats_template %
                        {'format_buttons': format_buttons,
                         'sort_first_buttons': sort_first_buttons,
                         'sort_second_buttons': sort_second_buttons,
                         'rawqueries' : b64encode(cPickle.dumps(queries)),
                         'rawstats': b64encode(pickle_stats(stats)),
                         'stats': "".join(output),
                         'url': request.path})
    return response


queries_template = """
<html>
    <head><title>SQL Queries for %(url)s</title></head>
    <body>
        <form method='post' action='?profile=1'>
            <fieldset style='float: left'>
                <legend style='font-weight: bold'>Sort by</legend>
                %(sort_buttons)s
            </fieldset>
            <div style='clear: both'></div>
            <input type='hidden' name='queries' value='%(rawqueries)s' />
            <input type='hidden' name='stats' value='%(rawstats)s' />
            <input type='hidden' name='show_queries' value='1' />
            <input type='submit' name='show_stats' value='Show Profile' />
            <input type='submit' name='sort' value='Sort' />
        </form>
        <hr />
        %(num_queries)d SQL queries:
        <pre>%(queries)s</pre>
    </body>
</html>
"""


def display_queries(request, stats, queries):
    """
    Generate a HttpResponse of SQL queries for a profiling run.

    _stats_ should contain a pstats.Stats of a hotshot session.
    _queries_ should contain a list of SQL queries.
    """
    sort = request.REQUEST.get('sort_by', 'time')
    sort_buttons = RadioButtons('sort_by', sort,
                                (('order', 'by order'),
                                 ('time', 'time'),
                                 ('queries', 'query count')))
    output = render_queries(queries, sort)
    output.reset()
    output = [html.escape(unicode(line))
              for line in output.readlines()]
    response = HttpResponse(mimetype='text/html; charset=utf-8')
    response.content = (queries_template %
                        {'sort_buttons': sort_buttons,
                         'num_queries': len(queries),
                         'queries': "".join(output),
                         'rawqueries' : b64encode(cPickle.dumps(queries)),
                         'rawstats': b64encode(pickle_stats(stats)),
                         'url': request.path})
    return response


class ProfileMiddleware(object):
    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed()
        self.profiler = None
 
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and ('profile' in request.GET
                            or 'profilebin' in request.GET):
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)
 
    def process_response(self, request, response):
        if settings.DEBUG:
            if 'profile' in request.GET:
                self.profiler.create_stats()
                out = StringIO()
                stats = pstats.Stats(self.profiler, stream=out)
                # Values for stats.sort_stats():
                # - calls           call count
                # - cumulative      cumulative time
                # - file            file name
                # - module          file name
                # - pcalls          primitive call count
                # - line            line number
                # - name            function name
                # - nfl                     name/file/line
                # - stdname         standard name
                # - time            internal time
                stats.sort_stats('time').print_stats(.2)
                response.content = out.getvalue()
                response['Content-type'] = 'text/plain'
                return response
            if 'profilebin' in request.GET:
                self.profiler.create_stats()
                response.content = marshal.dumps(self.profiler.stats)
                filename = request.path.strip('/').replace('/','_') + '.pstat'
                response['Content-Disposition'] = \
                    'attachment; filename=%s' % (filename,)
                response['Content-type'] = 'application/octet-stream'
                return response
        return response

class SubdomainsMiddleware:
    def process_request(self, request):
        """Parse out the subdomain from the request"""
        request.subdomain = None
        host = request.META.get('HTTP_HOST', '')
        host_s = host.replace('www.', '').split('.')
        if len(host_s) > 2:
            request.subdomain = ''.join(host_s[:-2])

        if request.subdomain == 'stylists':
            print 'STYLISTS DOMAIN'
            request.urlconf = 'retailers.urls'

class FilterPersistMiddleware(object):

    def _get_default(self, key):
        """ Gets any set default filters for the admin. Returns None if no 
            default is set. """
        default = settings.ADMIN_DEFAULT_FILTERS.get(key, None)
        # Filters are allowed to be functions. If this key is one, call it.
        if hasattr(default, '__call__'):
            default = default()
        return default

    def process_request(self, request):
        if '/admin/' not in request.path or request.method == 'POST':
            return None
        
        if request.META.has_key('HTTP_REFERER'):
            referrer = request.META['HTTP_REFERER'].split('?')[0]
            referrer = referrer[referrer.find('/admin'):len(referrer)]
        else:
            referrer = u''
        
        popup = 'pop=1' in request.META['QUERY_STRING']
        path = request.path
        query_string = request.META['QUERY_STRING']
        
        try:
            session = request.session
        except:
            print 'no session...'
            return None

        if session.get('redirected', False):#so that we dont loop once redirected
            del session['redirected']
            return None

        key = 'key'+path.replace('/','_')
        if popup:
            key = 'popup'+key

        if path == referrer: 
            """ We are in the same page as before. We assume that filters were
                changed and update them. """
            if query_string == '': #Filter is empty, delete it
                if session.has_key(key):
                    del session[key]
                return None
            else:
                request.session[key] = query_string
        else: 
            """ We are are coming from another page. Set querystring to
                saved or default value. """
            query_string=session.get(key, self._get_default(key))
            if query_string is not None:
                redirect_to = path+'?'+query_string
                request.session['redirected'] = True
                return http.HttpResponseRedirect(redirect_to)
            else:
                return None


class SSLMiddleware(object):
    def __init__(self):
        self.paths = getattr(settings, 'SSL_REQUIRED_PATHS')
        self.enabled = self.paths and not getattr(settings, 'DEBUG')

    def process_request(self, request):
        if self.enabled and not request.META.get('HTTP_X_FORWARDED_PROTO', '') == 'https':
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(secure_url)
        return None
