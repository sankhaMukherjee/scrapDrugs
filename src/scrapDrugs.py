from logs import logDecorator as lD
from lib import simpleLib as sL
from lib import webContent as wC

from lib.decoders import drugs as dr

import json

config = json.load(open('../config/config.json'))

@lD.logInit(config['logging']['logBase'], config['logging']['logFolder'])
def main(logger):
    '''main program
    
    This is the place where the entire program is going
    to be generated.
    '''

    # Lets just create a simple testing 
    # for other functions to follow
    # -----------------------------------
    

    # This is used for testing simple urls
    # ------------------------------------
    url = 'https://www.drugs.com/condition/depression.html'
    while True:

        results = wC.downloadURLsimple(url)
        results = results.decode("utf-8") 
        drugList = dr.getDrugList(results)

        print('-'*30)
        for k in drugList['medNames']:
            print('{:30} -> {}'.format(k, drugList['medNames'][k]))
        
        if drugList['nextLink'] is not None:
            url = 'https://www.drugs.com' + drugList['nextLink']
        else:
            break



    # dictRes = dr.drugOverview(results)
    # for s in results.split('\n'):
    #     print(s)
    # print(dictRes)
    
    # This uses webdrivers
    # ------------------------------------
    # dr.drugInfo('https://www.drugs.com/abilify.html')
    return

if __name__ == '__main__':
    main()