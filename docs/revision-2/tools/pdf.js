const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch(); const p=await b.newPage();
 await p.goto('file://'+path.resolve(__dirname,'..','deck.html'),{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(700);
 const out=process.argv[2]; await p.pdf({path:out,width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true,margin:{top:0,right:0,bottom:0,left:0}});
 console.log('pdf',out); await b.close();})();
