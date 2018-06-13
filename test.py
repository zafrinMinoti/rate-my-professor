####################################################################################################################
#                REVIEW COMMENTS AND THUMBS
####################################################################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS(executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.get('http://www.ratemyprofessors.com/ShowRatings.jsp?tid=1500075')

comments = []
thumbs_up = []
thumbs_down = []

test_output = open('test_output.txt', 'wb')

# First 20 review comments
soup = BeautifulSoup(driver.page_source)
comments_obj_first20 = soup.select('p.commentsParagraph')
comments_found = len(comments_obj_first20)
count = 1
for comment in comments_obj_first20:
    comments.append(comment.text.strip())
    print(count)
    pickle.dump(count, test_output)
    pickle.dump('\n', test_output)
    pickle.dump(comment.text, test_output)
    pickle.dump('\n\n', test_output)
    count += 1

try:
    while True:
        loadmore_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadMore')))
        loadmore_button.click()
        time.sleep(4)
except:
    pass

finally:

    # Rest of the review comments
    comments_obj = driver.find_elements_by_xpath("//td[@class='comments']/p")

    for comment in comments_obj[comments_found:]:
        print(count)
        comments.append(comment.text)
        #print(comment.text)
        pickle.dump(count, test_output)
        pickle.dump('\n', test_output)
        pickle.dump(comment.text, test_output)
        pickle.dump('\n\n', test_output)
        count +=1

    thumbs = driver.find_elements_by_xpath("//td[@class='comments']//span[@class='count']")
    for direction, thumb in enumerate(thumbs):
        if direction%2==0:
            thumbs_up.append(thumb.text)
        else:
            thumbs_down.append(thumb.text)


    print(len(comments), len(thumbs_up), len(thumbs_down))

    print('comment: ', comments[0])
    print('thumbs: ', thumbs_down[0])
    print('ALL DONE')

    driver.close()
    test_output.close()


######################################################################################################################

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from bs4 import BeautifulSoup
#
# driver = webdriver.PhantomJS(executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
# # driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
# driver.get('http://www.ratemyprofessors.com/ShowRatings.jsp?tid=1500075')
#
# comments = driver.find_elements_by_xpath("//td[@class='comments']/p")
# # for comment in comments:
# #     print(comment.text)
# print('Comments Before', len(comments))
#
# thumbs = driver.find_elements_by_xpath("//td[@class='comments']//span[@class='count']")
# print('Thumbs Before', len(thumbs))
#
# print("-------------------------------------")
#
# try:
#     count = 0
#     while True:
#         element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadMore')))
#         element.click()
#         count += 1
#         print('clicked: ', count)
#         comments = driver.find_elements_by_xpath("//td[@class='comments']/p")
#         print('Comments Found', len(comments))
#         thumbs = driver.find_elements_by_xpath("//td[@class='comments']//span[@class='count']")
#         print('Thumbs Found', len(thumbs))
#         time.sleep(2)
# except:
#     print('cannot load any more. aborting...')
#
# finally:
#     comments = driver.find_elements_by_xpath("//td[@class='comments']/p")
#     print('After using driver', len(comments))
#     # for comment in comments:
#     #     print(comment.text)
#
#     thumbs = driver.find_elements_by_xpath("//td[@class='comments']//span[@class='count']")
#     print('Thumbs After', len(thumbs))
#
# driver.close()
#
#
######################################################################################################################