from spacy import load
nlp = load('en')
from multiprocessing import Pool

def extract_comments_sents():
    '''
    IN: file: raw scraped reviews
    OUT 1: file: review comments - one sentence per line
    OUT 2: file: review comments tracker - prof_if, revirwer_id, sent_id - for each sentence per line
    '''

    raw = '../RateMyProfessor/data/raw/reviews.json'
    intermi = '../RateMyProfessor/data/intermediate/comments/'
    processed = '../RateMyProfessor/data/intermediate/processed/'

    with open(raw, 'r') as raw_file, \
            open(intermi+'comment_sents_tracker.txt', 'w') as tracker, \
            open(intermi+'comment_sents_raw.txt', 'w') as comments:

        for line in raw_file:
            indict = line[:-2]      # deselect the comma (,) from the end of the line
            indict = eval(indict)

            comment = indict['comments']
            parsed_comment = nlp(comment)

            for num, sent in enumerate(parsed_comment.sents):
                tracker.write('{},{},{}\n'.format(indict['prof_id'], indict['reviewer_id'], num))
                comments.write('{}\n'.format(sent))


def extract_comments():
    '''
    IN: file: raw scraped reviews
    OUT 1: file: review comments - one comment per line
    OUT 2: file: review comments tracker - prof_if, revirwer_id - for one comment per line
    '''

    raw = '../RateMyProfessor/data/raw/reviews.json'
    intermi = '../RateMyProfessor/data/intermediate/comments/'

    with open(raw, 'r') as raw_file, \
            open(intermi + 'comment_tracker.txt', 'w') as tracker, \
            open(intermi + 'comment_raw.txt', 'w') as comments:

        for line in raw_file:
            indict = line[:-2]  # deselect the comma (,) from the end of the line
            indict = eval(indict)

            tracker.write('{},{}\n'.format(indict['prof_id'], indict['reviewer_id']))
            comments.write('{}\n'.format(indict['comments']))

def write_raw_comments(raw_comment_list, outfile):
    outfile.write('llll')

def write_raw_comment_sents(raw_comment_sent_list, outfile):
    pass

def write_tokanized_comment(raw_comment_list, outfile):
    pass

def mainnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn():
    count = 0

    prof_ids = []
    reviewer_ids = []
    comments = []

    pr_sent_ids = []
    sents = []

    tokenized_comments = []
    tokenized_sents = []

    with open(raw, 'r') as raw_file, \
            open(intermi + 'comment_tracker.txt', 'w') as comment_tracker_file, \
            open(intermi + 'comment_raw.txt', 'w') as comment_raw_file, \
            open(intermi + 'comment_sents_tracker.txt', 'w') as sent_tracker_file, \
            open(intermi + 'comment_sents_raw.txt', 'w') as sent_raw_file, \
            open(processed + 'comment_tokenized_lemmatized.txt', 'w') as comment_token_file, \
            open(processed + 'sent_tokenized_lemmatized.txt', 'w') as sent_token_file:


        indict = raw_file.readline()[:-2]
        # print(indict)
        # print(type(indict))
        indict = eval(indict)
        # print(type(indict))

        comment = indict['comments']
        #
        parsed_comment = nlp(comment)

        # separate raw comments and treck them
        prof_ids.append(indict['prof_id'])
        reviewer_ids.append(indict['reviewer_id'])
        comments.append(comment)

        # tokenize comments and separate them
        tokenized_comments.append([token.lemma_ for token in parsed_comment])

        # separate sentences and track them
        for num, sent in enumerate(parsed_comment.sents):
            pr_sent_ids.append(zip(indict['prof_id'], indict['reviewer_id'], num))
            sents.append(sent)
            # tokenize sentences and separate them
            tokenized_sents.append([token.lemma_ for token in sent])


        # Write to files on batches
        count += 1

        if count == 1000:
            for i, comment in enumerate(comments):
                comment_raw_file.write(comment)
                comment_tracker_file.write(zip(prof_ids[i], reviewer_ids[i]))
                comment_token_file.write(tokenized_comments[i])

            for i, sent in enumerate(sents):
                sent_raw_file.write(sent)
                sent_tracker_file.write(pr_sent_ids)
                sent_token_file.wr

            count = 0






def main():
    raw = '../RateMyProfessor/data/raw/reviews.json'
    intermi = '../RateMyProfessor/data/intermediate/comments/'
    processed = '../RateMyProfessor/data/processed/'

    count = 0

    prof_ids = ''
    reviewer_ids = ''
    comments = ''

    pr_sent_ids = ''
    sents = ''

    tokenized_comments = ''
    tokenized_sents = ''

    with open(raw, 'r') as raw_file, \
            open(intermi + 'comment_tracker.txt', 'w') as comment_tracker_file, \
            open(intermi + 'comment_raw.txt', 'w') as comment_raw_file, \
            open(intermi + 'comment_sents_tracker.txt', 'w') as sent_tracker_file, \
            open(intermi + 'comment_sents_raw.txt', 'w') as sent_raw_file, \
            open(processed + 'comment_tokenized_lemmatized.txt', 'w') as comment_token_file, \
            open(processed + 'sent_tokenized_lemmatized.txt', 'w') as sent_token_file:

        for line in raw_file:
            indict = line[:-2]
            # print(type(indict))
            indict = eval(indict)
            # print(type(indict))

            comment = indict['comments']
            prof_id = indict['prof_id']
            reviewer_id = indict['reviewer_id']
            #
            parsed_comment = nlp(comment)

            # separate raw comments and treck them
            prof_ids += str(prof_id) + ',' + str(reviewer_id) + '\n'
            comments += comment + '\n'

            # tokenize comments and separate them
            tokenized_comments += str(([token.lemma_ for token in parsed_comment])) + '\n'

            # # separate sentences and track them
            # for num, sent in enumerate(parsed_comment.sents):
            #     pr_sent_ids.append(zip(indict['prof_id'], indict['reviewer_id'], num))
            #     sents.append(sent)
            #     # tokenize sentences and separate them
            #     tokenized_sents.append([token.lemma_ for token in sent])


            # Write to files on batches
            count += 1
            # print(comment)

            if count%1000 == 0:
                comment_raw_file.write(comments)
                comment_tracker_file.write(prof_ids)
                comment_token_file.write(tokenized_comments)
                print('{} DONE!!!'.format(count))


if __name__ == '__main__':
    # extract_comments_sents()
    # extract_comments()
    main()