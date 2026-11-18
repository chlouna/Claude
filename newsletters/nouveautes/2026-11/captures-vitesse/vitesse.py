import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC='/tmp/claude-0/-home-user-Claude/9a49f491-4c8c-58f0-84fb-d0f3353a8ad8/images/'
F='/home/user/Claude/guide-profil/assets/fonts/'
# fichier, vitesse, sortie
JOBS=[('29.jpg','68','capture-1-ES'),('30.png','28','capture-2'),('31.png','27','capture-3-IT'),('32.jpg','29','capture-4-EN'),('33.jpg','48','capture-5')]
for fn,v,out in JOBS:
    im=Image.open(SRC+fn).convert('RGB'); W,H=im.size; s=W/472
    if W==472: C=(61,808); r=35.5; L=(103,779); Lr=21
    else: C=(76,1010.5); r=44.5; L=(129,973); Lr=31
    R=r+7*s
    S=4; big=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); d=ImageDraw.Draw(big)
    cx,cy=C[0]*S,C[1]*S
    d.ellipse([cx-R*S,cy-R*S,cx+R*S,cy+R*S],fill=(238,241,246,255))
    d.ellipse([cx-r*S,cy-r*S,cx+r*S,cy+r*S],fill=(255,255,255,255),outline=(206,212,222,255),width=int(1.5*s*S))
    fb=ImageFont.truetype(F+'Inter-Bold.otf',int(27*s*S)); fr=ImageFont.truetype(F+'Inter-Regular.otf',int(15*s*S))
    d.text((cx,cy-6*s*S),v,font=fb,fill=(6,24,102,255),anchor='mm')
    d.text((cx,cy+15*s*S),'km/h',font=fr,fill=(90,98,115,255),anchor='mm')
    ov=big.resize((W,H),Image.LANCZOS)
    # masque : ne pas toucher au panneau de limitation
    m=Image.new('L',(W*S,H*S),255); ImageDraw.Draw(m).ellipse([(L[0]-Lr)*S,(L[1]-Lr)*S,(L[0]+Lr)*S,(L[1]+Lr)*S],fill=0)
    m=m.resize((W,H),Image.LANCZOS)
    a=Image.composite(ov.split()[3],Image.new('L',(W,H),0),m)
    ov.putalpha(a)
    res=im.convert('RGBA'); res.alpha_composite(ov); res=res.convert('RGB')
    ext='png' if fn.endswith('png') else 'jpg'
    res.save(out+'.'+ext,quality=95)
    z=res.crop((0,int(C[1]-80*s),int(170*s),int(C[1]+60*s))).resize((int(170*s)*3,int(140*s)*3)); z.save('/tmp/claude-0/-home-user-Claude/9a49f491-4c8c-58f0-84fb-d0f3353a8ad8/scratchpad/vit/z_'+out+'.png')
print('ok')
