#!/usr/bin/env python3
"""
Boom Meeting Summary — HTML Generator
Only Boom brand colors: Blue (#4d65ff) + Gold (#ffd310) + neutrals.

Usage:
    python3 generate.py --json '{"meeting_title": "...", ...}'
    python3 generate.py --file data.json -o summary.html
    python3 generate.py --set-photo /path/to/photo.jpg
"""

import json, sys, argparse, html, base64, os
from datetime import datetime

_dir = os.path.dirname(os.path.abspath(__file__))
LOGO_WHITE = open(os.path.join(_dir, "logo_white_b64.txt")).read().strip()
LOGO_COLOR = open(os.path.join(_dir, "logo_color_b64.txt")).read().strip()
ASSETS = os.path.join(_dir, "assets")
PHOTO_PATH = os.path.join(ASSETS, "idan_photo_b64.txt")

def _photo():
    return open(PHOTO_PATH).read().strip() if os.path.exists(PHOTO_PATH) else None

def e(t): return html.escape(str(t)) if t else ""
def ini(n):
    p = n.split()
    return (p[0][0]+p[-1][0]).upper() if len(p)>=2 else n[0].upper() if n else "?"

# ─── Only Boom colors ───
B  = "#4d65ff"  # blue
BD = "#3a4ecc"  # blue dark
B10= "#eef1ff"  # blue 10%
B20= "#dce1ff"  # blue 20%
B30= "#c5ccff"  # blue 30%
G  = "#ffd310"  # gold
GD = "#e6be00"  # gold dark
G10= "#fffbe6"  # gold 10%
G20= "#fff3b3"  # gold 20%
N9 = "#121428"  # navy (near-black)
N8 = "#1e2140"  # navy 800
N7 = "#2e3352"  # navy 700
N5 = "#6b7194"  # gray text
N3 = "#d0d3e0"  # gray border
N2 = "#e8eaf2"  # gray light
N1 = "#f4f5f9"  # gray bg
N0 = "#fafbfd"  # near-white
W  = "#ffffff"

# Cards: ONLY Boom blue + gold
CAT = {
    "challenges":    {"ico":"🔍","clr":GD, "bdr":G,  "bg":G10},
    "solutions":     {"ico":"✅","clr":B,  "bdr":B,  "bg":B10},
    "opportunities": {"ico":"🚀","clr":B,  "bdr":B20,"bg":B10},
    "decisions":     {"ico":"📋","clr":GD, "bdr":G,  "bg":G10},
}

# Hardcoded testimonials from boomnow.com (curated best quotes)
TESTIMONIALS = [
    {"q":"Boom's support has been leagues ahead of any PMS we've used before. You don't feel like just another subscription.","n":"Dean McLuckie","r":"Founder","c":"Euphoric Leisure"},
    {"q":"If I had to rate it, it's a 10. The platform is really fast, much faster than the other guys.","n":"Joakim Thörn","r":"CEO","c":"Guestly Homes"},
    {"q":"We're now in a position to attract creatives and true hospitality lovers to our team, because it is no longer a call center.","n":"Sab Mulligan","r":"Head of Teams","c":"Zzzing"},
    {"q":"The relationship has felt like more than just business. I've felt the genuine interest in helping us grow.","n":"Jonathan Ellse","r":"Managing Director","c":"Perch Short Stays"},
    {"q":"The software not only touches every facet of our business, but has added enormous improvements into areas which we never thought would be possible.","n":"Richard Marshall","r":"Director","c":"NOX"},
    {"q":"Boom has completely transformed how I manage my properties. It's streamlined, easy to use, and has taken so much stress off my plate.","n":"Chet Persaud","r":"Owner","c":"KFE Management"},
    {"q":"This solution is the ultimate software tool for all property management needs! We've enhanced our operations to less than 1% bad reviews.","n":"Liran Matok","r":"CEO","c":"250+ properties across US"},
    {"q":"After a decade in the STR industry, the Boom team has brought us into a new era of tech-driven best practices and optimization.","n":"Yuval Rephael","r":"CEO","c":"Yalarent"},
]

