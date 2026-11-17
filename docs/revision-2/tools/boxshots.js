const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const W=path.resolve(__dirname,'..'); const B='http://localhost:8765/';
const BASE='*{animation-duration:0s!important;transition-duration:0s!important}.reveal,[data-reveal]{opacity:1!important;transform:none!important}.chat-fab{display:none!important}';
// [name, page, selector|"viewport", pad, extraBottomSelector]
const T=[['home','index.html','VIEW:.quads'],['numbers','about.html','.numbers-panel'],['goals','about.html','.goals-band'],
         ['tier','membership.html','.tier-grid'],['conf','education.html','.conf-next'],['footer','index.html','.site-footer']];
(async()=>{
  const b=await chromium.launch(); const only=process.argv[2];
  for(const o of [0,1,2,3,4,5]){ if(only!==undefined && +only!==o) continue;
    const css=fs.readFileSync(path.join(W,'boxcss',`opt${o}.css`),'utf8').replace('url("sscrs-seal.png")','url("'+B+'sscrs-seal.png")');
    const ctx=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:2});
    const pages={};
    for(const [name,pg,sel] of T){
      let p=pages[pg]; if(!p){ p=pages[pg]=await ctx.newPage(); await p.goto(B+pg,{waitUntil:'networkidle'}); await p.addStyleTag({content:BASE+css});
        await p.evaluate(async()=>{window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,400));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,300));}); }
      let clip;
      if(sel.startsWith('VIEW:')){ const bot=await p.evaluate(s=>{const e=document.querySelector(s);const r=e.getBoundingClientRect();return r.bottom+window.scrollY;},sel.slice(5)); clip={x:0,y:0,width:1440,height:Math.round(bot)+6}; }
      else { clip=await p.evaluate(s=>{const e=document.querySelector(s);const r=e.getBoundingClientRect();const pad=s==='.site-footer'?0:26;return {x:Math.max(0,r.left-pad),y:r.top+window.scrollY-pad,width:Math.min(1440,r.width+2*pad),height:r.height+2*pad};},sel); }
      if(sel.startsWith('VIEW:')){ await p.setViewportSize({width:1440,height:clip.height}); await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(350); await p.screenshot({path:path.join(W,'box',`o${o}-${name}.png`)}); await p.setViewportSize({width:1440,height:900}); await p.waitForTimeout(200); }
      else await p.screenshot({path:path.join(W,'box',`o${o}-${name}.png`),fullPage:true,clip});
    }
    await ctx.close(); console.log('option',o,'done');
  } await b.close();
})();
