"""Visuel téléphone : tuto code promo, 5 langues (d'après les captures iOS de l'appli)."""
F = "font-family:'Noto Sans',Arial,Helvetica,sans-serif;"

L = {
 "FR": dict(head="Ton code promo en 5&nbsp;étapes", sub="Directement dans l’appli Michelin Truckfly.",
   s=["Ouvre ton profil", "Appuie sur ton statut", "Choisis le code promo", "Tape ton code", "Valide"],
   c1="👤 En haut à droite de la carte", c2="Truckfly Premium · aucun abonnement",
   t=["1 mois", "12 mois", "Utiliser un code promotionnel"], sheet="Activer l’offre", field="Code", c5="Activer",
   foot="<strong>Ça ne marche pas&nbsp;?</strong><br>Vérifie que tu es connecté à ton compte et que tu n’as aucun abonnement en cours."),
 "EN": dict(head="Your promo code in 5 steps", sub="Right in the Michelin Truckfly app.",
   s=["Open your profile", "Tap your status", "Choose the promo code", "Type your code", "Confirm"],
   c1="👤 Top right of the map", c2="Truckfly Premium · no subscription",
   t=["1 month", "12 months", "Use a promo code"], sheet="Redeem offer", field="Code", c5="Redeem",
   foot="<strong>Not working?</strong><br>Check that you are logged in to your account and have no active subscription."),
 "ES": dict(head="Tu código promocional en 5 pasos", sub="Directamente en la app Michelin Truckfly.",
   s=["Abre tu perfil", "Pulsa en tu estado", "Elige el código promocional", "Escribe tu código", "Confirma"],
   c1="👤 Arriba a la derecha del mapa", c2="Truckfly Premium · sin suscripción",
   t=["1 mes", "12 meses", "Usar un código promocional"], sheet="Activar la oferta", field="Código", c5="Activar",
   foot="<strong>¿No funciona?</strong><br>Comprueba que has iniciado sesión en tu cuenta y que no tienes ninguna suscripción activa."),
 "IT": dict(head="Il tuo codice promo in 5 passaggi", sub="Direttamente nell’app Michelin Truckfly.",
   s=["Apri il tuo profilo", "Tocca il tuo stato", "Scegli il codice promo", "Inserisci il codice", "Conferma"],
   c1="👤 In alto a destra della mappa", c2="Truckfly Premium · nessun abbonamento",
   t=["1 mese", "12 mesi", "Usa un codice promozionale"], sheet="Attiva l’offerta", field="Codice", c5="Attiva",
   foot="<strong>Non funziona?</strong><br>Verifica di aver effettuato l’accesso al tuo account e di non avere abbonamenti attivi."),
 "NL": dict(head="Je promotiecode in 5 stappen", sub="Rechtstreeks in de Michelin Truckfly app.",
   s=["Open je profiel", "Tik op je status", "Kies de promotiecode", "Typ je code", "Bevestig"],
   c1="👤 Rechtsboven op de kaart", c2="Truckfly Premium · geen abonnement",
   t=["1 maand", "12 maanden", "Promotiecode gebruiken"], sheet="Aanbieding activeren", field="Code", c5="Activeren",
   foot="<strong>Werkt het niet?</strong><br>Controleer of je bent ingelogd op je account en geen lopend abonnement hebt."),
}

def chip(t, bg="#F5F3F1", fg="#061866", bd="1px solid #B5D2F4"):
    return f'<p style="margin:6px 0 0 0;"><span style="display:inline-block;background-color:{bg};color:{fg};border:{bd};{F}font-size:10px;font-weight:700;line-height:1.3;border-radius:8px;padding:4px 8px;">{t}</span></p>'

