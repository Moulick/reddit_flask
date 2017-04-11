import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def preprocess(s, lowercase=False):
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def word_finder(comments):
    # takes a reddit.reddditor(username).comments.top and returns a dict and number of comments
    comment_count = 0
    word_dict = {}
    for comment in comments:
        comment_count += 1
        # print(comment_count)
        print(comment)
        comment_tokens = preprocess(comment.body)

        for wordy in comment_tokens:
            wordy = wordy.casefold()
            if wordy not in string.punctuation:
                if wordy not in stopwords.words('english'):
                    if wordy in word_dict:
                        word_dict[wordy] += 1
                    else:
                        word_dict[wordy] = 1

    return word_dict, comment_count
