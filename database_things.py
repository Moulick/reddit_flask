from datetime import datetime

import pymongo

client = pymongo.MongoClient()
database = client.reddit


def updatedb(redditor, word, word_count, comment_count, sorty):
    collection = database['word_analysis']
    # if sorty not in record['sorted_by'], add that to database
    # else if sorty in record['sorted_by'], updated that record
    record = record_finder(redditor)
    if sorty in record['sorted_by']:
        try:
            # modify record with new info and increase updated times by 1
            collection.update_one(
                {"redditor": redditor},
                {
                    "$set":
                        {
                            'common_word_' + sorty: word,
                            'common_word_count_' + sorty: word_count,
                            'last_updated_' + sorty: datetime.utcnow(),
                            'total_comments_' + sorty: comment_count,
                        },
                    "$inc":
                        {
                            'updated_times_' + sorty: 1
                        }
                }
            )

            return True
        except Exception as ex:
            print(ex)
            print('error in updatedb when sorty is spposed to be in \'sorted_by\'')
    elif sorty not in record['sorted_by']:
        try:
            collection.update_one(
                {"redditor": redditor},
                {
                    "$set":
                        {
                            'common_word_' + sorty: word,
                            'common_word_count_' + sorty: word_count,
                            'last_updated_' + sorty: datetime.utcnow(),
                            'total_comments_' + sorty: comment_count
                        },
                    "$inc":
                        {
                            'updated_times_' + sorty: 1
                        },
                    "$addToSet":
                        {
                            'sorted_by': sorty
                        }
                }
            )
        except Exception as ex:
            print(ex)
            print('error in updatedb when sorty not in sorty')


def addtodb(redditor, word, word_count, comment_count, sorty):
    collection = database['word_analysis']
    if sorty in ['controversial', 'hot', 'new', 'top']:
        try:
            post = {
                'redditor': redditor,
                'common_word_' + sorty: word,
                'common_word_count_' + sorty: word_count,
                'total_comments_' + sorty: comment_count,
                'sorted_by': [sorty],
                'last_updated_' + sorty: datetime.utcnow(),
                'add_on': datetime.utcnow(),
                'updated_times_' + sorty: 1
            }

            collection.insert_one(post)
            return True
        except pymongo.errors.DuplicateKeyError:
            print('Dupilcate Key error in AddToDb')
            return False
    else:
        print(sorty)
        raise Exception('Unknown sorting in addtodb')


def record_finder(redditor):
    collection = database['word_analysis']
    return collection.find_one({'redditor': redditor})


def data_fetcher(record, sorty):
    if sorty == 'top' or 'new' or 'controversial' or 'hot':

        word = record['common_word_' + sorty]
        word_count = record['common_word_count_' + sorty]
        comment_count = record['total_comments_' + sorty]

        return word, word_count, comment_count
    else:
        return False
