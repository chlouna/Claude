import yaml,re
d=yaml.safe_load(open('template_user_v3.yaml'))
def srcs(o,acc):
    if isinstance(o,dict):
        if 'src' in o: acc.append(o['src'])
        for v in o.values(): srcs(v,acc)
    elif isinstance(o,list):
        for v in o: srcs(v,acc)
    return acc
before=srcs(d,[])
NEW={
 'FR':'<li style="color: rgb(0, 0, 0);">Va dans <strong>«&nbsp;Alertes en navigation&nbsp;»</strong>.</li>',
 'IT':'<li style="color: rgb(0, 0, 0);">Vai in <strong>«Avvisi in navigazione»</strong>.</li>',
 'ES':'<li style="color: rgb(0, 0, 0);">Ve a <strong>«Alertas en navegación»</strong>.</li>',
 'EN':'<li style="color: rgb(0, 0, 0);">Go to <strong>“Navigation alerts”</strong>.</li>',
 'NL':'<li style="color: rgb(0, 0, 0);">Ga naar <strong>‘Meldingen tijdens navigatie’</strong>.</li>',
}
def lang(c):
    if '"EN" in' in c: return 'EN'
    for l in ['FR','IT','ES','NL']:
        if f'"{l}" in' in c: return l
done={}
for row in d['body']['content'][0]['content']:
    c=row.get('condition') or ''
    for col in row.get('content',[]):
        for it in col.get('content',[]):
            t=it.get('content')
            if isinstance(t,str) and '<ol>' in t and ('paramètres' in t or 'impostazioni' in t or 'ajustes' in t or 'settings' in t or 'instellingen' in t):
                lis=re.findall(r'<li[^>]*>.*?</li>',t)
                it['content']=t.replace(lis[1],NEW[lang(c)])
                done[lang(c)]=1
assert sorted(done)==['EN','ES','FR','IT','NL'],done
assert srcs(d,[])==before
yaml.safe_dump(d,open('template_final_v3.txt','w'),allow_unicode=True,sort_keys=False,width=10**9)
print(done,len(before))
