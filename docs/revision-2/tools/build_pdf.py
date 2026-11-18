# -*- coding: utf-8 -*-
# Assembles revision-2 deck: applied changes + 10 navbars + 5 box treatments.
import os, json
from PIL import Image
W=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
OLD=os.path.join(W,'..','proposals','render','current')
def jpg(src,name,maxw,q=88):
    im=Image.open(src).convert('RGB')
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    out=os.path.join(W,'img',name+'.jpg'); im.save(out,quality=q,optimize=True); return 'img/'+name+'.jpg',im.width,im.height
A=lambda n:['٠','١','٢','٣','٤','٥','٦','٧','٨','٩','١٠'][n]

NAVS=[
 ('الواضح الكبير','نفس ترتيب الناف بار الحالي، لكن بخط أكبر وأسمك وارتفاع أوسع. عند التحويم ينمو خط أخضر تحت العنصر، والقائمة المنسدلة بطاقات فيها أيقونة ووصف قصير.','Inter · IBM Plex Sans Arabic','16.5px'),
 ('الطابقان','شريط علوي أخضر رفيع للتأسيس والبريد واللغة ودخول الأعضاء، وتحته صف الروابط. التحويم: خلفية نعناعية وخط سفلي أخضر. القائمة: لوحة عريضة بعمودين متصلة بالعنصر.','IBM Plex Sans · IBM Plex Sans Arabic','17px'),
 ('الكبسولة العائمة','شريط بحواف دائرية كاملة يطفو فوق الصفحة بظل ناعم. التحويم: حبّة خضراء فاتحة حول العنصر. القائمة: بطاقة عائمة مستديرة.','Manrope · Tajawal','16.5px'),
 ('الشعار في المنتصف','الشعار والاسم في وسط الشريط والروابط موزّعة على جانبيه؛ اللغة والدخول في طرف وزر الانضمام في الطرف المقابل. التحويم: لون أخضر ونقطة تحت العنصر.','DM Sans · Noto Kufi Arabic','16px'),
 ('التبويبات المتصلة','الروابط على شكل تبويبات؛ عند التحويم يتحول التبويب إلى أخضر عميق، والقائمة المنسدلة تخرج منه بنفس اللون كقطعة واحدة.','Inter · Readex Pro','16.5px'),
 ('الشريط الأخضر','صف أبيض يحمل الشعار واسم الجمعية كاملًا، وتحته شريط تنقّل أخضر عميق بعرض الصفحة بروابط بيضاء، وفي طرفه إعلان الملتقى. التحويم: العنصر ينقلب أبيض.','IBM Plex Sans · IBM Plex Sans Arabic','16.5px'),
 ('الأيقونات','لكل رابط أيقونة فوق اسمه، فيُعرف القسم من النظرة الأولى. عند التحويم ترتفع الأيقونة وتتحول إلى أخضر بظل.','Manrope · Tajawal','14.5px + أيقونة 38px'),
 ('المفاتيح المقطّعة','الروابط داخل حاوية رمادية فاتحة واحدة، والعنصر الذي تحت المؤشر يصبح بطاقة بيضاء بارزة — على طريقة مفاتيح الاختيار في تطبيقات الجوال.','Inter · IBM Plex Sans Arabic','15.5px'),
 ('الكلاسيكي المكبَّر','يحافظ على خط Times الحالي لمن يفضّل طابعه الرسمي، لكن بحجم ١٩ وسماكة عريضة وخط أخضر أعلى الشريط. التحويم: شرطة خضراء قصيرة. القائمة مرقّمة.','Times New Roman · Noto Naskh Arabic','19px'),
 ('القائمة الشاملة','التحويم: حبّة داكنة حول العنصر. وعند الفتح تنزل لوحة بعرض الصفحة كاملة: عمودا روابط بأوصافها وبطاقة لإعلان الملتقى.','DM Sans · IBM Plex Sans Arabic','16.5px'),
]
BOX=[
 ('الوضع الحالي — للمقارنة','البوكسات الكحلية الداكنة كما هي الآن في الصفحة الرئيسية وصفحات «عن الجمعية» و«العضوية» و«التعليم».'),
 ('أخضر النخيل العميق','كل بوكس كحلي يأخذ نفس أخضر بطاقة الرئيسة المعتمدة. لون واحد موحّد وقوي، بلا تدرجات.'),
 ('نعناعي فاتح','خلفية خضراء فاتحة جدًا ونص داكن وبطاقات داخلية بيضاء. أخف الخيارات الخضراء وأهدؤها.'),
 ('أبيض بلمسات خضراء','بطاقات بيضاء بحدّ رفيع، والأخضر يظهر في الأرقام والشارات والأزرار فقط. الأكثر بساطة.'),
 ('سماوي فاتح','يحافظ على الهوية الزرقاء لكن بدرجة فاتحة ونص كحلي — يزيل الدكانة دون التحول للأخضر.'),
 ('المزيج المتدرّج','عنصر واحد أخضر عميق في كل صفحة (سلايدر الرئيسية، إعلان الملتقى، التذييل) والبقية نعناعي فاتح. يعطي تدرّجًا في الأهمية.'),
]
meta=json.load(open(os.path.join(W,'nav','meta.json')))
P=[]; pg=[0]
def page(body,cls=''):
    pg[0]+=1; P.append(f'<section class="page {cls}">{body}<div class="foot"><span>SSCRS — تعديلات الوضع الحالي</span><span class="num">{pg[0]}</span></div></section>')

