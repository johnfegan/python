import json, configparser
import pandas as pd

def main():
    conf=getconfig('config.ini')
    gkwm = fromjson('gkwm.json')
    cnt = csvwithindex('Unknown-Keywords.csv')
    cnt = cntsort(cnt)
    cnt = findnew(gkwm, cnt, conf['site'])
    pandaindexport('Unknown-Content.csv', cnt, 'index')
    print('Done')

def cntsort(cnt):
    kp = {}
    for k, v in cnt.items():
        kw = v['Keyword']
        geo = v['GEO']
        kp[kw + geo] = {'Keyword':v['Keyword'], 'GEO':v['Keyword']}
    return kp

def findnew(gkwm, cnt, site):
    nc = {}
    for k, v in gkwm.items():
        kw = v['Keyword']
        geo = v['GEO']
        if v['Domain'] != site and kw + geo not in cnt:
            l = str(len(nc) + 1)
            nc[l] = v
    return nc

def getconfig(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config['DEFAULT']

def csvwithindex(sheet):
    df = pd.read_csv(sheet, dtype='unicode', index_col=0).fillna('')
    return df.transpose().fillna('').to_dict()

def pandaindexport(filename, dic, index):
    df = pd.DataFrame(dic)
    df = pd.DataFrame.transpose(df)
    df.index.name = index
    df.to_csv(filename, mode='w' ,encoding='utf-8-sig')

def fromjson(filename, encoding='utf-8-sig'):
    with open(filename, encoding=encoding) as jsonfile:  
        jsondata = json.load(jsonfile)
    return jsondata

if __name__ == "__main__":
    main()
