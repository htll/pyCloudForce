import mechanize
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
        bowls = bowls + [ bowl for bowl in browser.forms() for param, regex in self.noodle_judges if regex.match( bowl.[param] ) ]

        # browser.select_form( predicate=(lambda x: (x.attrs['class'] == soup.textarea.findParent('form')['class']) if 'class' in x.attrs else False ) )
        return list( set( bowls ) )

if __name__ == "__main__":
    import argparse
    # argparse
    # save data
    # lel

