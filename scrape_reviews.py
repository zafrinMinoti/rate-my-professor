from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from bs4 import BeautifulSoup

fhand = open('tippit.html')
html = fhand.read()
soup = BeautifulSoup(html, 'html.parser')

def student_reviews(soup):
    reviews = dict()

    review_soup = soup.select('td.rating')
    # print(review_soup[0])
    print(len(review_soup))
    print(type(review_soup))

    dates = soup.select('div[class=date]')
    print('Dates', len(dates))

    rating_types = soup.select('span[class=rating-type]')
    print('Rating type', len(rating_types))

    overall_quality = soup.select('span.score average')
    print('Overall Quality', len(overall_quality))

    level_of_difficulty = soup.select('span.score inverse good')
    print('level_of_difficulty', len(level_of_difficulty))

    descriptor_container = soup.select('div.descriptor-container')
    print('descriptor_container', len(descriptor_container))


    class_info = soup.select('td.class')
    print('class', len(class_info))


    tags_by_user = soup.select('div.tagbox')
    print('tags', len(tags_by_user))


# driver = webdriver.PhantomJS(executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
# driver.get('http://www.ratemyprofessors.com/ShowRatings.jsp?tid=1500075')
#
# comments = []
# thumbs_up = []
# thumbs_down = []
#
# test_output = open('test_output.txt', 'wb')
#
# try:
#     while True:
#         loadmore_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadMore')))
#         loadmore_button.click()
#         time.sleep(4)
# except:
#     pass
#
# finally:
#     # First 20 review comments
#     soup = BeautifulSoup(driver.page_source)
#     comments_obj_first20 = soup.select('p.commentsParagraph')
#     comments_found = len(comments_obj_first20)
#     for comment in comments_obj_first20:
#         comments.append(comment.text.strip())
#
#     # Rest of the review comments
#     comments_obj = driver.find_elements_by_xpath("//td[@class='comments']/p")
#
#     # Verify if the number of student rating is equal to scraped student raviews
#
#     # Else report to problem
#
#     for comment in comments_obj[comments_found:]:
#         comments.append(comment.text)
#
#     # Were the comments helpful or not helpful
#     thumbs = driver.find_elements_by_xpath("//td[@class='comments']//span[@class='count']")
#     for direction, thumb in enumerate(thumbs):
#         if direction%2==0:
#             thumbs_up.append(thumb.text)
#         else:
#             thumbs_down.append(thumb.text)
#
#     driver.close()
#     test_output.close()


######################################################################################################################

# class Reviews(Professor):
#     def __init__(self):
#         prof_id
