# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect, abort
from json import dumps
import os
import json
import base64
import Cookie
import email.utils
import hashlib
import hmac
from collections import defaultdict
import time
import cgi
import urllib


facebook_app_id = None
facebook_app_secret = None
facebook_redirect_url = None

app = Bottle()


def setup(conf):
    global app
    global facebook_app_id
    global facebook_app_secret
    global facebook_redirect_url

    facebook_app_id = conf.get('FaceBook', 'app_id')
    facebook_app_secret = conf.get('FaceBook', 'app_secret')
    facebook_redirect_url = conf.get('FaceBook', 'redirect_url')

@app.get('/')
def homePage():
    user_id = parse_cookie(request.cookies.get("fb_user"))
    return template('home', current_user=user_id).replace('\n', '');


###########################################
# facebook関連
###########################################
def cookie_signature(*parts):
    """Generates a cookie signature.
    We use the Facebook app secret since it is different for every app (so
    people using this example don't accidentally all use the same secret).
    """
    hash = hmac.new(facebook_app_secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(part)
    return hash.hexdigest()


def parse_cookie(value):
    """Parses and verifies a cookie value from set_cookie"""
    if not value:
        return None
    parts = value.split("|")
    if len(parts) != 3:
        return None
    if cookie_signature(parts[0], parts[1]) != parts[2]:
        logging.warning("Invalid cookie signature %r", value)
        return None
    timestamp = int(parts[1])
    if timestamp < time.time() - 30 * 86400:
        logging.warning("Expired cookie %r", value)
        return None
    try:
        return base64.b64decode(parts[0]).strip()
    except:
        return None

def set_cookie(response, name, value, domain=None, path="/", expires=None):
    """Generates and signs a cookie for the give name/value"""
    timestamp = str(int(time.time()))
    value = base64.b64encode(value)
    signature = cookie_signature(value, timestamp)
    cookie = Cookie.BaseCookie()
    cookie[name] = "|".join([value, timestamp, signature])
    cookie[name]["path"] = path
    if domain:
        cookie[name]["domain"] = domain
    if expires:
        cookie[name]["expires"] = email.utils.formatdate(
            expires, localtime=False, usegmt=True)
    response.add_header("Set-Cookie", cookie.output()[12:])


@app.get('/login')
def login():
    verification_code = None
    verification_code = request.query.code
    redirect_uri = facebook_redirect_url
    args = dict(client_id=facebook_app_id,
                redirect_uri='http://localhost/check_facebook/login')
    if verification_code:
        args["client_secret"] = facebook_app_secret
        args["code"] = verification_code
        res = cgi.parse_qs(urllib.urlopen(
            "https://graph.facebook.com/oauth/access_token?" +
            urllib.urlencode(args)).read())
        access_token = res["access_token"][-1]

        # Download the user profile and cache a local instance of the
        # basic profile info
        profile = json.load(urllib.urlopen(
            "https://graph.facebook.com/me?" +
            urllib.urlencode(dict(access_token=access_token))))
        #user = User(key_name=str(profile["id"]), id=str(profile["id"]),
        #            name=profile["name"], access_token=access_token,
        #            profile_url=profile["link"])
        #user.put()
        set_cookie(response, "fb_user", str(profile["id"]),
                   expires=time.time() + 30 * 86400)
        redirect("/check_facebook")
    else:
        redirect(
            "https://graph.facebook.com/oauth/authorize?" +
            urllib.urlencode(args))


@app.get('/logout')
def logout():
    set_cookie(response, "fb_user", "", expires=time.time() - 86400)
    session = request.environ.get('beaker.session')
    session.delete()
    redirect("/check_facebook")

