from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from bs4 import BeautifulSoup

class WebConnection:
    _ROOT = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='

    def __init__(self, prof_id):
        self._prof_id = prof_id

        self.driver = webdriver.PhantomJS(executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        self.url = 'tippit.html'
        self.url = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid=1500075'
        self.driver.get(self.url)
        self._soup = self.make_soup()  # Is this necessary

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
        # fhand = open('tippit.html')
        # html = fhand.read()
        # return BeautifulSoup(html, 'html.parser')
        return BeautifulSoup(self.driver.page_source, 'lxml')



class ScrapeReviews(WebConnection):
    def __init__(self, prof_id):
        super(ScrapeReviews, self).__init__(prof_id)
        self._reviews = dict()
        self.init_comments_count = 0

        self.dates = []
        self.rating_types = []

        self.overall_quality = []
        self.level_of_difficulty = []

        self.class_names = []
        self.for_credits = []
        self.attendence_info = []
        self.textbook_used_info = []
        self.would_take_again_info = []
        self.grades_revieved_info = []

        self.tags_by_user = []

        self.comments = []
        self.thumbs_up = []
        self.thumbs_down = []

    @property
    def reviews(self):
        return self._reviews

    def scrape_reviews(self):
        self._review_count = self.total_review_count()
        trail = 1
        try:
            # Verify if the number of student rating is equal to scraped student raviews
            print('trying')
            while not self.all_loaded():
                self.loadmore()
                print(self.total_review_count(), self.loaded_review_count())

            # Else report to problem
        except:
            print('could not load all reviews for professor: {}'.format(self.prof_id))
            print('reporting...\ncooling down...')
            time.sleep(8)
            # with open(failed_report.txt, 'r'):
                ## write

        finally:
            if self.all_loaded():
                ## ADD Professor ID
                ##
                print('All loaded')
                self.set_all_values()
                self.create_records()
                self.dump_records()

            else:
                print('not all_loaded')

            print('All done')

    def set_all_values(self):
        # function calls for setting values to all the fields
        # self.set_loaded_review_count()
        self.review_basic()
        self.set_course_level_info()
        self.set_tags_by_user()
        self.get_comments()
        # self.thumbs()

    def create_records(self):
        # Create touples of records
        self.records = zip(self.dates,
        self.rating_types,
        self.overall_quality,
        self.level_of_difficulty,
        self.class_names,
        self.for_credits,
        self.attendence_info,
        self.textbook_used_info,
        self.would_take_again_info,
        self.grades_revieved_info,
        self.tags_by_user,
        self.comments,
        self.thumbs_up,
        self.thumbs_down)

        return self.records

    def dump_records(self):
        json_to_dump = dict()
        count =0
        for record in self.records:
            print(record)
            print()
            count +=1
            if count ==3: break
            # jason_to_dump[key] = record[0]

    def loadmore(self):
        loadmore_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'loadMore')))
        loadmore_button.click()
        time.sleep(6)

    # Review counts - total and loaded

    def total_review_count(self):
        review_count = self.soup.select(
            'div.table-toggle')[0].get_text().strip().split()[0]
        return int(review_count)

    @property
    def review_count(self):
        return _review_count

    def loaded_review_count(self):
        review_soup = self.driver.find_elements_by_xpath("//td[@class='comments']")
        return len(review_soup)

    def all_loaded(self):
        return self.loaded_review_count() == self.total_review_count()

    # Infomation about the reviews

    def review_basic(self):
        self.set_dates()
        self.set_rating_types()
        self.set_quality_and_difficulity()

    def set_dates(self):
        dates = self.soup.select('div[class=date]')
        self.dates = self.parse_tags(dates)

    def set_rating_types(self):
        rating_types = self.soup.select('span[class=rating-type]')
        self.rating_types = self.parse_tags(rating_types)

    def set_quality_and_difficulity(self):
        quality_and_difficulity = self.soup.select('div.descriptor-container')
        quality_and_difficulity = self.parse_tags(quality_and_difficulity)

        for i, value in enumerate(quality_and_difficulity):
            extracted_value = value.split('\n')[0]
            self.overall_quality.append(extracted_value) if i % 2 == 0 else self.level_of_difficulty.append(extracted_value)

    @staticmethod
    def parse_tags(elements_list):
        for i, element in enumerate(elements_list):
            elements_list[i] = element.text.strip()
        return elements_list

    # Information about the course reviewed

    def set_course_level_info(self):
        classes_raw = self.soup.select('td.class')
        for cls in classes_raw:
            class_info = cls.text.strip().split('\n')
            self.class_names.append(class_info[0])
            class_info = class_info[1:]
            for i, info in enumerate(class_info):
                class_info[i] = info.split(': ')

            self.for_credits.append(class_info[0][1])
            self.attendence_info.append(class_info[1][1])
            self.textbook_used_info.append(class_info[2][1])
            self.would_take_again_info.append(class_info[3][1])
            self.grades_revieved_info.append(class_info[4][1])

    # Tags used in the review

    def set_tags_by_user(self):
        tags_by_user = self.soup.select('div.tagbox')
        print('tags', len(tags_by_user))
        for i, tags in enumerate(tags_by_user):
            user_tags = tags.text.strip().split('\n')
            self.tags_by_user.append(user_tags)

    # Comments
    def get_comments(self):
        self.first_20comments()
        self.more_comments()
        self.thumbs()

    def first_20comments(self):
        # First 20 review comments
        comments_obj_first20 = self.soup.select('p.commentsParagraph')
        self.init_comments_count = len(comments_obj_first20)
        for comment in comments_obj_first20:
            self.comments.append(comment.text.strip())

    def more_comments(self):
        # Rest of the review comments
        comments_obj = self.driver.find_elements_by_xpath("//td[@class='comments']/p")

        for comment in comments_obj[self.init_comments_count:]:
            self.comments.append(comment.text)

    def thumbs(self):
        # Were the comments helpful or not helpful
        thumbs = self.driver.find_elements_by_xpath("//td[@class='comments']//span[@class='count']")
        for direction, thumb in enumerate(thumbs):
            if direction%2==0:
                self.thumbs_up.append(thumb.text)
            else:
                self.thumbs_down.append(thumb.text)



    def test_scrape_reviews(self):
        self.loaded_review_count()
        print(self._loaded_review_count)
        self.set_dates()
        print(self.dates)
        self.set_rating_types()
        print(self.rating_types)

        self.set_quality_and_difficulity()
        print(self.overall_quality)
        print(self.level_of_difficulty)

        self.set_course_level_info()
        print(self.class_names)
        print(self.for_credits)
        print(self.attendence_info)
        print(self.textbook_used_info)
        print(self.would_take_again_info)
        print(self.grades_revieved_info)

        self.set_tags_by_user()
        print(self.tags_by_user)

        self.first_20comments()
        self.more_comments()
        print(self.comments[19:24], sep='\n\n')

        self.thumbs()
        print(self.thumbs_up)
        print(self.thumbs_down)


# test_output = open('test_output.txt', 'wb')
#     test_output.close()

x = ScrapeReviews(1000)
x.scrape_reviews()

print(x.create_records())


x.driver.close()