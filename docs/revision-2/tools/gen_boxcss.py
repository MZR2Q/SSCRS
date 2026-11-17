# Generates the five "lighten the dark navy boxes" stylesheets.
# Each is a plain override layer on top of styles.css, so the chosen
# one can be appended to the site as-is.
import os
OUT=os.path.join(os.path.dirname(__file__),'..','boxcss')
DEEP='#2F5A24'

def quads(acc,tint,extra=''):
    return f'''
.quad{{background:#fff!important;color:var(--ink);border:1px solid var(--line);box-shadow:var(--shadow-sm)}}
.quad::after{{display:none}}
.quad strong{{color:var(--ink)}}.quad-desc{{color:var(--body)}}.quad-cta{{color:{acc}}}
.quad-icon{{background:{tint};border-color:transparent;color:{acc}}}{extra}'''

def deep(parts,g=DEEP):
    c=''
    if 'slider' in parts: c+=f'''
.hero-slider{{background:{g}}}
.hs-img{{filter:hue-rotate(-95deg) saturate(.7)}}
.hs-slide::after{{background:linear-gradient(180deg,rgba(47,90,36,.10) 20%,rgba(47,90,36,.72) 62%,rgba(38,74,29,.95) 100%)}}
.hs-kind{{color:#DDF1D5}}
.hs-cta{{background:#fff!important;color:{g}!important;border-color:#fff!important;box-shadow:none!important}}
.hs-dot.is-active{{background:#fff}}'''
    if 'numbers' in parts: c+=f'''
.numbers-panel{{background:{g};box-shadow:var(--shadow-md)}}
.num-val sup{{color:#B9E5A8}}'''
    if 'goals' in parts: c+=f'''
.goals-band{{background:{g};box-shadow:var(--shadow-md)}}
.goal-num{{color:#B9E5A8}}.goal:hover{{border-top-color:#B9E5A8}}'''
    if 'tier' in parts: c+=f'''
.tier-card.is-honorary{{background:{g};box-shadow:var(--shadow-md)}}
.tier-card.is-honorary .tier-for{{background:rgba(255,255,255,.16)}}'''
    if 'conf' in parts: c+=f'''
.conf-next{{background:{g};box-shadow:var(--shadow-md)}}
.conf-next::after{{display:none}}
.conf-kicker{{background:rgba(255,255,255,.16)}}
.conf-next .btn-green{{background:#fff;color:{g};border-color:#fff;box-shadow:none}}'''
    if 'news' in parts: c+=f'''
.news-thumb{{background:{g}}}'''
    if 'footer' in parts: c+=f'''
.site-footer{{background:{g};color:rgba(255,255,255,.78)}}
.footer-about p{{color:rgba(255,255,255,.72)}}
.footer-col a:hover{{color:#C9EBBB}}'''
    return c

