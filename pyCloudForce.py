import mechanize
import re
from BeautifulSoup import BeautifulSoup

class CloudForcer:
    def __init__( self, proxies=None ):
        self.browser = mechanize.Browser()
        self.browser.set_proxies( proxies )

    def upload( data, url ):
        resp = browser.open( url )
        soup = BeautifulSoup( browser.read() )
        browser.select_form( predicate=(lambda x: (x.attrs['class'] == soup.textarea.findParent('form')['class']) if 'class' in x.attrs else False ) )


if __name__ == "__main__":
    import argparse
    # argparse
    # save data
    # lel

