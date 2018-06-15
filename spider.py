from scrape_professor import ScrapeProfessor
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


def main():
    error = 0
    currentid = get_lastid()
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

            if currentid == get_lastid() + 1:
                error += 1
            else:
                error = 1
        finally:
            output_lastid(currentid)
            currentid += 1
            time.sleep(5)

if __name__ == '__main__':
    main()