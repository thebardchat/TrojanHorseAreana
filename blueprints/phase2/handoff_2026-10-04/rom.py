import math, json
GSF=85793
esc=1552/1149; loc=0.852
base=173.39*esc*loc
print(f"escalation {esc:.4f}; RSMeans gym open-shop 2019 173.39 -> 2026 national {173.39*esc:.2f} -> Huntsville {base:.2f}")
print("localized national ranges: school gym", [round(x*loc) for x in (190,320)], "multi-sport spectator", [round(x*loc) for x in (275,336)], "field house/multi-sport", [round(x*loc) for x in (210,425)])
psf={"low":215,"mid":260,"high":340}
# portal stone area
W,Hh,D,op,spr,rise=44,50,6,28,22.1,11.9
opening=op*spr+math.pi/4*op*rise
a,b=op/2,rise; half=math.pi*(3*(a+b)-math.sqrt((3*a+b)*(a+3*b)))/2
stone=2*(W*Hh-opening)+2*D*Hh+(2*spr+half)*D+W*D
print(f"portal opening {opening:.0f} SF, stone {stone:.0f} SF")
seats=2200; spaces=math.ceil(seats/3)
L={}
for k,i in (("low",0),("mid",1),("high",2)):
    bld=GSF*psf[k]
    seat=seats*(80,165,250)[i]
    ffe=(400e3,750e3,1.5e6)[i]
    portal=stone*(60,100,150)[i]+(250e3,500e3,900e3)[i]+(75e3,150e3,300e3)[i]
    walk=69111+(0,10000,20412)[i] + 1200*(20,35,50)[i] + (5e3,10e3,15e3)[i]
    park=spaces*(4500,5650,6800)[i]
    sitedev=bld*(0.05,0.08,0.12)[i]
    hard=bld+seat+ffe+portal+walk+park+sitedev
    soft=hard*(0.08,0.11,0.14)[i]
    cont=(hard+soft)*(0.10,0.15,0.20)[i]
    tot=hard+soft+cont
    L[k]=dict(psf=psf[k],bld=bld,seat=seat,ffe=ffe,portal=portal,walk=walk,park=park,sitedev=sitedev,hard=hard,soft=soft,cont=cont,tot=tot,allin_psf=tot/GSF)
for r in L["low"]:
    print(f"{r:8s}", *[f"{L[k][r]:>14,.0f}" for k in L])
print("spaces",spaces)
json.dump(L,open(r"%s/rom.json"%r"C:/Users/Hubby/AppData/Local/Temp/claude/C--Users-Hubby-Desktop-ARENA/202807a2-361c-4275-8ca9-11bac63af77d/scratchpad","w"),indent=1)
