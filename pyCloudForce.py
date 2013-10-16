import urllib
import urllib2
import re
import base64
from BeautifulSoup import BeautifulSoup

class CloudForm:
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

    def submit():
        data = getSubmitString()
        if self.method == 'get':
            self.action += '?' + data
            data = None

        response = urllib2.urlopen( urllib2.Request( self.action, data, self.headers ) )
        if response.code != 200:
            raise Exception( "HTTP Error (Status code {})".format( response.code ) )
        pool = BeautifulSoup( response.read() )
        return pool

class TestForm( CloudForm ):
    def __init__( self, action, method = 'get', url = None, user_agent = 'Mozilla/6 (Unix/Linux 64bit) Gecko' ):
        super( self.__class__, self ).__init__( action, method, url, user_agent )
        self.data = {}

    def setInput( self, name, value = None ):
        value = value | base64.b64encode( name )
        self.data[ name ] = value


class FieldJudge:
    def __init__( self, parameters = ['name', 'id', 'class'], regex = re.compile('(paste|text|input|data|comment)') ):
        self.params = parameters
        self.regex = regex

    def test( self, field ):
        for param in self.params:
            if regex.match( field[param] ):
               return true
        return false

    def testAll( self, things ):
        return [ thing for thing in things if test( thing ) ]

class CloudForcer:
    def __init__( self, user_agent = 'Mozilla/6 (Unix/Linux 64bit) Gecko' ):
        self.headers = { 'User-Agent': user_agent }
        self.form_attributes = ['name', 'id', 'class', 'method', 'action']

    def getForms( self, forms ):
        ret_forms = []
        return ret_forms

    def find_forms( self, url ):
        response = urllib2.urlopen( urllib2.Request( url, None, self.headers ) )
        if response.code != 200:
            raise Exception( "HTTP Error (Status code {})".format( response.code ) )
        pool = BeautifulSoup( response.read() )

        forms = []
        for i, form in enumerate( pool.findAll( "form" ) ):
            cForm = CloudForm( form['action'], form['method'], url, self.headers['User-Agent'] )
            if form['method'] != 'post':
                continue
            for child in form.contents:
                try:
                    if child.name == "input" or child.name == "textarea" or child.name == "select":
                        if child['type'] == "submit":
                            cForm.addSubmit( child['name'] )
                        else:
                            cForm.addInput( child['name'], child['value'] )
                except AttributeError, err:
                    pass
            forms.append( cForm )

        for form in forms:
            print "Method:", form.method
            print "Action:", form.action
            print form.getSubmitString()


if __name__ == "__main__":

    forcer = CloudForcer()
    forcer.find_forms( "http://pastebin.com/" )


    # argparse
    # save data
    # lel

