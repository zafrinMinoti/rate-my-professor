from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from bs4 import BeautifulSoup

# For test
driver = webdriver.PhantomJS(executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get('tippit.html')


fhand = open('tippit.html')
html = fhand.read()
soup = BeautifulSoup(html, 'html.parser')

def student_reviews(soup):
    reviews = dict()

    review_soup = soup.select('td.rating')
    print(review_soup[0])
    print('number of reviews', len(review_soup))

    # dates = soup.select('div[class=date]')
    # print('Dates', len(dates))
    # print(dates[0].text.strip())

    # rating_types = soup.select('span[class=rating-type]')
    # print('Rating type', len(rating_types))
    # print(rating_types[0].text.strip())

    # overall_quality = []
    # level_of_difficulty = []
    #
    # quality_and_difficulity = soup.select('div.descriptor-container')
    # print('quality_and_difficulity', len(quality_and_difficulity))
    # for i, value in enumerate(quality_and_difficulity):
    #     overall_quality.append(value) if i%2==0 else level_of_difficulty.append(value)

    # print('Overall_quality: ', len(overall_quality))
    # print('leval of difficulity: ', len(level_of_difficulty))

    class_names = []
    for_credits = []
    attendence_info = []
    textbook_used_info = []
    would_take_again_info = []
    grades_revieved_info = []
    classes_raw = soup.select('td.class')
    print('class', len(classes_raw))

    for cls in classes_raw:
        class_info = cls.text.strip().split('\n')
        class_names.append(class_info[0])
        class_info = class_info[1:]
        for i, info in enumerate(class_info):
            class_info[i] = info.split(': ')

        for_credits.append(class_info[0][1])
        attendence_info.append(class_info[1][1])
        textbook_used_info.append(class_info[2][1])
        would_take_again_info.append(class_info[3][1])
        grades_revieved_info.append(class_info[4][1])
        print(class_info)


    for i in [class_names, for_credits, attendence_info, textbook_used_info, would_take_again_info, grades_revieved_info]:
        print(len(i), sep='  ')

    for i in [class_names, for_credits, attendence_info, textbook_used_info, would_take_again_info, grades_revieved_info]:
        print(i)



    tags_by_user = soup.select('div.tagbox')
    print('tags', len(tags_by_user))
    print(tags_by_user[0].text)

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

student_reviews(soup)

driver.close()