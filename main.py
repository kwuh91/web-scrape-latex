from LaTeX import LaTeX
from NomoScrape import NomoScrape

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# settings JSON for LaTeX
docSettings: dict[str, str       |
                       list[str] |
                       dict[str, list[str]]] = {
    'fileName'     : 'myFile',
    'filePath'     : 'default', # latex folder dir
    'fileMode'     : 'w',
    'fileEncoding' : 'utf-8',
    'docClassType' : 'article',
    'docClassPars' : ['a4paper, 12pt, oneside'],
    'packages'     : { 
        'babel'     : ['russian'],
        'amsmath'   : [],
        'geometry'  : ['top=26mm', 'bottom=20mm', 'left=20mm', 'right=20mm'],
        # ...
    },
    'title'  : 'title', # no title
    'author' : 'author', # no author
}

# settings JSON for NomoScrape
nomoSettings: dict[str, str] = { 
    'username' : '',       
    'password' : '',      
    'url'      : 'https://nomotex.bmstu.ru/element/1252/?from=eyJ0IjoiYyIsImNpIjoiMDIuMDMuMDFfMDEiLCJsZSI6MTkwLCJjIjoxNCwibSI6MjE2LCJwIjo4ODEsImUiOjEyNTJ9'
}

if __name__ == '__main__':
    # print(LaTeX.DOC_SETTINGS_TEMPLATE)
    # print(NomoScrape.NOMO_SETTINGS_TEMPLATE)

    # doc = LaTeX(docSettings)
    scrape = NomoScrape(nomoSettings)
    
    scrape.testing()
