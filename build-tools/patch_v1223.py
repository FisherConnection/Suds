#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import numpy as np
import sys
root=Path(sys.argv[1]); assets=root/"app/src/main/assets"
def repl(path,old,new):
    s=path.read_text()
    if old not in s: raise RuntimeError("Missing required source anchor: "+old[:65])
    path.write_text(s.replace(old,new))
html=assets/"index.html"
repl(html,"transform-origin:11% center;transform-style:preserve-3d","transform-origin:0% 50%;transform-style:preserve-3d")
repl(html,"perspective:700px","perspective:1500px")
repl(html,"transform:translateX(-11%) scaleX(.32)","transform:rotateY(-79deg)")
repl(html,"left:34%;top:53.0%;width:54%;height:31.0%","left:25%;top:52.1%;width:53%;height:32.5%")
repl(html,"#drum-menu.options{left:33%;width:56%","#drum-menu.options{left:25%;width:53%")
repl(html,"#touchOpenDoor{display:none;position:absolute;z-index:8;left:0%;top:48%;width:31%;height:40%","#touchOpenDoor{display:none;position:absolute;z-index:8;left:6%;top:48%;width:19%;height:38%")
css="\n#tv-ad,#tv-ad-blur,#tv-motion{left:6.9%!important;top:7.45%!important;width:86.2%!important;height:auto!important;aspect-ratio:16 / 9!important;border:0!important;box-shadow:none!important;border-radius:0!important}\n#tv-ad{object-fit:contain!important;background:#081527!important;z-index:3}\n#tv-ad-blur{display:none!important}\n#tv-motion{object-fit:contain!important;background:#081527!important}\n#tapTv{left:6.9%;top:7.45%;width:86.2%;height:27.2%}\n#cycle-lights{position:absolute;inset:0;z-index:4;pointer-events:none}\n#cycle-lights i{position:absolute;display:block;top:91.3%;width:3.0%;height:1.55%;border-radius:50%;background:radial-gradient(circle at 40% 30%,#667886 0%,#263c4e 48%,#071d2c 75%,#071b2b 100%);box-shadow:inset 0 0 .5cqw #071b2b,0 0 .6cqw #20394d}\n#cycle-lights i:nth-child(1){left:23.0%}#cycle-lights i:nth-child(2){left:50.35%}#cycle-lights i:nth-child(3){left:78.25%}\n#cycle-lights i.on{background:radial-gradient(circle at 45% 40%,#fcffff 4%,#80ffff 42%,#00aeed 66%,#0884c8 100%);box-shadow:0 0 2cqw .5cqw #01c7ff,inset 0 0 .7cqw #d1ffff}\n#active-indicator{display:none!important}\n#drum-menu{overflow:hidden}\n#drum-menu .control{font-size:clamp(9px,2.25cqw,14px);min-height:4.3cqw;line-height:1.0}\n#drum-menu .menu-list{max-height:66%;overflow-y:auto}\n.report-entry{display:flex;align-items:flex-start;gap:1cqw;text-align:left;padding:.7cqw 0;border-bottom:1px solid #ffffff22}\n.report-thumb{width:11cqw;height:11cqw;object-fit:cover;border-radius:3px;flex:none;background:#183852;border:1px solid #51a0ba}\n.report-details{font-size:clamp(8px,2cqw,12px);line-height:1.28;overflow-wrap:anywhere;min-width:0}\n.report-total{font-weight:800;color:#7bffef}\n"
repl(html,"@media(prefers-reduced-motion:reduce)",css+"\n@media(prefers-reduced-motion:reduce)")
repl(html,' <button class="control muted" id="seeFiles">SEE MY FILES</button>\n',"")
repl(html,'id="viewReport" hidden>VIEW REPORT','id="viewReport" hidden>CLEANING REPORT')
repl(html,'<div id="active-indicator"></div>','<div id="cycle-lights" aria-hidden="true"><i></i><i></i><i></i></div><div id="active-indicator"></div>')
repl(html,"image/heic,image/heif,","")
repl(html,",.heic,.heif","")
repl(root/"app/src/main/java/com/oshkitech/suds/MainActivity.java",'"image/heic","image/heif",',"")
repl(assets/"app.js","if(p==='wash')for(const f of state.files){try{f.result=await SUDSCore.clean(f.file);f.status='clean';state.cleaned.push(f);}catch(e){f.status='error';f.error=String(e.message||e);}}","if(p==='wash')for(const f of state.files){try{f.result=await SUDSCore.clean(f.file);const check=await SUDSCore.clean(f.result.data);if(check.removedItems!==0)throw Error('Cleaned output failed second-pass verification');f.result.verified=true;f.status='clean';state.cleaned.push(f);}catch(e){f.status='error';f.error=String(e.message||e);}}")

