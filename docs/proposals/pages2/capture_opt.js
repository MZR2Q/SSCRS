const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const out=path.join(__dirname,'..','options','render','opt');
fs.mkdirSync(out,{recursive:true});
// [file, label, [home,board,membership,committees,faq] times]
const JOBS=[
 ['tour15.html?t=A','01',[4.0,18.5,27.0,35.5,51.0]],
 ['tour15.html?t=B','02',[4.0,18.5,27.0,35.5,51.0]],
 ['tour15.html?t=C','03',[4.0,18.5,27.0,35.5,51.0]],
 ['tour15.html?t=D','04',[4.0,18.5,27.0,35.5,51.0]],
 ['tour15.html?t=E','05',[4.0,18.5,27.0,35.5,51.0]],
 ['demo6.html','06',[5.0,29.0,34.5,42.5,55.5]],
 ['tour7.html','07',[3.0,14.0,20.0,31.0,37.5]],
 ['tour8.html','08',[3.0,19.5,26.0,33.2,38.5]],
 ['tour9.html','09',[3.0,14.5,20.0,26.5,34.5]],
 ['tour10.html','10',[3.0,15.0,20.5,26.5,34.5]],
];
const NAMES=['home','board','membership','committees','faq'];
(async()=>{
 const b=await chromium.launch({args:['--allow-file-access-from-files']});
 for(const [file,dir,times] of JOBS){
  const ctx=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:2});
  const page=await ctx.newPage();
  page.on('pageerror',e=>console.log(dir,'ERR',e.message));
  await page.goto('file://'+path.resolve(file),{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  for(let i=0;i<50;i++){if(await page.evaluate(()=>window.__frame(0)))break;await page.waitForTimeout(80);}
  await page.addStyleTag({content:'#wk-cur,#wk-rip,#wk-end,#cursor,#ripple,#end{display:none!important}'});
  for(let i=0;i<times.length;i++){
   await page.evaluate(t=>window.__frame(t),times[i]);
   await page.waitForTimeout(120);
   await page.screenshot({path:path.join(out,`${dir}-${NAMES[i]}.png`)});
  }
  await ctx.close(); console.log('captured',dir);
 }
 await b.close();
})();