# 2,3 — applied before/after
for title,note,b,a in [
 ('تم التطبيق ١ — الدائرة الخضراء خلف الشعار','الشعار في الهيرو صار على قرص أخضر فاتح كما في الأسلوب ٣، مع تخفيف الظل تحته.',os.path.join(OLD,'home.png'),os.path.join(W,'shots','after-home.png')),
 ('تم التطبيق ٢ — بطاقة رئيسة مجلس الإدارة','الخلفية الكحلية المتدرجة أصبحت أخضر النخيل العميق، وأُزيل الإطار الأخضر حول الصورة، وشارة المنصب صارت شفافة هادئة.',os.path.join(OLD,'board.png'),os.path.join(W,'shots','after-board.png'))]:
    i=len(P); bp,_,_=jpg(b,f'ba{i}-before',1440); ap,_,_=jpg(a,f'ba{i}-after',1600)
    page(f'''<div class="head"><h2>{title}</h2><span class="tag ok">مطبّق على الموقع</span></div><p class="idea">{note}</p>
 <div class="ba"><figure><figcaption>قبل</figcaption><div class="frame"><img src="{bp}"></div></figure><figure><figcaption class="g">بعد</figcaption><div class="frame"><img src="{ap}"></div></figure></div>''')

# nav intro: the current bar
cp,cw,ch=jpg(os.path.join(W,'nav','current.png'),'nav-current',2560)
page(f'''<div class="head"><h2>الناف بار — الوضع الحالي</h2><span class="tag">للمقارنة</span></div>
 <p class="idea">الملاحظة: الروابط صغيرة وغير واضحة والخط غير مناسب. القياسات الحالية: خط Times New Roman بحجم 14px وسماكة متوسطة، ولون رمادي مزرق، واسم الجمعية بحجم 13.5px.</p>
 <div class="strip"><div class="frame"><img src="{cp}"></div></div>
 <div class="cols3">
  <div><h4>ما تغيّره المقترحات العشرة</h4><p>حجم الروابط من 14px إلى 16–19px، وسماكة أوضح، ولون أغمق، وارتفاع أوسع للشريط، واسم الجمعية أكبر.</p></div>
  <div><h4>ثلاث حالات لكل مقترح</h4><p>الوضع العادي، ثم عند مرور المؤشر على «Membership»، ثم قائمة «About» المنسدلة مفتوحة.</p></div>
  <div><h4>الخط</h4><p>كل مقترح يذكر خطّه الإنجليزي والعربي. النسخ العربية للعشرة مجموعة في صفحتين بعد المقترحات.</p></div>
 </div>''')

