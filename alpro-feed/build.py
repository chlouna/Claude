import base64,re
for src,out in [('template.html','alpro-feed-avent.html'),('landing-template.html','landing-avent.html'),('profil-template.html','profil-alpro-noel.html'),('concours-template.html','concours.html'),('premiers-contenus-template.html','premiers-contenus.html'),('scenarios-template.html','scenarios.html'),('publications-template.html','publications.html')]:
    h=open(src).read()
    for k in set(re.findall(r'\{\{(\w+)\}\}',h)):
        h=h.replace('{{%s}}'%k,'data:image/jpeg;base64,'+base64.b64encode(open(k+'.jpg','rb').read()).decode())
    open(out,'w').write(h)
