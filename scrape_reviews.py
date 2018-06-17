from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

from bs4 import BeautifulSoup
from web_connection import WebConnection

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
        try:
            # Verify if the number of student rating is equal to scraped student raviews
            while not self.all_loaded():
                self.loadmore()
            # print('Review retrived: {} of {}'.format(self.total_review_count(), self.loaded_review_count()))

            # Else report to problem
        except:
            print('ERROR!\ncould not load all reviews for professor: {}'.format(self.prof_id))
            print('reporting...\ncooling down...')
            time.sleep(4)
            # keep prof_id as metadata for failed jobs
            with open("data/metadata/fialed_loding_reviews.txt", "a+") as file:
                json.dump(self.prof_id, file)
                file.write('\n')

        finally:
            if self.all_loaded():
                self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
                self.set_all_values()
                self.create_record_dict()
                # print('Successul!')

                time.sleep(3)
                self.driver.close()

            else:
                print('not all_loaded')

    def set_all_values(self):
        # function calls for setting values to all the fields
        self.review_basic()
        self.set_course_level_info()
        self.set_tags_by_user()
        self.get_comments()

    def create_record_tuples(self):
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

    def create_record_dict(self):
        self.create_record_tuples()

        for record_tuple in self.records:
            record = dict()
            record['prof_id'] = self.prof_id
            record['date'] = record_tuple[0]
            record['rating_type'] = record_tuple[1]
            record['overall_quality'] = record_tuple[2]
            record['level_of_difficulty'] = record_tuple[3]
            record['class_names'] = record_tuple[4]
            record['for_credits'] = record_tuple[5]
            record['attendence'] = record_tuple[6]
            record['textbook_used'] = record_tuple[7]
            record['would_take_again'] = record_tuple[8]
            record['grades_revieved'] = record_tuple[9]
            record['tags_by_user'] = record_tuple[10]
            record['comments'] = record_tuple[11]
            record['thumbs_up'] = record_tuple[12]
            record['thumbs_down'] = record_tuple[13]

            with open("data/reviews.json", "a+") as file:
                json.dump(record, file)
                file.write(',S\n')

    def loadmore(self):
        loadmore_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'loadMore')))
        loadmore_button.click()
        time.sleep(4)

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
        quality_and_difficulity = self.soup.select('div.break')
        # quality_and_difficulity = self.parse_tags(quality_and_difficulity).split()[0]

        for i, value in enumerate(quality_and_difficulity):
            extracted_value = value.text.split()[0]
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
                class_info[i] = info.split(':')

            self.for_credits.append(class_info[0][1])
            self.attendence_info.append(class_info[1][1])
            self.textbook_used_info.append(class_info[2][1])
            self.would_take_again_info.append(class_info[3][1])
            self.grades_revieved_info.append(class_info[4][1])

    # Tags used in the review

    def set_tags_by_user(self):
        tags_by_user = self.soup.select('div.tagbox')
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