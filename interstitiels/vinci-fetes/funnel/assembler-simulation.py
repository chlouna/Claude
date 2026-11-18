# Assemble simulation.html à partir de simulation.tpl.html et des écrans du quiz de funnel.html.
# Usage : python3 interstitiels/vinci-fetes/funnel/assembler-simulation.py
import os

ici = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(ici, 'funnel.html')).read()
css = s[s.index('<style>') + 7:s.index('</style>')]


def page(nom):
    i = s.index(f'data-nom="{nom}"')
    a = s.index('<div class="page">', i)
    b = s.index('</section>', i)
    inner = s[a + len('<div class="page">'):b]
    return inner[:inner.rindex('</div>')]


contenu = page('2-quiz-debut') + page('3-quiz-fin')
contenu = contenu.replace('class="opt ok"', 'class="opt" data-ok')
contenu = contenu.replace('<div class="case"', '<div class="case" id="case"', 1)
contenu = contenu.replace('<div class="bouton">', '<div class="bouton" id="valider">', 1)
tpl = open(os.path.join(ici, 'simulation.tpl.html')).read()
open(os.path.join(ici, 'simulation.html'), 'w').write(tpl.replace('__CSS__', css).replace('__CONTENU__', contenu))
