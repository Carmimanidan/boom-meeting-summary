#!/usr/bin/env python3
"""
Boom Meeting Summary — HTML Generator v3
Boom brand only: Blue #4d65ff · Gold #ffd310 · Navy/neutrals.

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
_logos_path = os.path.join(ASSETS, "partner_logos.json")
PARTNER_LOGOS = json.load(open(_logos_path)) if os.path.exists(_logos_path) else {}

def _photo():
    return open(PHOTO_PATH).read().strip() if os.path.exists(PHOTO_PATH) else None

def e(t): return html.escape(str(t)) if t else ""
def ini(n):
    p = n.split()
    return (p[0][0]+p[-1][0]).upper() if len(p)>=2 else n[0].upper() if n else "?"

# ─── Boom palette ───
B   = "#4d65ff"
BD  = "#3a4ecc"
B10 = "#eef1ff"
B20 = "#dce1ff"
B30 = "#c5ccff"
G   = "#ffd310"
GD  = "#e6be00"
G10 = "#fffbe6"
G20 = "#fff3b3"
N9  = "#121428"
N8  = "#1e2140"
N7  = "#2e3352"
N6  = "#464b6e"
N5  = "#6b7194"
N4  = "#9398b0"
N3  = "#d0d3e0"
N2  = "#e8eaf2"
N1  = "#f4f5f9"
N0  = "#fafbfd"
W   = "#ffffff"

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

# Case studies for dynamic matching by portfolio size
CASE_STUDIES = [
    {"name":"Zzzing","props":360,"region":"UK","slug":"how-boom-helped-zzzing-scale-without-getting-slowed-down-by-tech"},
    {"name":"Perch Short Stays","props":300,"region":"UK","slug":"how-perch-short-stays-reduced-overhead-and-gained-a-competitive-edge-with-boom"},
    {"name":"Livestay","props":250,"region":"UK","slug":"how-livestay-made-busy-urban-operations-work-smarter-with-boom-automation"},
    {"name":"Nox Cape Town","props":200,"region":"South Africa","slug":"how-nox-cape-town-elevates-luxury-hospitality-with-boom-ai-tools"},
    {"name":"Housepitality","props":140,"region":"UK","slug":"how-housepitality-uses-boom-to-make-owner-and-guest-communication-a-breeze"},
    {"name":"Enjoy Unique Stays","props":110,"region":"UK","slug":"enjoy-unique-stays"},
    {"name":"Guestly Homes","props":105,"region":"Sweden","slug":"how-guestly-homes-streamlined-operations-and-scaled-with-ai-powered-hospitality"},
    {"name":"Euphoric Leisure","props":100,"region":"UK","slug":"how-euphoric-leisure-future-proofed-operations-with-ai-and-a-unified-tech-stack"},
    {"name":"Wehom.es","props":100,"region":"Hungary","slug":"how-wehom-es-used-ai-to-take-their-time-back-from-constant-calls"},
    {"name":"PureServiced","props":71,"region":"UK","slug":"how-pureserviced-made-the-leap-to-ai-powered-hospitality-with-boom"},
    {"name":"KFE Management","props":70,"region":"UK","slug":"how-kfe-management-reduced-costs-and-unlocked-new-revenue-streams-with-boom"},
]

# Partner names for the logo strip
PARTNERS = ["Zzzing","Perch Short Stays","Guestly Homes","NOX","Euphoric Leisure",
            "KFE Management","Livestay","Housepitality","PureServiced","Yalarent"]

# Blog posts for contextual linking (keyword → post)
BLOG_POSTS = [
    {"kw":["pricing","revenue","dynamic"],"title":"Smarter Pricing with Boom × Wheelhouse","url":"https://www.boomnow.com/blog/pricing-strategy-just-got-smarter-with-boom-x-wheelhouse-integration"},
    {"kw":["ai","automation","guest","communication","messaging"],"title":"Introducing BAM: The First Business Agentic Manager","url":"https://www.boomnow.com/blog/introducing-bam-the-first-ever-business-agentic-manager-for-the-short-term-rental-industry"},
    {"kw":["damage","protection","insurance"],"title":"Introducing BoomGuard: Damage Protection","url":"https://www.boomnow.com/blog/introducing-boomguard-damage-protection-built-into-your-aipms"},
    {"kw":["accounting","finance","trust","owner","payment"],"title":"Industry's First AI-Powered Trust Accounting","url":"https://www.boomnow.com/blog/introducing-the-industrys-first-fully-integrated-ai-powered-trust-accounting-system"},
    {"kw":["noise","smart home","monitor"],"title":"Real-Time Noise Management with Boom × Minut","url":"https://www.boomnow.com/blog/introducing-boom-x-minut-real-time-noise-management-without-the-manual-work"},
    {"kw":["website","direct booking","book direct"],"title":"Smarter Websites with Boom × ICND","url":"https://www.boomnow.com/blog/introducing-the-boom-x-icnd-integration-smarter-websites-smarter-operations"},
]

CAT = {
    "challenges":    {"ico":"🔍","accent":G,  "bg":"rgba(255,211,16,.06)", "bdr":"rgba(255,211,16,.25)"},
    "solutions":     {"ico":"✅","accent":B,  "bg":"rgba(77,101,255,.05)", "bdr":"rgba(77,101,255,.2)"},
    "opportunities": {"ico":"🚀","accent":B,  "bg":"rgba(77,101,255,.05)", "bdr":"rgba(77,101,255,.15)"},
    "decisions":     {"ico":"📋","accent":G,  "bg":"rgba(255,211,16,.06)", "bdr":"rgba(255,211,16,.25)"},
}

PILLS = {
    "today":{"b":"#e03e3e","f":W},"tomorrow":{"b":GD,"f":N9},
    "this week":{"b":B,"f":W},"next week":{"b":BD,"f":W},
    "ongoing":{"b":N6,"f":W},"tbd":{"b":N2,"f":N5},
}

def pstyle(tl):
    t=(tl or"TBD").strip().lower()
    for k,c in PILLS.items():
        if k in t: return f'background:{c["b"]};color:{c["f"]}'
    return f'background:{B};color:{W}'


def _match_case_study(data):
    """Find the best matching case study based on discussion content and portfolio size."""
    # Build text blob from all content
    blob = " ".join([
        data.get("executive_summary",""),
        data.get("company_name",""),
        " ".join(i for dp in data.get("discussion_points",[]) for i in dp.get("items",[])),
        " ".join(h.get("description","") for h in data.get("demo_highlights",[])),
    ]).lower()
    # Try to extract property count from content
    import re
    nums = [int(x) for x in re.findall(r'(\d+)\s*(?:properties|units|listings|apartments)', blob)]
    target = max(nums) if nums else 100
    # Sort by closest match
    ranked = sorted(CASE_STUDIES, key=lambda cs: abs(cs["props"]-target))
    # Return top 2
    return ranked[:2]

def _match_blog_posts(data):
    """Find 1-2 relevant blog posts based on discussion topics."""
    blob = " ".join([
        data.get("executive_summary",""),
        " ".join(i for dp in data.get("discussion_points",[]) for i in dp.get("items",[])),
        " ".join(h.get("feature","")+" "+h.get("description","") for h in data.get("demo_highlights",[])),
    ]).lower()
    scored = []
    for bp in BLOG_POSTS:
        hits = sum(1 for kw in bp["kw"] if kw in blob)
        if hits > 0:
            scored.append((hits, bp))
    scored.sort(key=lambda x: -x[0])
    return [s[1] for s in scored[:2]]


# ─── Renderers ───

def r_people(parts):
    ph = _photo()
    o = []
    for p in parts:
        nm=p.get("name",""); co=p.get("company",""); rl=p.get("role","")
        ib="boom" in co.lower()
        ii="idan" in nm.lower() and ib
        img=p.get("image")
        if not img and ii and ph: img=f"data:image/jpeg;base64,{ph}"
        if img:
            av=f'<img class="av-img" src="{e(img)}" alt="{e(nm)}"/>'
        elif ib:
            av=f'<div class="av av-boom">{e(ini(nm))}</div>'
        else:
            av=f'<div class="av av-ext">{e(ini(nm))}</div>'
        tag = f'<span class="ptag ptag-boom">Boom</span>' if ib else f'<span class="ptag">{e(co)}</span>' if co else ''
        o.append(f'<div class="person">{av}<div class="pinfo"><div class="pn">{e(nm)}</div><div class="pr">{e(rl)}</div>{tag}</div></div>')
    return "\n".join(o)

def r_cards(dps):
    o=[]
    for d in dps:
        c=CAT.get(d.get("category","solutions"),CAT["solutions"])
        li="\n".join(f'<li><span class="li-dot" style="background:{c["accent"]}"></span>{e(i)}</li>' for i in d.get("items",[]))
        o.append(
            f'<div class="crd" style="background:{c["bg"]};border:1.5px solid {c["bdr"]}">'
            f'<div class="crd-h"><span class="crd-i">{c["ico"]}</span>'
            f'<span class="crd-t">{e(d.get("title",""))}</span></div>'
            f'<ul>{li}</ul></div>')
    return "\n".join(o)

def r_demo(hl, is_prospect=False):
    if not hl: return ""
    rows=[]
    for i,h in enumerate(hl):
        desc = h.get("benefit") or h.get("description","")
        rows.append(
            f'<div class="demo-row">'
            f'<div class="demo-num">{i+1:02d}</div>'
            f'<div class="demo-body"><div class="demo-feat">{e(h.get("feature",""))}</div>'
            f'<div class="demo-desc">{e(desc)}</div></div></div>')
    feat_title = "What Boom Can Do for You" if is_prospect else "Features We Explored Together"
    bam_intro = "Everything on this page is powered by" if is_prospect else "Everything you saw today runs on"
    return (f'<div class="sec"><div class="sec-label">WHAT THIS MEANS FOR YOU</div>'
            f'<h2 class="sec-title">{feat_title}</h2>'
            f'<div class="demo-list">{"".join(rows)}</div>'
            f'<div class="bam-callout">'
            f'<div class="bam-icon">🤖</div>'
            f'<div class="bam-body">'
            f'<div class="bam-title">Powered by BAM — Your AI Operations Manager</div>'
            f'<div class="bam-desc">{bam_intro} BAM (Business Agentic Manager) — '
            f'think of it as ChatGPT for your property management business. BAM doesn\'t just automate tasks, '
            f'it makes decisions, learns your preferences, and runs your day-to-day operations autonomously.</div>'
            f'<a href="https://www.boomnow.com/blog/introducing-bam-the-first-ever-business-agentic-manager-for-the-short-term-rental-industry" class="bam-link">Learn more about BAM →</a>'
            f'</div></div></div>')

def r_steps(steps):
    rows=[]
    for i,s in enumerate(steps):
        ow=s.get("owner",""); ib="boom" in ow.lower() or "idan" in ow.lower()
        oc = "opill-boom" if ib else "opill-ext"
        rows.append(
            f'<div class="step-row">'
            f'<div class="step-check"><svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="9" stroke="{B}" stroke-width="1.5" opacity=".3"/></svg></div>'
            f'<div class="step-body"><div class="step-act">{e(s.get("action",""))}</div>'
            f'<div class="step-meta"><span class="pill" style="{pstyle(s.get("timeline",""))}">{e(s.get("timeline","TBD"))}</span>'
            f'<span class="opill {oc}">{e(ow)}</span></div></div></div>')
    return "\n".join(rows)

def r_logos():
    """Render partner name strip — animated scroll."""
    names = "".join(f'<span class="plogo-name">{e(p)}</span><span class="plogo-dot">·</span>' for p in PARTNERS)
    return f'''<div class="plogo-sec">
    <div class="plogo-inner">
      <div class="plogo-label">TRUSTED BY LEADING PROPERTY MANAGERS</div>
      <div class="plogo-strip"><div class="plogo-track">{names}{names}</div></div>
    </div>
  </div>'''

def r_testi():
    cards=[]
    for t in TESTIMONIALS:
        cards.append(
            f'<div class="tc">'
            f'<div class="tc-stars">★★★★★</div>'
            f'<div class="tc-q">"{e(t["q"])}"</div>'
            f'<div class="tc-ft"><div class="tc-av">{e(ini(t["n"]))}</div>'
            f'<div><div class="tc-nm">{e(t["n"])}</div>'
            f'<div class="tc-rl">{e(t["r"])} · {e(t["c"])}</div></div></div></div>')
    return f'''<div class="testi-wrap">
    <div class="testi-inner">
      <div class="testi-badge">TRUSTED BY PROPERTY MANAGERS IN 30+ COUNTRIES</div>
      <h2 class="testi-title">What Our Partners Say</h2>
      <p class="testi-sub">Hear from property managers who transformed their business with Boom</p>
      <div class="testi-scroll">{"".join(cards)}</div>
      <div class="testi-cta"><a href="https://www.boomnow.com/partner-testimonials" class="btn-testi">See all partner stories <span>→</span></a></div>
    </div>
  </div>'''

def r_case_studies(data):
    matches = _match_case_study(data)
    if not matches: return ""
    cards = []
    for cs in matches:
        url = f'https://www.boomnow.com/case-studies/{cs["slug"]}'
        cards.append(
            f'<a href="{e(url)}" class="cs-card">'
            f'<div class="cs-tag">CASE STUDY</div>'
            f'<div class="cs-name">{e(cs["name"])}</div>'
            f'<div class="cs-meta">{cs["props"]} properties · {e(cs["region"])}</div>'
            f'<div class="cs-link">Read the full story →</div></a>')
    return f'''<div class="sec">
    <div class="sec-label">SIMILAR TO YOU</div>
    <h2 class="sec-title">See How Others Made the Switch</h2>
    <div class="cs-grid">{"".join(cards)}</div></div>
    <div class="divider"></div>'''

def r_blog(data):
    posts = _match_blog_posts(data)
    if not posts: return ""
    items = []
    for bp in posts:
        items.append(
            f'<a href="{e(bp["url"])}" class="blog-card">'
            f'<div class="blog-ico">📖</div>'
            f'<div class="blog-body"><div class="blog-title">{e(bp["title"])}</div>'
            f'<div class="blog-link">Read on our blog →</div></div></a>')
    return "\n".join(items)

def r_res(res, is_prospect=False):
    items=[]
    cal_title = "Book a Discovery Call" if is_prospect else "Book Your Next Session"
    cal_desc = "Let's explore what Boom can do for your business — pick a time" if is_prospect else "Pick a time — or reply with 2-3 slots that work for you"
    for k,ic,tt,ds in [("recording_url","📹","Meeting Recording","Watch the full conversation"),("calendar_url","📅",cal_title,cal_desc)]:
        u=res.get(k)
        if u: items.append(f'<a href="{e(u)}" class="res-card"><div class="res-ico">{ic}</div><div class="res-body"><div class="res-title">{tt}</div><div class="res-desc">{ds}</div></div><div class="res-arrow">→</div></a>')
    return "\n".join(items)


def generate_html(data):
    is_prospect = data.get("page_type") == "prospect_overview"
    mt   = data.get("meeting_title","Meeting Summary")
    md   = data.get("meeting_date",datetime.now().strftime("%B %d, %Y"))
    dur  = data.get("meeting_duration","")
    mtype= data.get("meeting_type","Meeting")
    co   = data.get("company_name","")
    summ = data.get("executive_summary","")
    takeaway = data.get("key_takeaway","")
    bullets = data.get("summary_bullets",[])
    parts= data.get("participants",[])
    dps  = data.get("discussion_points",[])
    demos= data.get("demo_highlights",[])
    steps= data.get("next_steps",[])
    res  = data.get("resources",{})
    nc   = len(dps)
    gc   = "g2" if nc<=2 else "g3" if nc==3 else "g2"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{e(mt)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"/>
<style>
/* ── RESET ── */
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{overflow-x:hidden;width:100%}}
body{{
  background:{N1};color:{N9};
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  line-height:1.6;-webkit-font-smoothing:antialiased;
}}

/* ════════════════════════════════════════
   HERO
   ════════════════════════════════════════ */
.hero{{
  background:{N9};color:{W};
  position:relative;overflow:hidden;padding:0;
}}
.hero::before{{
  content:'';position:absolute;width:700px;height:700px;
  top:-300px;right:-150px;border-radius:50%;
  background:radial-gradient(circle,rgba(77,101,255,.15) 0%,transparent 60%);
}}
.hero::after{{
  content:'';position:absolute;width:500px;height:500px;
  bottom:-200px;left:-100px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,211,16,.08) 0%,transparent 60%);
}}
.hero-accent{{height:4px;background:linear-gradient(90deg,{B},{G},{B})}}
.hero-inner{{
  max-width:1100px;margin:0 auto;padding:60px 56px 56px;
  position:relative;z-index:1;
}}
.hero-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:40px}}
.hero-logo{{height:32px;display:block;opacity:.9}}
.hero-badge{{
  font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  color:{G};border:1.5px solid rgba(255,211,16,.25);
  padding:6px 18px;border-radius:100px;background:rgba(255,211,16,.06);
}}
.hero h1{{
  font-size:42px;font-weight:900;line-height:1.1;
  margin-bottom:16px;letter-spacing:-.5px;
  background:linear-gradient(135deg,{W} 60%,{B30} 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.hero-sub{{font-size:17px;color:rgba(255,255,255,.5);margin-bottom:36px}}
.hero-pills{{display:flex;gap:12px;flex-wrap:wrap}}
.hero-pill{{
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);
  padding:10px 20px;border-radius:12px;
  font-size:13px;color:rgba(255,255,255,.6);
  backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);
}}
.hero-pill strong{{color:{W};font-weight:600}}
.hero-pill-dot{{width:5px;height:5px;border-radius:50%;background:{G};flex-shrink:0}}
.hero-wave{{height:48px;background:{N1};position:relative;z-index:2;border-radius:24px 24px 0 0;margin-top:-24px}}

/* ════════════════════════════════════════
   STATS BAR — floating credibility strip
   ════════════════════════════════════════ */
.stats-bar{{
  max-width:1100px;margin:-28px auto 0;padding:0 56px;position:relative;z-index:3;
}}
.stats-inner{{
  display:flex;align-items:stretch;
  background:{W};border-radius:24px;
  box-shadow:0 8px 32px rgba(18,20,40,.08),0 1px 2px rgba(18,20,40,.04);
  overflow:hidden;
}}
.stat{{
  flex:1;padding:28px 24px;display:flex;align-items:center;gap:16px;
  position:relative;
}}
.stat:not(:last-child)::after{{
  content:'';position:absolute;right:0;top:24%;height:52%;width:1px;
  background:linear-gradient(180deg,transparent,{N2},{N3},{N2},transparent);
}}
.stat-icon{{
  width:48px;height:48px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  font-size:22px;flex-shrink:0;
}}
.stat-icon-blue{{background:{B10}}}
.stat-icon-gold{{background:{G10}}}
.stat-content{{min-width:0}}
.stat-num{{font-size:24px;font-weight:900;color:{N9};letter-spacing:-.5px;line-height:1.1}}
.stat-num span{{color:{B}}}
.stat-label{{font-size:11px;font-weight:600;color:{N5};margin-top:3px;line-height:1.3}}

/* ════════════════════════════════════════
   MAIN CONTENT
   ════════════════════════════════════════ */
.main{{max-width:1100px;margin:0 auto;padding:48px 56px 32px}}
.sec{{margin-bottom:56px}}
.sec-label{{
  font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
  color:{B};margin-bottom:8px;
}}
.sec-title{{font-size:26px;font-weight:800;color:{N9};margin-bottom:24px;letter-spacing:-.3px}}
.divider{{height:1px;margin:0 0 56px;background:linear-gradient(90deg,{N3},transparent 70%)}}

/* ── Participants ── */
.ppl{{display:flex;flex-wrap:wrap;gap:12px}}
.person{{
  display:flex;align-items:center;gap:14px;
  background:{W};border:1px solid {N2};border-radius:16px;
  padding:14px 22px 14px 14px;transition:all .2s;
}}
.person:hover{{border-color:{B20};box-shadow:0 4px 16px rgba(77,101,255,.06)}}
.av{{
  width:44px;height:44px;border-radius:14px;
  display:flex;align-items:center;justify-content:center;
  font-size:15px;font-weight:700;flex-shrink:0;
}}
.av-boom{{background:{B};color:{W}}}
.av-ext{{background:{B10};color:{B}}}
.av-img{{width:44px;height:44px;border-radius:14px;object-fit:cover;flex-shrink:0;border:2px solid {G}}}
.pinfo{{min-width:0}}
.pn{{font-size:14px;font-weight:700;color:{N9}}}
.pr{{font-size:12px;color:{N5};margin-top:1px}}
.ptag{{
  display:inline-block;margin-top:4px;
  font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;
  padding:2px 8px;border-radius:6px;background:{N1};color:{N5};
}}
.ptag-boom{{background:rgba(77,101,255,.1);color:{B}}}

/* ── Key Takeaway ── */
.takeaway{{
  background:linear-gradient(135deg,{N9} 0%,{N8} 100%);
  border-radius:20px;padding:32px 36px;position:relative;overflow:hidden;
  margin-bottom:24px;
}}
.takeaway::before{{
  content:'';position:absolute;left:0;top:0;bottom:0;width:5px;
  background:linear-gradient(180deg,{G},{B});
}}
.takeaway::after{{
  content:'';position:absolute;top:-60px;right:-40px;width:200px;height:200px;
  background:radial-gradient(circle,rgba(77,101,255,.1) 0%,transparent 60%);border-radius:50%;
}}
.takeaway-label{{font-size:10px;font-weight:800;letter-spacing:2px;color:{G};text-transform:uppercase;margin-bottom:10px;position:relative;z-index:1}}
.takeaway-text{{font-size:18px;font-weight:700;color:{W};line-height:1.5;position:relative;z-index:1}}

/* ── Summary Bullets ── */
.sbullets{{display:flex;flex-direction:column;gap:12px}}
.sbullet{{
  display:flex;align-items:flex-start;gap:14px;
  background:{W};border:1px solid {N2};border-radius:16px;
  padding:18px 22px;font-size:14px;color:{N7};line-height:1.7;
}}
.sbullet-num{{
  width:28px;height:28px;border-radius:8px;
  background:{B10};color:{B};
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:800;flex-shrink:0;
}}

/* ── Summary (fallback for no bullets) ── */
.sbox{{
  background:{W};border-radius:20px;padding:32px 36px;
  font-size:15px;line-height:1.85;color:{N7};
  border:1px solid {N2};position:relative;
  box-shadow:0 1px 3px rgba(0,0,0,.02);
}}
.sbox::before{{
  content:'';position:absolute;left:0;top:20px;bottom:20px;width:4px;
  background:linear-gradient(180deg,{B},{G});border-radius:0 4px 4px 0;
}}

/* ── Discussion Cards ── */
.grid{{display:grid;gap:16px}}
.g2{{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}}
.g3{{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.crd{{border-radius:20px;padding:28px;transition:all .2s}}
.crd:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.04)}}
.crd-h{{display:flex;align-items:center;gap:10px;margin-bottom:18px}}
.crd-i{{font-size:20px}}
.crd-t{{font-size:16px;font-weight:800;color:{N9}}}
.crd ul{{list-style:none}}
.crd li{{
  display:flex;align-items:flex-start;gap:12px;
  font-size:14px;color:{N7};padding:8px 0;
  border-bottom:1px solid rgba(0,0,0,.04);line-height:1.6;
}}
.crd li:last-child{{border-bottom:none}}
.li-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0;margin-top:8px}}

/* ── Demo Highlights ── */
.demo-list{{display:flex;flex-direction:column;gap:0}}
.demo-row{{
  display:flex;align-items:flex-start;gap:20px;
  padding:22px 28px;background:{W};
  border:1px solid {N2};border-bottom:none;transition:background .15s;
}}
.demo-row:first-child{{border-radius:20px 20px 0 0}}
.demo-row:last-child{{border-radius:0 0 20px 20px;border-bottom:1px solid {N2}}}
.demo-row:only-child{{border-radius:20px;border-bottom:1px solid {N2}}}
.demo-row:hover{{background:{B10}}}
.demo-num{{
  font-size:13px;font-weight:800;color:{B};
  width:36px;height:36px;display:flex;align-items:center;justify-content:center;
  background:{B10};border-radius:10px;flex-shrink:0;
}}
.demo-body{{flex:1;min-width:0}}
.demo-feat{{font-size:15px;font-weight:700;color:{N9};margin-bottom:4px}}
.demo-desc{{font-size:14px;color:{N5};line-height:1.6}}

/* ── BAM Callout ── */
.bam-callout{{
  margin-top:20px;display:flex;gap:20px;align-items:flex-start;
  padding:28px 32px;border-radius:20px;
  background:linear-gradient(135deg,rgba(77,101,255,.04) 0%,rgba(255,211,16,.04) 100%);
  border:1.5px solid rgba(77,101,255,.12);
}}
.bam-icon{{font-size:28px;flex-shrink:0;margin-top:2px}}
.bam-body{{flex:1;min-width:0}}
.bam-title{{font-size:16px;font-weight:800;color:{N9};margin-bottom:6px}}
.bam-desc{{font-size:14px;color:{N5};line-height:1.7;margin-bottom:10px}}
.bam-link{{
  font-size:13px;font-weight:700;color:{B};text-decoration:none;
  display:inline-flex;align-items:center;gap:4px;transition:gap .2s;
}}
.bam-link:hover{{gap:8px}}

/* ── Next Steps ── */
.step-list{{display:flex;flex-direction:column;gap:0}}
.step-row{{
  display:flex;align-items:flex-start;gap:16px;
  padding:20px 28px;background:{W};
  border:1px solid {N2};border-bottom:none;transition:background .15s;
}}
.step-row:first-child{{border-radius:20px 20px 0 0}}
.step-row:last-child{{border-radius:0 0 20px 20px;border-bottom:1px solid {N2}}}
.step-row:only-child{{border-radius:20px;border-bottom:1px solid {N2}}}
.step-row:hover{{background:{N0}}}
.step-check{{flex-shrink:0;padding-top:2px}}
.step-body{{flex:1;min-width:0}}
.step-act{{font-size:15px;font-weight:600;color:{N9};margin-bottom:8px;line-height:1.5}}
.step-meta{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.pill{{display:inline-block;padding:4px 14px;border-radius:8px;font-size:11px;font-weight:700;white-space:nowrap;letter-spacing:.3px}}
.opill{{display:inline-block;padding:4px 14px;border-radius:8px;font-size:11px;font-weight:600;white-space:nowrap}}
.opill-boom{{background:{B10};color:{B}}}
.opill-ext{{background:{N1};color:{N5}}}

/* ── CTA Banner ── */
.cta-banner{{
  background:linear-gradient(135deg,{B} 0%,{BD} 100%);
  border-radius:24px;padding:40px 44px;
  display:flex;align-items:center;justify-content:space-between;gap:24px;
  margin-bottom:56px;position:relative;overflow:hidden;
}}
.cta-banner::before{{
  content:'';position:absolute;top:-50px;right:-30px;width:200px;height:200px;
  background:radial-gradient(circle,rgba(255,211,16,.15) 0%,transparent 60%);border-radius:50%;
}}
.cta-body{{position:relative;z-index:1}}
.cta-title{{font-size:22px;font-weight:800;color:{W};margin-bottom:6px}}
.cta-desc{{font-size:14px;color:rgba(255,255,255,.65)}}
.cta-btn{{
  display:inline-flex;align-items:center;gap:10px;
  background:{W};color:{B};font-size:15px;font-weight:800;
  padding:14px 32px;border-radius:14px;text-decoration:none;
  transition:all .2s;flex-shrink:0;position:relative;z-index:1;
  box-shadow:0 4px 16px rgba(0,0,0,.15);
}}
.cta-btn:hover{{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.2)}}
.cta-btn span{{transition:transform .2s}}
.cta-btn:hover span{{transform:translateX(4px)}}

/* ── Case Studies ── */
.cs-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}
.cs-card{{
  display:flex;flex-direction:column;gap:8px;
  padding:28px;background:{W};border:1.5px solid {N2};border-radius:20px;
  text-decoration:none;color:{N9};transition:all .2s;
}}
.cs-card:hover{{border-color:{B};box-shadow:0 6px 24px rgba(77,101,255,.08);transform:translateY(-2px)}}
.cs-tag{{
  font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase;
  color:{B};background:{B10};padding:4px 10px;border-radius:6px;
  display:inline-block;width:fit-content;
}}
.cs-name{{font-size:18px;font-weight:800;color:{N9};margin-top:4px}}
.cs-meta{{font-size:13px;color:{N5}}}
.cs-link{{font-size:13px;font-weight:700;color:{B};margin-top:4px;transition:letter-spacing .2s}}
.cs-card:hover .cs-link{{letter-spacing:.5px}}

/* ════════════════════════════════════════
   TESTIMONIALS
   ════════════════════════════════════════ */
.testi-wrap{{
  background:linear-gradient(170deg,{N9} 0%,{N8} 100%);
  position:relative;overflow:hidden;padding:72px 0 64px;margin-top:24px;
}}
.testi-wrap::before{{
  content:'';position:absolute;width:500px;height:500px;
  top:-200px;right:-100px;border-radius:50%;
  background:radial-gradient(circle,rgba(77,101,255,.12) 0%,transparent 60%);
}}
.testi-inner{{max-width:1100px;margin:0 auto;padding:0 56px;position:relative;z-index:1}}

/* ── Partner Logo Strip — light section ── */
.plogo-sec{{
  background:{W};border-top:1px solid {N2};border-bottom:1px solid {N2};
  padding:40px 0;
}}
.plogo-inner{{max-width:1100px;margin:0 auto;padding:0 56px;text-align:center}}
.plogo-label{{
  font-size:10px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;
  color:{N4};margin-bottom:28px;
}}
.plogo-strip{{
  overflow:hidden;position:relative;
  mask-image:linear-gradient(90deg,transparent 0%,black 8%,black 92%,transparent 100%);
  -webkit-mask-image:linear-gradient(90deg,transparent 0%,black 8%,black 92%,transparent 100%);
}}
.plogo-track{{
  display:flex;align-items:center;gap:20px;
  animation:scroll-logos 40s linear infinite;
}}
@keyframes scroll-logos{{
  0%{{transform:translateX(0)}}
  100%{{transform:translateX(-50%)}}
}}
.plogo-name{{
  font-size:15px;font-weight:700;color:{N5};white-space:nowrap;
  letter-spacing:1px;text-transform:uppercase;flex-shrink:0;
}}
.plogo-dot{{color:{N3};font-size:18px;flex-shrink:0}}

.testi-badge{{
  display:inline-block;font-size:10px;font-weight:800;letter-spacing:2.5px;
  color:{G};opacity:.7;margin-bottom:12px;
}}
.testi-title{{font-size:32px;font-weight:900;color:{W};margin-bottom:8px;letter-spacing:-.3px}}
.testi-sub{{font-size:15px;color:rgba(255,255,255,.4);margin-bottom:36px;max-width:460px;line-height:1.5}}
.testi-scroll{{
  display:flex;gap:20px;overflow-x:auto;padding-bottom:16px;
  scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;
}}
.testi-scroll::-webkit-scrollbar{{height:4px}}
.testi-scroll::-webkit-scrollbar-track{{background:rgba(255,255,255,.04);border-radius:2px}}
.testi-scroll::-webkit-scrollbar-thumb{{background:rgba(77,101,255,.3);border-radius:2px}}
.tc{{
  flex:0 0 320px;scroll-snap-align:start;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.07);border-radius:20px;
  padding:28px;display:flex;flex-direction:column;transition:all .25s;
}}
.tc:hover{{
  background:rgba(255,255,255,.07);border-color:rgba(77,101,255,.25);
  transform:translateY(-3px);box-shadow:0 16px 48px rgba(0,0,0,.25);
}}
.tc-stars{{font-size:13px;color:{G};letter-spacing:3px;margin-bottom:16px}}
.tc-q{{font-size:14px;line-height:1.8;color:rgba(255,255,255,.65);flex:1;margin-bottom:24px}}
.tc-ft{{display:flex;align-items:center;gap:12px;padding-top:16px;border-top:1px solid rgba(255,255,255,.06)}}
.tc-av{{
  width:36px;height:36px;border-radius:10px;
  background:linear-gradient(135deg,{B},{BD});color:{W};
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:700;flex-shrink:0;
}}
.tc-nm{{font-size:13px;font-weight:700;color:rgba(255,255,255,.85)}}
.tc-rl{{font-size:11px;color:rgba(255,255,255,.35);margin-top:1px}}
.testi-cta{{margin-top:32px}}
.btn-testi{{
  display:inline-flex;align-items:center;gap:8px;
  font-size:13px;font-weight:700;color:rgba(255,255,255,.5);
  text-decoration:none;padding:10px 0;
  border-bottom:1px solid rgba(255,255,255,.1);transition:all .2s;
}}
.btn-testi:hover{{color:{G};border-color:{G}}}
.btn-testi span{{transition:transform .2s}}
.btn-testi:hover span{{transform:translateX(4px)}}

/* ── Resources ── */
.res-sec{{max-width:1100px;margin:0 auto;padding:56px 56px 32px}}
.res-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:20px}}
.res-g2{{grid-template-columns:repeat(2,1fr)}}
.res-card,.blog-card{{
  display:flex;align-items:center;gap:16px;
  padding:22px 24px;background:{W};
  border:1.5px solid {N2};border-radius:16px;
  text-decoration:none;color:{N9};transition:all .2s;
}}
.res-card:hover,.blog-card:hover{{border-color:{B};box-shadow:0 4px 20px rgba(77,101,255,.08);transform:translateY(-2px)}}
.res-ico,.blog-ico{{font-size:28px;flex-shrink:0}}
.res-body,.blog-body{{flex:1;min-width:0}}
.res-title,.blog-title{{font-size:15px;font-weight:700}}
.res-desc{{font-size:12px;color:{N5};margin-top:2px}}
.blog-link{{font-size:12px;color:{B};font-weight:600;margin-top:2px}}
.res-arrow{{color:{B};font-size:20px;font-weight:700;opacity:.5;transition:opacity .2s}}
.res-card:hover .res-arrow{{opacity:1}}

/* ════════════════════════════════════════
   FOOTER
   ════════════════════════════════════════ */
.ftr{{background:{N9};padding:40px 56px 36px;position:relative}}
.ftr::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,{B},{G},{B})}}
.ftr-in{{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px}}
.ftr-left{{display:flex;align-items:center;gap:16px}}
.ftr-logo{{height:24px;opacity:.6}}
.ftr-tag{{font-size:12px;color:rgba(255,255,255,.25)}}
.ftr-right{{display:flex;flex-direction:column;align-items:flex-end;gap:8px}}
.ftr-links{{display:flex;gap:8px;align-items:center}}
.ftr-a{{
  font-size:12px;color:rgba(255,255,255,.3);text-decoration:none;
  padding:6px 12px;border-radius:8px;transition:all .15s;
}}
.ftr-a:hover{{color:{G};background:rgba(255,211,16,.06)}}
.ftr-sep{{color:rgba(255,255,255,.1);font-size:10px}}
.ftr-trust{{display:flex;gap:12px;align-items:center}}
.ftr-badge{{
  font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;
  color:rgba(255,255,255,.25);border:1px solid rgba(255,255,255,.08);
  padding:4px 10px;border-radius:6px;
}}

/* ════════════════════════════════════════
   MOBILE — 800px
   ════════════════════════════════════════ */
@media(max-width:800px){{
  .hero-inner{{padding:40px 24px 36px}}
  .hero-top{{flex-direction:column;gap:16px;margin-bottom:28px}}
  .hero-logo{{height:28px}}
  .hero h1{{font-size:28px}}
  .hero-sub{{font-size:15px;margin-bottom:24px}}
  .hero-pills{{gap:8px}}
  .hero-pill{{padding:8px 14px;font-size:12px}}
  .hero::before{{width:400px;height:400px;top:-200px;right:-100px}}
  .hero::after{{width:300px;height:300px;bottom:-150px;left:-80px}}
  .hero-wave{{height:24px;border-radius:12px 12px 0 0;margin-top:-12px}}

  .stats-bar{{padding:0 20px;margin-top:-12px}}
  .stats-inner{{flex-wrap:wrap}}
  .stat{{flex:1 1 45%;padding:20px 16px;gap:12px}}
  .stat:nth-child(2)::after{{display:none}}
  .stat-icon{{width:40px;height:40px;border-radius:12px;font-size:18px}}
  .stat-num{{font-size:18px}}
  .stat-label{{font-size:10px}}

  .main{{padding:32px 20px 24px}}
  .sec{{margin-bottom:40px}}
  .sec-title{{font-size:22px;margin-bottom:20px}}
  .divider{{margin-bottom:40px}}

  .ppl{{flex-direction:column;gap:10px}}
  .person{{padding:12px 16px 12px 12px}}
  .av,.av-img{{width:38px;height:38px;border-radius:12px}}

  .takeaway{{padding:24px;border-radius:16px}}
  .takeaway-text{{font-size:16px}}
  .sbullet{{padding:14px 16px;font-size:13px;border-radius:14px}}
  .sbullet-num{{width:24px;height:24px;font-size:11px;border-radius:6px}}
  .sbox{{padding:24px;font-size:14px;border-radius:16px}}
  .sbox::before{{width:3px;top:16px;bottom:16px}}

  .cta-banner{{flex-direction:column;padding:28px 24px;border-radius:20px;text-align:center;gap:20px}}
  .cta-title{{font-size:20px}}
  .cta-desc{{font-size:13px}}
  .cta-btn{{padding:12px 28px;font-size:14px;width:100%;justify-content:center}}

  .g2,.g3{{grid-template-columns:1fr}}
  .crd{{padding:22px;border-radius:16px}}
  .crd li{{font-size:13px}}

  .demo-row{{flex-direction:column;gap:12px;padding:18px 20px}}
  .demo-row:first-child{{border-radius:16px 16px 0 0}}
  .demo-row:last-child{{border-radius:0 0 16px 16px}}
  .demo-row:only-child{{border-radius:16px}}
  .demo-num{{width:32px;height:32px;font-size:12px;border-radius:8px}}

  .bam-callout{{flex-direction:column;gap:14px;padding:22px;border-radius:16px}}
  .bam-title{{font-size:15px}}
  .bam-desc{{font-size:13px}}

  .step-row{{padding:16px 20px;gap:12px}}
  .step-row:first-child{{border-radius:16px 16px 0 0}}
  .step-row:last-child{{border-radius:0 0 16px 16px}}
  .step-row:only-child{{border-radius:16px}}
  .step-act{{font-size:14px}}
  .step-meta{{gap:6px}}

  .cs-grid{{grid-template-columns:1fr}}
  .cs-card{{padding:22px;border-radius:16px}}
  .cs-name{{font-size:16px}}

  .plogo-sec{{padding:24px 0}}
  .plogo-inner{{padding:0 20px}}
  .plogo-label{{margin-bottom:16px;font-size:9px}}
  .plogo-track{{gap:24px}}
  .plogo-name{{font-size:12px}}
  .plogo-dot{{font-size:14px}}

  .testi-wrap{{padding:48px 0 40px}}
  .testi-inner{{padding:0 20px}}
  .testi-title{{font-size:24px}}
  .testi-sub{{font-size:14px;margin-bottom:28px}}
  .testi-scroll{{gap:14px}}
  .tc{{flex:0 0 270px;padding:22px;border-radius:16px}}
  .tc-q{{font-size:13px;line-height:1.7}}
  .tc-av{{width:32px;height:32px;border-radius:8px;font-size:11px}}
  .tc-nm{{font-size:12px}}
  .tc-rl{{font-size:10px}}
  .res-sec{{padding:40px 20px 24px}}
  .res-grid,.res-g2{{grid-template-columns:1fr}}
  .res-card,.blog-card{{padding:18px 20px;border-radius:14px}}


  .ftr{{padding:28px 20px 24px}}
  .ftr-in{{flex-direction:column;align-items:flex-start;gap:16px}}
  .ftr-right{{align-items:flex-start}}
  .ftr-logo{{height:20px}}
  .ftr-tag{{font-size:11px}}
  .ftr-a{{font-size:11px;padding:4px 10px}}
}}

@media(max-width:400px){{
  .hero-inner{{padding:32px 16px 28px}}
  .hero h1{{font-size:24px}}
  .hero-pill{{padding:6px 12px;font-size:11px}}
  .stats-bar{{padding:0 14px;margin-top:-12px}}
  .stat{{flex:1 1 100%;padding:16px 14px;gap:10px}}
  .stat::after{{display:none!important}}
  .stat-icon{{width:36px;height:36px;border-radius:10px;font-size:16px}}
  .stat-num{{font-size:16px}}
  .stat-label{{font-size:9px}}
  .main{{padding:24px 14px 20px}}
  .takeaway{{padding:20px}}
  .takeaway-text{{font-size:15px}}
  .sbox{{padding:20px}}
  .cta-banner{{padding:24px 20px;border-radius:16px}}
  .crd{{padding:18px}}
  .demo-row{{padding:14px 16px}}
  .bam-callout{{padding:18px}}
  .step-row{{padding:14px 16px}}
  .testi-inner{{padding:0 14px}}
  .tc{{flex:0 0 250px;padding:18px}}
  .res-sec{{padding:32px 14px 20px}}
  .ftr{{padding:24px 14px 20px}}
}}

@media print{{
  body{{background:#fff}}
  .hero,.testi-wrap{{break-inside:avoid}}
  .testi-wrap{{background:#1a1d3a!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
  .plogo-track{{animation:none}}
  .tc:hover,.res-card:hover,.blog-card:hover,.person:hover,.crd:hover,.demo-row:hover,.cs-card:hover{{transform:none;box-shadow:none}}
}}
</style>
</head>
<body>

<!-- ▌ HERO ▌ -->
<div class="hero">
  <div class="hero-accent"></div>
  <div class="hero-inner">
    <div class="hero-top">
      <img src="data:image/webp;base64,{LOGO_WHITE}" alt="Boom" class="hero-logo"/>
      <div class="hero-badge">{e(mtype)}</div>
    </div>
    <h1>{e(mt)}</h1>
    <p class="hero-sub">Meeting summary prepared for {e(co)}</p>
    <div class="hero-pills">
      <div class="hero-pill"><span class="hero-pill-dot"></span><strong>{e(md)}</strong></div>
      {"<div class='hero-pill'><span class='hero-pill-dot'></span><strong>"+e(dur)+"</strong></div>" if dur else ""}
      <div class="hero-pill"><span class="hero-pill-dot"></span><strong>{len(parts)} participants</strong></div>
    </div>
  </div>
  <div class="hero-wave"></div>
</div>

<!-- ▌ STATS BAR ▌ -->
<div class="stats-bar">
  <div class="stats-inner">
    <div class="stat">
      <div class="stat-icon stat-icon-blue">🌍</div>
      <div class="stat-content"><div class="stat-num"><span>20+</span> Countries</div><div class="stat-label">5 continents worldwide</div></div>
    </div>
    <div class="stat">
      <div class="stat-icon stat-icon-blue">🔗</div>
      <div class="stat-content"><div class="stat-num"><span>250+</span> Channels</div><div class="stat-label">Direct API with Airbnb &amp; Booking.com</div></div>
    </div>
    <div class="stat">
      <div class="stat-icon stat-icon-gold">💰</div>
      <div class="stat-content"><div class="stat-num"><span>$12.7M</span> Raised</div><div class="stat-label">Led by Avenue Growth Partners</div></div>
    </div>
    <div class="stat">
      <div class="stat-icon stat-icon-blue">⚡</div>
      <div class="stat-content"><div class="stat-num"><span>6</span> Week Onboarding</div><div class="stat-label">Average time to go live</div></div>
    </div>
  </div>
</div>

<!-- ▌ CONTENT ▌ -->
<div class="main">

  {"" if is_prospect else f"""<div class="sec">
    <div class="sec-label">ATTENDEES</div>
    <h2 class="sec-title">Who Was There</h2>
    <div class="ppl">{r_people(parts)}</div>
  </div>
  <div class="divider"></div>"""}

  <div class="sec">
    <div class="sec-label">{"PREPARED FOR YOU" if is_prospect else "EXECUTIVE SUMMARY"}</div>
    <h2 class="sec-title">{"Why Boom for " + e(co) if is_prospect else "Overview"}</h2>
    {"" if not takeaway else f'<div class="takeaway"><div class="takeaway-label">KEY TAKEAWAY</div><div class="takeaway-text">{e(takeaway)}</div></div>'}
    {"" if not bullets else '<div class="sbullets">' + "".join(f'<div class="sbullet"><div class="sbullet-num">{i+1}</div><div>{e(b)}</div></div>' for i,b in enumerate(bullets)) + '</div>'}
    {"" if takeaway or bullets else f'<div class="sbox">{e(summ)}</div>'}
  </div>
  <div class="divider"></div>

  {"" if not dps else f'''<div class="sec">
    <div class="sec-label">{"YOUR BUSINESS" if is_prospect else "KEY INSIGHTS"}</div>
    <h2 class="sec-title">{"How Boom Fits Your World" if is_prospect else "Discussion Points"}</h2>
    <div class="grid {gc}">{r_cards(dps)}</div>
  </div>
  <div class="divider"></div>'''}

  {r_demo(demos, is_prospect)}
  {"<div class='divider'></div>" if demos else ""}

  {"" if not steps else f'''<div class="sec">
    <div class="sec-label">ACTION ITEMS</div>
    <h2 class="sec-title">Next Steps</h2>
    <div class="step-list">{r_steps(steps)}</div>
  </div>
  <div class="divider"></div>'''}

  {"" if not res.get("calendar_url") else f'''<a href="{e(res["calendar_url"])}" style="text-decoration:none;display:block">
  <div class="cta-banner">
    <div class="cta-body">
      <div class="cta-title">Ready to See the Full Platform?</div>
      <div class="cta-desc">{"Book a discovery call — we\\'ll tailor the demo to " + e(co) + "\\'s specific needs." if is_prospect else "Book your next session — we\\'ll tailor the demo to " + e(co) + "\\'s specific needs."}</div>
    </div>
    <div class="cta-btn">Book a Session <span>→</span></div>
  </div></a>'''}

  {r_case_studies(data)}

</div>

<!-- ▌ PARTNER LOGOS ▌ -->
{r_logos()}

<!-- ▌ TESTIMONIALS ▌ -->
{r_testi()}

<!-- ▌ RESOURCES ▌ -->
{"" if not res else f"""<div class="res-sec">
  <div class="sec-label">RESOURCES</div>
  <h2 class="sec-title">{"Let's Talk" if is_prospect else "Continue the Conversation"}</h2>
  <div class="res-grid res-g2">{r_res(res, is_prospect)}</div>
  {f'<div class="blog-sec"><div class="sec-label" style="margin-top:32px">RECOMMENDED READING</div><div class="res-grid res-g2">{r_blog(data)}</div></div>' if r_blog(data) else ''}
</div>"""}

<!-- ▌ FOOTER ▌ -->
<div class="ftr">
  <div class="ftr-in">
    <div class="ftr-left">
      <img src="data:image/webp;base64,{LOGO_WHITE}" alt="Boom" class="ftr-logo"/>
      <span class="ftr-tag">Prepared by Idan Carmi, Chief Growth Officer</span>
    </div>
    <div class="ftr-right">
      <div class="ftr-links">
        <a href="https://www.boomnow.com" class="ftr-a">boomnow.com</a>
        <span class="ftr-sep">·</span>
        <a href="https://www.boomnow.com/partner-testimonials" class="ftr-a">Partner Stories</a>
        <span class="ftr-sep">·</span>
        <a href="https://meetings.hubspot.com/idan-carmi" class="ftr-a">Book a Call</a>
      </div>
      <div class="ftr-trust">
        <span class="ftr-badge">GDPR Compliant</span>
        <span class="ftr-badge">ISO 27001</span>
      </div>
      <div style="font-size:10px;color:rgba(255,255,255,.3)">Backed by Avenue Growth Partners · Advisors include former Hilton International CEO Ian Carter</div>
    </div>
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
