'''obtain information from drugs.com

This file contains functions that help with the 
download of files from the internet. 
'''

import json

from bs4                           import BeautifulSoup
from logs                          import logDecorator as lD
from time                          import sleep
from selenium                      import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC

config = json.load(open('../config/config.json'))
logBase = config['logging']['logBase'] + '.lib.decoders.drugs'

@lD.log(logBase + '.drugOverview')
def drugOverview(logger, html):
    '''retrieve an overview of the drug
    
    Given information about a particular drug, this 
    
    Parameters
    ----------
    logger : {logging.Logger}
        Unsed for logging information
    html : {str}
        The HTML string containing the description of the 
        drug in question. 
    
    Returns
    -------
    dict
        Information about the drug
    '''

    result = {}

    soup = BeautifulSoup(html, 'html.parser')
    result['title'] = soup.title.string

    for d in soup.find_all('p'):
        temp = d.string
        temp1 = d.attrs
        try:
            print(temp1,'--->',temp)
        except Exception as e:
            pass
    
    return result


@lD.log(logBase + '.drugInfo')
def drugInfo(logger, url, VERBOSE=None):
    '''retrieve an overview of the drug
    
    This function does the job of going to a particular
    website, and downloading information from the website
    directly. This function is useful wheh the page is not
    static, and information is retrieved through some form
    of JS before displaying that to the webpage.

    Parsing website - https://drugs.com
    
    Information that this returns:

        - Generic Name
        - Brand Names
        - types of diagnosis associated with

    
    Parameters
    ----------
    logger : {logging.Logger}
        Unsed for logging information
    url : {str}
        The url from which information has to be extracted.
    
    Returns
    -------
    dict
        Information about the drug
    '''

    # Automatically turn off verbosity
    if VERBOSE is None:
        try:
            VERBOSE = config['verbose']
        except:
            VERBOSE = False

    result = {}


    # Normal things related to invoking the web driver
    try:
        driver = webdriver.Chrome(executable_path='../drivers/chromedriver')
        driver.get(url)
        if VERBOSE:
            print('Waiting for the page to load')
        sleep( config['webpageLoadTime'] )

    except Exception as e:
        logger.error('Unable to get the webpage: [{}]\n{}'.format(
            url, str(e)))
        return result

    # Specifically get information about the webpage
    # --------------------------------------------------

    # First lets get the generic if possible
    try:
        elements = driver.find_elements_by_class_name("drug-subtitle")
        for e in elements:
            text = e.text.split('\n')
            for t in text:
                k, v = t.split(':')
                result[k] = v
    except Exception as e:
        if VERBOSE:
            print('Unable to locate information for the generics\n{}'.format(str(e)))
        logger.error('Unable to find the generic and commercial names ...\n{}'.format(
            str(e)))

    # Next go to the dose tab
    foundProf = False
    try:
        elements = driver.find_elements_by_class_name("nav-item")
        for e in elements:
            text = e.text
            
            if VERBOSE:
                print('Nav-item: {}'.format(text))
            
            if 'Professional' in text:
                foundProf = True
                e.click()
                break

    except Exception as e:
        if VERBOSE:
            print('Unable to go to the dose tab\n{}'.format(str(e)))
        logger.error('Unable to go to the dose tab\n{}'.format(
            str(e)))  


    if foundProf: 
        if VERBOSE:
            print('Going to the dose tab')
        sleep( config['webpageLoadTime'] )

        try:
            if VERBOSE:
                print('Finding the fda element')
            element0  = driver.find_element_by_id("fda")
            element1  = element0.find_element_by_tag_name('dl')
            elements2 = element1.find_elements_by_tag_name('dd')

            if VERBOSE:
                print('{} elements found for the dd tages'.format(len(elements2)))
            for e in elements2:
                text = e.text
                text = text.split('[')[0].strip()
                if 'disorder' not in result:
                    result['disorder'] = [text]
                else:
                    result['disorder'].append(text)


        except Exception as e:
            if VERBOSE:
                print('problem with finding elements within the error tabs:\n{}'.format(str(e)))
            logger.error('Unable to locate FDA information.\n{}'.format(
                str(e)))

    else:
        logger.warning('Unable to get to the dosage tab ...')

    driver.close()

    print(result)

    return result