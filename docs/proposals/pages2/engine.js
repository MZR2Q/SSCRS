/* Shared walkthrough engine — deterministic window.__frame(T) for video capture.
   A page sets window.CFG then includes this file. */
(function(){
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const eo=t=>1-Math.pow(1-t,3), eio=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const seg=(T,t0,d)=>clamp((T-t0)/d);
const W=innerWidth, H=innerHeight;
const C=window.CFG||{};
const LIGHT=/mode=light/.test(location.search);
if(C.lightParam && LIGHT) document.documentElement.classList.add('light');

// --- injected chrome ---
const style=document.createElement('style');
style.textContent=`
html{cursor:none}
#wk-cur{position:fixed;z-index:60;width:18px;height:18px;border-radius:50%;background:var(--cur,#0B2444);box-shadow:0 0 0 2px var(--curr,rgba(255,255,255,.9)),0 4px 14px rgba(0,0,0,.35);pointer-events:none;transform:translate(-50%,-50%);left:-100px;top:-100px}
#wk-rip{position:fixed;z-index:59;border-radius:50%;border:2px solid var(--cur,#0B2444);pointer-events:none;transform:translate(-50%,-50%);opacity:0}
#wk-end{position:fixed;inset:0;z-index:71;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;opacity:0;pointer-events:none;background:var(--fade,#0B2444);color:var(--endfg,#fff);gap:12px;padding:40px}
#wk-end img{width:120px;margin-bottom:8px}
#wk-end h2{font-size:38px;font-weight:400;letter-spacing:-.02em;max-width:22ch}
#wk-end .s{font-size:20px;opacity:.72}
#wk-end .l{font-size:12px;letter-spacing:.22em;text-transform:uppercase;opacity:.5;margin-top:14px}
.wk-hov{box-shadow:0 18px 50px rgba(0,0,0,.14),0 0 0 1.5px var(--accent,#1B4C93)!important;border-color:var(--accent,#1B4C93)!important}
.wk-sel{box-shadow:inset 3px 0 0 var(--accent,#1B4C93)!important}
`;
document.head.appendChild(style);
const mk=(id,html)=>{const d=document.createElement('div');d.id=id;if(html!==undefined)d.innerHTML=html;document.body.appendChild(d);return d};
const cur=mk('wk-cur',''), rip=mk('wk-rip','');
const E=C.end||{};
const end=mk('wk-end', (E.seal?`<img src="${E.seal}">`:'')+`<h2>${E.title||''}</h2>`+(E.sub?`<div class="s">${E.sub}</div>`:'')+(E.label?`<div class="l">${E.label}</div>`:''));

// measure faq bodies
$$('.qb').forEach(b=>{b.style.maxHeight='none';b.dataset.h=b.scrollHeight;b.style.maxHeight='0'});

// --- scroll ---
const horiz=!!C.track;
const trackEl=horiz?$(C.track):null;
function target(v){ if(typeof v!=='string')return v; const el=$(v); if(!el)return 0; return horiz?el.offsetLeft-(C.hpad||40):el.offsetTop-(C.vpad||90); }
function keyScroll(T){const K=C.scroll||[[0,0]];let y=target(K[0][1]);for(let i=0;i<K.length-1;i++){const a=K[i],b=K[i+1];const A=target(a[1]),B=target(b[1]);if(T<=a[0])return A;if(T<b[0])return A+(B-A)*eio((T-a[0])/(b[0]-a[0]));y=B}return y}
function applyScroll(y){ if(horiz){trackEl.style.transform=`translateX(${-y}px)`;} else window.scrollTo(0,y); }

// --- cursor ---
function pt(p){if(typeof p[1]==='string'){const e=$(p[1]);const r=e?e.getBoundingClientRect():null;if(!r||r.width===0)return[W/2,H*0.5];return[r.left+r.width/2,r.top+Math.min(r.height/2,34)]}return[p[1],p[2]]}
function cursorAt(T){const P=C.path||[[0,W/2,H/2]];if(T<=P[0][0])return pt(P[0]);for(let i=0;i<P.length-1;i++){const a=P[i],b=P[i+1];if(T>=a[0]&&T<b[0]){const A=pt(a),B=pt(b);const k=eio((T-a[0])/(b[0]-a[0]));return[A[0]+(B[0]-A[0])*k,A[1]+(B[1]-A[1])*k]}}return pt(P[P.length-1])}

// --- frame ---
window.__frame=function(T){
 const y=keyScroll(T); applyScroll(y);
 $$('.rv').forEach(el=>{let e;if(el.dataset.rv!==undefined){e=eo(seg(T,+el.dataset.rv,.8));}else if(horiz){const r=el.getBoundingClientRect();e=eo(clamp((W*0.92-r.left)/220));}else{const r=el.getBoundingClientRect();e=eo(clamp((H*0.86-r.top)/120));}el.style.opacity=e;el.style.transform=`translateY(${(1-e)*(+el.dataset.dy||24)}px)`});
 $$('.cnt').forEach(el=>{const r=el.getBoundingClientRect();const p=eo(clamp((H*0.84-r.top)/120));el.textContent=Math.round(+el.dataset.v*p)+(p>=1?(el.dataset.s||''):'')});
 (C.faq||[]).forEach(f=>{const el=$(f.id);if(!el)return;const q=eo(seg(T,f.at,0.5));const b=el.querySelector('.qb');if(b){b.style.maxHeight=(q*(+b.dataset.h||140))+'px';b.style.opacity=q}const ch=el.querySelector('.chev');if(ch)ch.style.transform=`rotate(${q*180}deg)`;el.classList.toggle('open',q>0.03)});
 (C.docs||[]).forEach(dc=>{let idx=dc.start||0;for(const s of dc.sched){if(T>=s[0])idx=s[1]}$$(dc.list+' .doc, '+dc.list+' .docrow').forEach((e,i)=>e.classList.toggle('wk-sel',i===idx));if(dc.title){const t=$(dc.title);if(t)t.textContent=dc.titles[idx]}});
 const cu=cursorAt(T);cur.style.left=cu[0]+'px';cur.style.top=cu[1]+'px';
 $$('.wk-hov').forEach(e=>e.classList.remove('wk-hov'));
 if(T>(C.hoverFrom||5)){const u=document.elementFromPoint(cu[0],cu[1]);const g=u&&u.closest&&u.closest(C.hoverSel||'.card,.glass');if(g&&!g.closest('#wk-end'))g.classList.add('wk-hov')}
 const clicks=(C.clicks||[]);let r0=0,rs=0;for(const tc of clicks){const q=seg(T,tc,0.5);if(q>0&&q<1){r0=1-q;rs=12+64*q}}rip.style.opacity=r0;rip.style.width=rip.style.height=rs+'px';rip.style.left=cu[0]+'px';rip.style.top=cu[1]+'px';cur.style.transform=`translate(-50%,-50%) scale(${r0>0?0.82:1})`;
 end.style.opacity=E.at?eo(seg(T,E.at,1.0)):0;
 if(window.__bg)window.__bg(T,y,cu);
 return (window.__bgReady===undefined)?true:window.__bgReady;
};
})();
