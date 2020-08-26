import requests, csv, os, sys, hashlib, time, datetime, json, lxml.html, configparser
from requests.auth import HTTPDigestAuth
import pandas as pd
from datetime import date, timedelta 

def main():
    crawl = csvwithindex('structured_data_all.csv')
    types, organised = sortcrawl(crawl)
    organised = detype(organised)
    pandaexport('SortedSchema.csv', organised)

def detype(organised):
    keep = {}
    for url, val in organised.items():
        keep[url] = {}
        for k, v in val.items():
            if 'Type-' not in k:
                keep[url][k] = v
    return keep

def sortcrawl(crawl):
    keep = {}
    types = {}
    for k, v in crawl.items():
        del v['Indexability Status']
        if v['Indexability'] != 'Non-Indexable':
            keep[k] = {}
            for name, value in v.items():
                if 'Type-' in name and value != '':
                    keep[k][value] = True
                    if value not in types:
                        types[value] = {'Count': 1}
                    else:
                        types[value]['Count'] += 1
                else:
                    keep[k][name] = value
    return types, keep

def csvwithindex(sheet):
    df = pd.read_csv(sheet, dtype='unicode', index_col=0).fillna('')
    return df.transpose().fillna('').to_dict()

def pandaexport(filename, dic):
    order = ['Indexability', 'Errors', 'Warnings', 'Total Types', 'Unique Types']
    
    df = pd.DataFrame(dic)
    df = pd.DataFrame.transpose(df).fillna(False)
    rest = list(df.columns.values)
    for k in rest:
        if k not in order:
            order.append(k)
    df = df[order]
    df.index.name = 'URL'
    df.to_csv(filename, mode='w' ,encoding='utf-8-sig')

if __name__ == "__main__":
    main()
