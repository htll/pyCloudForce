import urllib
import urllib2
import re
from BeautifulSoup import BeautifulSoup

class CloudForcer:
    def __init__( self, proxies=None, judges=[(param, re.compile('(paste|text|input|data|comment)')) for param in ['name', 'id', 'class']] ):
        self.browser = mechanize.Browser()
        self.browser.set_proxies( proxies )
        self.noodle_judges = judges

    def save_data( self, data, url ):
        forms = find_forms( url )

    def find_forms( self, url ):
        resp = self.browser.open( url )
        soup = BeautifulSoup( resp.read() )

        useful_soup = soup.findAll( "input" )
        valuable_soup = soup.findAll( "textarea" ) # textareas are always valuable!

        for noodle in useful_soup:
            for param, regex in self.noodle_judges:
                if regex.match( noodle[param] ):
                    valuable_soup.append( noodle )
        bowls = [ noodle.findParent('form') for noodle in useful_soup ]
        bowls = bowls + [ bowl for bowl in browser.forms() for param, regex in self.noodle_judges if regex.match( bowl[param] ) ]

        # browser.select_form( predicate=(lambda x: (x.attrs['class'] == soup.textarea.findParent('form')['class']) if 'class' in x.attrs else False ) )
        return list( set( bowls ) )

class CloudForm:
    def __init__(self,method="get",action=None):
        self.method = method
        self.action = action
        self.inputs = {}
        self.submit = None

    def addInput(self,name=None,value=None):
        self.inputs[name] = value

    def addSubmit(self,name):
        self.submit = name

    def getSubmitString(self,values=[]):
        submitstr = {}
        for kv in self.inputs:
            #submitstr[key] = val
            print kv
        if self.submit:
            submitstr[self.submit] = "Submit"
        return urllib.urlencode(submitstr)



class CloudForcer2:
    def __init__(self):
        self.user_agent = "Mozilla/6 (Unix/Linux 64bit) Gecko"
        self.headers = {"user-agent": self.user_agent}
        self.form_attributes = ["name","id","class","method","action"]

    def getForms(self,forms):
        ret_forms = []
        for i,form in enumerate(forms):
            cForm = CloudForm()
            for attribute in self.form_attributes:
                try:
                    cForm.method = form["method"]
                    cForm.action = form["action"]
                except KeyError,err:
                    pass
            for child in form.contents:
                try:
                    if child.name == "input" or child.name == "textarea" or child.name == "select":
                        if child["type"] == "submit":
                            cForm.addSubmit(child["name"])
                        elif child["type"] == "hidden":
                            cForm.addInput(child["name"],child["value"])
                        else:
                            cForm.addInput(name=child["name"])
                except AttributeError,err:
                    pass
            ret_forms.append(cForm)
        return ret_forms






    def find_forms(self,url):
        request = urllib2.Request(url,None,self.headers)
        response = urllib2.urlopen(request)
        page = response.read()
        pool = BeautifulSoup(page)

        #Find all forms
        poolforms = pool.findAll("form")

        #
        forms = self.getForms(poolforms)
        for form in forms:
            print "Method:",form.method
            print "Action:",form.action
            print form.getSubmitString(["Testing"])





if __name__ == "__main__":

    forcer = CloudForcer2()
    forcer.find_forms("http://pastebin.com/")


    # argparse
    # save data
    # lel

