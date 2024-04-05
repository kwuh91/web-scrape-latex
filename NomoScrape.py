from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from LaTeX import LaTeX

import time
import atexit

class NomoScrape:

    # constructor
    def __init__(self, settings: dict[str, str]):

        # declare class fields
        self.__cleanup_required:  bool = True  # needed for atexit && __exit__ logic   

        self.__username: str 
        self.__password: str 
        self.__url:      str

        # check for settings
        assert settings is not None

        # initialize driver
        self.__driver = webdriver.Firefox(
                            service=FirefoxService(
                                GeckoDriverManager().install()
                            )
                        )

        # assign class fields
        self.__username = settings['username']
        self.__password = settings['password']
        self.__url      = settings['url']

        # open url
        self.__driver.get(self.__url)

        # make sure url leads to nomotex
        assert "Nomotex" in self.__driver.title

        # enter user credentials
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located(('name', 
                                            'username'))
        ).send_keys(self.__username)

        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located(('name', 
                                            'password'))
        ).send_keys(self.__password)

        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                                            NomoScrape.SUBMIT_LOGIN_BUTTON_CSS_SELECTOR))
        ).click()
                
        # explicitly wait for the page to load
        time.sleep(10)

        atexit.register(self.__cleanup)

    def __str__(self) -> str:
        pass # todo

    def __repr__(self) -> str:
        pass # todo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__cleanup

    def __cleanup(self):
        if self.__cleanup_required:
            # ... cleanup logic

            # quit driver
            # self.__driver.quit()

            # self.__file.close()

            self.__cleanup_required = False

    def scrape(self, output: LaTeX) -> None:
<<<<<<< HEAD
=======
        # get page header <h4>
        pageHeader: WebElement = self.__driver.find_element(By.CSS_SELECTOR, 
                                                            NomoScrape.PAGE_HEADER_CSS_SELECTOR) 
        pageHeaderText: str = pageHeader.text
        output.writeSection(pageHeaderText, centered=True)
        # print(f'page header: {pageHeaderText}')
