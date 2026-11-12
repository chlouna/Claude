"""B2B novembre 2026 : corrections sur le template collé par l'utilisatrice (v2).
Entrée : template_user_v2.yaml ; sortie : template_final.yaml (+ .txt)."""
import yaml, sys

REPLI = '( "EN" in contact.LANG ) or ( ( contact.LANG != "FR" ) and ( contact.LANG != "ES" ) and ( contact.LANG != "NL" ) and ( contact.LANG != "IT" ) )'
ART_OLD = 'https://www.truckfly.com/blog/fr/navigation-poids-lourds/nouveaut%C3%A9s-fonctionnalit%C3%A9s/ton-profil-%C3%A9volue-et-devient-encore-plus-communautaire/'
ART_NEW = 'https://www.truckfly.com/blog/fr/navigation-poids-lourds/nouveaut%C3%A9s-fonctionnalit%C3%A9s/nouveautes-michelin-truckfly-likes-photo-profil-alerte-peage/'
UOMINI = 'https://www.uominietrasporti.it/professione/leggi-e-politica/nuovo-codice-della-strada-il-testo-arriva-alla-camera-cqc-senza-esame-per-un-anno-autisti-fino-a-70-anni-e-nuove-regole-per-i-trasporti-eccezionali/'

y = yaml.safe_load(open('template_user_v2.yaml'))
secs = y['body']['content'][0]['content']

def items(sec):
    for col in sec['content']:
        for it in col['content']:
            yield it

def by_id(i):
    for s in secs:
        for it in items(s):
            if it['id'] == i:
                return it
    raise KeyError(i)

def rep(it, old, new, key='content'):
    v = it[key]
    if isinstance(v, dict):
        found = False
        for k in ('text', 'href'):
            if k in v and old in v[k]:
                v[k] = v[k].replace(old, new); found = True
        if 'text' in it and old in it['text']:
            it['text'] = it['text'].replace(old, new); found = True
        assert found, (it['id'], old)
    else:
        assert old in v, (it['id'], old)
        it[key] = v.replace(old, new)

# 1. Objet : condition EN en repli (texte inchangé, à remplacer par l'objet de novembre)
y['subject'] = y['subject'].replace('( "EN" in contact.LANG ) or ( !contact.LANG )', REPLI)

# 2. Récap ES : plus de partie Événements, renumérotation
ri = by_id('ed122658-3807-4553-a754-dbe10ae0634c')
c = ri['content']; cut = '<p><strong><br></strong></p>'
c = c[c.index(cut) + len(cut):]
c = c.replace('II.&nbsp;', 'I.&nbsp;').replace('III. ', 'II. ').replace('IV. ', 'III. ')
ri['content'] = c

# 3. Événements : ES supprimé, IT Klimamobility, NL Mega Trucks Festival
secs[:] = [s for s in secs if s.get('title') != 'Bannière ES · Événements']

def event(title_id, text_id, img_id, btn_id, titre, texte, href, bouton):
    for s in secs:
        for col in s['content']:
            col['content'] = [it for it in col['content'] if it['id'] != img_id]
    by_id(title_id)['content'] = '<div><h3 class="default-heading3"><span style="color: rgb(249, 250, 252);"><strong>%s</strong></span></h3></div>' % titre
    by_id(text_id)['content'] = texte
    b = by_id(btn_id)
    html = '<p><strong><span style="color: rgb(0, 0, 0);">%s</span></strong></p>' % bouton
    b['text'] = html; b['content']['text'] = html; b['content']['href'] = href

W = '<span style="color: rgb(255, 255, 255);">%s</span>'
def corps(date, intro, pourquoi, puces):
    return ('<p class="default"><br></p><p class="default">' + W % ('<strong>%s</strong>' % date) + '</p>'
            '<p class="default"><br></p><p class="default">' + W % intro + '</p>'
            '<p class="default"><br></p><p class="default">' + W % ('<strong>%s</strong>' % pourquoi) + '</p>'
            '<p class="default"><br></p><ul>' + ''.join('<li style="color: rgb(255, 255, 255);">%s</li>' % p for p in puces) + '</ul>')

event('d93d939d-47e4-406f-87ea-52f406873feb', '6de5e0f1-d4be-4561-be13-f8f17ff6168d',
      '67ea5e8f-793f-4206-9ff7-8f4fce692c87', '69d60dda-5117-4e0b-bd8b-b90bb6ec91a1',
      'Klimamobility 2027: a Bolzano la mobilità sostenibile',
      corps('Dal 27 al 30 gennaio 2027 · Fiera Bolzano',
            'Klimamobility è la fiera con congresso dedicata alla mobilità sostenibile. Un appuntamento per capire come cambiano veicoli, energie e infrastrutture, e cosa significa per la Sua flotta.',
            'Perché è interessante per Lei?',
            ['Scoprire le soluzioni per ridurre consumi ed emissioni della Sua flotta',
             'Seguire il congresso sulle energie alternative e la ricarica',
             'Incontrare costruttori, fornitori ed esperti della mobilità']),
      'https://www.fierabolzano.it/', 'Scopri il salone')

event('80b9871a-363c-4f13-bd0d-ad126b6c98c7', '2cab7f0c-6707-4938-85df-35620edb827d',
      '56cdc690-159c-4165-af74-c92d7b1539c0', '3e577e68-1bfd-441b-8120-2211a372cbc5',
      'Mega Trucks Festival 2026: het grootste indoor truckevenement van de Benelux',
      corps('12 en 13 december 2026 · Brabanthallen, \'s-Hertogenbosch',
            'Het Mega Trucks Festival brengt elk jaar in december chauffeurs, transportliefhebbers en de sector samen rond meer dan 400 trucks, met dealers en leveranciers aanwezig.',
            'Waarom is het interessant voor u?',
            ['Chauffeurs ontmoeten in een ontspannen sfeer en uw bedrijf zichtbaar maken',
             'De nieuwste trucks en uitrustingen bekijken bij dealers en leveranciers',
             'Contacten leggen met andere spelers uit de transportsector']),
      'https://www.trucksmagazine.nl/', 'Ontdek het festival')

