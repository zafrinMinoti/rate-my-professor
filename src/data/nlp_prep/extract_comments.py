from spacy import load
nlp = load('en')

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
    main()