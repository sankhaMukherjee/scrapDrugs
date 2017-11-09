'''obtain information from drugs.com

This file contains functions that help with the 
download of files from the internet. 
'''

from bs4  import BeautifulSoup
from logs import logDecorator as lD
import json


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