>>>>>>> 94c44c98c5a4d4e4c727a1f5ffae85396f41e256

        # # # # # # # # # # # # # # # # # # # # # #
        # <a>                                     #
        # <span data-content-type='text'>         # 
        # <script type='math/tex'>                #
        # <script type='math/tex; mode=display'>  #
        # # # # # # # # # # # # # # # # # # # # # #

        page_elements_css_selector: str = "h4,"                             \
                                          "h5,"                             \
                                          "a,"                              \
                                          "span[data-content-type='text']," \
                                          "script[type='math/tex'],"        \
                                          "script[type='math/tex; mode=display']"

        pageElements: list[WebElement]
        pageElements = self.__driver.find_elements(By.CSS_SELECTOR, 
                                                   page_elements_css_selector)
            
        scriptInstructionsDict = {
            'math/tex'              : lambda element: output.writeFormula(element.get_attribute('innerHTML'), display=False),
            'math/tex; mode=display': lambda element: output.writeFormula(element.get_attribute('innerHTML'), display=True)
        }

        instructionsDict = {
            'h4'    : lambda element: output.writeSection(element.text, centered=True),
            'h5'    : lambda element: output.writeSubSection(element.text),
            'a'     : lambda element: output.write(element.text),
            'span'  : lambda element: output.write(element.text),
            'script': lambda element: scriptInstructionsDict[element.get_attribute('type')](element)
        }

        # find first occurrence of h4 
        firstH4Occurrence: int
        webEl: WebElement
        for index, webEl in enumerate(pageElements):
            if webEl.tag_name == 'h4':
                firstH4Occurrence = index
                break

        # iterate through all the pageElements 
        for i in range(firstH4Occurrence, len(pageElements)):
            pageElement:    WebElement = pageElements[i]
            currentTagName: str        = pageElement.tag_name 

            if currentTagName   == 'h5' and \
               pageElement.text == 'Математические примеры и задачи':
                break

            instructionsDict[currentTagName](pageElement)

    # def scrape(self, output: LaTeX) -> None:
    #     # get page header <h4>
    #     pageHeader: WebElement = self.__driver.find_element(By.CSS_SELECTOR, 
    #                                                         NomoScrape.PAGE_HEADER_CSS_SELECTOR) 
    #     pageHeaderText: str = pageHeader.text
    #     output.writeSection(pageHeaderText, centered=True)
    #     # print(f'page header: {pageHeaderText}')

    #     # get page blocks: Теорема и ее связи, Замечания, Доказательство...
    #     # <div data-name='presentation-slide'>
    #     pageBlocks: list[WebElement] = self.__driver.find_elements(By.CSS_SELECTOR, 
    #                                                                NomoScrape.PAGE_BLOCKS_DIV_CSS_SELECTOR) 

    #     # iterate through <div data-name='presentation-slide'>
    #     pageBlock: WebElement
    #     for pageBlock in pageBlocks: 
    #         # get current page block header <h5>
    #         pageBlockHeader: WebElement
    #         pageBlockHeader = pageBlock.find_element(By.CSS_SELECTOR, 
    #                                                  NomoScrape.PAGE_BLOCK_HEADER_CSS_SELECTOR)
    #         pageBlockHeaderText: str = pageBlockHeader.text
    #         if pageBlockHeaderText != 'Математические примеры и задачи':
    #             output.writeSubSection(pageBlockHeaderText)
    #             # print(f'header: {pageBlockHeaderText}')
            
    #         # get current page block content <span class='phrase'>
    #         pageBlockContents: list[WebElement] 
    #         pageBlockContents = pageBlock.find_elements(By.CSS_SELECTOR, 
    #                                                     NomoScrape.PAGE_BLOCK_CONTENT_CSS_SELECTOR) 
            
    #         # iterate through <span class='phrase'>
    #         pageBlockContent: WebElement
    #         for pageBlockContent in pageBlockContents: 
                
    #             '''
    #             <a>    -> get text
    #             <span> -> get type ->  <span data-content-type='text'>    -> get text
    #                                    <span data-content-type='formula'> -> find script element -> <script type='math/tex'>               -> get text
    #                                                                          && get its type        <script type='math/tex; mode=display'> -> get text
    #             '''

    #             # get current page block content children (<span> or <a>)
    #             child_elements_xpath: str = "./*[self::span or self::a]"
    #             pageBlockContentChildren: list[WebElement] 
    #             pageBlockContentChildren = pageBlockContent.find_elements(By.XPATH, 
    #                                                                       child_elements_xpath)
                                                                          
    #             # iterate through (<span> or <a>)
    #             pageBlockContentChild: WebElement
    #             for pageBlockContentChild in pageBlockContentChildren: 
    #                 currPageBlockContentChildTag = pageBlockContentChild.tag_name # (<span> or <a>)

    #                 if currPageBlockContentChildTag == 'a':
    #                     pageBlockContentChildLink: str = pageBlockContentChild.text # get <a> text
    #                     output.write(pageBlockContentChildLink)
    #                     # print(f'link: {pageBlockContentChildLink}') 

    #                 elif currPageBlockContentChildTag == 'span':
    #                     currSpanDataContentType: str = pageBlockContentChild.get_attribute('data-content-type') # <span data-content-type='formula'> or
    #                                                                                                             # <span data-content-type='text'>
    #                     if currSpanDataContentType == 'text': # <span data-content-type='text'>
    #                         pageBlockContentChildText: str = pageBlockContentChild.text # get <span data-content-type='text'> text
    #                         output.write(pageBlockContentChildText)
    #                         # print(f'text: {pageBlockContentChildText}') 

    #                     elif currSpanDataContentType == 'formula': # <span data-content-type='formula'>
    #                         currFormula: WebElement = pageBlockContentChild.find_element(By.CSS_SELECTOR, 
    #                                                                                      'script')

    #                         currFormulaType: str = currFormula.get_attribute('type') # <script type='math/tex'> or
    #                                                                                  # <script type='math/tex; mode=display'>
    #                         if currFormulaType == 'math/tex': # <script type='math/tex'>
    #                             currFormulaText: str = currFormula.get_attribute("innerHTML") # get <script type='math/tex'> text
    #                             output.writeFormula(currFormulaText, display=False)
    #                             # print(f'formula(in text): {currFormulaText}') 

    #                         elif currFormulaType == 'math/tex; mode=display': # <script type='math/tex; mode=display'>
    #                             currFormulaText: str = currFormula.get_attribute("innerHTML") # get <script type='math/tex; mode=display'> text
    #                             output.writeFormula(currFormulaText, display=True)
    #                             # print(f'formula(display): {currFormulaText}')

    #                         else:
    #                             raise Exception(f'MET UNEXPECTED FORMULA-TYPE: {currFormulaType}')
                        
    #                     else:
    #                         raise Exception(f'MET UNEXPECTED DATA-CONTENT-TYPE: {currSpanDataContentType}')

    #                 else:
    #                     raise Exception(f'MET UNEXPECTED TAG: {currPageBlockContentChildTag}')
                    
    # instructions for selenium to access data
    SUBMIT_LOGIN_BUTTON_CSS_SELECTOR: str = 'button[type="submit"]'
    # PAGE_BLOCKS_DIV_CSS_SELECTOR:     str = 'div[data-name="presentation-slide"]'
    # PAGE_HEADER_CSS_SELECTOR:         str = 'h4'
    # PAGE_BLOCK_HEADER_CSS_SELECTOR:   str = 'h5'
    # PAGE_BLOCK_CONTENT_CSS_SELECTOR:  str = 'span[class="phrase"]'

    # json document settings template
    NOMO_SETTINGS_TEMPLATE: str = \
        "nomoSettings: dict[str, str] = {  \n" \
        "    'username' : 'your username', \n" \
        "    'password' : 'your password', \n" \
        "    'url'      : 'your url'       \n" \
        "}                                 \n" \
