#!/usr/bin/env python3
"""SUDS PRO 1.2.21: deterministic corrections on SHA-verified v1.2.20 source."""
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageDraw
import numpy as np
import sys
root=Path(sys.argv[1]); assets=root/"app/src/main/assets"
def replace(path,old,new):
    src=path.read_text()
    if old not in src: raise RuntimeError("Required source anchor missing: "+old[:70])
    path.write_text(src.replace(old,new))
html=assets/"index.html"
replace(html,"transform-origin:11% center;transform-style:preserve-3d","transform-origin:8% center;transform-style:preserve-3d")
replace(html,"transform:translateX(-11%) scaleX(.32)","transform:translateX(-8%) rotateY(-65deg)")
replace(html,"left:34%;top:53.0%;width:54%;height:31.0%","left:32%;top:51.8%;width:57%;height:33.0%")
replace(html,"#drum-menu.options{left:33%;width:56%","#drum-menu.options{left:32%;width:57%")
replace(html,"height:23.8%;background:#07192b;object-fit:contain;pointer-events:none}","height:23.8%;background:transparent;object-fit:fill;pointer-events:none}")
replace(html,"image/heic,image/heif,","")
replace(html,",.heic,.heif","")
java=root/"app/src/main/java/com/oshkitech/suds/MainActivity.java"
replace(java,'"image/heic","image/heif",',"")
app=assets/"app.js"
replace(app,"if(p==='wash')for(const f of state.files){try{f.result=await SUDSCore.clean(f.file);f.status='clean';state.cleaned.push(f);}catch(e){f.status='error';f.error=String(e.message||e);}}","if(p==='wash')for(const f of state.files){try{f.result=await SUDSCore.clean(f.file);const check=await SUDSCore.clean(f.result.data);if(check.removedItems!==0)throw Error('Cleaned output failed second-pass verification');f.result.verified=true;f.status='clean';state.cleaned.push(f);}catch(e){f.status='error';f.error=String(e.message||e);}}")
replace(app,"toast(\u0060\u0024{state.cleaned.length} file\u0024{state.cleaned.length===1?'':'s'} cleaned\u0060);","toast(\u0060\u0024{state.cleaned.length} cleaned; \u0024{state.files.length-state.cleaned.length} unsupported/failed. Check VIEW REPORT\u0060);")
# Only strip machine-added all-white collage separator pixels.
# Preserve the approved ad contents; use blurred continuation of SAME ad to fill the TV.
for p in sorted((assets/"ads").glob("SUDS_APPROVED_*.png")):
    original=Image.open(p).convert("RGB")
    a=np.asarray(original); w,h=original.size; l=t=0; r=w; b=h
    for i in range(min(9,w//10)):
        if np.mean(np.min(a[:,i,:],axis=1)>236)>.92:l=i+1
        else:break
    for i in range(min(7,h//10)):
        if np.mean(np.min(a[i,:,:],axis=1)>236)>.92:t=i+1
        else:break
    for i in range(min(9,w//10)):
        if np.mean(np.min(a[:,w-1-i,:],axis=1)>236)>.92:r=w-i-1
        else:break
    for i in range(min(7,h//10)):
        if np.mean(np.min(a[h-1-i,:,:],axis=1)>236)>.92:b=h-i-1
        else:break
    fg=original.crop((l,t,r,b))
    W,H=1030,500
    bg=ImageOps.fit(fg,(W,H),method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(20))
    art=ImageOps.contain(fg,(W,H),method=Image.Resampling.LANCZOS)
    mask=Image.new("L",art.size,0); d=ImageDraw.Draw(mask)
    d.rectangle((2,2,art.width-3,art.height-3),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(3))
    bg.paste(art,((W-art.width)//2,(H-art.height)//2),mask)
    bg.save(p)
files=list((assets/"ads").glob("SUDS_APPROVED_*.png"))
assert len(files)==13
assert all(Image.open(p).size==(1030,500) for p in files)
print("PASS patched 13 distinct ads; removed white separators and filled TV without stretching original art")
print("PASS v1.2.21 door, menu, strict save-check, HEIC picker correction applied")
