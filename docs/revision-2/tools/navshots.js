const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const W=path.resolve(__dirname,'..');
(async()=>{
  const b=await chromium.launch();
  // backdrop: the live hero below its header, at 1280 wide
  { const ctx=await b.newContext({viewport:{width:1280,height:900},deviceScaleFactor:2}); const p=await ctx.newPage();
    await p.goto('http://localhost:8765/index.html',{waitUntil:'networkidle'});
    await p.addStyleTag({content:'*{animation-duration:0s!important;transition-duration:0s!important}.reveal{opacity:1!important;transform:none!important}.chat-fab{display:none!important}'});
    await p.waitForTimeout(500);
    const hh=await p.evaluate(()=>Math.round(document.querySelector('.site-header').getBoundingClientRect().bottom));
    await p.screenshot({path:path.join(W,'backdrop.png'),clip:{x:0,y:hh,width:1280,height:520}});
    await p.screenshot({path:path.join(W,'nav','current.png'),clip:{x:0,y:0,width:1280,height:hh+34}});
    console.log('backdrop ok, current header h',hh); await ctx.close(); }
  const meta={};
  for(let v=1;v<=10;v++){ meta[v]={};
    for(const [s,l] of [['default','en'],['hover','en'],['open','en'],['default','ar']]){
      const ctx=await b.newContext({viewport:{width:1280,height:640},deviceScaleFactor:2}); const p=await ctx.newPage();
      p.on('pageerror',e=>console.log('ERR',v,s,e.message));
      await p.goto('file://'+path.join(W,'nav.html')+`?v=${v}&s=${s}&l=${l}`,{waitUntil:'networkidle'});
      const m=await p.evaluate(()=>window.__ready()); await p.waitForTimeout(150);
      const h = s==='open' ? Math.max(m.menu,m.nav)+26 : m.nav+30;
      const key=l==='ar'?'ar':s; meta[v][key]={h,nav:m.nav};
      await p.screenshot({path:path.join(W,'nav',`n${v}-${key}.png`),clip:{x:0,y:0,width:1280,height:h}});
      await ctx.close();
    } console.log('nav',v,JSON.stringify(meta[v]));
  }
  fs.writeFileSync(path.join(W,'nav','meta.json'),JSON.stringify(meta)); await b.close();
})();