def light(parts,bg,ink,body,acc,border,card,tint,shadow='none',footbg=None):
    c=''
    if 'slider' in parts: c+=f'''
.hero-slider{{background:{bg} url("sscrs-seal.png") no-repeat right 78px top 34px / 132px;box-shadow:{shadow};border:1px solid {border}}}
[dir="rtl"] .hero-slider{{background-position:left 78px top 34px}}
.hs-img{{display:none}}.hs-slide::after{{display:none}}
.hs-title{{color:{ink}}}.hs-when{{color:{body}}}
.hs-kind{{background:{tint};color:{acc};backdrop-filter:none}}
.hs-arrow{{background:{card};border-color:{border};color:{ink};backdrop-filter:none}}
.hs-dot{{background:{border}}}.hs-dot.is-active{{background:{acc}}}'''
    if 'numbers' in parts: c+=f'''
.numbers-panel{{background:{bg};box-shadow:{shadow};border:1px solid {border}}}
.numbers-panel h2{{color:{ink}}}
.numbers-panel .eyebrow-dark{{background:{tint};color:{acc}}}
.num-card{{background:{card};border-color:{border}}}.num-card:hover{{background:{card}}}
.num-val{{color:{acc}}}.num-val sup{{color:{acc}}}.num-label{{color:{body}}}'''
    if 'goals' in parts: c+=f'''
.goals-band{{background:{bg};box-shadow:{shadow};border:1px solid {border}}}
.goals-head h3{{color:{ink}}}
.goals-band .vmg-tag.is-onDark{{background:{tint};color:{acc}}}
.goal{{color:{body};border-top-color:{border}}}.goal:hover{{color:{ink};border-top-color:{acc}}}
.goal-num{{color:{acc}}}'''
    if 'tier' in parts: c+=f'''
.tier-card.is-honorary{{background:{bg};box-shadow:{shadow};border-color:{border}}}
.tier-card.is-honorary .tier-for{{background:{acc};color:#fff}}
.tier-card.is-honorary h3{{color:{ink}}}
.tier-card.is-honorary .tier-lead{{color:{body};border-bottom-color:{border}}}
.tier-card.is-honorary .tier-list li{{color:{body}}}
.tier-card.is-honorary .tier-list li::before{{background-color:{tint}}}
.tier-card.is-honorary .tier-btn.is-static{{border-color:{border};color:{body}}}
.tier-badge{{background-color:{acc};border-color:{acc}}}'''
    if 'conf' in parts: c+=f'''
.conf-next{{background:{bg};color:{ink};box-shadow:{shadow};border:1px solid {border}}}
.conf-next::after{{display:none}}
.conf-kicker{{background:{acc}}}
.conf-next h3{{color:{ink}}}.conf-theme{{color:{body}}}
.conf-facts li{{color:{ink}}}.conf-fact-ic{{background:{tint};color:{acc}}}
.conf-next .btn-ghost{{background:transparent;color:{ink};border-color:{border}}}
.conf-dates{{background:{card};border-color:{border};backdrop-filter:none}}
.conf-dates-h{{color:{acc}}}.conf-dates dl>div{{border-top-color:{border}}}
.conf-dates dt{{color:{body}}}.conf-dates dd{{color:{ink}}}'''
    if 'news' in parts: c+=f'''
.news-thumb{{background:{bg}}}.news-thumb svg{{filter:none}}'''
    if 'footer' in parts:
        fb=footbg or bg; c+=f'''
.site-footer{{background:{fb};color:{body};border-top:1px solid {border}}}
.footer-identity svg{{filter:none}}
.footer-identity .lockup-ar,.footer-identity .lockup-en{{color:{ink}}}.footer-identity .lockup-est{{color:{body}}}
.footer-about p{{color:{body}}}.footer-col h5{{color:{ink}}}.footer-col a:hover{{color:{acc}}}
.footer-bottom{{border-top-color:{border}}}.footer-legal a:hover{{color:{ink}}}
.footer-social a{{background:{card};border-color:{border};color:{acc}}}'''
    return c

ALL=['slider','numbers','goals','tier','conf','news','footer']
MINT=dict(bg='#E7F1E2',ink='#1E2A22',body='#4A5A4E',acc='#3C7A2A',border='#D3E5CB',card='#FFFFFF',tint='#D6E9CD')
opts={
 1:('/* 1 — Deep palm green, flat: every dark navy panel takes the chair-card green */\n'+deep(ALL)+quads('#3C7A2A','#E7F1E2')),
 2:('/* 2 — Mint wash: light green panels, dark text */\n'+light(ALL,footbg='#F1F7EE',**MINT)+quads('#3C7A2A','#E7F1E2')),
 3:('/* 3 — White cards with green details: the most minimal */\n'+light(ALL,bg='#FFFFFF',ink='#101B2B',body='#56637A',acc='#3C7A2A',border='#E3E9E1',card='#F6FAF4',tint='#E7F1E2',shadow='0 1px 2px rgba(11,36,68,.04), 0 10px 30px rgba(11,36,68,.06)',footbg='#F7F9F6')+quads('#3C7A2A','#E7F1E2')),
 4:('/* 4 — Sky wash: keeps the blue identity, drops the darkness */\n'+light(ALL,bg='#EAF1FB',ink='#0B2444',body='#4B5A72',acc='#1B4C93',border='#D5E2F4',card='#FFFFFF',tint='#DCE8F8',footbg='#F3F7FC')+quads('#1B4C93','#E7EFFA')),
 5:('/* 5 — Hierarchy mix: one deep-green anchor per page, mint for the rest */\n'+deep(['slider','conf','footer'])+light(['numbers','goals','tier','news'],**MINT)+quads('#3C7A2A','#E7F1E2')),
}
os.makedirs(OUT,exist_ok=True)
for k,v in opts.items(): open(os.path.join(OUT,f'opt{k}.css'),'w').write(v.strip()+'\n')
open(os.path.join(OUT,'opt0.css'),'w').write('/* current */\n')
print('wrote',len(opts),'option stylesheets')
