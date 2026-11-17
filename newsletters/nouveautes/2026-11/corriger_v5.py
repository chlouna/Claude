import yaml,re
d=yaml.safe_load(open('template_user_v5.yaml'))
def srcs(o,acc):
    if isinstance(o,dict):
        if 'src' in o: acc.append(o['src'])
        for v in o.values(): srcs(v,acc)
    elif isinstance(o,list):
        for v in o: srcs(v,acc)
    return acc
before=srcs(d,[])
LI='<li style="color: rgb(0, 0, 0);">'
FIX={
 'Voici tout ce qui change&nbsp; :':'Voici tout ce qui change&nbsp;:',
 'Ecco tutto quello che cambia :':'Ecco tutto quello che cambia:',
 'Esto es todo lo que cambia :':'Esto es todo lo que cambia:',
 'Here’s everything that’s changing :':'Here’s everything that’s changing:',
 'Dit is alles wat er verandert :':'Dit is alles wat er verandert:',
}
n=0;alert=0
for row in d['body']['content'][0]['content']:
    for col in row.get('content',[]):
        for it in col.get('content',[]):
            t=it.get('content')
            if not isinstance(t,str): continue
            for a,b in FIX.items():
                if a in t: t=t.replace(a,b); n+=1
            if 'Alertes en navigation' in t:
                a=t.index('<ol>')+4; b=t.index('</ol>')
                t=t[:a]+LI+'Va dans les <strong>paramètres</strong> de l’appli.</li>'+LI+'Va dans <strong>«&nbsp;Alertes en navigation&nbsp;»</strong>.</li>'+LI+'<strong>Coche les alertes que tu veux garder.</strong></li>'+t[b:]
                alert+=1
            it['content']=t
assert n==5 and alert==1,(n,alert)
assert srcs(d,[])==before
yaml.safe_dump(d,open('template_final_v5.txt','w'),allow_unicode=True,sort_keys=False,width=10**9)
print('ok',len(before))
