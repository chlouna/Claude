// Personnages 3D cartoon partagés (Léa, Max) : dégradés + fonctions perso() et tete().
document.body.insertAdjacentHTML('afterbegin', `<svg width="0" height="0" style="position:absolute">
  <defs>
    <radialGradient id="peau" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#FFE1C7"/><stop offset=".6" stop-color="#F7BF96"/><stop offset="1" stop-color="#E39A72"/></radialGradient>
    <radialGradient id="peau2" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#E9B48C"/><stop offset=".6" stop-color="#C98B62"/><stop offset="1" stop-color="#A86C46"/></radialGradient>
    <linearGradient id="cyl-peau" x1="0" x2="1"><stop offset="0" stop-color="#E39A72"/><stop offset=".4" stop-color="#FFD4B3"/><stop offset="1" stop-color="#E0966D"/></linearGradient>
    <linearGradient id="cyl-moutarde" x1="0" x2="1"><stop offset="0" stop-color="#D38E1E"/><stop offset=".38" stop-color="#FFCB5C"/><stop offset="1" stop-color="#C9841A"/></linearGradient>
    <linearGradient id="cyl-corail" x1="0" x2="1"><stop offset="0" stop-color="#D9434A"/><stop offset=".38" stop-color="#FF8286"/><stop offset="1" stop-color="#CF3B42"/></linearGradient>
    <linearGradient id="cyl-marine" x1="0" x2="1"><stop offset="0" stop-color="#1D1F45"/><stop offset=".4" stop-color="#3D4080"/><stop offset="1" stop-color="#1A1C40"/></linearGradient>
    <linearGradient id="cyl-jean" x1="0" x2="1"><stop offset="0" stop-color="#2D4682"/><stop offset=".4" stop-color="#5677C2"/><stop offset="1" stop-color="#28407A"/></linearGradient>
    <radialGradient id="brun" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#8A5536"/><stop offset=".7" stop-color="#5E3520"/><stop offset="1" stop-color="#432414"/></radialGradient>
    <radialGradient id="bleu" cx="40%" cy="30%" r="75%"><stop offset="0" stop-color="#8FD3FF"/><stop offset=".6" stop-color="#3FA9F5"/><stop offset="1" stop-color="#1E7BC8"/></radialGradient>
    <radialGradient id="casq" cx="40%" cy="25%" r="80%"><stop offset="0" stop-color="#9A86FF"/><stop offset=".6" stop-color="#5B3DF5"/><stop offset="1" stop-color="#3B22C4"/></radialGradient>
    <radialGradient id="chaus" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#C9C3DE"/></radialGradient>
    <radialGradient id="noir" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="#4A4570"/><stop offset="1" stop-color="#14122A"/></radialGradient>
  </defs>
</svg>`);
// ---------- Personnages 3D cartoon (SVG ombré) ----------
const BRAS_G = "transform-box:view-box;transform-origin:56px 188px";
const BRAS_D = "transform-box:view-box;transform-origin:144px 188px";
function perso(qui, opts = {}) {
  const lea = qui === "lea";
  const haut = lea ? "url(#cyl-moutarde)" : "url(#cyl-corail)";
  const bas = lea ? "url(#cyl-marine)" : "url(#cyl-jean)";
  const peau = lea ? "url(#peau)" : "url(#peau2)";
  const tel = opts.tel ? `<g transform="translate(144 268) rotate(-12)"><rect x="-13" y="-24" width="26" height="44" rx="6" fill="url(#noir)"/><rect x="-9" y="-19" width="18" height="32" rx="3" fill="#8B6CFF"/></g>` : "";
  const cheveuxArriere = lea
    ? `<circle cx="100" cy="38" r="26" fill="url(#brun)"/><circle cx="100" cy="102" r="63" fill="url(#brun)"/>`
    : `<path d="M38 86 Q30 132 50 146 Q46 118 58 100Z M162 86 Q170 132 150 146 Q154 118 142 100Z" fill="url(#bleu)"/>`;
  const cheveuxAvant = lea
    ? `<path d="M42 104 Q44 44 100 42 Q156 44 158 104 Q148 76 118 70 Q110 84 92 74 Q62 76 42 104Z" fill="url(#brun)"/>
       <path d="M64 62 Q80 50 96 54" stroke="#9A6646" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>`
    : `<path d="M44 86 Q48 124 60 104 Q66 116 74 100 Q86 112 96 98 Q110 112 120 98 Q132 112 140 100 Q150 120 156 86Z" fill="url(#bleu)"/>
       <path d="M42 86 Q44 34 100 32 Q156 34 158 86Z" fill="url(#casq)"/>
       <path d="M60 46 Q78 36 98 38" stroke="#B9AAFF" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>
       <circle cx="100" cy="33" r="6" fill="#3B22C4"/>
       <path d="M36 88 Q100 72 164 88 Q170 100 100 98 Q30 100 36 88Z" fill="#3B22C4"/>`;
  const lunettes = lea
    ? `<g fill="rgba(255,255,255,.18)" stroke="#1E1B3A" stroke-width="4"><circle cx="79" cy="112" r="18"/><circle cx="121" cy="112" r="18"/><path d="M97 110 Q100 106 103 110" fill="none"/></g>`
    : "";
  const col = lea
    ? `<path d="M86 172 L114 172 L100 214Z" fill="#fff"/><path d="M80 172 L100 214 L92 176Z M120 172 L100 214 L108 176Z" fill="#C9841A" opacity=".55"/>`
    : `<path d="M72 168 Q100 196 128 168 Q128 160 100 160 Q72 160 72 168Z" fill="#CF3B42"/><path d="M92 182 L90 214 M108 182 L110 214" stroke="#fff" stroke-width="3" stroke-linecap="round"/>`;
  return `<svg viewBox="0 0 200 390">
    <ellipse cx="100" cy="374" rx="60" ry="10" fill="rgba(30,27,58,.16)"/>
    <g class="corps">
      <g class="jambe-g" style="transform-box:view-box;transform-origin:87px 280px"><rect x="77" y="270" width="21" height="92" rx="10" fill="${bas}"/><ellipse cx="84" cy="364" rx="18" ry="10" fill="url(#chaus)"/></g>
      <g class="jambe-d" style="transform-box:view-box;transform-origin:113px 280px"><rect x="102" y="270" width="21" height="92" rx="10" fill="${bas}"/><ellipse cx="116" cy="364" rx="18" ry="10" fill="url(#chaus)"/></g>
      <g class="bras-g" style="${BRAS_G}"><rect x="45" y="176" width="22" height="88" rx="11" fill="${haut}"/><circle cx="56" cy="268" r="12" fill="${peau}"/></g>
      <g class="bras-d" style="${BRAS_D}"><rect x="133" y="176" width="22" height="88" rx="11" fill="${haut}"/><circle cx="144" cy="268" r="12" fill="${peau}"/>${tel}</g>
      <rect x="56" y="166" width="88" height="118" rx="38" fill="${haut}"/>
      ${col}
      <g class="tete" style="transform-box:view-box;transform-origin:100px 160px">
        ${cheveuxArriere}
        <rect x="90" y="146" width="20" height="26" rx="8" fill="url(#cyl-peau)"/>
        <circle cx="42" cy="114" r="12" fill="${peau}"/><circle cx="158" cy="114" r="12" fill="${peau}"/>
        <circle cx="100" cy="106" r="58" fill="${peau}"/>
        <ellipse cx="70" cy="134" rx="10" ry="6" fill="#FF5A5F" opacity=".28"/><ellipse cx="130" cy="134" rx="10" ry="6" fill="#FF5A5F" opacity=".28"/>
        <g class="yeux" style="transform-box:view-box;transform-origin:100px 112px">
          <ellipse cx="79" cy="112" rx="11" ry="13" fill="#fff"/><ellipse cx="121" cy="112" rx="11" ry="13" fill="#fff"/>
          <circle cx="81" cy="114" r="7.5" fill="#1E1B3A"/><circle cx="123" cy="114" r="7.5" fill="#1E1B3A"/>
          <circle cx="84" cy="110" r="2.6" fill="#fff"/><circle cx="126" cy="110" r="2.6" fill="#fff"/>
        </g>
        <path d="M66 ${lea ? 90 : 96} Q78 ${lea ? 84 : 90} 90 ${lea ? 90 : 96} M110 ${lea ? 90 : 96} Q122 ${lea ? 84 : 90} 134 ${lea ? 90 : 96}" stroke="${lea ? "#5E3520" : "#1E7BC8"}" stroke-width="4.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="100" cy="126" rx="5" ry="4" fill="#000" opacity=".1"/>
        <g class="bouche" style="transform-box:view-box;transform-origin:100px 136px"><path d="M86 134 Q100 152 114 134Z" fill="#8E2F3F"/><path d="M92 141 Q100 146 108 141" stroke="#FF8B92" stroke-width="3" fill="none" stroke-linecap="round"/></g>
        ${lunettes}
        ${cheveuxAvant}
      </g>
    </g>
  </svg>`;
}
function tete(peau, cheveux, casquette) {
  return `<svg viewBox="30 30 140 140" style="width:100%;height:100%;background:#F2ECFF">
    <circle cx="100" cy="106" r="58" fill="${peau}"/>
    <path d="M42 104 Q44 44 100 42 Q156 44 158 104 Q140 72 100 72 Q60 72 42 104Z" fill="${cheveux}"/>
    ${casquette ? `<path d="M42 86 Q44 34 100 32 Q156 34 158 86Z" fill="${casquette}"/>` : ""}
    <circle cx="81" cy="114" r="7" fill="#1E1B3A"/><circle cx="121" cy="114" r="7" fill="#1E1B3A"/>
    <path d="M86 134 Q100 150 114 134Z" fill="#8E2F3F"/>
  </svg>`;
}

