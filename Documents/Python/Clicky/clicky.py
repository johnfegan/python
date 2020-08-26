import requests, csv, os, sys, hashlib, time, datetime, json, configparser
from requests.auth import HTTPDigestAuth
import pandas as pd
import numpy as np
from datetime import date, timedelta
from time import sleep

def getnewurls(sc, urls):
    for cbid, values in urls.items():
        url = values['URL']
        if url not in sc['URLs']:
            sc['URLs'][url] = {'cbid': cbid, 'Data': {}}
    return sc

def getweeks(num):
    delta = num * 7
    dates = [] 
    start = datetime.datetime.now() - timedelta(delta)
    end = datetime.datetime.now()
    while start < end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += timedelta(1)
    return dates


def getmonthstoday(start, delta, dateformat="%Y-%m-%d"):
    start = datetime.datetime.strptime(start, dateformat)   
    end = datetime.datetime.now()
    dates = []
    dtf = start
    if delta == 28:
        while dtf < end:
            if dtf.date().day < 27:
                sub = dtf.replace(day=1)
                sub = sub.strftime(dateformat)
                dates.append(sub)
            dtf += timedelta(28)
            
    else:
        while dtf < end:
            sub = dtf.strftime(dateformat)
            dates.append(sub)
            dtf += timedelta(delta)
    return dates

def getmonths(start, delta, dateformat="%Y-%m-%d"):
    start = datetime.datetime.strptime(start, dateformat)   
    end = datetime.datetime.now() - timedelta(1)
    dates = []
    dtf = start
    if delta == 28:
        while dtf < end:
            if dtf.date().day < 27:
                sub = dtf.replace(day=1)
                sub = sub.strftime(dateformat)
                dates.append(sub)
            dtf += timedelta(28)
            
    else:
        while dtf < end:
            sub = dtf.strftime(dateformat)
            dates.append(sub)
            dtf += timedelta(delta)
    return dates

def dateify(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d")  

def stringify(string):
    return string.strftime("%Y-%m-%d")
    
def getsha(keypair, param):
    key = keypair[0]
    hl = hashlib.sha256()
    t = str(int(time.time()/10))
    access = key + param + t
    hl.update(access.encode('utf-8'))
    return hl.hexdigest()

def getcbid(key, url):
    param = 'action=page_info&url_or_id=' + url 
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    try:
        return r.json()['response']
    except:
        value = r.content.decode('utf-8').split('<br />')
        value = value[-1]
        return json.loads(value)['response']
    
def getsites(key):
    param = 'action=site_list'
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    return r.json()['response']
    
def getkeywords(key, cbid, start, end):
    param = 'action=page_keywords&limit=1000&id=' + cbid + '&start_date=' + start + '&end_date=' + end
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    return r.json()['response']

def getpagetraffic(key, cbid, start, end):
    param = 'action=page_metrics&id=' + cbid + '&start_date=' + start + '&end_date=' + end
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    return r.json()['response']

def getallpagetraffic(key, cbid, start, end):
    param = 'action=page_metrics&id=' + cbid + '&start_date=' + start + '&end_date=' + end + '&include_non_search=1' 
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    return r.json()['response']

def gettraffic(key, siteid, start, end):
    param = 'action=site_metrics&id=' + siteid + '&start_date=' + start + '&end_date=' + end
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    return r.json()['response']

def getpaths(key, cbid, prevornext, start, end):
    param = 'action=page_visit_paths' + '&prev_or_next=' + prevornext + '&id=' + cbid + '&start_date=' + start + '&end_date=' + end
    sha = getsha(key, param)
    r = requests.get('https://cb.legendcorp.com/api/?' + param, auth=requests.auth.HTTPBasicAuth(key[1], sha))
    return r.json()['response']