PILLS = {
    "today":{"b":"#d03030","f":W},"tomorrow":{"b":GD,"f":N9},
    "this week":{"b":B,"f":W},"next week":{"b":BD,"f":W},
    "ongoing":{"b":N5,"f":W},"tbd":{"b":N2,"f":N5},
}

def pstyle(tl):
    t=(tl or"TBD").strip().lower()
    for k,c in PILLS.items():
        if k in t: return f'background:{c["b"]};color:{c["f"]}'
    return f'background:{B};color:{W}'

def r_people(parts):
    ph = _photo()
    o = []
    for p in parts:
        nm=p.get("name",""); ib="boom" in p.get("company","").lower()
        ii="idan" in nm.lower() and ib
        img=p.get("image")
        if not img and ii and ph: img=f"data:image/jpeg;base64,{ph}"
        if img:
            av=f'<img class="av-img" src="{e(img)}" alt="{e(nm)}"/>'
        elif ib:
            av=f'<div class="av" style="background:{B};color:{W};border:2.5px solid {G}">{e(ini(nm))}</div>'
        else:
            av=f'<div class="av" style="background:{B10};color:{B};border:2.5px solid {B20}">{e(ini(nm))}</div>'
        o.append(f'<div class="person">{av}<div><div class="pn">{e(nm)}</div><div class="pr">{e(p.get("role",""))}{(" · "+e(p.get("company",""))) if p.get("company") else ""}</div></div></div>')
    return "\n".join(o)

def r_cards(dps):
    o=[]
    for d in dps:
        c=CAT.get(d.get("category","solutions"),CAT["solutions"])
        li="\n".join(f'<li>{e(i)}</li>' for i in d.get("items",[]))
        o.append(f'<div class="crd" style="border-left:4px solid {c["bdr"]};background:{c["bg"]}"><div class="crd-h"><span class="crd-i">{c["ico"]}</span><span class="crd-t" style="color:{c["clr"]}">{e(d.get("title",""))}</span></div><ul>{li}</ul></div>')
    return "\n".join(o)

def r_demo(hl):
    if not hl: return ""
    rows="\n".join(f'<tr><td class="ft">{e(h.get("feature",""))}</td><td>{e(h.get("description",""))}</td></tr>' for h in hl)
    return f'<div class="sec"><div class="sh"><h2>💻 What We Showed You</h2></div><table class="dt"><tbody>{rows}</tbody></table></div><div class="sdiv"></div>'

def r_steps(steps):
    rows=[]
    for s in steps:
        ow=s.get("owner",""); ib="boom" in ow.lower() or "idan" in ow.lower()
        os_=f'background:{B};color:{W}' if ib else f'background:{N1};color:{N5};border:1px solid {N2}'
        rows.append(f'<tr><td><span class="pill" style="{pstyle(s.get("timeline",""))}">{e(s.get("timeline","TBD"))}</span></td><td class="act">{e(s.get("action",""))}</td><td><span class="opill" style="{os_}">{e(ow)}</span></td></tr>')
    return "\n".join(rows)

def r_testi():
    cards=[]
    for t in TESTIMONIALS:
        cards.append(f'<div class="tc"><div class="tc-q">{e(t["q"])}</div><div class="tc-ft"><div class="tc-av">{e(ini(t["n"]))}</div><div><div class="tc-nm">{e(t["n"])}</div><div class="tc-rl">{e(t["r"])} · {e(t["c"])}</div></div></div></div>')
    return f'''<div class="testi-sec">
    <div class="testi-hdr"><h2>💬 What Our Partners Say</h2><a href="https://www.boomnow.com/partner-testimonials" class="testi-more">See more stories →</a></div>
    <div class="testi-scroll">{"".join(cards)}</div>
  </div>
  <div class="sdiv"></div>'''

