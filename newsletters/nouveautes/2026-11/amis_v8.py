import yaml,copy,uuid
d=yaml.safe_load(open('template_user_v8.yaml'))
R=d['body']['content'][0]['content']
def srcs(o,acc):
    if isinstance(o,dict):
        if 'src' in o: acc.append(o['src'])
        for v in o.values(): srcs(v,acc)
    elif isinstance(o,list):
        for v in o: srcs(v,acc)
    return acc
before=sorted(srcs(d,[]))
def newids(o):
    if isinstance(o,dict):
        if 'id' in o: o['id']=str(uuid.uuid4())
        for v in o.values(): newids(v)
    elif isinstance(o,list):
        for v in o: newids(v)
def lang(c):
    if '"EN" in' in c: return 'EN'
    for l in ['FR','IT','ES','NL']:
        if f'"{l}" in' in c: return l
S='<span style="color: rgb(0, 0, 0);">'
def P(*ps): return '<p><br></p>'.join(f'<p>{S}{x}</span></p>' for x in ps)
# 1) section images amis (sans condition, 5 images)
idx=[i for i,r in enumerate(R) if not r.get('condition') and sum(1 for it in r['content'][0]['content'] if it.get('type')=='image')==5][0]
imgs=R[idx]['content'][0]['content']
ORDER=['FR','EN','IT','ES','NL']
IMG={L:imgs[k] for k,L in enumerate(ORDER)}
T={
'FR':('Agrandis ton réseau grâce aux amis en commun',P('Tu peux maintenant voir <strong>les amis en commun</strong> que tu as avec tes amis.','<strong>Pratique</strong> pour repérer d’autres chauffeurs que tu connais et agrandir ton réseau sur la route.','Un collègue croisé sur une aire, un ancien de ta boîte&nbsp;? Retrouve-le en quelques secondes.'),'Je retrouve mes amis'),
'IT':('Allarga la tua rete con gli amici in comune',P('Ora puoi vedere <strong>gli amici in comune</strong> che hai con i tuoi amici.','<strong>Comodo</strong> per trovare altri autisti che conosci e allargare la tua rete su strada.','Un collega incontrato in un’area di sosta, un ex della tua azienda? Ritrovalo in pochi secondi.'),'Ritrovo i miei amici'),
'ES':('Amplía tu red con los amigos en común',P('Ahora puedes ver <strong>los amigos en común</strong> que tienes con tus amigos.','<strong>Práctico</strong> para encontrar a otros camioneros que conoces y ampliar tu red en la carretera.','¿Un compañero que conociste en un área de servicio, alguien de tu antigua empresa? Encuéntralo en pocos segundos.'),'Encuentro a mis amigos'),
'EN':('Grow your network with mutual friends',P('You can now see <strong>the mutual friends</strong> you share with your friends.','<strong>Handy</strong> for spotting other drivers you know and growing your network on the road.','A colleague you met at a truck stop, someone from your old company? Find them in seconds.'),'Find my friends'),
'NL':('Breid je netwerk uit met gemeenschappelijke vrienden',P('Je ziet nu <strong>de gemeenschappelijke vrienden</strong> die je met je vrienden deelt.','<strong>Handig</strong> om andere chauffeurs te vinden die je kent en je netwerk onderweg uit te breiden.','Een collega die je op een parkeerplaats tegenkwam, iemand van je oude bedrijf? Vind ze in een paar seconden.'),'Ik vind mijn vrienden'),
}
al=[i for i,r in enumerate(R) if r.get('condition') and any(k in str(r) for k in ['Alertes en navigation','Avvisi in navigazione','Alertas en navegación','Navigation alerts','Meldingen tijdens navigatie']) and 'Comment faire' in str(r) or (r.get('condition') and any(k in str(r) for k in ['Avvisi in navigazione','Alertas en navegación','“Navigation alerts”','Meldingen tijdens navigatie']))]
al=sorted(set(al)); assert len(al)==5,al
new=[]
for i in al:
    r=copy.deepcopy(R[i]); newids(r); L=lang(r['condition']); r['title']=f'Amis en commun {L}'
    title,para,img,btn=r['content'][0]['content']
    title['content']=f'<h3 class="default-heading3"><span style="font-style:normal;text-decoration:none;font-weight:700;color:rgb(6, 24, 102);">{T[L][0]}</span></h3>'
    para['content']=T[L][1]
    u=copy.deepcopy(IMG[L]); u['content']['href']='https://truckflyapp.onelink.me/2ysq/r4vkfd60'; u['layout']['default']['type']='absoluteLink'
    h=f'<p><span style="color: rgb(0, 0, 0);"><strong>{T[L][2]}</strong></span></p>'
    btn['text']=h; btn['content']['text']=h
    r['content'][0]['content']=[title,para,u,btn]
    new.append(r)
