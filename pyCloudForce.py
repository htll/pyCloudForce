import urllib
import urllib2
import urlparse
import mechanize
import re
import base64
from BeautifulSoup import BeautifulSoup

class CloudForm( object ):
    def __init__( self, action, method = "get", url = None, user_agent = 'Mozilla/6 (Unix/Linux 64bit) Gecko' ):
        self.method = method
        self.action = action
        self.inputs = {}
        self.submit = None
        self.headers = { 'User-Agent': user_agent, 'Referer' : url }

    def addInput( self, name, value = None ):
        self.inputs[ name ] = value

    def addSubmit( self, name ):
        self.submit = name

    def getSubmitString( self ):
        submitstr = {}
        for key in self.inputs:
            submitstr[key] = self.inputs[key]
        if self.submit:
            submitstr[self.submit] = 'Submit'
        return urllib.urlencode( submitstr )

    def submit( self ):
        data = self.getSubmitString()
        if self.method == 'get':
            self.action += '?' + data
            data = None

        response = urllib2.urlopen( urllib2.Request( self.action, data, self.headers ) )
        if response.code != 200:
            raise Exception( "HTTP Error (Status code {})".format( response.code ) )
        pool = BeautifulSoup( response.read() )
        return pool


class TestForm( CloudForm ):
    def __init__( self, action, method = 'get', url = None, user_agent = 'Mozilla/6 (Unix/Linux 64bit) Gecko', attrs = [ 'href', 'src', 'id', 'name', 'class' ] ):
        CloudForm.__init__( self, action, method, url, user_agent )
        self.data = {}
        self.attrs = attrs

    def getAttrs( self, data ):
        ret = {}
        for attr in self.attrs:
            ret[ attr ] = data
        return ret

    def setInput( self, name, value = None ):
        value = value or base64.b64encode( name )
        self.data[ name ] = value
        self.inputs[ name ] = value

    def checkStore( self ):
        pool = super( TestForm, self ).submit()
        return [ key for key in self.data if pool.find( text=re.compile( self.data[ key ]  ) ) or pool.find( attrs=self.getAttrs( self.data[ key ] ) ) ] # find self.data[ key ] in response


class FieldJudge( object ):
    def __init__( self, parameters = ['name', 'id', 'class'], regex = re.compile('(paste|text|input|data|comment)') ):
        self.params = parameters
        self.regex = regex

    def test( self, field ):
        for param in self.params:
            try:
                if self.regex.match( field[param] ):
                    return True
            except KeyError, e:
                pass
        return False

    def testAll( self, things ):
        return [ thing for thing in things if self.test( thing ) ]


class CloudForcer( object ):
    def __init__( self, user_agent = 'Mozilla/6 (Unix/Linux 64bit) Gecko', proxies = None ):
        self.headers = { 'User-Agent': user_agent }
        self.browser = mechanize.Browser()
        self.browser.set_proxies( proxies );
        self.form_attributes = ['name', 'id', 'class', 'method', 'action']
        self.judge = FieldJudge()

    def getForms( self, forms ):
        ret_forms = []
        return ret_forms

    def find_forms( self, url ):
        response = self.browser.open( urllib2.Request( url, None, self.headers ) )
        if response.code != 200:
            raise Exception( "HTTP Error (Status code {})".format( response.code ) )
        pool = BeautifulSoup( response.read() )

        forms = []
        for i, form in enumerate( pool.findAll( "form" ) ):
            cForm = TestForm( urlparse.urljoin( url, form['action'] ), form['method'], url, self.headers['User-Agent'] )
            if form['method'] != 'post':
                continue
            for child in form.findAll( ['input', 'textarea', 'select'] ):
                try:
                    if False: #not 'name' in child.keys():
                        continue
                    if 'value' in child:
                        cForm.addInput( child['name'], child['value'] or None )
                    if self.judge.test( child ) or child.name == 'textarea':
                        cForm.setInput( child['name'] )
                except AttributeError, err:
                    pass
            forms.append( cForm )
        for form in forms:
            print "Method:", form.method
            print "Action:", form.action
            print form.getSubmitString()
            print form.checkStore()

if __name__ == "__main__":

    forcer = CloudForcer()
    forcer.find_forms( "http://pastebin.com/" )

    # argparse
    # save data
    # lel