def r_res(res):
    o=[]
    for k,ic,tt,ds in [("recording_url","📹","Meeting Recording","Watch the full conversation"),("calendar_url","📅","Book Your Next Session","Pick a time that works for you")]:
        u=res.get(k)
        if u: o.append(f'<a href="{e(u)}" class="rl"><span class="ri">{ic}</span><div><div class="rt">{tt}</div><div class="rd">{ds}</div></div><span class="ra">→</span></a>')
    return "\n".join(o)

def generate_html(data):
    mt=data.get("meeting_title","Meeting Summary")
    md=data.get("meeting_date",datetime.now().strftime("%B %d, %Y"))
    dur=data.get("meeting_duration","")
    mtype=data.get("meeting_type","Meeting")
    co=data.get("company_name","")
    summ=data.get("executive_summary","")
    parts=data.get("participants",[])
    dps=data.get("discussion_points",[])
    demos=data.get("demo_highlights",[])
    steps=data.get("next_steps",[])
    res=data.get("resources",{})
    nc=len(dps); gc="g2" if nc<=2 else "g3" if nc==3 else "g2"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{e(mt)}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:{N0};color:{N9};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.65;padding:0;-webkit-font-smoothing:antialiased}}

/* ── HEADER — full-width hero ── */
.hero{{
  background:linear-gradient(160deg,{N9} 0%,{N8} 40%,{N7} 100%);
  color:{W};padding:0;position:relative;overflow:hidden;
}}
.hero::before{{content:'';position:absolute;top:-120px;right:-60px;width:500px;height:500px;background:radial-gradient(circle,rgba(77,101,255,.12) 0%,transparent 65%);border-radius:50%}}
.hero::after{{content:'';position:absolute;bottom:-100px;left:10%;width:400px;height:400px;background:radial-gradient(circle,rgba(255,211,16,.06) 0%,transparent 65%);border-radius:50%}}
.hero-bar{{height:5px;background:linear-gradient(90deg,{B} 0%,{G} 50%,{B} 100%)}}
.hero-inner{{max-width:1320px;margin:0 auto;padding:56px 72px 52px;position:relative;z-index:1}}
.hero-logo{{height:36px;margin-bottom:32px;display:block}}
.hero-type{{
  display:inline-block;background:{B};color:{W};
  font-size:13px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  padding:8px 20px;border-radius:8px;margin-bottom:20px;
}}
.hero h1{{font-size:44px;font-weight:800;line-height:1.15;margin-bottom:12px;max-width:900px}}
.hero .sub{{font-size:17px;color:rgba(255,255,255,.6);max-width:700px}}
.hero-meta{{display:flex;gap:32px;margin-top:32px;flex-wrap:wrap}}
.hero-mi{{display:flex;align-items:center;gap:8px;font-size:14px;color:rgba(255,255,255,.5)}}
.hero-mi strong{{color:{W};font-weight:600}}
.hero-mi .dot{{width:6px;height:6px;border-radius:50%;background:{G};flex-shrink:0}}
.hero-gold{{height:4px;background:linear-gradient(90deg,{G},transparent 80%)}}

/* ── MAIN ── */
.main{{max-width:1320px;margin:0 auto;padding:56px 72px 40px}}

/* ── Sections ── */
.sec{{margin-bottom:48px}}
.sh{{margin-bottom:24px}}
.sh h2{{font-size:22px;font-weight:700;color:{N9};display:flex;align-items:center;gap:10px}}
.sdiv{{height:2px;background:linear-gradient(90deg,{B20} 0%,{G20} 40%,transparent 100%);margin-bottom:48px;border-radius:2px}}

