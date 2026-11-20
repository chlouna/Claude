import yaml
d=yaml.safe_load(open('template_user_v4.yaml'))
def srcs(o,acc):
    if isinstance(o,dict):
        if 'src' in o: acc.append(o['src'])
        for v in o.values(): srcs(v,acc)
    elif isinstance(o,list):
        for v in o: srcs(v,acc)
    return acc
before=srcs(d,[])
S='<span style="color: rgb(0, 0, 0);">'
def P(*ps): return '<p><br></p>'.join(f'<p>{S}{x}</span></p>' for x in ps)
INTRO={
'FR':P('Ce mois-ci, la mise à jour <strong>6.5.0</strong> de Michelin Truckfly arrive avec <strong>3 nouveautés dans le GPS</strong> pour rouler plus serein.',
 'Un itinéraire recalculé plus vite après une sortie ratée, ta destination visible avant d’y arriver, et des alertes que tu choisis toi-même&nbsp;: des petits changements qui te font gagner du temps au quotidien.',
 'Pour en profiter, pense juste à <strong>mettre ton appli à jour</strong>. Voici tout ce qui change.'),
'IT':P('Questo mese l’aggiornamento <strong>6.5.0</strong> di Michelin Truckfly porta <strong>3 novità nel GPS</strong> per guidare più tranquillo.',
 'Un percorso ricalcolato più in fretta dopo un’uscita mancata, la tua destinazione visibile prima di arrivarci e avvisi che scegli tu: piccoli cambiamenti che ti fanno risparmiare tempo ogni giorno.',
 'Per approfittarne, ricordati solo di <strong>aggiornare la tua app</strong>. Ecco tutto quello che cambia.'),
'ES':P('Este mes, la actualización <strong>6.5.0</strong> de Michelin Truckfly llega con <strong>3 novedades en el GPS</strong> para que circules más tranquilo.',
 'Una ruta recalculada más rápido tras una salida perdida, tu destino visible antes de llegar y avisos que eliges tú: pequeños cambios que te ahorran tiempo cada día.',
 'Para aprovecharlos, solo tienes que <strong>actualizar tu app</strong>. Esto es todo lo que cambia.'),
'EN':P('This month, Michelin Truckfly update <strong>6.5.0</strong> brings <strong>3 new GPS features</strong> to help you drive with peace of mind.',
 'Faster rerouting after a missed exit, a look at your destination before you get there, and alerts you choose yourself: small changes that save you time every day.',
 'To enjoy them, just <strong>update your app</strong>. Here’s everything that’s changing.'),
'NL':P('Deze maand brengt update <strong>6.5.0</strong> van Michelin Truckfly <strong>3 nieuwe functies in de GPS</strong>, zodat je met een gerust hart rijdt.',
 'Sneller een nieuwe route na een gemiste afslag, je bestemming zien voordat je er bent en meldingen die je zelf kiest: kleine veranderingen die je elke dag tijd besparen.',
 'Om ervan te profiteren, hoef je alleen <strong>je app te updaten</strong>. Dit is alles wat er verandert.'),
}
def lang(c):
    if '"EN" in' in c: return 'EN'
    for l in ['FR','IT','ES','NL']:
        if f'"{l}" in' in c: return l
done=[];fixed=0
for row in d['body']['content'][0]['content']:
    c=row.get('condition') or ''
    for col in row.get('content',[]):
        for it in col.get('content',[]):
            t=it.get('content')
            if isinstance(t,str) and '6.5.0' in t:
                it['content']=INTRO[lang(c)]; done.append(lang(c))
            if isinstance(t,str) and 'Alertes en navigation' in t:
                a=t.index('<li style="color: rgb(0, 0, 0);">Va dans'); b=t.index('</li>',a)+5
                it['content']=t[:a]+'<li style="color: rgb(0, 0, 0);">Va dans <strong>«&nbsp;Alertes en navigation&nbsp;»</strong>.</li>'+t[b:]; fixed+=1
assert sorted(done)==['EN','ES','FR','IT','NL'] and fixed==1,(done,fixed)
assert srcs(d,[])==before
yaml.safe_dump(d,open('template_final_v4.txt','w'),allow_unicode=True,sort_keys=False,width=10**9)
print(done,len(before))
