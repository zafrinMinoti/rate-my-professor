from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from itertools import count
import json
import time

_ROOT = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='
driver = webdriver.PhantomJS(
    executable_path='/home/zafrin/Programs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

id_generator = (x for x in count(103667))


def get_lastid(gen=id_generator):
    return next(gen)

def get_reviewer_ids():
    reviewer_ids = []
    raw_ids = driver.find_elements_by_xpath("//tbody//tr")
    for i in raw_ids:
        prob_id = i.get_attribute("id")
        try:
            reviewer_ids.append(int(prob_id))
        except:
            pass

    return reviewer_ids

def loadmore():
    loadmore_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadMore')))
    loadmore_button.click()
    time.sleep(4)

def main():
    prof_id = 103667

    while prof_id < 126962:
        if prof_id not in ids404:
            record = dict()

            url = _ROOT + str(prof_id)
            driver.get(url)

            # Keep loding more reviews as long as there's more to load
            while True:
                try:
                    loadmore()
                except:
                    break

            # Get all the ids and put it in a list and map to prof id in a dictionary
            reviewer_ids = get_reviewer_ids()
            record[prof_id] = reviewer_ids

            # output the dictionary in json
            with open('/RateMyProfessor/data/raw/reviewer_ids.json', 'a+') as file:
                json.dump(record, file)
                file.write(',\n')

            prof_id = next(id_generator)
            print('Ids left:', 126962 - prof_id)
        else:
            prof_id = next(id_generator)

if __name__ == '__main__':
    ids404 = []
    with open('/RateMyProfessor/data/raw/metadata/404.txt') as file:
        for line in file:
            i = int(line.strip().strip('\"'))
            if i > 100470 and i < 126962:
                ids404.append(i)

    main()
    driver.close()