/* ── Participants ── */
.ppl{{display:flex;flex-wrap:wrap;gap:14px}}
.person{{display:flex;align-items:center;gap:12px;background:{W};border:1px solid {N2};border-radius:14px;padding:12px 20px 12px 12px;box-shadow:0 1px 3px rgba(0,0,0,.03)}}
.av{{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;flex-shrink:0}}
.av-img{{width:42px;height:42px;border-radius:50%;object-fit:cover;border:2.5px solid {G};flex-shrink:0}}
.pn{{font-size:15px;font-weight:600}}
.pr{{font-size:12px;color:{N5}}}

/* ── Summary ── */
.sbox{{
  background:linear-gradient(135deg,{B10} 0%,{G10} 100%);
  border-left:5px solid {B};border-radius:0 16px 16px 0;
  padding:28px 34px;font-size:16px;line-height:1.8;color:{N7};
}}

/* ── Cards ── */
.grid{{display:grid;gap:20px}}
.g2{{grid-template-columns:repeat(auto-fit,minmax(360px,1fr))}}
.g3{{grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}}
.crd{{border-radius:16px;padding:26px;border:1px solid transparent}}
.crd-h{{display:flex;align-items:center;gap:10px;margin-bottom:16px}}
.crd-i{{font-size:22px}}
.crd-t{{font-size:17px;font-weight:700}}
.crd ul{{list-style:none;padding:0}}
.crd li{{font-size:14px;padding:7px 0 7px 20px;position:relative;border-bottom:1px solid rgba(0,0,0,.04)}}
.crd li:last-child{{border-bottom:none}}
.crd li::before{{content:'›';position:absolute;left:4px;color:{N5};font-weight:700;font-size:15px}}

/* ── Demo ── */
.dt{{width:100%;border-collapse:collapse;background:{W};border:1px solid {N2};border-radius:16px;overflow:hidden}}
.dt tr{{border-bottom:1px solid {N2}}}
.dt tr:last-child{{border-bottom:none}}
.dt td{{padding:18px 24px;font-size:15px;vertical-align:top}}
.dt .ft{{font-weight:700;color:{B};white-space:nowrap;width:220px}}

/* ── Steps ── */
.st{{width:100%;border-collapse:collapse}}
.st thead th{{background:{B10};text-align:left;padding:14px 20px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:{B};border-bottom:3px solid {B20}}}
.st thead th:first-child{{border-radius:16px 0 0 0}}.st thead th:last-child{{border-radius:0 16px 0 0}}
.st tbody tr{{border-bottom:1px solid {N2};transition:background .15s}}
.st tbody tr:last-child{{border-bottom:none}}
.st tbody tr:hover{{background:{B10}}}
.st tbody td{{padding:16px 20px;font-size:15px;vertical-align:middle}}
.act{{font-weight:500}}
.pill{{display:inline-block;padding:5px 16px;border-radius:20px;font-size:12px;font-weight:700;white-space:nowrap}}
.opill{{display:inline-block;padding:5px 16px;border-radius:20px;font-size:12px;font-weight:600;white-space:nowrap}}

