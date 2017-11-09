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
    

    results = wC.downloadURLsimple('https://www.drugs.com/abilify.html')
    results = results.decode("utf-8") 
    dictRes = dr.drugOverview(results)
    # for s in results.split('\n'):
    #     print(s)

    print(dictRes)

    return

if __name__ == '__main__':
    main()