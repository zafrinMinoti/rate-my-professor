from selenium import webdriver
from bs4 import BeautifulSoup

class WebConnection:
    _ROOT = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='

    def __init__(self, prof_id):
        self._prof_id = prof_id
        self.url = WebConnection._ROOT+str(self.prof_id)
        self.driver = webdriver.PhantomJS(executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')

    @property
    def prof_id(self):
        return self._prof_id