R[idx:idx+1]=new   # même place : avant le bandeau GPS
# 2) intro
INTRO={
'FR':P('Ce mois-ci, ton appli Michelin Truckfly arrive avec <strong>5 nouveautés</strong>, dont <strong>4 dans le GPS</strong> pour rouler plus serein.','Les amis en commun pour agrandir ton réseau, un itinéraire recalculé plus vite après une sortie ratée, ta destination visible avant d’y arriver, le nom de ta rue toujours affiché et des alertes que tu choisis toi-même&nbsp;: des petits changements qui te simplifient la route au quotidien.','Pour en profiter, pense juste à <strong>mettre ton appli à jour</strong>.','Voici tout ce qui change&nbsp;:'),
'IT':P('Questo mese la tua app Michelin Truckfly porta <strong>5 novità</strong>, di cui <strong>4 nel GPS</strong>, per guidare più tranquillo.','Gli amici in comune per allargare la tua rete, un percorso ricalcolato più in fretta dopo un’uscita mancata, la tua destinazione visibile prima di arrivarci, il nome della strada sempre visibile e avvisi che scegli tu: piccoli cambiamenti che ti semplificano la strada ogni giorno.','Per approfittarne, ricordati solo di <strong>aggiornare la tua app</strong>.','Ecco tutto quello che cambia:'),
'ES':P('Este mes, tu app Michelin Truckfly llega con <strong>5 novedades</strong>, <strong>4 de ellas en el GPS</strong>, para que circules más tranquilo.','Los amigos en común para ampliar tu red, una ruta recalculada más rápido tras una salida perdida, tu destino visible antes de llegar, el nombre de la calle siempre a la vista y avisos que eliges tú: pequeños cambios que te facilitan la carretera cada día.','Para aprovecharlos, solo tienes que <strong>actualizar tu app</strong>.','Esto es todo lo que cambia:'),
'EN':P('This month, your Michelin Truckfly app brings <strong>5 new features</strong>, <strong>4 of them in the GPS</strong>, to help you drive with peace of mind.','Mutual friends to grow your network, faster rerouting after a missed exit, a look at your destination before you get there, the street name always on screen and alerts you choose yourself: small changes that make life on the road easier every day.','To enjoy them, just <strong>update your app</strong>.','Here’s everything that’s changing:'),
'NL':P('Deze maand krijgt je Michelin Truckfly-app <strong>5 nieuwe functies</strong>, waarvan <strong>4 in de GPS</strong>, zodat je met een gerust hart rijdt.','Gemeenschappelijke vrienden om je netwerk uit te breiden, sneller een nieuwe route na een gemiste afslag, je bestemming zien voordat je er bent, de straatnaam altijd in beeld en meldingen die je zelf kiest: kleine veranderingen die je elke dag onderweg helpen.','Om ervan te profiteren, hoef je alleen <strong>je app te updaten</strong>.','Dit is alles wat er verandert:'),
}
n=0
TIT=[('Sai sempre in che strada ti trovi','Basta cercare il cartello della via'),('Sabe siempre por qué calle circulas','Ya no tienes que buscar el cartel de la calle'),('Always know which street you’re on','No more looking for street signs'),('Weet altijd in welke straat je rijdt','Nooit meer zoeken naar het straatnaambord')]
m=0
for r in R:
    c=r.get('condition') or ''
    for col in r.get('content',[]):
        for it in col.get('content',[]):
            t=it.get('content')
            if isinstance(t,str):
                if '6.5.0' in t: it['content']=INTRO[lang(c)]; n+=1; continue
                for a,b in TIT:
                    if a in t: it['content']=t.replace(a,b); m+=1
assert n==5 and m==4,(n,m)
d['subject']='{% if "FR" in contact.LANG %}Ton appli a 5 nouveautés, tu les as vues ? 👀{% elif "IT" in contact.LANG %}La tua app ha 5 novità, le hai viste? 👀{% elif "ES" in contact.LANG %}Tu app tiene 5 novedades, ¿las has visto? 👀{% elif "NL" in contact.LANG %}Je app heeft 5 nieuwe functies. Al gezien? 👀{% else %}Your app has 5 new features. Seen them? 👀{% endif %}'
after=sorted(srcs(d,[])); assert after==before,(set(before)^set(after))
ids=[]
def col(o):
    if isinstance(o,dict):
        if 'id' in o: ids.append(o['id'])
        for v in o.values(): col(v)
    elif isinstance(o,list):
        for v in o: col(v)
col(d); assert len(ids)==len(set(ids))
yaml.safe_dump(d,open('template_final_v8.txt','w'),allow_unicode=True,sort_keys=False,width=10**9)
print('ok',len(after),[r.get('title') for r in R][14:32])