files=sorted((assets/"ads").glob("SUDS_APPROVED_*.png"))
assert len(files)==13
for f in files:
 im=Image.open(f).convert("RGB");a=np.asarray(im)
 l=0;r=im.width;t=0;b=im.height
 def white_line(arr):return float(np.mean(np.min(arr,axis=1)>240))>.90
 for i in range(min(8,im.width//20)):
  if white_line(a[:,i,:]):l=i+1
  else:break
 for i in range(min(8,im.width//20)):
  if white_line(a[:,im.width-1-i,:]):r=im.width-1-i
  else:break
 for i in range(min(8,im.height//20)):
  if white_line(a[i,:,:]):t=i+1
  else:break
 for i in range(min(8,im.height//20)):
  if white_line(a[im.height-1-i,:,:]):b=im.height-1-i
  else:break
 im=im.crop((l,t,r,b));w,h=im.size
 if w/h>16/9:
  H=int(np.ceil(w*9/16));v=H-h;pad=((v//2,v-v//2),(0,0),(0,0))
 else:
  W=int(np.ceil(h*16/9));v=W-w;pad=((0,0),(v//2,v-v//2),(0,0))
 a=np.pad(np.asarray(im),pad,mode="edge")
 Image.fromarray(a,"RGB").resize((960,540),Image.Resampling.LANCZOS).save(f,optimize=True)
assert all(Image.open(f).size==(960,540) for f in files)
print("PASS: thirteen original approved ads, exact 16:9")

import re
app=assets/"app.js"
def change(old,new):
 s=app.read_text()
 if old not in s:raise RuntimeError("Missing required app anchor: "+old[:55])
 app.write_text(s.replace(old,new))
change("show('addPhotos','seeFiles','photoTv');","show('addPhotos','photoTv');")
change("hide('addPhotos','seeFiles','photoTv','viewReport','createSlideshow','saveClean');","hide('addPhotos','photoTv','viewReport','createSlideshow','saveClean');")
change("hide('addPhotos','seeFiles','photoTv','viewReport','createSlideshow','saveClean','menuList');","hide('addPhotos','photoTv','viewReport','createSlideshow','saveClean','menuList');")
change("$('seeFiles').addEventListener('click',()=>showFiles(false));","")
change("state.menu=report?'report':'files';","state.menu='report';")
change("report?'CLEANING REPORT':'MY FILES'","'CLEANING REPORT'")
s=app.read_text()
s,n=re.subn(r"\$\('menuCaption'\)\.textContent=report\?[^;]*;","$('menuCaption').textContent=String(state.cleaned.length)+' files cleaned';",s)
if n!=1:raise RuntimeError("Cannot replace report caption")
start=s.index(" for(const [i,entry] of state.files.entries()){")
end=s.index(" fitControls();\n}",start)
s=s[:start]+""" for(const [i,entry] of state.files.entries()){
  const el=document.createElement('div');el.className='report-entry';const r=entry.result;
  const thumb=document.createElement('img');thumb.className='report-thumb';thumb.alt='Photo thumbnail';
  if(entry.file.type.startsWith('image/')){
   const url=URL.createObjectURL(entry.file);thumb.src=url;thumb.onload=()=>URL.revokeObjectURL(url);
  }
  const detail=document.createElement('div');detail.className='report-details';
  const filename=document.createElement('div');filename.textContent=safeName(entry.file.name);filename.style.fontWeight='700';detail.append(filename);
  if(entry.status==='clean'){
   const total=document.createElement('div');total.className='report-total';total.textContent=String(r.removedItems||0)+' metadata items removed';detail.append(total);
   for(const [type,count] of Object.entries(r.removedBreakdown||{})){
    const line=document.createElement('div');line.textContent=type+': '+count;detail.append(line);
   }
   if(r.verified){const flag=document.createElement('div');flag.textContent='Verified output';detail.append(flag);}
  }else{const line=document.createElement('div');line.textContent=entry.status==='error'?'Cleaning failed: '+entry.error:'Not cleaned';detail.append(line);}
  el.append(thumb,detail);list.append(el);
 }
"""+s[end:]
app.write_text(s)
s=app.read_text()
s,n=re.subn(r"toast\(\x60[^\x60]*cleaned\x60\);","toast(String(state.cleaned.length)+' cleaned; '+String(state.files.length-state.cleaned.length)+' failed/unsupported');",s)
if n!=1:raise RuntimeError("Cannot replace toast")
app.write_text(s)
change("let light=$('active-indicator');","let light=$('active-indicator'),bulbs=[...document.querySelectorAll('#cycle-lights i')];")
change("light.className=cls;light.style.display='block';","light.className=cls;light.style.display='none';bulbs.forEach((e,i)=>e.classList.toggle('on',i===['wash','rinse','spin'].indexOf(p)));")
change("state.busy=false;light.style.display='none';m.classList.remove('washing','rinsing','spinning');","state.busy=false;light.style.display='none';bulbs.forEach(e=>e.classList.remove('on'));m.classList.remove('washing','rinsing','spinning');")
change("function showFiles(report=false)","function showFiles(report=true)")
print("PASS: one CLEANING REPORT with thumbnails and five completed-cycle controls")
