from flask import render_template, request

import main_backend
from reddit_flask import app


# @app.route('/')
# def landing():
#     return 'ok'


# @app.route('/<redditor>')
# def count(redditor):
#     common_word, number, total_comments = redditstuff.word(redditor)
#
#     return render_template('basic.html',
#                            common_word=common_word,
#                            number=number,
#                            total_comments=total_comments,
#                            redditor=redditor)


@app.route('/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        return render_template('commonwordform.html')

    elif request.method == 'POST':
        redditor = request.form['redditor']
        sorty = request.form['sorting']

        word, word_count, comment_count = main_backend.main_backend(redditor, sorty)
        data = {'word': word.title(),
                'word_count': word_count,
                'comment_count': comment_count,
                'redditor': redditor,
                'sorty': sorty
                }

        return render_template('basic.html', data=data)
