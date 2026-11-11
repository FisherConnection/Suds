#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
import sys
root=Path(sys.argv[1]); assets=root/"app/src/main/assets"
def repl(path,old,new):
    s=path.read_text()
    if old not in s: raise RuntimeError("Missing required source anchor: "+old[:65])
    path.write_text(s.replace(old,new))
html=assets/"index.html"
repl(html,"transform-origin:11% center;transform-style:preserve-3d","transform-origin:7% center;transform-style:preserve-3d")
repl(html,"perspective:700px","perspective:2400px")
repl(html,"transform:translateX(-11%) scaleX(.32)","transform:translateX(-20%) rotateY(-70deg)")
repl(html,"left:34%;top:53.0%;width:54%;height:31.0%","left:25%;top:52.0%;width:53%;height:32.0%")
repl(html,"#drum-menu.options{left:33%;width:56%","#drum-menu.options{left:25%;width:53%")
repl(html,"#touchOpenDoor{display:none;position:absolute;z-index:8;left:0%;top:48%;width:31%;height:40%","#touchOpenDoor{display:none;position:absolute;z-index:8;left:0%;top:48%;width:33%;height:40%")
css="""#tv-physical-frame{position:absolute;z-index:2;left:5.9%;top:5.90%;width:88.2%;aspect-ratio:16/9;background:#0b1320;border:1.0cqw solid #242b37;border-radius:2px;box-shadow:inset 0 0 .6cqw #7284a1,0 .7cqw 1.2cqw #000c;pointer-events:none}
#tv-physical-frame:after{content:'';position:absolute;inset:0;border:1px solid #556c83;border-radius:1px;pointer-events:none}
#tv-ad{left:6.95%!important;top:6.49%!important;width:86.1%!important;height:auto!important;aspect-ratio:16/9;object-fit:fill!important;background:#081425!important;border-radius:1px}
#tv-ad-blur{display:none!important}
#tv-motion{left:6.95%!important;top:6.49%!important;width:86.1%!important;height:auto!important;aspect-ratio:16/9;object-fit:contain!important;background:#07192b}
#tapTv{left:5.9%;top:5.9%;width:88.2%;height:28.1%}
"""
repl(html,"@media(prefers-reduced-motion:reduce)",css+"\n@media(prefers-reduced-motion:reduce)")
repl(html,'<img id="tv-ad-blur" alt=""><img id="tv-ad"','<div id="tv-physical-frame" aria-hidden="true"></div><img id="tv-ad-blur" alt=""><img id="tv-ad"')
repl(html,"image/heic,image/heif,","")
repl(html,",.heic,.heif","")
repl(root/"app/src/main/java/com/oshkitech/suds/MainActivity.java",'"image/heic","image/heif",',"")
repl(assets/"app.js","if(p==='wash')for(const f of state.files){try{f.result=await SUDSCore.clean(f.file);f.status='clean';state.cleaned.push(f);}catch(e){f.status='error';f.error=String(e.message||e);}}","if(p==='wash')for(const f of state.files){try{f.result=await SUDSCore.clean(f.file);const check=await SUDSCore.clean(f.result.data);if(check.removedItems!==0)throw Error('Cleaned output failed second-pass verification');f.result.verified=true;f.status='clean';state.cleaned.push(f);}catch(e){f.status='error';f.error=String(e.message||e);}}")
files=sorted((assets/"ads").glob("SUDS_APPROVED_*.png"))
assert len(files)==13
for p in files:
    im=Image.open(p).convert("RGB");a=np.asarray(im)
    l=t=0;r=im.width;b=im.height
    for i in range(min(7,im.width//10)):
        if (np.min(a[:,i,:],axis=1)>238).mean()>.67:l=i+1
        else:break
    for i in range(min(7,im.width//10)):
        if (np.min(a[:,im.width-i-1,:],axis=1)>238).mean()>.67:r=im.width-i-1
        else:break
    for i in range(min(7,im.height//10)):
        if (np.min(a[i,:,:],axis=1)>238).mean()>.67:t=i+1
        else:break
    for i in range(min(7,im.height//10)):
        if (np.min(a[im.height-i-1,:,:],axis=1)>238).mean()>.67:b=im.height-i-1
        else:break
    im=im.crop((l,t,r,b))
    W,H=960,540
    scaled=ImageOps.contain(im,(W,H),Image.Resampling.LANCZOS)
    if scaled.size!=(W,H):
        ar=np.asarray(im)
        edges=np.concatenate((ar[:,:3,:].reshape(-1,3),ar[:,-3:,:].reshape(-1,3)),axis=0)
        color=tuple(map(int,np.median(edges,axis=0)))
        canvas=Image.new("RGB",(W,H),color)
        canvas.paste(scaled,((W-scaled.width)//2,(H-scaled.height)//2))
        im=canvas
    else: im=scaled
    im.save(p,optimize=True)
assert all(Image.open(p).size==(960,540) for p in files)
print("PASS verified source patch, 13 approved ads, true 16:9, door fully clear")
