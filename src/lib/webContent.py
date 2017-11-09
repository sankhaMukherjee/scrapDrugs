'''get url contents

This file contains functions that help with the 
download of files from the internet. 
'''

from logs import logDecorator as lD
import json
from urllib import request
from selenium import webdriver

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.webContent'

@lD.log(logBase + '.downloadURLsimple')
def downloadURLsimple(logger, url):
    '''obtain the data from a url and return it
    
    Given a url, this is going to read data from the url and
    return it as a string. This is not goign to run scripts
    so if there is javascript, then this is not a good function
    to use. 
    
    Parameters
    ----------
    logger : {logging.logger}
        The logging object
    url : {str}
        The url from which the data is to be downloaded.
    
    Returns
    -------
    str
        contents of the webpage in the form of a string. In the case
        that there was a problem, theh, this will return an empty
        string. 
    '''

    result = ''

    req     = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    results = request.urlopen(req).read()

    
    return results

@lD.log(logBase + '.downloadURLselenium')
def downloadURLselenium(logger, url):
    '''obtain the data from a url and return it
    
    Given a url, this is going to read data from the url and
    return it as a string. This is not goign to run scripts
    so if there is javascript, then this is not a good function
    to use. 
    
    Parameters
    ----------
    logger : {logging.logger}
        The logging object
    url : {str}
        The url from which the data is to be downloaded.
    
    Returns
    -------
    str
        contents of the webpage in the form of a string. In the case
        that there was a problem, theh, this will return an empty
        string. 
    '''

    result = ''

    driver = webdriver.Chrome(executable_path='../drivers/chromedriver')
    driver.get(url)

    
    return results

