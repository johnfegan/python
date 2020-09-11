import json, configparser
import pandas as pd

def main():
    conf=getconfig('config.ini')
    try:
        gkwm = fromjson('gkwm.json')
    except:
        gkwm = csvnoindex(conf['kwmatrix'])
        ctr = csvwithindex('ctr.csv')
        gkwm = getdata(gkwm, ctr)
        tojson('gkwm.json', gkwm)
    dips = getdips(gkwm, conf['site'])
    pandaindexport('Dips.csv', dips, 'index')
    ukws = getmaps(gkwm, conf['site'])
    pandaindexport('Unknown-Keywords.csv', ukws, 'index')
    print('Done')

def getmaps(gkwm, site):
    sims = {}
    kkws = {}
    ourls = {}
    turls = {}
    for k, v in gkwm.items():
        if int(v['Position']) < 21:
            url = v['URL']
            kw = v['Keyword']
            geo = v['GEO']
            if v['Domain'] == site:
                kkws[kw] = {}
                if geo not in ourls:
                    ourls[geo]={}
                if url not in ourls[geo]:
                    ourls[geo][url] = [kw]
                else:
                    ourls[geo][url].append(kw)
            else:
                if geo not in turls:
                    turls[geo]={}
                if url not in turls[geo]:
                    turls[geo][url] = [kw]
                else:
                    turls[geo][url].append(kw)
    for geo, db in turls.items():
        if geo not in sims:
            sims[geo] = {}
        if geo in ourls:
            comp = ourls[geo]
            for turl, kws in db.items():
                for url in comp:
                    if url not in sims[geo]:
                        sims[geo][url] = {}
                    for kw in kws:
                        if kw in comp[url]:
                            
                            if turl not in sims[geo][url]:
                                sims[geo][url][turl] = 1
                            else:
                                sims[geo][url][turl] += 1
    mapd = {}
    for geo, db in sims.items():
        for url, vals in db.items():
            try:
                max_key = max(vals, key=vals.get)
                mapd[max_key] = {'URL': url, 'Shared Portfolio': vals[max_key]}
            except:
                pass

    try:
        ukws = csvwithindex('mapped.csv')
    except:
        ukws = {}
    for k, v in gkwm.items():
        kw = v['Keyword']
        if int(v['Position']) < 21 and kw not in kkws:
            kkws[kw] = {}
            url = v['URL']
            geo = v['GEO']
            if v['Domain'] != 'casino.org' and url in mapd:
                crg = mapd[url]
                l = str(len(ukws) + 1)
                ukws[l] = {'Keyword': kw, 'Mapped URL': crg['URL'], 'Common Keywords': crg['Shared Portfolio']}
                for i, d in v.items():
                    ukws[l][i] = d
    return ukws

def getdips(gkwm, site):
    com = {'Non-commercial': 0.1, 'Free': 1, 'Secondary-commercial': 10, 'Primary-commercial': 1000}
    dips = {}
    for k, v in gkwm.items():
        dip = v['Traffic'] - v['Traffic History']
        if dip < 0 and site == v['Domain']:
            v['Dips'] = dip
            v['Importance'] = (v['Traffic History'] - v['Traffic']) * com[v['Market']]
            ind = str(len(dips) + 1)
            dips[ind] = v
    return dips

def getdata(gkwm, ctr):
    for k, v in gkwm.items():
        v['Search Volume'] = int(v['Search Volume'])
        for t in ['Traffic', 'Traffic History']:
            v[t] = getctr(v[t.replace('Traffic', 'Position')], ctr) * v['Search Volume']
        v['Page'] = str(int(v['Position']) + 10)[:1]
    return gkwm

def getctr(rank, ctr):
    try:
        return float(ctr[int(rank)]['CTR'])
    except:
        return 0

def getconfig(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config['DEFAULT']

def csvnoindex(sheet, encoding="utf-8", sep=','):
    df = pd.read_csv(sheet, dtype='unicode', encoding=encoding, sep=sep).fillna('')
    return df.transpose().fillna('').to_dict()

def csvwithindex(sheet):
    df = pd.read_csv(sheet, dtype='unicode', index_col=0).fillna('')
    return df.transpose().fillna('').to_dict()

def pandaexport(filename, dic):
    df = pd.DataFrame(dic)
    df = pd.DataFrame.transpose(df)
    df.to_csv(filename, mode='w' ,encoding='utf-8-sig')

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
