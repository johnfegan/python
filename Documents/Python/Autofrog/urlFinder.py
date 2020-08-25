## For me to work you'll need python3 with pandas installed
## install using cmd pip install pandas and pathlib
import csv, os, json, pathlib
import pandas as pd

def main():
    ## Working out our current and parent directory & getting text files
    home = os.path.dirname(os.path.abspath(__file__))
    sites = gettext(home+'\\sites.txt')

    ## Looping through sites and adding any new URLs to a dictionary
    new = {}
    for site in sites:
        dom = site.split('/')[2]
        new = sortcrawl(home+'\\'+dom, new)

    ## Create file if any new URLs are found
    if len(new) > 0:
        pandaindexport(home+'\\New-URLs.csv', new, 'URLs')

def sortcrawl(site, new):
    ## opening known dictionary or creating it as applicable
    try:
        known = fromjson(site+'\\known.json')
    except:
        known = {}
    ## getting csv from screaming frog, adding new values to known
    crawl = csvwithindex(site+'\\internal_all.csv')
    for k,v in crawl.items():
        if k not in known and 'html' in v['Content'] and v['Status Code'] == '200':
            print('Found ' + k)
            known[k] = v
            new[k] = v
    tojson(site+'\\known.json', known)
    return new

def gettext(file):
    with open(file, 'r') as file:
        data = file.read().splitlines()
    return data

def csvwithindex(sheet):
    df = pd.read_csv(sheet, dtype='unicode', index_col=0).fillna('')
    return df.transpose().fillna('').to_dict()

def pandaindexport(filename, dic, index):
    df = pd.DataFrame(dic)
    df = pd.DataFrame.transpose(df)
    df.index.name = index
    df.to_csv(filename, mode='w' ,encoding='utf-8-sig')

def tojson(filename, db):
    with open(filename, 'w') as jsonfile:   
        json.dump(db, jsonfile)

def fromjson(filename, encoding='utf-8-sig'):
    with open(filename, encoding=encoding) as jsonfile:  
        jsondata = json.load(jsonfile)
    return jsondata

if __name__ == "__main__":
    main()