def tiles(t):
    def tile(txt, on=False):
        st = ("background-color:#FFFFFF;border:2px solid #061866;" if on else "background-color:#F5F3F1;border:1px solid #D9D9D9;")
        col = "#061866" if on else "#8A8A8A"
        icon = '<span style="font-size:12px;">⚙</span><br>' if on else ""
        return f'<td width="33%" align="center" valign="middle" style="{st}border-radius:6px;padding:5px 3px;{F}font-size:9px;line-height:1.2;font-weight:700;color:{col};">{icon}{txt}</td>'
    gap = '<td width="4" style="font-size:0;line-height:0;">&nbsp;</td>'
    return (f'<table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" style="width:100%;margin-top:6px;border-collapse:separate;"><tr>'
            f'{tile(t[0])}{gap}{tile(t[1])}{gap}{tile(t[2], True)}</tr></table>')

def sheet(title, field):
    return (f'<p style="margin:6px 0 2px 0;{F}font-size:11px;font-weight:700;color:#000000;">{title}</p>'
            f'<table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" style="width:100%;border-collapse:separate;"><tr>'
            f'<td style="background-color:#F0F0F0;border-radius:6px;padding:6px 8px;{F}font-size:10px;color:#8A8A8A;">{field}<span style="color:#061866;">|</span></td></tr></table>')

def step(n, title, ui):
    return f'''
                  <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" style="width:100%;border-collapse:separate;background-color:#FFFFFF;border-radius:12px;margin-bottom:6px;">
                    <tr>
                      <td width="34" style="padding:9px 0 9px 9px;vertical-align:top;"><div style="background-color:#FFFF1A;border-radius:999px;width:26px;height:26px;line-height:26px;text-align:center;{F}font-size:13px;font-weight:700;color:#061866;">{n}</div></td>
                      <td style="padding:9px 9px 9px 8px;vertical-align:top;{F}">
                        <p style="margin:0;font-size:12px;line-height:1.3;color:#061866;font-weight:700;">{title}</p>{ui}
                      </td>
                    </tr>
                  </table>'''

def tuto(lang):
    d = L[lang]; s = d["s"]
    steps = (step(1, s[0], chip(d["c1"])) + step(2, s[1], chip(d["c2"])) + step(3, s[2], tiles(d["t"])) +
             step(4, s[3], sheet(d["sheet"], d["field"])) + step(5, s[4], chip(d["c5"], "#061866", "#FFFFFF", "1px solid #061866")))
    return f'''<!-- VISUEL TÉLÉPHONE – tuto code promo ({lang}) – à coller dans un bloc HTML Brevo -->
<style type="text/css">
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&display=swap");
</style>
<table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" style="width:100%;max-width:600px;margin:0 auto;border-collapse:collapse;">
  <tr>
    <td align="center" style="padding:15px 0 10px 0;">
      <table cellspacing="0" cellpadding="0" border="0" role="presentation" align="center" width="260" style="width:260px;margin:0 auto;border-collapse:separate;">
        <tr>
          <td style="background-color:#000000;border-radius:38px;padding:8px;">
            <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="244" style="width:244px;border-collapse:separate;background-color:#F5F3F1;border-radius:31px;">
              <tr>
                <td style="background-color:#061866;border-radius:31px 31px 0 0;padding:24px 14px 16px 14px;{F}">
                  <p style="margin:0 0 8px 0;"><span style="display:inline-block;background-color:#FFFF1A;color:#061866;{F}font-size:9px;font-weight:700;letter-spacing:0.5px;border-radius:999px;padding:4px 9px;">TUTO</span></p>
                  <p style="margin:0;font-size:16px;line-height:1.25;color:#FFFFFF;font-weight:700;">{d["head"]}</p>
                  <p style="margin:5px 0 0 0;font-size:10px;line-height:1.4;color:#FFFFFF;">{d["sub"]}</p>
                </td>
              </tr>
              <tr>
                <td style="padding:10px 9px 4px 9px;">{steps}
                </td>
              </tr>
              <tr>
                <td style="padding:4px 12px 20px 12px;text-align:center;{F}">
                  <p style="margin:0;font-size:10px;line-height:1.4;color:#061866;">{d["foot"]}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
'''
