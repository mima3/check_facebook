# coding=utf-8
import MeCab
import os
import re
import facebook
import requests
from collections import defaultdict
from math import log
import json

class FacebookAnalyzer:
    def __init__(self, access_token):
        p = ""
        #if dicdir == "":
        #    p = "-u%s" % (usrdicdir)
        #else:
        #    p = " -d%s -u%s" % (dicdir ,usrdicdir)
        self.graph = facebook.GraphAPI(access_token)
        self.mecab = MeCab.Tagger(p)
        self.wordcount = defaultdict(int)


    def AnalyzePage(self, page, count):
        profile = self.graph.get_object(page)
        posts = self.graph.get_connections(profile['id'], 'posts')

        self.wordcount = defaultdict(int)
        i = 0
        while True:
            try:
                # Perform some action on each post in the collection we receive from
                # Facebook.
                for d in posts['data']:
                    if 'message' in d:
                        self.morph(d['message'].encode('utf-8'))
                        i = i + 1
                        if i >= count:
                            break
                if i >= count:
                    break
                # Attempt to make a request to the next page of data, if it exists.
                posts = requests.get(posts['paging']['next']).json()
            except KeyError:
                # When there are no more pages (['paging']['next']), break from the
                # loop and end the script.
                break
        ret = []
        i = 0
        for k, v in sorted(self.wordcount.items(), key=lambda x:x[1], reverse=True):
            if i >= count:
                break
            word = k
            word = word.replace("\"","")
            word = word.replace("\'","")
            word = word.replace("\\","\\\\")
            ret.append( {"text":word ,"weight":v} )
            i += 1
        return ret


    def morph(self,text):
        pos = ['名詞'] #'形容詞', '形容動詞','感動詞','副詞','連体詞','名詞','動詞']
        #pos = ['名詞']
        exclude=['RT','TL','sm','#','さん','する','いる','やる','これ','それ','あれ','://','こと','の','そこ','ん','なる','http','co','jp','com']
        node = self.mecab.parseToNode(text)
        while node:
            fs = node.feature.split(",")
            if fs[0] in pos:
                word = (fs[6] != '*' and fs[6] or node.surface)
                word = word.strip()
                if word.isdigit() == False:
                    if len(word)!=1:
                        if word not in exclude:
                            self.wordcount[word] += 1
            node = node.next
