import requests
from bs4 import BeautifulSoup
import re
from ast import literal_eval

class WebConnection:
    _ROOT = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='

    def __init__(self, prof_id):
        self._prof_id = prof_id
        self._soup = self.make_soup()   # Is this necessary

    @property
    def prof_id(self):
        return self._prof_id

    @property
    def soup(self):
        return self._soup

    def make_soup(self):
        '''
        Should be made using driver
        '''
        # page = requests.get(_ROOT+str(self.prof_id))
        # html = page.text
        fhand = open('tippit.html')
        html = fhand.read()
        return BeautifulSoup(html, 'html.parser')


class ScrapeProfessor(WebConnection):
    def __init__(self, prof_id):
        super(ScrapeProfessor, self).__init__(prof_id)
        self._info = dict()

    @property
    def info(self):
        return self._info

    def scrape(self):
        self.info['id'] = self.prof_id
        self.info.update(self.scrape_basic_info())
        self.info.update(self.scrape_quality_info())
        self.info.update(self.scrape_tags())

        return self.info

    def scrape_basic_info(self):
        basic = dict()

        basic_info_script = self.soup.select('script')[3].text
        info_dict = re.search(
            'pageLevelData:\s({.+}),\s*reloadInterval:', basic_info_script).group(1)
        basic_info = literal_eval(info_dict)

        basic['name'] = basic_info['prop7']
        basic['school'] = basic_info['prop6']
        basic['school_id'] = basic_info['schoolid']
        basic['subject'] = basic_info['prop3']
        # fname = soup.select('span.pfname')[0].get_text().strip()
        # mname = soup.select('span.pfname')[1].get_text().strip()
        # lname = soup.select('span.plname')[0].get_text().strip()
        # name = fname+' '+lname if mname == '' else fname+' '+mname+' '+lname
        # print(name)
        geo_info = self.soup.select('h2.schoolname')[0].get_text().split(',')
        basic['city'] = geo_info[1].strip()
        basic['state'] = geo_info[2].strip()

        return basic

    def scrape_quality_info(self):
        quality = dict()

        all_qualities = self.soup.select('div.grade')

        quality['overall_quality'] = all_qualities[0].get_text().strip()
        quality['take_again'] = all_qualities[1].get_text().strip()
        quality['level_of_difficulity'] = all_qualities[2].get_text().strip()

        hotness = re.search('chilis/(.+)\.png', str(self.soup)).group(1)
        quality['hotness'] = hotness

        review_count = self.soup.select(
            'div.table-toggle')[0].get_text().strip().split()[0]
        quality['review_count'] = int(review_count)

        return quality

    def scrape_tags(self):
        tags = dict()
        raw_tags = self.soup.select('span.tag-box-choosetags')

        for tag in raw_tags:
            tag = tag.get_text().strip()
            tag_key = tag[:-4].strip().lower()
            tag_count = tag[-2]
            tags[tag_key] = tag_count

        return tags

# professor = ScrapeProfessor(0000)
# print(professor.scrape())