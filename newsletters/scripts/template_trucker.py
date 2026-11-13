"""Template Trucker mensuel « Le Relais » (charte Michelin Digital Chapter 2).
python3 newsletters/scripts/template_trucker.py  →  newsletters/template/trucker-mensuel/
Chaque mois : copier le dictionnaire MODELE, remplacer les [crochets], puis traduire (skill brevo-traduction-mail-multilingue).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from trucker_2026_11_charte import page, blocs

SORTIE = Path(__file__).resolve().parent.parent / "template" / "trucker-mensuel"

MODELE = dict(
    numero="N° [XX] · [Mois Année]", sous="Le rendez-vous des routiers de la communauté Michelin Truckfly",
    gps="L'appli gratuite préférée des routiers en Europe. Et pour ceux qui en veulent plus :", gps_lien_txt="un GPS en option !", gps_lien="LIEN-GPS",
    edito_tag="L'édito",
    accroche="[Accroche : une question au routier, 8 mots max. Ex. « Tu as bien tes chaînes dans le camion ? »]",
    salut="Salut {{ contact.PRENOM | default : \"la route\" }},",
    edito=["[Phrase 1 : ce qui se passe sur la route ce mois-ci (saison, règle, événement).]",
           "[Phrase 2 : pourquoi ça compte pour le routier, avec 1 bénéfice en gras.]",
           "[Phrase 3 : ce qu'il va trouver dans ce numéro, en teasant le classement ou le sondage.]"],
    signe="[Prénom]", role="[rôle] chez Michelin Truckfly",
    prog_tag="Au programme",
    prog=["[Titre du sujet 1]", "[Titre du tuto]", "[Titre de la partie communauté]", "[Titre du bloc bravo]"],
    lab_s1="[Thème du sujet 1 : Réglementation, Sécurité, Saison…]", lab_s2="Le tuto du mois", lab_danger="[Mot-clé]", lab_s3="La communauté", lab_s4="Bravo !",
    s1_titre="[Sujet 1 : l'info utile du mois, en question si possible]",
    s1=["<strong>Le savais-tu ?</strong> [2 à 3 phrases : le fait, la date, où ça s'applique.]"],
    s1_liste_tit="[Ce qu'il faut retenir :]",
    s1_liste=["<strong>[Point clé 1]</strong> : [explication courte].", "<strong>[Point clé 2]</strong> : [explication courte]."],
    s1_suite=["<strong>[Attention :]</strong> [le piège à éviter ou la conséquence concrète, 2 phrases max.]"],
    check_tit="Ta checklist avant de partir",
    check=["<strong>[Action 1]</strong> : [vérification simple]", "<strong>[Action 2]</strong> : [vérification simple]"],
    s1_btn="[Verbe + bénéfice, ex. Je prépare mon trajet]",
    s2_titre="[Tuto : ce que l'app permet de faire, ex. « Préviens les autres en 3 gestes »]",
    s2=["<strong>[Situation concrète du routier]</strong> [1 phrase.]", "Sur Michelin Truckfly, tu peux <strong>[la fonctionnalité]</strong>. [Ce que ça change, 1 phrase.]"],
    pour_signaler="[Pour faire X]", etapes_signaler=["[Étape 1]", "[Étape 2]", "[Étape 3]"],
    pour_anticiper="[Pour faire Y]", etapes_anticiper=["[Étape 1]", "[Étape 2]", "[Étape 3]"],
    s2_btn="[Verbe + action dans l'app]",
    s3_titre="[Ex. Deviens le meilleur contributeur du mois]",
    s3=["[2 phrases : pourquoi contribuer aide toute la communauté.]", "Et la règle est simple : <strong>chaque action vaut 1 point.</strong> Une pause café suffit pour en gagner plusieurs !"],
    regle="1 action = 1 point",
    actions=[("Ajouter une photo", "Parking, entrée, douches…"), ("Laisser un avis", "Note ou commente un arrêt"),
             ("Liker une photo ou une activité", "Encourage les autres conducteurs"), ("Mettre à jour un lieu", "Horaires, services, accès"),
             ("Ajouter un lieu", "Un arrêt pas encore sur l'appli"), ("Signaler une alerte", "Neige, accident, danger…")],
    s3_fin="<strong>Plus tu as de points, plus ta parole compte.</strong> Prêt à grimper au classement ?", s3_btn="Je gagne des points",
    top_titre="Les meilleurs contributeurs du mois de [mois précédent]", top_btn="C'est mon tour !",
    sondage=dict(label="Ton avis compte", question="[Question du sondage, ex. « Ton plus gros souci pour te garer le soir ? »]",
                 consigne="Clique sur ta réponse, c'est tout. Les résultats dans le prochain Relais.",
                 reponses=["[Réponse A]", "[Réponse B]", "[Réponse C]"], lien="LIEN-SONDAGE"),
    mot_tag="Le mot de la route",
    mot=["[Merci à la communauté, 1 phrase.]", "[Rendez-vous du mois prochain : ce qui arrive, 1 phrase.]", "<strong>D'ici là, prends soin de toi, sois prudent sur la route et bonne route !</strong>"],
    equipe="L'équipe Michelin Truckfly",
    faq_tit="Une question ? Un problème ?", faq="Consulte notre FAQ ou contacte-nous :",
    raison="Tu reçois cet e-mail car tu t'es inscrit à l'application mobile Michelin Truckfly.", desinscription="Se désinscrire",
    alt_loi="[Texte alternatif de l'image du sujet 1]", alt_alerte="[Texte alternatif de la capture]", alt_top="Les meilleurs contributeurs du mois",
)

IMAGES = {"loi": "[Image du sujet 1 · 1040 × 520 px · moins de 150 Ko]",
          "alerte": "[Capture ou GIF de l'app · 480 × 600 px]",
          "top": "[Visuel du classement · 1040 × 600 px]"}
LIENS = {"s1": "LIEN-SUJET-1", "s2": "LIEN-TUTO", "s3": "LIEN-POINTS", "top": "LIEN-CLASSEMENT"}

if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    corps = blocs("FR", MODELE, IMAGES, LIENS)
    html = page("[Preheader : complète l'objet, 60 à 90 caractères, ne répète pas l'objet]", corps, "fr")
    (SORTIE / "brevo-fr.html").write_text(html.replace("../../../assets/logo-truckfly-blanc.png", "URL-LOGO-BLANC"), encoding="utf-8")
    apercu = html.replace("url('URL-BIB-BOLD')", "url('URL-BIB-BOLD'), url('../../../guide-profil/assets/fonts/BIB-Bold.woff2')").replace("../../../assets/", "../../assets/")
    (SORTIE / "apercu-fr.html").write_text(apercu, encoding="utf-8")
    print("ok")
