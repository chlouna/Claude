import yaml
d=yaml.safe_load(open('template_user_v6.yaml'))
def srcs(o,acc):
    if isinstance(o,dict):
        if 'src' in o: acc.append(o['src'])
        for v in o.values(): srcs(v,acc)
    elif isinstance(o,list):
        for v in o: srcs(v,acc)
    return acc
before=srcs(d,[])
CTA={'recalc':{'FR':'Je lance mon GPS','IT':'Avvio il mio GPS','ES':'Abro mi GPS','EN':'Open my GPS','NL':'Ik open mijn GPS'},
     'street':{'FR':'Je vois ma destination','IT':'Vedo la mia destinazione','ES':'Veo mi destino','EN':'See my destination','NL':'Ik bekijk mijn bestemming'}}
def lang(c):
    if '"EN" in' in c: return 'EN'
    for l in ['FR','IT','ES','NL']:
        if f'"{l}" in' in c: return l
done=[]
for row in d['body']['content'][0]['content']:
    c=row.get('condition') or ''
    for col in row.get('content',[]):
        items=col.get('content',[])
        txt=' '.join(i.get('content','') for i in items if isinstance(i.get('content'),str))
        kind='recalc' if '6.5' not in txt and ('ricalcol' in txt or 'recalcul' in txt or 'recalcula' in txt or 'recalculates' in txt or 'opnieuw' in txt) else ('street' if 'Street View' in txt else None)
        if not kind: continue
        for it in items:
            if it.get('type')=='text-button':
                h=f'<p><span style="color: rgb(0, 0, 0);"><strong>{CTA[kind][lang(c)]}</strong></span></p>'
                it['text']=h; it['content']['text']=h; done.append((kind,lang(c)))
assert len(done)==10,done
assert srcs(d,[])==before
yaml.safe_dump(d,open('template_final_v6.txt','w'),allow_unicode=True,sort_keys=False,width=10**9)
print(sorted(done))
