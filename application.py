# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect, abort
from json import dumps
import os
import json
from collections import defaultdict
import time
import cgi
import urllib
from facebook_analyze import FacebookAnalyzer
import facebook


facebook_app_id = None
facebook_app_secret = None

app = Bottle()


def setup(conf):
    global app
    global facebook_app_id
    global facebook_app_secret

    facebook_app_id = conf.get('FaceBook', 'app_id')
    facebook_app_secret = conf.get('FaceBook', 'app_secret')

@app.get('/')
def homePage():
    session = request.environ.get('beaker.session')
    session['redirect_url'] = '/check_facebook'
    access_token = None
    if 'access_token' in session:
        access_token = session['access_token']
    session.save()
    return template('home', access_token=access_token).replace('\n', '');


@app.get('/analyze_page')
def analyzePage():
    session = request.environ.get('beaker.session')
    session['redirect_url'] = '/check_facebook/analyze_page'
    access_token = None
    session.save()
    if not 'access_token' in session:
        # ログインしていない場合は、ログインページにリダイレクト
        redirect('/check_facebook/login')
        return
    access_token = session['access_token']
    return template('analyze_page', access_token=access_token).replace('\n', '');


@app.get('/json/analyze_page/<page>')
def analyzePageJson(page):
    res = {'data' : None, 'result':0, 'error': ''}
    response.content_type = 'application/json;charset=utf-8'
    session = request.environ.get('beaker.session')
    if not 'access_token' in session:
        # ログインしていない場合は、エラー
        res['result'] = 1
        res['error'] = 'ログインされていません。'
        return json.dumps(res)
    access_token = session['access_token']
    try:
        analyzer = FacebookAnalyzer(access_token)
        data = analyzer.AnalyzePage(page, 200)
        res['data'] = data
        return json.dumps(res)
    except facebook.GraphAPIError, ex:
        res['result'] = 3
        for item in ex:
            for e in item:
                res['error'] = ex.message
        return json.dumps(res)

###########################################
# facebook関連
###########################################
@app.get('/login')
def login():
    verification_code = None
    verification_code = request.query.code
    callback_url = callback_url = "https://" + os.environ['HTTP_HOST']  + os.path.dirname(os.environ['REQUEST_URI']) + '/login'
    args = dict(client_id=facebook_app_id,
                redirect_uri=callback_url,
                scope='read_stream')
    if verification_code:
        args["client_secret"] = facebook_app_secret
        args["code"] = verification_code
        res = cgi.parse_qs(urllib.urlopen(
            "https://graph.facebook.com/oauth/access_token?" +
            urllib.urlencode(args)).read())

        session = request.environ.get('beaker.session')
        access_token = res["access_token"][-1]
        session['access_token'] = access_token
        session.save()
        if 'redirect_url' in session:
            redirect(session['redirect_url'])
        else:
            redirect("/check_facebook")
    else:
        redirect(
            "https://graph.facebook.com/oauth/authorize?" +
            urllib.urlencode(args))


@app.get('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect("/check_facebook")

