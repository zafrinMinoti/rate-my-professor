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
    startid = get_lastid()
    ids_to_process = []
    for core in range(cores):
        ids_to_process.append(startid)
        startid += 1
    output_lastid(ids_to_process[-1])
    return ids_to_process

def process(prof_id):
    error = 0
    currentid = prof_id
    generate_metadata(currentid)

    while True and error < 100000:
        try:
            professor = ScrapeProfessor(currentid)
            professor.scrape_professor()
            professor.scrape_reviews()
            print('seccess retriving id: {}'.format(currentid))

        except:
            print('404 ERROR for id: {}'.format(currentid))
            # feed error ids to 404.txt
            with open("data/metadata/404.txt", "a+") as file:
                json.dump(str(currentid), file)
                file.write('\n')

            error += 1

            # process another one
            process_another()
            break

        finally:
            time.sleep(5)

def process_another():
    nextid = get_lastid() + 1
    process(nextid)
    output_lastid(nextid)

def main():
    pool = Pool()
    ids = get_ids(cores=2)
    pool.map(process, ids)


if __name__ == '__main__':
    main()