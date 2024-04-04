from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# from typing import TextIO
# import os
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

    def testing(self):

        time.sleep(10)

        pageStructure = self.__driver.find_elements(By.XPATH, NomoScrape.PAGE_STRUCTURE_DIV_XPATH)
        pageHeader    = self.__driver.find_elements(By.XPATH, NomoScrape.PAGE_HEADER_XPATH)
        trafficLight  = self.__driver.find_elements(By.XPATH, NomoScrape.TRAFFIC_LIGHT_XPATH)
        remarks       = self.__driver.find_elements(By.XPATH, NomoScrape.REMARKS_XPATH)
        proofs        = self.__driver.find_elements(By.XPATH, NomoScrape.PROOFS_XPATH)

        mathJax  = self.__driver.find_elements(By.CSS_SELECTOR, NomoScrape.MATH_JAX_TEX_SCRIPT_CSS_SELECTOR)
        mathJax2 = self.__driver.find_elements(By.CSS_SELECTOR, NomoScrape.MATH_JAX_TEX_SCRIPT_2_CSS_SELECTOR)

        mainText = self.__driver.find_elements(By.CSS_SELECTOR, NomoScrape.MAIN_TEXT_CSS_SELECTOR)

        print(f'pageStructure = {pageStructure}', end='\n\n')
        print(f'pageHeader = {pageHeader}',       end='\n\n')
        print(f'trafficLight = {trafficLight}',   end='\n\n')
        print(f'remarks = {remarks}',             end='\n\n')
        print(f'proofs = {proofs}',               end='\n\n')
        print(f'mathJax = {mathJax}',             end='\n\n')
        print(f'mainText = {mainText}',           end='\n\n')

        # for element in proofs:
        #     print(element.text)

        print()

        # TODO: go by phrase_roots in each block and act depending on data-content-type (text\formula links aswell) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # formulas can also either have type="math/tex; mode=display" or just type="math/tex"                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # REMEMBER TO CHECK XPATH                                                                                   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        for element in proofs:
            print(element.get_attribute('innerHTML'))

    # instructions for selenium to access data
    SUBMIT_LOGIN_BUTTON_CSS_SELECTOR: str = 'button[type="submit"]'
    PAGE_STRUCTURE_DIV_XPATH:         str = '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]'
    PAGE_HEADER_XPATH:                str = '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/div[1]/h4'
    TRAFFIC_LIGHT_XPATH:              str = '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div[1]/div'
    REMARKS_XPATH:                    str = '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div'
    PROOFS_XPATH:                     str = '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div'

    MATH_EXAMPLES_XPATH:              str = '/html/body/div[2]/div/div[2]/div/div[1]/div/div[1]/div[4]/div/div'

    MATH_JAX_TEX_SCRIPT_CSS_SELECTOR:   str = 'script[type="math/tex"]'               # in text
    MATH_JAX_TEX_SCRIPT_2_CSS_SELECTOR: str = 'script[type="math/tex; mode=display"]' # center-aligned

    MAIN_TEXT_CSS_SELECTOR:           str = 'div[class="phrase__root"]'

    # json document settings template
    NOMO_SETTINGS_TEMPLATE: str = \
        "nomoSettings: dict[str, str] = {  \n" \
        "    'username' : 'your username', \n" \
        "    'password' : 'your password', \n" \
        "    'url'      : 'your url'       \n" \
        "}                                 \n" \
