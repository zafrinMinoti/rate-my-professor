from spacy import load
nlp = load('en')

def extract_comments():
    '''
    IN: file: raw scraped reviews
    OUT 1: file: review comments - one sentence per line
    OUT 2: file: review comments tracker - prof_if, revirwer_id, sent_id - for each sentence per line
    '''

    raw = '../RateMyProfessor/data/raw/reviews.json'
    intermi = '../RateMyProfessor/data/intermediate/comments/'

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

if __name__ == '__main__':
    extract_comments()