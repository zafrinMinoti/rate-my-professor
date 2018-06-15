import re
import json
from scrape_reviews import ScrapeReviews

class ScrapeProfessor(ScrapeReviews):
    def __init__(self, prof_id):
        super(ScrapeProfessor, self).__init__(prof_id)
        self._prof_info = dict()

    @property
    def prof_info(self):
        return self._prof_info

    def scrape_professor(self):
        print('Connecting to professor: {}'.format(self.prof_id))
        self.prof_info['id'] = self.prof_id
        self.prof_info.update(self.scrape_basic_info())
        self.prof_info.update(self.scrape_quality_info())
        self.prof_info.update(self.scrape_tags())

        # return self.prof_info
        try:
            with open("data/professors.json", "a+") as file:
                json.dump(self.prof_info, file)
                file.write('\n')

        except TypeError:
            pass

        finally:
            # print('Retrived professor: {}'.format(self.prof_id))
            pass

    def scrape_basic_info(self):
        basic = dict()

        fname = self.driver.find_element_by_xpath("//span[@class='pfname']").text
        lname = self.driver.find_element_by_xpath("//span[@class='plname']").text
        basic['name'] = fname + ' ' + lname
        basic['school'] = self.driver.find_element_by_xpath("//a[@class='school']").text
        basic['school_link'] = self.driver.find_element_by_xpath("//a[@class='school']").get_attribute("href")
        basic['dept'] = self.driver.find_element_by_xpath("//div[@class='result-title']").text.split('\n')[0]
        geo = self.driver.find_element_by_xpath("//h2[@class='schoolname']").text.split(',')
        basic['city'] = geo[1].strip()
        basic['state'] = geo[2].strip()

        return basic

    def scrape_quality_info(self):
        quality = dict()

        all_qualities = self.soup.select('div.grade')

        quality['overall_quality'] = all_qualities[0].get_text().strip()
        quality['take_again'] = all_qualities[1].get_text().strip()
        quality['level_of_difficulity'] = all_qualities[2].get_text().strip()

        hotness = re.search('chilis/(.+)\.png', str(self.soup)).group(1)
        quality['hotness'] = hotness

        quality['review_count'] = self.total_review_count()

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