/* ── Testimonials ── */
.testi-sec{{margin-bottom:48px}}
.testi-hdr{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.testi-hdr h2{{font-size:22px;font-weight:700;color:{N9};display:flex;align-items:center;gap:10px}}
.testi-more{{font-size:14px;font-weight:600;color:{B};text-decoration:none;display:flex;align-items:center;gap:6px;transition:color .2s}}
.testi-more:hover{{color:{BD}}}
.testi-scroll{{display:flex;gap:20px;overflow-x:auto;padding-bottom:16px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}}
.testi-scroll::-webkit-scrollbar{{height:6px}}
.testi-scroll::-webkit-scrollbar-track{{background:{N1};border-radius:3px}}
.testi-scroll::-webkit-scrollbar-thumb{{background:{B30};border-radius:3px}}
.testi-scroll::-webkit-scrollbar-thumb:hover{{background:{B}}}
.tc{{flex:0 0 340px;scroll-snap-align:start;background:{W};border:1.5px solid {N2};border-radius:18px;padding:28px;display:flex;flex-direction:column;justify-content:space-between;transition:all .2s;position:relative}}
.tc:hover{{border-color:{B20};box-shadow:0 6px 24px rgba(77,101,255,.08);transform:translateY(-2px)}}
.tc::before{{content:'❝';position:absolute;top:16px;right:22px;font-size:36px;color:{B20};line-height:1}}
.tc-q{{font-size:15px;line-height:1.7;color:{N7};flex:1;margin-bottom:20px;font-style:italic}}
.tc-ft{{display:flex;align-items:center;gap:12px;border-top:1px solid {N1};padding-top:16px}}
.tc-av{{width:38px;height:38px;border-radius:50%;background:{B};color:{W};display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}}
.tc-nm{{font-size:14px;font-weight:600;color:{N9}}}
.tc-rl{{font-size:12px;color:{N5}}}

/* ── Resources ── */
.rg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}}
.rl{{display:flex;align-items:center;gap:16px;padding:20px 24px;background:{W};border:2px solid {N2};border-radius:16px;text-decoration:none;color:{N9};transition:all .2s}}
.rl:hover{{border-color:{B};background:{B10};box-shadow:0 4px 16px rgba(77,101,255,.1);transform:translateY(-2px)}}
.ri{{font-size:28px;flex-shrink:0}}
.rt{{font-size:16px;font-weight:600}}
.rd{{font-size:13px;color:{N5}}}
.ra{{margin-left:auto;color:{B};font-size:22px;font-weight:700}}
.tz{{margin-top:16px;padding:16px 20px;background:{G10};border:1.5px solid {G20};border-radius:12px;font-size:13px;color:{N7}}}

/* ── Footer ── */
.ftr{{background:{N9};padding:48px 72px 40px;position:relative}}
.ftr::before{{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,{G} 0%,{B} 100%)}}
.ftr-in{{max-width:1320px;margin:0 auto;text-align:center}}
.ftr-logo{{height:38px;margin-bottom:16px}}
.ftr-tag{{font-size:15px;color:rgba(255,255,255,.45);margin-bottom:24px}}
.ftr-lnk{{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;align-items:center}}
.ftr-a{{font-size:14px;color:rgba(255,255,255,.4);text-decoration:none;padding:6px 14px;border-radius:8px;transition:all .2s}}
.ftr-a:hover{{color:{G};background:rgba(255,211,16,.08)}}
.ftr-d{{color:rgba(255,255,255,.12);font-size:10px}}
.ftr-c{{margin-top:28px;padding-top:20px;border-top:1px solid rgba(255,255,255,.05);font-size:12px;color:rgba(255,255,255,.2)}}

/* ── Prevent horizontal overflow globally ── */
html,body{{overflow-x:hidden;width:100%}}

