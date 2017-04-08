from flask import Flask

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
