from scrape_professor import ScrapeProfessor
from multiprocessing import Pool
from itertools import count
import json
import time

static_startid = 235359
id_generator = (x for x in count(static_startid))
ids404 = []
local_datapath = '/home/zafrin/PycharmProjects/RateMyProfessor'
aws_datapath = '/home/ec2-user'

def output_lastid(prof_id):
    with open(local_datapath+'/data/raw/metadata/lastid.txt', 'w') as file:
        file.write(str(prof_id))

def generate_metadata(prof_id):
    with open(local_datapath+'/data/raw/metadata/metadata.txt', 'a+') as file:
        file.write(str(time.localtime()))
        file.write('\nstarting id: {}\n'.format(prof_id))

def get_ids(cores=8):
    ids_to_process = []
    for core in range(cores):
        ids_to_process.append(next(id_generator))
    print('start id', ids_to_process[0])
    # output_lastid(ids_to_process[-1])
    return ids_to_process


def process(prof_id,cores=4):
    try:
        # print('Spider: trying in spider')
        professor = ScrapeProfessor(prof_id)
        # print('Spider: professor obj created')
        professor.scrape_professor()
        # print('Spider: professor has been scraped')
        professor.scrape_reviews()
        print('Spider: seccess retriving id: {}'.format(prof_id))

    except:
        print('Spider: 404 ERROR for id: {}'.format(prof_id))
        ids404.append(prof_id)

    finally:
        time.sleep(4)


def main():
    pool = Pool()
    generate_metadata(static_startid)
    count = 0

    while True:
        count += 4
        ids = get_ids(cores=4)

        try:
            pool.map(process, ids)
            # output_lastid(ids[-1])

            if count % 100 == 0:
                print('================================')
                print('\n\t{} urls crawled\n'.format(count))
                print('================================')

        except KeyboardInterrupt:
            output_lastid(ids[0]-4)
            print(ids404)
            # feed error ids to 404.txt
            with open(local_datapath+"/RateMyProfessor/data/raw/metadata/404.txt", "a+") as file:
                for i in ids404:
                    json.dump(i, file)
                    file.write('\n')
            break


if __name__ == '__main__':
    main()
    # process(static_startid)