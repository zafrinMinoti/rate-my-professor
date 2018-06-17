from scrape_professor import ScrapeProfessor
from multiprocessing import Pool
from itertools import count
import json
import time


id_generator = (x for x in count(126960))
static_id = next(id_generator)

def get_lastid(source='data/metadata/lastid.txt'):
    return next(id_generator)
#    with open(source, 'r') as file:
#        return int(file.read())


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


def process(prof_id,cores=8):
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
        time.sleep(1)


def main():
    pool = Pool()
    generate_metadata(static_id + 1)
    count = 0

    while True:
        count += 8
        ids = get_ids(cores=8)

        try:
            pool.map(process, ids)
            # output_lastid(ids[-1])

            if count % 100 == 0:
                print('================================')
                print('\n\t{} urls crawled\n'.format(count))
                print('================================')

        except KeyboardInterrupt:
            output_lastid(ids[0]-8)
            break


if __name__ == '__main__':
    main()