@media(max-width:800px){{
  /* Hero */
  .hero-inner{{padding:32px 20px 28px}}
  .hero-logo{{height:28px;margin-bottom:20px}}
  .hero-type{{font-size:11px;padding:6px 14px;margin-bottom:14px}}
  .hero h1{{font-size:24px;line-height:1.25}}
  .hero .sub{{font-size:14px}}
  .hero-meta{{gap:12px 24px;margin-top:20px}}
  .hero-mi{{font-size:12px}}
  .hero::before{{width:200px;height:200px;top:-80px;right:-60px}}
  .hero::after{{width:160px;height:160px}}

  /* Main */
  .main{{padding:32px 20px 24px}}

  /* Sections */
  .sec{{margin-bottom:28px}}
  .sh h2{{font-size:18px}}
  .sdiv{{margin-bottom:28px}}

  /* Participants — stack vertically */
  .ppl{{flex-direction:column;gap:10px}}
  .person{{padding:10px 14px 10px 10px}}
  .av,.av-img{{width:36px;height:36px}}
  .pn{{font-size:14px}}
  .pr{{font-size:11px}}

  /* Summary */
  .sbox{{padding:20px;font-size:14px;line-height:1.7;border-radius:0 12px 12px 0}}

  /* Cards — single column */
  .g2,.g3{{grid-template-columns:1fr}}
  .crd{{padding:18px;border-radius:12px}}
  .crd-t{{font-size:15px}}
  .crd li{{font-size:13px;padding:6px 0 6px 18px}}

  /* Demo table — full block layout on mobile */
  .dt,.dt thead,.dt tbody,.dt tr,.dt td{{display:block;width:100%}}
  .dt{{border-radius:12px}}
  .dt tr{{padding:14px 16px;border-bottom:1px solid {N2}}}
  .dt tr:last-child{{border-bottom:none}}
  .dt td{{padding:0}}
  .dt .ft{{width:auto;white-space:normal;font-size:15px;margin-bottom:4px}}
  .dt td:last-child{{font-size:13px;color:{N5}}}

  /* Steps table — card layout on mobile */
  .st,.st thead,.st tbody,.st tr,.st td,.st th{{display:block;width:100%}}
  .st thead{{display:none}}
  .st tbody tr{{padding:14px 0;border-bottom:1px solid {N2}}}
  .st tbody tr:last-child{{border-bottom:none}}
  .st tbody td{{padding:3px 0;font-size:14px}}
  .st tbody td:first-child{{order:2;margin-top:8px}}
  .st tbody td:nth-child(2){{order:1;font-size:15px}}
  .st tbody td:last-child{{order:3;margin-top:4px}}

  /* Testimonials — swipeable cards */
  .testi-hdr{{flex-direction:column;align-items:flex-start;gap:10px}}
  .testi-scroll{{gap:14px;padding-bottom:12px;scroll-padding:0 20px}}
  .tc{{flex:0 0 280px;padding:20px;border-radius:14px}}
  .tc::before{{font-size:28px;top:12px;right:16px}}
  .tc-q{{font-size:14px;line-height:1.6;margin-bottom:16px}}
  .tc-ft{{padding-top:12px}}
  .tc-av{{width:32px;height:32px;font-size:11px}}
  .tc-nm{{font-size:13px}}
  .tc-rl{{font-size:11px}}

  /* Resources — single column */
  .rg{{grid-template-columns:1fr}}
  .rl{{padding:16px 18px;border-radius:12px;gap:12px}}
  .ri{{font-size:22px}}
  .rt{{font-size:14px}}
  .rd{{font-size:12px}}
  .ra{{font-size:18px}}
  .tz{{padding:12px 16px;font-size:12px;border-radius:10px}}

  /* Footer */
  .ftr{{padding:32px 20px 28px}}
  .ftr-logo{{height:28px;margin-bottom:12px}}
  .ftr-tag{{font-size:13px;margin-bottom:16px}}
  .ftr-lnk{{gap:6px}}
  .ftr-a{{font-size:13px;padding:5px 10px}}
  .ftr-c{{margin-top:20px;padding-top:16px;font-size:11px}}
}}

@media(max-width:400px){{
  .hero-inner{{padding:24px 14px 22px}}
  .main{{padding:24px 14px 20px}}
  .ftr{{padding:24px 14px 22px}}
  .hero h1{{font-size:20px}}
  .hero .sub{{font-size:13px}}
  .hero-meta{{gap:8px 16px}}
  .hero-mi{{font-size:11px}}
  .tc{{flex:0 0 250px;padding:16px}}
  .person{{padding:8px 10px 8px 8px}}
  .crd{{padding:16px}}
  .sbox{{padding:16px;font-size:13px}}
  .rl{{padding:14px 16px}}
}}

