#!/usr/bin/python

import httplib
import json
import os
from sets import Set
import subprocess
import urllib


def get_link(title, artist):
    q = {'q': ' '.join([title, artist, 'official'])}
    q = urllib.urlencode(q)
    searchUrl = '/feeds/api/videos?alt=json&max-results=1&{0}'.format(q)
    
    conn = httplib.HTTPSConnection('gdata.youtube.com')
    conn.request("GET", searchUrl)
    resp = conn.getresponse()
    data = resp.read()
    
    obj = json.loads(data)
    entry_id = obj['feed']['entry'][0]['id']['$t']
    
    key = entry_id.split('/')[-1]
    
    return 'http://www.youtube.com/watch?v={0}'.format(key)

def download(link):
    subprocess.call(['youtube-dl', '-f', '22', link])

def generate_json():
    try:
        os.remove('billboard.json')
    except OSError:
        pass
    
    subprocess.call(['scrapy', 'crawl', '-o', 'billboard.json', '-t', 'json', 'billboard'])
    
def process_json():
    # read exlude json
    exclude_set = Set()
    
    try:
        with open('exclude.json', 'r') as f:
            exclude_content = f.read()
        
        exclude_items = json.loads(exclude_content)
        for item in exclude_items:
            exclude_set.add(item['title'] + item['artist'])
    except IOError:
        pass
    
    # read json
    with open('billboard.json', 'r') as f:
        content = f.read()
        
    items = json.loads(content)
    items = sorted(items, key=lambda x: x['position'])
    
    # generate links
    links = []
    for item in items:
        combined = item['title'] + item['artist']
        if (combined in exclude_set):
            continue
        
        links.append(get_link(item['title'], item['artist']))

    # download
    for link in links:
        download(link)

generate_json()
process_json()
