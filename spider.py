from scrape_professor import ScrapeProfessor
from multiprocessing import Pool
from itertools import count
import json
import time

id_generator = (x for x in count(151103))
static_id = next(id_generator)
ids404 = []

def get_lastid(gen=id_generator):
    return next(gen)


def output_lastid(prof_id):
    with open('data/metadata/lastid.txt', 'w') as file:
        file.write(str(prof_id))


def generate_metadata(prof_id):
    with open('data/metadata/metadata.txt', 'a+') as file:
        file.write(str(time.localtime()))
        file.write('\nstarting id: {}\n'.format(prof_id))

def get_ids(cores=8):
    startid = get_lastid()
    ids_to_process = []
    for core in range(cores):
        ids_to_process.append(next(id_generator))
        print('start id', startid)
        startid += 1
    # output_lastid(ids_to_process[-1])
    return ids_to_process


def process(prof_id,cores=20):
    try:
        professor = ScrapeProfessor(prof_id)
        professor.scrape_professor()
        professor.scrape_reviews()
        print('seccess retriving id: {}'.format(prof_id))

    except:
        print('404 ERROR for id: {}'.format(prof_id))
        ids404.append(prof_id)

    finally:
        time.sleep(4)


def main():
    pool = Pool()
    generate_metadata(static_id + 1)
    count = 0

    while True:
        count += 20
        ids = get_ids(cores=20)

        try:
            pool.map(process, ids)
            # output_lastid(ids[-1])

            if count % 100 == 0:
                print('================================')
                print('\n\t{} urls crawled\n'.format(count))
                print('================================')

        except KeyboardInterrupt:
            output_lastid(ids[0]-20)
            # feed error ids to 404.txt
            with open("data/metadata/404.txt", "a+") as file:
                for i in ids404:
                    json.dump(i, file)
                    file.write('\n')
            break


if __name__ == '__main__':
    main()