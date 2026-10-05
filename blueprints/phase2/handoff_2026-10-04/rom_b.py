import math, json
GSF=85793
print("RSMeans open shop check:", round(129.64*1.25*1.07,2), "A/E $/SF", round(129.64*1.25*0.07,2), "share of total", round(129.64*1.25*0.07/173.39*100,2),"%")
AE=129.64*1.25*0.07/173.39        # architect-fee share embedded in the RSMeans total
psf={"low":215,"mid":260,"high":340}
stone=4013
def run(frac=1.0, fix=True):
    out={}
    for k,i in (("low",0),("mid",1),("high",2)):
        bld=GSF*psf[k]; seat=2200*(80,165,250)[i]; ffe=(400e3,750e3,1.5e6)[i]
        portal=stone*(60,100,150)[i]+(250e3,500e3,900e3)[i]+(75e3,150e3,300e3)[i]
        walk=69111+(0,10000,20412)[i]+1200*(20,35,50)[i]+(5e3,10e3,15e3)[i]
        spaces=math.ceil(734*frac); park=spaces*(4500,5650,6800)[i]
        site=bld*(0.05,0.08,0.12)[i]
        hard=bld+seat+ffe+portal+walk+park+site
        soft_old=hard*(0.08,0.11,0.14)[i]
        soft=soft_old-(AE*bld if fix else 0)
        cont=(hard+soft)*(0.10,0.15,0.20)[i]
        out[k]=dict(bld=bld,seat=seat,ffe=ffe,portal=portal,walk=walk,park=park,spaces=spaces,site=site,hard=hard,soft_old=soft_old,ae_removed=AE*bld if fix else 0,soft=soft,cont=cont,tot=hard+soft+cont)
    return out
old=run(1.0,False); new=run(1.0,True)
for r in ("bld","seat","ffe","portal","walk","park","site","hard","soft_old","ae_removed","soft","cont","tot"):
    print(f"{r:10s}", *[f"{new[k][r]:>14,.0f}" for k in new])
print("OLD totals", [round(old[k]['tot']) for k in old], "NEW totals", [round(new[k]['tot']) for k in new], "all-in $/GSF", [round(new[k]['tot']/GSF) for k in new])
print("delta", [round(new[k]['tot']-old[k]['tot']) for k in new])
for f in (1.0,0.5,0.25):
    r=run(f); print(f, [r[k]['spaces'] for k in r], [round(r[k]['tot']) for k in r], [round(r[k]['park']) for k in r], "vs100%", [round(r[k]['tot']-new[k]['tot']) for k in r])
print("portal high with stone at $200/SF and structure 1.5M:", round(stone*200+1.5e6+300e3))
json.dump({"new":new},open(f"{'C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad'}/rom_b.json","w"),indent=1)