# 10 navbars — one per page, three states
AVAIL=139.0; FULL=273.0
for v in range(1,11):
    name,idea,font,size=NAVS[v-1]; m=meta[str(v)]
    tot=m['default']['h']+m['hover']['h']+m['open']['h']
    wmm=min(FULL, AVAIL/tot*1280)
    rows=''
    for key,lab in [('default','١ · الوضع العادي'),('hover','٢ · عند التحويم (Hover)'),('open','٣ · القائمة المنسدلة')]:
        p,_,_=jpg(os.path.join(W,'nav',f'n{v}-{key}.png'),f'n{v}-{key}',2560)
        rows+=f'<div class="st"><span>{lab}</span><div class="frame"><img src="{p}"></div></div>'
    page(f'''<div class="head"><h2><i>ناف بار {A(v)}</i>{name}</h2><span class="tag">الخط: <span class="en">{font}</span> · حجم الروابط <span class="en">{size}</span></span></div>
 <p class="idea">{idea}</p><div class="strips" style="width:{wmm:.1f}mm">{rows}</div>''')

# Arabic versions — two pages of five
for grp in [(1,2,3,4,5),(6,7,8,9,10)]:
    tot=sum(meta[str(v)]['ar']['h'] for v in grp); wmm=min(FULL,(160.0-5*5.2)/tot*1280)
    rows=''
    for v in grp:
        p,_,_=jpg(os.path.join(W,'nav',f'n{v}-ar.png'),f'n{v}-ar',2560)
        rows+=f'<div class="st"><span>ناف بار {A(v)} — {NAVS[v-1][0]} · <span class="en">{NAVS[v-1][2].split(" · ")[1]}</span></span><div class="frame"><img src="{p}"></div></div>'
    page(f'''<div class="head"><h2>الناف بارات بالعربية ({A(grp[0])}–{A(grp[-1])})</h2><span class="tag">نفس المقترحات عند تبديل اللغة</span></div>
 <div class="strips" style="width:{wmm:.1f}mm">{rows}</div>''')

# boxes — current + five options
for o in range(0,6):
    name,idea=BOX[o]
    im={n:jpg(os.path.join(W,'box',f'o{o}-{n}.png'),f'o{o}-{n}',1500,86) for n in ['home','numbers','goals','tier','conf','footer']}
    # crop footer to its top band
    f=Image.open(os.path.join(W,'img',f'o{o}-footer.jpg')); f=f.crop((0,0,f.width,round(f.width*0.19))); f.save(os.path.join(W,'img',f'o{o}-footer.jpg'),quality=86); im['footer']=(im['footer'][0],f.width,f.height)
    r=lambda n: im[n][2]/im[n][1]
    gap=2.2; avail=154.0
    ca=(avail-gap)/(r('home')+r('tier')); cb=(avail-3*gap)/(r('numbers')+r('goals')+r('conf')+r('footer'))
    col=min(132.0,ca,cb)
    fig=lambda n:f'<div class="frame"><img src="{im[n][0]}"></div>'
    head=(f'<h2>{name}</h2><span class="tag">مرجع</span>' if o==0 else f'<h2><i>معالجة {A(o)}</i>{name}</h2><span class="tag">{"البوكسات الزرقاء → "+name}</span>')
    page(f'''<div class="head">{head}</div><p class="idea">{idea}{"" if o==0 else " في كل المعالجات تتحول بلاطات الرئيسية الأربع الملوّنة إلى بطاقات بيضاء بأيقونة ملوّنة."}</p>
 <div class="boxes" style="grid-template-columns:{col:.1f}mm {col:.1f}mm"><div class="bc">{fig('home')}{fig('tier')}</div><div class="bc">{fig('numbers')}{fig('goals')}{fig('conf')}{fig('footer')}</div></div>''')

