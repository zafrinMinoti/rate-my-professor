from scrape_professor import ScrapeProfessor
from multiprocessing import Pool
import json
import time

def get_lastid(source='data/metadata/lastid.txt'):
    with open(source, 'r') as file:
        return int(file.read())

def output_lastid(prof_id):
    with open('data/metadata/lastid.txt', 'w') as file:
        file.write(str(prof_id))

def generate_metadata(prof_id):
    with open('data/metadata/metadata.txt', 'a+') as file:
        file.write(str(time.localtime()))
        file.write('\nstarting id: {}\n'.format(prof_id))

def get_ids(cores=2):
    startid = get_lastid() + 1
    ids_to_process = []
    for core in range(cores):
        ids_to_process.append(startid)
        startid += 1
        print('start id', startid)
    return ids_to_process

def process(prof_id):
    try:
        professor = ScrapeProfessor(prof_id)
        professor.scrape_professor()
        professor.scrape_reviews()
        print('seccess retriving id: {}'.format(prof_id))

    except:
        print('404 ERROR for id: {}'.format(prof_id))
        # feed error ids to 404.txt
        with open("data/metadata/404.txt", "a+") as file:
            json.dump(str(prof_id), file)
            file.write('\n')

    finally:
        time.sleep(6)

def main():
    pool = Pool()
    generate_metadata(get_lastid()+1)
    count = 0

    while True:
        count+=4

        ids = get_ids(cores=4)
        output_lastid(ids[-1])
        pool.map(process, ids)

        if count%100 == 0:
            print('================================')
            print('\n\t{} urls crawled\n'.format(count))
            print('================================')

if __name__ == '__main__':
    main()