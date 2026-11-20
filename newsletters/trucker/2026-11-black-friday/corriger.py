"""Black Friday trucker nov. 2026 : corrections (PT retiré, objet, mise en page, liens, ponctuation FR)."""
import yaml, re
y = yaml.safe_load(open('template_original.yaml'))
NB = ' '
y['subject'] = ('{% if "FR" in contact.LANG %}Du 27 au 30 novembre'+NB+': -50'+NB+'% sur ton abonnement'+NB+'!'
 '{% elif "ES" in contact.LANG %}Del 27 al 30 de noviembre: ¡-50% en tu suscripción!'
 '{% elif "IT" in contact.LANG %}Dal 27 al 30 novembre: -50% sul tuo abbonamento!'
 '{% elif "DE" in contact.LANG %}27. bis 30. November: -50% auf dein Jahresabo!'
 '{% elif "NL" in contact.LANG %}27 t/m 30 november: -50% op je jaarabonnement!'
 '{% elif "PL" in contact.LANG %}Od 27 do 30 listopada: -50% na roczną subskrypcję!'
 '{% elif "RO" in contact.LANG %}Între 27 și 30 noiembrie: -50% la abonamentul anual!'
 '{% else %}From 27 to 30 November: 50% off your annual plan!{% endif %}')

secs = y['body']['content'][0]['content']
PROMO = 'https://www.truckfly.com/add-promo-code?promoCode=BF50'
PTCOND = ['( contact.LANG == "PT" )', '( "PT" in contact.LANG )']

def cond_fix(c):
    for pat in [' and ( contact.LANG != "PT" )', '( contact.LANG != "PT" ) and ']:
        c = c.replace(pat, '')
    return c

LONG = r'<span style="color: rgb\(0, 0, 0\); font-family: Arial, helvetica, sans-serif; font-size: 16px; font-style: normal;[^"]*">'
def fix_break(t):
    t = re.sub(r'</span></p><p>' + LONG + r'<span> </span>Michelin(&nbsp;)?</span>',
               lambda m: 'Michelin' + (' </span>' if m.group(1) else '</span>'), t)
    t = re.sub(r'</span>' + LONG + r'Michelin</span></p><p style="text-align: center;">', 'Michelin</span>', t)
    return t

n_pt = n_href = n_brk = 0
for s in secs:
    if s.get('condition'): s['condition'] = cond_fix(s['condition'])
    fr = s.get('condition') == '( "FR" in contact.LANG )'
    for col in s['content']:
        keep = []
        for it in col['content']:
            if it.get('condition') in PTCOND:
                n_pt += 1; continue
            if it.get('condition'): it['condition'] = cond_fix(it['condition'])
            c = it.get('content')
            if it['type'] == 'image' and isinstance(c, dict) and not c.get('href') and s.get('title','').startswith('Bannière'):
                c['href'] = PROMO; it['layout']['default']['type'] = 'absoluteLink'; n_href += 1
            if isinstance(c, str):
                new = fix_break(c)
                if new != c: n_brk += 1
                c = new
                if fr:
                    for a, b in [('annuel !', 'annuel&nbsp;!'), ('Black Friday !', 'Black Friday&nbsp;!'),
                                 ('-50%', '-50&nbsp;%'), ('37,99€', '37,99&nbsp;€'), ('74,99€', '74,99&nbsp;€'),
                                 ('5000 codes', '5&nbsp;000 codes'), ('camion : ', 'camion&nbsp;: '),
                                 ('limités : ', 'limités&nbsp;: '), ('obstacles : ', 'obstacles&nbsp;: '),
                                 ('<h2 class="default-heading2"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 255);">Profite',
                                  '<h2 class="default-heading2" style="text-align: center;"><span style="font-family: Arial, Helvetica, sans-serif; color: rgb(255, 255, 255);">Profite')]:
                        c = c.replace(a, b)
                it['content'] = c
            if it['type'] == 'text-button' and fr:
                for k in ('text',):
                    it[k] = it[k].replace('37,99€', '37,99&nbsp;€')
                it['content']['text'] = it['content']['text'].replace('37,99€', '37,99&nbsp;€')
            keep.append(it)
        col['content'] = keep

def walk(o):
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list): return [walk(v) for v in o]
    if isinstance(o, str):
        return (o.replace('MICHELIN', 'Michelin')
                 .replace('Un GPS en option !', 'Un GPS en option&nbsp;!')
                 .replace('Consultez notre FAQ ou contactez-nous :', 'Consulte notre FAQ ou contacte-nous&nbsp;:')
                 .replace('Vous avez reçu cet email car vous vous êtes inscrit à l&#39;application mobile',
                          'Tu reçois cet e-mail car tu t&#39;es inscrit sur l&#39;application mobile')
                 .replace('geregistreerd bent in de&nbsp;Michelin&nbsp;Truckfly.', 'geregistreerd bent in de&nbsp;Michelin&nbsp;Truckfly app.'))
    return o
y['body'] = walk(y['body'])

txt = yaml.dump(y, allow_unicode=True, sort_keys=False, width=10**9)
assert '"PT"' not in txt, 'PT restant'
assert '<span> </span>Michelin' not in txt
assert 'MICHELIN' not in txt
ids = re.findall(r'^\s*id: (\S+)$', txt, re.M); assert len(ids) == len(set(ids))
open('template_corrige.yaml', 'w').write(txt); open('template_corrige.txt', 'w').write(txt)
print('PT supprimés', n_pt, '| liens bannières', n_href, '| textes réparés', n_brk, '|', len(txt))