CSS='''@page{size:A4 landscape;margin:0}*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#0B2444;--navy:#1B4C93;--green:#3C7A2A;--deep:#2F5A24;--mint:#E7F1E2;--muted:#6B778C;--line:#E0E6EE;--g50:#F5F7FA}
body{font-family:"IBM Plex Sans Arabic","IBM Plex Sans",sans-serif;color:var(--ink);background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.en{font-family:"IBM Plex Sans",sans-serif;direction:ltr;unicode-bidi:isolate}
.page{width:297mm;height:210mm;padding:11mm 12mm 12mm;page-break-after:always;position:relative;overflow:hidden}
.page:last-child{page-break-after:auto}
.foot{position:absolute;bottom:5mm;left:12mm;right:12mm;display:flex;justify-content:space-between;font-size:7.5pt;color:var(--muted)}
.num{font-family:"IBM Plex Sans";direction:ltr}
.head{display:flex;align-items:center;justify-content:space-between;gap:6mm;margin-bottom:2mm}
h2{font-size:15pt;font-weight:600;line-height:1.3}
h2 i{font-style:normal;color:var(--green);margin-inline-end:3mm;font-size:11pt;font-weight:600;background:var(--mint);padding:.8mm 3mm;border-radius:99px;vertical-align:middle}
.tag{flex:none;font-size:8.5pt;color:var(--muted);background:var(--g50);border:1px solid var(--line);padding:1.2mm 3.5mm;border-radius:99px;white-space:nowrap}
.tag.ok{background:var(--mint);border-color:#CFE3C6;color:var(--deep);font-weight:600}
.idea{font-size:9.5pt;line-height:1.75;color:#3F4A5C;margin-bottom:3.5mm;max-width:250mm}
.frame{border:1px solid var(--line);border-radius:3px;overflow:hidden;background:#fff}
.frame img{display:block;width:100%}
.strips{margin:0 auto}
.st{margin-bottom:2mm}.st span{display:block;font-size:8pt;font-weight:600;color:var(--navy);margin-bottom:.9mm}
.strip{margin:4mm 0 8mm}
.cols3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8mm}
.cols3 h4{font-size:10.5pt;font-weight:600;margin-bottom:1.5mm;color:var(--deep)}.cols3 p{font-size:9.5pt;line-height:1.8;color:#3F4A5C}
.ba{display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin-top:2mm}
.ba figcaption{font-size:9.5pt;font-weight:600;color:var(--muted);margin-bottom:1.5mm}.ba figcaption.g{color:var(--green)}
.boxes{display:grid;gap:5mm;justify-content:center;align-items:start}
.bc{display:flex;flex-direction:column;gap:2.2mm}
.coverp{display:flex;align-items:center}
.cover{width:100%}
.cover .k{font-size:9.5pt;font-weight:600;color:var(--green);margin-bottom:4mm}
.cover h1{font-size:32pt;font-weight:600;line-height:1.25;margin-bottom:4mm}
.cover .lead{font-size:12pt;line-height:1.85;color:#3F4A5C;max-width:190mm;margin-bottom:9mm}
.items{display:grid;gap:3mm}
.it{display:grid;grid-template-columns:11mm 1fr auto;gap:5mm;align-items:center;border:1px solid var(--line);border-radius:5px;padding:4mm 5mm}
.it>b{width:9mm;height:9mm;border-radius:50%;background:var(--g50);display:grid;place-items:center;font-size:11pt;color:var(--navy)}
.it h3{font-size:11.5pt;font-weight:600;margin-bottom:.6mm}.it p{font-size:9.5pt;color:#4B5565;line-height:1.7}
.it>span{font-size:8.5pt;font-weight:600;color:var(--navy);background:var(--g50);padding:1.2mm 3.5mm;border-radius:99px;white-space:nowrap}
.it.done{background:#F6FAF4;border-color:#CFE3C6}.it.done>b{background:var(--green);color:#fff}.it.done>span{background:var(--green);color:#fff}
'''
html=f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>SSCRS — تعديلات الوضع الحالي</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(P)}</body></html>'''
open(os.path.join(W,'deck.html'),'w',encoding='utf-8').write(html); print('deck.html pages',pg[0])