# EN : espace en trop dans le lien de l'image
by_id('dcef6800-2d91-4c22-8df0-5b0be4489856')['content']['href'] = 'https://roadtransportexpo.co.uk/'

# 4. Infos FR : nouvel article
for s in secs:
    if s.get('condition') == '( "FR" in contact.LANG )':
        for it in items(s):
            if isinstance(it.get('content'), dict) and it['content'].get('href') == ART_OLD:
                it['content']['href'] = ART_NEW

# 5. Marché IT : bon lien et « Fonte »
by_id('6b319ce0-82c2-4212-8242-470589880775')['content']['href'] = UOMINI
rep(by_id('e7089815-8676-4fd1-b6b2-20fdb8231298'), 'Fonti:&nbsp;', 'Fonte:&nbsp;')

# 6. Teaser : le mois prochain
for i, o, n in [
    ('0cad7df4-13ca-4e66-ab3d-6b013aca5f28', 'Rendez-vous dans <strong>15 jours</strong> pour', 'Rendez-vous <strong>le mois prochain</strong> pour'),
    ('6a6437a0-5750-41d7-9683-162c5632a6ac', 'See you in <strong>15 days</strong> to', 'See you <strong>next month</strong> to'),
    ('a1623799-dae9-4fa8-863f-63b5bcca9f87', 'Nos vemos dentro de <strong>15 días</strong> para', 'Nos vemos <strong>el próximo mes</strong> para'),
    ('d9a35389-8eee-488f-a02b-440e1dc78620', 'Appuntamento tra <strong>15 giorni</strong> per', 'Appuntamento <strong>il mese prossimo</strong> per'),
    ('bfeab0b9-82e9-449b-a308-9aafc51c75d4', 'Over <strong>15 dagen</strong> ontdekt u', '<strong>Volgende maand</strong> ontdekt u'),
]:
    rep(by_id(i), o, n)

# 7. Footer avis : Lei (IT) et u (NL), plus de <code>
rep(by_id('b9d1731e-2044-4e5a-b66d-7c38ae7ced54'), 'Cosa ne pensate della', 'Cosa ne pensa della')
rep(by_id('c992735f-dd24-4f5d-8b5e-f043586f4e0b'), 'Se questa newsletter vi è piaciuta, non esitate a condividerla con i vostri colleghi. Il vostro supporto ci aiuta molto!', 'Se questa newsletter Le è piaciuta, non esiti a condividerla con i Suoi colleghi. Il Suo supporto ci aiuta molto!')
it = by_id('6dbaf8bc-127c-4d17-8946-87f4cd284070')
rep(it, 'La tua opinione conta!', 'La Sua opinione conta!')
rep(it, 'che vorresti vedere trattati nelle nostre prossime newsletter? Non esitare a segnalarceli!', 'che vorrebbe vedere trattati nelle nostre prossime newsletter? Non esiti a segnalarceli!')
rep(by_id('e0939d07-f97e-4e54-bdb8-ded06ebca3e0'), 'Wat vond je van', 'Wat vond u van')
rep(by_id('76dbd41e-940a-47df-a2b1-d7514c16ec5e'), 'Als je deze nieuwsbrief goed vond, deel hem dan gerust met je collega&#39;s. Jouw steun helpt ons enorm!', 'Als u deze nieuwsbrief goed vond, deel hem dan gerust met uw collega&#39;s. Uw steun helpt ons enorm!')
it = by_id('e71f38e6-9f52-4942-a9ce-e888fbaa8958')
rep(it, '<code>', ''); rep(it, '</code>', '')

# 8. Conditions EN du footer en repli (dont la désinscription)
for i in ['153edaad-18db-4465-9854-98d2b3e0ef72', 'd35d0416-0181-4cf5-9c33-9473e0dba811',
          '99f845c3-b99a-49fd-ad7b-1f7910a72ba6', 'dc60ca6d-0379-4575-9d1b-18c819c00c0b',
          '21f0bf37-a16c-4d3f-b061-644c673f1364']:
    by_id(i)['condition'] = REPLI

# 9. Menu NL : utm
rep(by_id('7f27cd8c-7b14-4efe-a385-6792638a88a4'), 'utm_source=truckfly_web&amp;utm_medium=header', 'utm_source=brevo&amp;utm_medium=transactional_emails')

# 10. Charte : MICHELIN Truckfly, doubles espaces
def walk(o):
    if isinstance(o, dict):
        return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v) for v in o]
    if isinstance(o, str):
        return o.replace('Michelin Truckfly', 'MICHELIN Truckfly').replace('Michelin</strong>', 'MICHELIN</strong>').replace("sur  l'établissement", "sur l'établissement")
    return o
y['body'] = walk(y['body'])

# Contrôles
ids = []
def collect(o):
    if isinstance(o, dict):
        if 'id' in o: ids.append(o['id'])
        for v in o.values(): collect(v)
    elif isinstance(o, list):
        for v in o: collect(v)
collect(y['body'])
assert len(ids) == len(set(ids)), 'ids en double'
txt = yaml.dump(y, allow_unicode=True, sort_keys=False, width=10**9)
assert '!contact.LANG ) %}' not in txt
open('template_final.yaml', 'w').write(txt)
open('template_final.txt', 'w').write(txt)
print('ok', len(ids), 'ids,', len(txt), 'caractères')