@media print{{body{{padding:0;background:#fff}}.hero{{break-inside:avoid}}.rl:hover{{transform:none;box-shadow:none}}}}
</style>
</head>
<body>

<!-- HEADER -->
<div class="hero">
  <div class="hero-bar"></div>
  <div class="hero-inner">
    <img src="data:image/webp;base64,{LOGO_WHITE}" alt="Boom" class="hero-logo"/>
    <div class="hero-type">{e(mtype)}</div>
    <h1>{e(mt)}</h1>
    <p class="sub">Meeting summary prepared for {e(co)}</p>
    <div class="hero-meta">
      <div class="hero-mi"><span class="dot"></span><strong>{e(md)}</strong></div>
      {"<div class='hero-mi'><span class='dot'></span><strong>"+e(dur)+"</strong></div>" if dur else ""}
      <div class="hero-mi"><span class="dot"></span><strong>{len(parts)} participants</strong></div>
    </div>
  </div>
  <div class="hero-gold"></div>
</div>

<!-- CONTENT -->
<div class="main">

  <div class="sec">
    <div class="sh"><h2>👥 Participants</h2></div>
    <div class="ppl">{r_people(parts)}</div>
  </div>
  <div class="sdiv"></div>

  <div class="sec">
    <div class="sh"><h2>📄 Summary</h2></div>
    <div class="sbox">{e(summ)}</div>
  </div>
  <div class="sdiv"></div>

  {"" if not dps else f'''<div class="sec">
    <div class="sh"><h2>💬 Key Discussion Points</h2></div>
    <div class="grid {gc}">{r_cards(dps)}</div>
  </div>
  <div class="sdiv"></div>'''}

  {r_demo(demos)}

  {"" if not steps else f'''<div class="sec">
    <div class="sh"><h2>✅ Next Steps</h2></div>
    <table class="st"><thead><tr><th>Timeline</th><th>Action</th><th>Owner</th></tr></thead>
    <tbody>{r_steps(steps)}</tbody></table>
  </div>
  <div class="sdiv"></div>'''}

  {r_testi()}

  {"" if not res else f'''<div class="sec">
    <div class="sh"><h2>🔗 Resources</h2></div>
    <div class="rg">{r_res(res)}</div>
    <div class="tz">💡 If you don't see availability that works (time zones can be tricky), just send me 2-3 windows that fit your schedule and I'll make it work on my end.</div>
  </div>'''}

</div>

<!-- FOOTER -->
<div class="ftr">
  <div class="ftr-in">
    <img src="data:image/webp;base64,{LOGO_WHITE}" alt="Boom" class="ftr-logo"/>
    <div class="ftr-tag">Property Management, Simplified</div>
    <div class="ftr-lnk">
      <a href="https://www.boomnow.com" class="ftr-a">boomnow.com</a>
      <span class="ftr-d">·</span>
      <a href="https://www.boomnow.com/partner-testimonials" class="ftr-a">Partner Stories</a>
      <span class="ftr-d">·</span>
      <a href="https://meetings.hubspot.com/idan-carmi" class="ftr-a">Book a Call</a>
    </div>
    <div class="ftr-c">Prepared by Boom · Idan Carmi, Chief Growth Officer</div>
  </div>
</div>

</body>
</html>'''


def set_photo(path):
    os.makedirs(ASSETS, exist_ok=True)
    with open(path,"rb") as f: b=base64.b64encode(f.read()).decode()
    with open(PHOTO_PATH,"w") as f: f.write(b)
    print(f"✅ Photo saved → {PHOTO_PATH}",file=sys.stderr)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--set-photo",metavar="IMG")
    g=ap.add_mutually_exclusive_group()
    g.add_argument("--json"); g.add_argument("--file")
    ap.add_argument("--output","-o")
    a=ap.parse_args()
    if a.set_photo:
        set_photo(a.set_photo)
        if not a.json and not a.file: return
    if not a.json and not a.file: ap.error("--json or --file required")
    d=json.loads(a.json) if a.json else json.load(open(a.file))
    h=generate_html(d)
    if a.output:
        with open(a.output,"w") as f: f.write(h)
        print(f"✅ Generated: {a.output}",file=sys.stderr)
    else: print(h)

if __name__=="__main__": main()
