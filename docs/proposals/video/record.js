const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const [,, file, outdir, fpsArg, durArg, startArg, endArg] = process.argv;
const FPS=+fpsArg||60, DUR=+durArg||43, START=+startArg||0, END=endArg?+endArg:DUR;
(async()=>{
 const b=await chromium.launch({args:['--allow-file-access-from-files']});
 const ctx=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1});
 const page=await ctx.newPage();
 await page.goto('file://'+path.resolve(file),{waitUntil:'networkidle'});
 await page.evaluate(()=>document.fonts.ready);
 // wait for particles ready
 for(let i=0;i<50;i++){ if(await page.evaluate(()=>window.__frame(0))) break; await page.waitForTimeout(100); }
 const cdp=await ctx.newCDPSession(page);
 const n0=Math.round(START*FPS), n1=Math.round(END*FPS);
 const t0=Date.now();
 for(let n=n0;n<n1;n++){
  const T=n/FPS;
  await page.evaluate(t=>window.__frame(t),T);
  const {data}=await cdp.send('Page.captureScreenshot',{format:'jpeg',quality:93});
  fs.writeFileSync(path.join(outdir,`f${String(n).padStart(5,'0')}.jpg`),Buffer.from(data,'base64'));
  if(n%300===0)console.log('frame',n,'/',n1,((Date.now()-t0)/1000).toFixed(0)+'s');
 }
 await b.close(); console.log('done',n1-n0,'frames');
})();
