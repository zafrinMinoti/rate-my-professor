from spacy import load
nlp = load('en')

def main():
    raw = '../RateMyProfessor/data/raw/reviews.json'
    intermi = '../RateMyProfessor/data/intermediate/comments/'
    processed = '../RateMyProfessor/data/processed/'

    count = 0

    comment_tracker = ''
    comments = ''

    sent_tracker = ''
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
            prof_id = str(indict['prof_id'])
            reviewer_id = str(indict['reviewer_id'])
            #
            parsed_comment = nlp(comment)

            # separate raw comments and treck them
            comment_tracker += prof_id + ',' + reviewer_id + '\n'
            comments += comment + '\n'

            # tokenize comments and separate them
            tokenized_comments += str(([token.lemma_ for token in parsed_comment])) + '\n'

            # separate sentences and track them
            for num, sent in enumerate(parsed_comment.sents):
                sent_tracker += prof_id + ',' + reviewer_id + ','+ str(num) + '\n'
                sents += sent.text + '\n'
                # tokenize sentences and separate them
                tokenized_sents += str([token.lemma_ for token in sent]) + '\n'


            # Write to files on batches
            count += 1
            # print(comment)

            if count%1000 == 0:
                comment_raw_file.write(comments)
                comment_tracker_file.write(comment_tracker)
                comment_token_file.write(tokenized_comments)

                sent_raw_file.write(sents)
                sent_tracker_file.write(sent_tracker)
                sent_token_file.write(tokenized_sents)

                print('{} DONE!!!'.format(count))


if __name__ == '__main__':
    main()