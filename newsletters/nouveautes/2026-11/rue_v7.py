import yaml,copy,uuid
d=yaml.safe_load(open('template_user_v7.yaml'))
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
# section images de l'utilisateur (sans condition, 5 images)
idx=[i for i,r in enumerate(R) if not r.get('condition') and sum(1 for it in r['content'][0]['content'] if it.get('type')=='image')==5][0]
imgs=[it['content']['src'] for it in R[idx]['content'][0]['content']]
del R[idx]
# ordre des captures envoyées : 1 ES, 2 FR?, 3 IT, 4 EN, 5 NL?
IMG={'ES':imgs[0],'FR':imgs[1],'IT':imgs[2],'EN':imgs[3],'NL':imgs[4]}
S='<span style="color: rgb(0, 0, 0);">'
def P(*ps): return '<p><br></p>'.join(f'<p>{S}{x}</span></p>' for x in ps)
T={
'FR':('Sache toujours dans quelle rue tu roules',P('En bas de ton écran, le GPS affiche maintenant <strong>le nom de la voie que tu empruntes</strong>. Rue, quai, boulevard ou nationale&nbsp;: tu sais en un coup d’œil où tu te trouves.','<strong>Pratique</strong> pour vérifier que tu es sur la bonne route, ou pour donner ta position à ton exploitation ou à ton client.','Rien à régler&nbsp;: le nom s’affiche automatiquement pendant ta navigation.'),'Je démarre un trajet'),
'IT':('Sai sempre in che strada ti trovi',P('In basso sullo schermo, il GPS ora mostra <strong>il nome della strada che stai percorrendo</strong>. Via, lungofiume, viale o statale: capisci al volo dove ti trovi.','<strong>Comodo</strong> per controllare di essere sulla strada giusta, o per indicare la tua posizione al tuo ufficio traffico o al tuo cliente.','Non devi impostare nulla: il nome compare automaticamente durante la navigazione.'),'Avvio un percorso'),
'ES':('Sabe siempre por qué calle circulas',P('En la parte inferior de la pantalla, el GPS muestra ahora <strong>el nombre de la vía por la que circulas</strong>. Calle, avenida, bulevar o nacional: sabes de un vistazo dónde estás.','<strong>Práctico</strong> para comprobar que vas por la ruta correcta o para dar tu posición a tu tráfico o a tu cliente.','No tienes que configurar nada: el nombre aparece automáticamente durante la navegación.'),'Inicio una ruta'),
'EN':('Always know which street you’re on',P('At the bottom of your screen, the GPS now shows <strong>the name of the road you’re driving on</strong>. Street, quay, boulevard or main road: you know where you are at a glance.','<strong>Handy</strong> for checking you’re on the right route, or for giving your position to your planner or customer.','Nothing to set up: the name appears automatically while you navigate.'),'Start a route'),
'NL':('Weet altijd in welke straat je rijdt',P('Onderaan je scherm toont de GPS nu <strong>de naam van de weg waarop je rijdt</strong>. Straat, kade, boulevard of rijksweg: je ziet in één oogopslag waar je bent.','<strong>Handig</strong> om te checken of je op de goede route zit, of om je locatie door te geven aan je planner of klant.','Je hoeft niets in te stellen: de naam verschijnt automatisch tijdens het navigeren.'),'Ik start een route'),
}
# lignes alertes (5) : on clone chacune
al=[i for i,r in enumerate(R) if r.get('condition') and any('instellingen' in str(it.get('content')) or 'paramètres' in str(it.get('content')) or 'impostazioni' in str(it.get('content')) or 'ajustes' in str(it.get('content')) or 'app <strong>settings' in str(it.get('content')) for it in r['content'][0]['content'])]
assert len(al)==5,al
new=[]
for i in al:
    r=copy.deepcopy(R[i]); newids(r); L=lang(r['condition'])
    r['title']=f'Nom de rue {L}'
    items=r['content'][0]['content']
    title,para,img,btn=items
    title['content']=f'<h3 class="default-heading3"><span style="font-style:normal;text-decoration:none;font-weight:700;color:rgb(6, 24, 102);">{T[L][0]}</span></h3>'
    para['content']=T[L][1]
    img['content']['src']=IMG[L]
    img['layout']['default']['width']='45%'; img['layout']['default']['canvas-height']='504px'
    img['layout']['320px']['width']='70%'
    h=f'<p><span style="color: rgb(0, 0, 0);"><strong>{T[L][2]}</strong></span></p>'
    btn['text']=h; btn['content']['text']=h
    new.append(r)
R[al[0]:al[0]]=new  # avant les alertes, qui restent la dernière section
# intro : 3 -> 4 nouveautés + liste
INTRO=[('<strong>3 nouveautés dans le GPS</strong>','<strong>4 nouveautés dans le GPS</strong>'),
 ('et des alertes que tu choisis toi-même&nbsp;:','des alertes que tu choisis toi-même et le nom de ta rue toujours affiché&nbsp;:'),
 ('<strong>3 novità nel GPS</strong>','<strong>4 novità nel GPS</strong>'),
 ('e avvisi che scegli tu:',', avvisi che scegli tu e il nome della strada sempre visibile:'),
 ('<strong>3 novedades en el GPS</strong>','<strong>4 novedades en el GPS</strong>'),
 ('y avisos que eliges tú:',', avisos que eliges tú y el nombre de la calle siempre a la vista:'),
 ('<strong>3 new GPS features</strong>','<strong>4 new GPS features</strong>'),
 ('and alerts you choose yourself:','alerts you choose yourself and the street name always on screen:'),
 ('<strong>3 nieuwe functies in de GPS</strong>','<strong>4 nieuwe functies in de GPS</strong>'),
 ('en meldingen die je zelf kiest:',', meldingen die je zelf kiest en de straatnaam altijd in beeld:')]
n=0
for r in R:
    for col in r.get('content',[]):
        for it in col.get('content',[]):
            t=it.get('content')
            if isinstance(t,str):
                for a,b in INTRO:
                    if a in t: t=t.replace(a,b); n+=1
                it['content']=t
assert n==10,n
# virgules propres
s=yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=10**9)
s=s.replace('arrivarci , avvisi','arrivarci, avvisi').replace('llegar , avisos','llegar, avisos').replace('bent , meldingen','bent, meldingen')
d=yaml.safe_load(s)
subj=d['subject']
for a,b in [('a 3 nouveautés','a 4 nouveautés'),('ha 3 novità','ha 4 novità'),('tiene 3 novedades','tiene 4 novedades'),('heeft 3 nieuwe','heeft 4 nieuwe'),('has 3 new','has 4 new')]:
    assert a in subj; subj=subj.replace(a,b)
d['subject']=subj.strip()
after=sorted(srcs(d,[]))
assert after==before,(set(before)^set(after))
yaml.safe_dump(d,open('template_final_v7.txt','w'),allow_unicode=True,sort_keys=False,width=10**9)
print('ok',len(after)); print(d['subject'])
