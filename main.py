import os
import uuid
from urllib.parse import urlparse

from flask import Flask, redirect, request, render_template, make_response
from flask_restful import Api, Resource

import redis


app = Flask(__name__)
api = Api(app)
r = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379, db=0)


# FIXME
SITE = "http://13.127.169.69/"

def random_id():
    return uuid.uuid4().hex[:8]

def get_domain(url):
    o = urlparse(url)
    return o.netloc


class TinyUrl(Resource):
    def get(self, tinyurl):

        main_url = r.get(tinyurl)
        if main_url:
            return redirect(main_url)
        else:
            return "This url is not registered with us !! "

    def post(self):
        pass

class MainUrl(Resource):
    def post(self):
        url = request.form['url']
        main_url = url
        if not main_url:
            return redirect("/")
        if request.host==get_domain(main_url) or  get_domain(main_url)=="13.127.169.69": #FIXME
            return make_response(render_template('response.html',
                url="", msg="We don't do for this URL. Try another !!"))

        hash_id = random_id()
        r.set(hash_id, main_url)

        return make_response(render_template('response.html', url=SITE+hash_id, \
                msg="This is for you"))

    def get(self):
        return make_response(render_template('my-form.html'))

api.add_resource(TinyUrl, '/<tinyurl>')
api.add_resource(MainUrl, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, debug=True)
