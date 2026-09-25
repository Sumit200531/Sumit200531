import os, random, math, textwrap
from xml.sax.saxutils import escape as esc

random.seed(11)
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

CY, VI, PK, GR = "#00E5FF", "#7C3AED", "#FF3DA8", "#3DDC97"
WHITE, TXT, DIM = "#F2F6FF", "#AEB9CC", "#66748C"
MONO = "'JetBrains Mono','Fira Code','SF Mono',Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI Variable Display','Segoe UI','Inter',system-ui,-apple-system,Helvetica,Arial,sans-serif"

BASE_CSS = """
.o1{animation:f1 16s ease-in-out infinite}.o2{animation:f2 19s ease-in-out infinite}.o3{animation:f3 13s ease-in-out infinite}
@keyframes f1{0%,100%{transform:translate(0,0)}50%{transform:translate(80px,40px)}}
@keyframes f2{0%,100%{transform:translate(0,0)}50%{transform:translate(-90px,-35px)}}
@keyframes f3{0%,100%{transform:translate(0,0)}50%{transform:translate(55px,-45px)}}
.tw{animation:tw 4s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.08}50%{opacity:.95}}
.pulse{animation:pl 1.8s ease-in-out infinite}@keyframes pl{0%,100%{opacity:1}50%{opacity:.2}}
.blink{animation:bk 1s steps(1) infinite}@keyframes bk{50%{opacity:0}}
.shine{animation:sh 8s ease-in-out infinite}@keyframes sh{0%{transform:translateX(-400px)}55%,100%{transform:translateX(1900px)}}
.up{opacity:0;animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.spin{transform-box:fill-box;transform-origin:center;animation:sp 14s linear infinite}.spinr{transform-box:fill-box;transform-origin:center;animation:sp 22s linear infinite reverse}@keyframes sp{to{transform:rotate(360deg)}}
.eq{transform-box:fill-box;transform-origin:50% 100%;animation:eq 1.1s ease-in-out infinite}@keyframes eq{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}
@media (prefers-reduced-motion:reduce){*{animation-duration:0s!important;animation-iteration-count:1!important}}
"""

DEFS = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#04060C"/><stop offset=".55" stop-color="#090E1B"/><stop offset="1" stop-color="#08051A"/></linearGradient>
<radialGradient id="orbC"><stop offset="0" stop-color="{CY}" stop-opacity=".85"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>
<radialGradient id="orbV"><stop offset="0" stop-color="{VI}" stop-opacity=".95"/><stop offset="1" stop-color="{VI}" stop-opacity="0"/></radialGradient>
<radialGradient id="orbP"><stop offset="0" stop-color="{PK}" stop-opacity=".8"/><stop offset="1" stop-color="{PK}" stop-opacity="0"/></radialGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".3" stop-color="#fff" stop-opacity=".07"/><stop offset=".7" stop-color="{CY}" stop-opacity=".25"/><stop offset="1" stop-color="{VI}" stop-opacity=".7"/></linearGradient>
<linearGradient id="glassFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".11"/><stop offset="1" stop-color="#fff" stop-opacity=".02"/></linearGradient>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}"/><stop offset=".55" stop-color="{VI}"/><stop offset="1" stop-color="{PK}"/></linearGradient>
<linearGradient id="neonV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{VI}"/></linearGradient>
<linearGradient id="shineG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="fadeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="frost" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>
<filter id="glow" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .07 0"/></filter>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern>
"""


def svg(name, w, h, body, css="", title="", extra_defs=""):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'role="img" aria-label="{esc(title)}" font-family="{MONO}">\n<title>{esc(title)}</title>\n'
         f'<style>{BASE_CSS}{css}</style>\n<defs>{DEFS}{extra_defs}'
         f'<mask id="gridMask"><rect width="{w}" height="{h}" fill="url(#fadeV)"/></mask></defs>\n{body}\n</svg>\n')
    with open(os.path.join(OUT, name), "w") as f:
        f.write(s)


def orbs(spec):
    return "".join(f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}" fill="url(#{g})" opacity="{o}"/>'
                   for x, y, r, g, c, o in spec)


def stars(w, h, n, x0=0, y0=0):
    out = []
    for _ in range(n):
        x, y = random.uniform(x0, w), random.uniform(y0, h)
        r = random.choice([.6, .8, 1, 1.3])
        out.append(f'<circle class="tw" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" '
                   f'style="animation-delay:-{random.uniform(0, 4):.2f}s;animation-duration:{random.uniform(2.5, 6):.1f}s"/>')
    return "".join(out)


def backdrop(w, h, spec, n_stars=30, rx=24):
    return (f'<clipPath id="frame"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
            f'<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#bg)"/>{orbs(spec)}'
            f'<rect width="{w}" height="{h}" fill="url(#grid)" mask="url(#gridMask)"/>{stars(w, h, n_stars)}</g>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".08"/>')


_gid = [0]


def glass(x, y, w, h, r, spec, shine=True, tint=".38"):
    _gid[0] += 1
    i = _gid[0]
    sh = (f'<rect class="shine" style="animation-delay:{random.uniform(0, 3):.1f}s" x="{x-260}" y="{y-40}" '
          f'width="160" height="{h+80}" fill="url(#shineG)" transform="skewX(-18)"/>') if shine else ""
    return (f'<clipPath id="gc{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
            f'<g clip-path="url(#gc{i})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0A1124" fill-opacity="{tint}"/>'
            f'<g filter="url(#frost)">{orbs(spec)}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#glassFill)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#noise)"/>{sh}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="url(#edge)" stroke-width="1.2"/>'
            f'<path d="M{x+r} {y+1}H{x+w-r}" stroke="#fff" stroke-opacity=".4" stroke-width="1"/>')


def chip(x, y, text, color=CY, size=12):
    w = len(text) * size * .62 + 26
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="#fff" fill-opacity=".05" '
            f'stroke="{color}" stroke-opacity=".55"/><text x="{x+13}" y="{y+17.5}" font-size="{size}" '
            f'fill="{color}" letter-spacing=".5">{esc(text)}</text>'), w


def cycle_css(prefix, n, period):
    css, seg = "", 100 / n
    for i in range(n):
        a, b = i * seg, (i + 1) * seg
        css += (f"@keyframes {prefix}{i}{{0%,{a:.2f}%{{opacity:0;transform:translateY(10px)}}"
                f"{a+2.5:.2f}%,{b-2.5:.2f}%{{opacity:1;transform:translateY(0)}}"
                f"{b:.2f}%,100%{{opacity:0;transform:translateY(-10px)}}}}"
                f".{prefix}{i}{{opacity:0;animation:{prefix}{i} {period}s infinite}}")
    return css


def seq_css(prefix, n, period, start=3, end=78):
    css = ""
    for i in range(n):
        p = start + (end - start) * i / max(1, n - 1)
        css += (f"@keyframes {prefix}{i}{{0%,{p:.1f}%{{opacity:0;transform:translateX(-6px)}}"
                f"{p+1.8:.1f}%,93%{{opacity:1;transform:translateX(0)}}97%,100%{{opacity:0}}}}"
                f".{prefix}{i}{{opacity:0;animation:{prefix}{i} {period}s infinite}}")
    return css


def corners(x, y, w, h, s=18, c=CY):
    p = [f"M{x} {y+s}V{y}H{x+s}", f"M{x+w-s} {y}H{x+w}V{y+s}",
         f"M{x} {y+h-s}V{y+h}H{x+s}", f"M{x+w-s} {y+h}H{x+w}V{y+h-s}"]
    return "".join(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" stroke-opacity=".8"/>' for d in p)


# ───────────────────────── HERO ─────────────────────────
def hero():
    W, H = 1200, 480
    spec = [(230, 130, 300, "orbC", "o1", .75), (990, 380, 330, "orbV", "o2", .95), (720, 40, 210, "orbP", "o3", .55)]
    roles = ["building somewhere between backend, AI and chaos",
             "B.Tech CSE student, hunting a SWE internship",
             "Java, Spring Boot, Node, React, MongoDB",
             "taking LLMs, RAG and embeddings apart"]
    css = cycle_css("r", len(roles), 14) + """
.gA{animation:gA 7s steps(1) infinite}.gB{animation:gB 7s steps(1) infinite}
@keyframes gA{0%,88%,100%{opacity:0;transform:translate(0,0)}89%{opacity:.75;transform:translate(-7px,2px)}91%{opacity:.75;transform:translate(6px,-1px)}93%{opacity:0}}
@keyframes gB{0%,88%,100%{opacity:0;transform:translate(0,0)}89%{opacity:.7;transform:translate(7px,-2px)}91%{opacity:.7;transform:translate(-5px,2px)}93%{opacity:0}}
.scan{animation:scan 6s linear infinite}@keyframes scan{from{transform:translateY(0)}to{transform:translateY(340px)}}
.glint{animation:gl 5s ease-in-out infinite}@keyframes gl{0%{transform:translateX(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateX(930px);opacity:0}}
"""
    extra = (f'<linearGradient id="nameG" gradientUnits="userSpaceOnUse" x1="130" y1="0" x2="980" y2="0">'
             f'<stop offset="0" stop-color="{CY}"/><stop offset=".45" stop-color="#FFFFFF"/><stop offset="1" stop-color="{VI}"/>'
             f'<animate attributeName="x1" values="130;-300;130" dur="9s" repeatCount="indefinite"/>'
             f'<animate attributeName="x2" values="980;560;980" dur="9s" repeatCount="indefinite"/></linearGradient>'
             f'<clipPath id="reveal"><rect x="120" y="150" width="0" height="120">'
             f'<animate attributeName="width" from="0" to="1000" dur="1.6s" begin=".3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect></clipPath>')
    px, py, pw, ph = 80, 70, 1040, 340
    name = "SUMIT GOSWAMI"
    nm = f'font-family="{SANS}" font-size="88" font-weight="800" letter-spacing="7"'
    b = [backdrop(W, H, spec, 70), glass(px, py, pw, ph, 30, spec), corners(px + 14, py + 14, pw - 28, ph - 28)]
    b.append(f'<g clip-path="url(#gc1)"><rect class="scan" x="{px}" y="{py}" width="{pw}" height="2" fill="{CY}" opacity=".18"/></g>')
    b.append(f'<text x="132" y="130" font-size="13" fill="{CY}" letter-spacing="3" class="up" style="animation-delay:.1s">'
             f'<tspan class="pulse">▍</tspan> sys://profile/init <tspan fill="{DIM}">— handshake ok</tspan></text>')
    b.append(f'<text x="1068" y="130" font-size="13" fill="{DIM}" text-anchor="end" letter-spacing="2" class="up" style="animation-delay:.2s">github.com/Sumit200531</text>')
    b.append(f'<g clip-path="url(#reveal)">'
             f'<text x="128" y="238" {nm} fill="{CY}" opacity=".55" filter="url(#soft)">{name}</text>'
             f'<text class="gA" x="128" y="238" {nm} fill="{CY}">{name}</text>'
             f'<text class="gB" x="128" y="238" {nm} fill="{PK}">{name}</text>'
             f'<text x="128" y="238" {nm} fill="url(#nameG)">{name}</text></g>')
    b.append(f'<text x="134" y="292" font-size="21" fill="{CY}" class="blink">&gt;</text>')
    for i, r in enumerate(roles):
        b.append(f'<text class="r{i}" x="158" y="292" font-size="21" fill="{WHITE}">{esc(r)}<tspan fill="{CY}" class="blink"> _</tspan></text>')
    b.append(f'<path d="M132 326H1068" stroke="url(#neon)" stroke-opacity=".45"/>'
             f'<circle class="glint" cx="134" cy="326" r="3" fill="#fff" filter="url(#glow)"/>')
    x = 132
    for t, c in [("full-stack", CY), ("backend / systems", CY), ("LLM + RAG", VI), ("docker", VI)]:
        s, w = chip(x, 346, t, c)
        b.append(f'<g class="up" style="animation-delay:{1.2 + (x-132)/900:.2f}s">{s}</g>')
        x += w + 10
    b.append(f'<g class="up" style="animation-delay:1.7s"><rect x="836" y="346" width="232" height="26" rx="13" fill="{GR}" fill-opacity=".1" stroke="{GR}" stroke-opacity=".6"/>'
             f'<circle class="pulse" cx="854" cy="359" r="4.5" fill="{GR}" filter="url(#glow)"/>'
             f'<text x="868" y="363.5" font-size="12" fill="{GR}" letter-spacing=".5">open to SWE internships</text></g>')
    b.append(f'<text class="pulse" x="600" y="452" text-anchor="middle" font-size="12" fill="{DIM}" letter-spacing="4" style="animation-duration:3s">scroll · the transmission continues</text>')
    svg("hero.svg", W, H, "".join(b), css, "Sumit Goswami — full stack, backend and AI developer", extra)


# ───────────────────────── SECTION HEADERS ─────────────────────────
def header(fname, glyph, title, sub, hue=CY):
    W, H = 1200, 124
    spec = [(90, 62, 180, "orbC" if hue == CY else "orbV", "o1", .55), (1120, 62, 220, "orbV", "o2", .6)]
    b = [backdrop(W, H, spec, 22, 22),
         glass(14, 14, W - 28, H - 28, 18, spec, tint=".2"),
         f'<text x="1070" y="100" text-anchor="end" font-family="{SANS}" font-size="100" font-weight="800" fill="none" stroke="#fff" stroke-opacity=".08">{esc(glyph)}</text>',
         f'<rect x="44" y="36" width="4" height="52" rx="2" fill="url(#neonV)" filter="url(#glow)"/>',
         f'<text x="70" y="66" font-family="{SANS}" font-size="30" font-weight="800" fill="{WHITE}" letter-spacing="1.5" class="up">{esc(title)}</text>',
         f'<text x="71" y="92" font-size="14" fill="{TXT}" class="up" style="animation-delay:.25s"><tspan fill="{hue}">//</tspan> {esc(sub)}</text>']
    for k in range(6):
        b.append(f'<rect class="eq" x="{1100 + k*11}" y="44" width="5" height="36" rx="2" fill="url(#neonV)" opacity=".85" '
                 f'style="animation-delay:-{random.uniform(0, 1.1):.2f}s;animation-duration:{random.uniform(.8, 1.5):.2f}s"/>')
    svg(fname, W, H, "".join(b), "", title)


# ───────────────────────── DIVIDER ─────────────────────────
def divider():
    css = ".gl{animation:g 4s ease-in-out infinite}@keyframes g{from{transform:translateX(-200px)}to{transform:translateX(1400px)}}"
    extra = (f'<linearGradient id="gw" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    b = (f'<rect y="5" width="1200" height="2" fill="url(#neon)" opacity=".5"/>'
         f'<rect class="gl" y="4" width="200" height="4" rx="2" fill="url(#gw)" filter="url(#glow)"/>')
    svg("divider.svg", 1200, 12, b, css, "divider", extra)


# ───────────────────────── TERMINALS ─────────────────────────
def terminal(fname, title, lines, period):
    W, H = 590, 360
    spec = [(80, 60, 200, "orbC", "o1", .45), (520, 320, 220, "orbV", "o2", .6)]
    b = [backdrop(W, H, spec, 18, 22), glass(12, 12, W - 24, H - 24, 16, spec, tint=".5")]
    b.append(f'<path d="M12 56H{W-12}" stroke="#fff" stroke-opacity=".08"/>')
    for k, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        b.append(f'<circle cx="{38 + k*20}" cy="34" r="6" fill="{c}" opacity=".9"/>')
    b.append(f'<text x="{W/2}" y="39" text-anchor="middle" font-size="13" fill="{DIM}">{esc(title)}</text>')
    y = 92
    for i, spans in enumerate(lines):
        ts = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in spans)
        b.append(f'<text class="L{i}" x="36" y="{y}" font-size="15">{ts}</text>')
        y += 28
    b.append(f'<text x="36" y="{y}" font-size="15"><tspan fill="{CY}">$ </tspan><tspan class="blink" fill="{WHITE}">█</tspan></text>')
    svg(fname, W, H, "".join(b), seq_css("L", len(lines), period), title)


def P(cmd):
    return [("$ ", CY), (cmd, WHITE)]


def O(txt, c=TXT):
    return [("  ", TXT), (txt, c)]


# ───────────────────────── DOSSIER ─────────────────────────
def dossier():
    W, H = 1200, 420
    spec = [(160, 200, 240, "orbC", "o1", .6), (1050, 330, 280, "orbV", "o2", .8), (700, 40, 160, "orbP", "o3", .4)]
    b = [backdrop(W, H, spec, 40), glass(40, 36, 1120, 348, 28, spec)]
    cx, cy = 190, 205
    b.append(f'<circle class="spin" cx="{cx}" cy="{cy}" r="96" fill="none" stroke="url(#neon)" stroke-width="2" stroke-dasharray="4 10"/>'
             f'<circle class="spinr" cx="{cx}" cy="{cy}" r="84" fill="none" stroke="{CY}" stroke-opacity=".35" stroke-dasharray="120 40 30 40"/>'
             f'<circle cx="{cx}" cy="{cy}" r="70" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".25"/>'
             f'<text x="{cx}" y="{cy+19}" text-anchor="middle" font-family="{SANS}" font-size="54" font-weight="800" fill="url(#neon)" filter="url(#glow)">SG</text>'
             f'<text x="{cx}" y="{cy+132}" text-anchor="middle" font-size="12" fill="{DIM}" letter-spacing="2">id: Sumit200531</text>')
    b.append(f'<text x="340" y="92" font-size="13" fill="{CY}" letter-spacing="3" class="up">candidate file / swe-intern</text>')
    rows = [("seeking", "Software Engineering internship"),
            ("education", "B.Tech, Computer Science Engineering"),
            ("stack", "Java/Spring Boot, Node/Express, React, MongoDB/MySQL"),
            ("ai", "LLMs, RAG, embeddings, vector DBs (hands-on)"),
            ("ships with", "Docker, tests, and actually reading the error"),
            ("available", "internships, part-time, open-source collabs")]
    y = 138
    for i, (k, v) in enumerate(rows):
        b.append(f'<g class="up" style="animation-delay:{.3 + i*.14:.2f}s"><text x="340" y="{y}" font-size="12" fill="{DIM}" letter-spacing="2">{esc(k)}</text>'
                 f'<text x="480" y="{y}" font-family="{SANS}" font-size="18" fill="{WHITE}">{esc(v)}</text>'
                 f'<path d="M340 {y+14}H1110" stroke="#fff" stroke-opacity=".06"/></g>')
        y += 40
    b.append(f'<g transform="rotate(-10 1030 92)" class="pulse" style="animation-duration:2.6s">'
             f'<rect x="950" y="70" width="162" height="42" rx="6" fill="none" stroke="{PK}" stroke-width="2.5"/>'
             f'<text x="1031" y="98" text-anchor="middle" font-size="16" font-weight="700" fill="{PK}" letter-spacing="3">OPEN TO WORK</text></g>')
    svg("dossier.svg", W, H, "".join(b), "", "Recruiter TL;DR — candidate file")


# ───────────────────────── MISSION ─────────────────────────
def mission():
    W, H = 1200, 420
    spec = [(1000, 90, 260, "orbC", "o1", .5), (200, 360, 280, "orbV", "o2", .8)]
    css = ".sweep{animation:sw 5s ease-in-out infinite}@keyframes sw{0%{transform:translateY(0);opacity:0}10%,90%{opacity:1}100%{transform:translateY(270px);opacity:0}}"
    b = [backdrop(W, H, spec, 30), glass(36, 30, 1128, 360, 26, spec)]
    b.append(f'<text x="70" y="76" font-size="13" fill="{CY}" letter-spacing="3">quest log</text>'
             f'<text x="1130" y="76" text-anchor="end" font-size="13" fill="{DIM}">7 objectives · 0 abandoned (so far)</text>')
    b.append(f'<g clip-path="url(#gc{_gid[0]})"><rect class="sweep" x="36" y="96" width="1128" height="30" fill="url(#shineG)" opacity=".7"/></g>')
    items = [("Production-ready applications, not just tutorials", "active", CY),
             ("A Software Engineering internship", "hunting", PK),
             ("Sharper DSA and problem-solving", "grinding", CY),
             ("Real fluency in Java and Spring Boot", "active", CY),
             ("LLM / RAG apps that do something useful", "in the lab", VI),
             ("Docker and backend deployment", "active", CY),
             ("An actual open-source contribution", "next up", GR)]
    for i, (t, tag, c) in enumerate(items):
        col, row = i % 2, i // 2
        x, y = 66 + col * 544, 100 + row * 70
        tw = len(tag) * 11 * .62 + 22
        b.append(f'<g class="up" style="animation-delay:{.2 + i*.12:.2f}s">'
                 f'<rect x="{x}" y="{y}" width="524" height="54" rx="14" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".1"/>'
                 f'<rect x="{x+20}" y="{y+19}" width="14" height="14" rx="3" fill="none" stroke="{c}" stroke-width="1.6" transform="rotate(45 {x+27} {y+26})"/>'
                 f'<text x="{x+50}" y="{y+32}" font-family="{SANS}" font-size="16" fill="{WHITE}">{esc(t)}</text>'
                 f'<rect x="{x+504-tw:.0f}" y="{y+16}" width="{tw:.0f}" height="22" rx="11" fill="{c}" fill-opacity=".12"/>'
                 f'<text class="pulse" style="animation-delay:-{i*.3:.1f}s;animation-duration:2.4s" x="{x+504-tw/2:.0f}" y="{y+31}" text-anchor="middle" font-size="11" fill="{'#B69CFF' if c == VI else c}">{tag}</text></g>')
    svg("mission.svg", W, H, "".join(b), css, "Current mission — quest log")


# ───────────────────────── PROJECT CARDS ─────────────────────────
def card(fname, title, desc, tags, icon, spec):
    W, H = 390, 280
    extra = (f'<linearGradient id="rot" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CY}"/>'
             f'<stop offset=".45" stop-color="{CY}" stop-opacity="0"/><stop offset=".55" stop-color="{VI}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{PK}"/><animateTransform attributeName="gradientTransform" type="rotate" '
             f'from="0 .5 .5" to="360 .5 .5" dur="6s" repeatCount="indefinite"/></linearGradient>')
    css = (".chk{stroke-dasharray:20;stroke-dashoffset:20;animation:ck 4s ease-out infinite}"
           "@keyframes ck{0%,10%{stroke-dashoffset:20}30%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:20}}")
    b = [backdrop(W, H, spec, 14, 22), glass(10, 10, W - 20, H - 20, 18, spec, tint=".45"),
         f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="18" fill="none" stroke="url(#rot)" stroke-width="1.6"/>',
         f'<rect x="32" y="32" width="50" height="50" rx="14" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".18"/>',
         icon,
         f'<circle class="pulse" cx="{W-102}" cy="52" r="4" fill="{GR}" filter="url(#glow)"/>'
         f'<text x="{W-32}" y="56.5" text-anchor="end" font-size="12" fill="{GR}" letter-spacing="1">shipped</text>',
         f'<text x="32" y="118" font-family="{SANS}" font-size="{20 if len(title) < 26 else 17.5}" font-weight="700" fill="{WHITE}">{esc(title)}</text>']
    y = 146
    for ln in textwrap.wrap(desc, 42):
        b.append(f'<text x="32" y="{y}" font-family="{SANS}" font-size="14.5" fill="{TXT}">{esc(ln)}</text>')
        y += 22
    x = 32
    for t in tags:
        s, w = chip(x, 222, t, CY, 11)
        b.append(s)
        x += w + 8
    svg(fname, W, H, "".join(b), css, title, extra)


def icon_tasks():
    s = ""
    for k in range(3):
        y = 44 + k * 10
        s += (f'<rect x="42" y="{y}" width="7" height="7" rx="1.5" fill="none" stroke="{CY}" stroke-width="1.3"/>'
              f'<path class="chk" style="animation-delay:{k*.4}s" d="M43 {y+3.5}l2 2 4-5" fill="none" stroke="{GR}" stroke-width="1.6" stroke-linecap="round"/>'
              f'<rect x="54" y="{y+2}" width="{18 - k*3}" height="3" rx="1.5" fill="#fff" opacity=".5"/>')
    return s


def icon_backup():
    return (f'<ellipse cx="57" cy="47" rx="13" ry="4.5" fill="none" stroke="{CY}" stroke-width="1.4"/>'
            f'<path d="M44 47v18c0 2.5 5.8 4.5 13 4.5s13-2 13-4.5V47M44 56c0 2.5 5.8 4.5 13 4.5s13-2 13-4.5" fill="none" stroke="{CY}" stroke-width="1.4"/>'
            f'<circle class="spin" cx="57" cy="57" r="21" fill="none" stroke="{VI}" stroke-width="1.5" stroke-dasharray="14 8" style="animation-duration:5s"/>')


def icon_voice():
    s = ""
    for k in range(7):
        s += (f'<rect class="eq" x="{40 + k*5}" y="42" width="3" height="30" rx="1.5" fill="url(#neonV)" '
              f'style="animation-delay:-{random.uniform(0, 1):.2f}s;animation-duration:{random.uniform(.6, 1.2):.2f}s"/>')
    return s


# ───────────────────────── AI LAB ─────────────────────────
def ailab():
    W, H = 1200, 460
    spec = [(260, 200, 280, "orbC", "o1", .5), (960, 260, 300, "orbV", "o2", .8), (560, 420, 160, "orbP", "o3", .4)]
    b = [backdrop(W, H, spec, 30), glass(36, 36, 580, 370, 24, spec), glass(648, 36, 516, 370, 24, spec)]
    b.append(f'<text x="66" y="74" font-size="13" fill="{CY}" letter-spacing="3">embedding space</text>'
             f'<text x="586" y="74" text-anchor="end" font-size="12" fill="{DIM}">dim 1536 → 2 (artistic liberty)</text>')
    b.append(f'<path d="M80 370H580M80 370V100" stroke="#fff" stroke-opacity=".12"/>')
    pts, clusters = [], [((190, 220), CY), ((420, 170), VI), ((360, 310), PK)]
    for (mx, my), c in clusters:
        for _ in range(15):
            pts.append((mx + random.gauss(0, 38), my + random.gauss(0, 30), c))
    pts = [(min(max(x, 95), 570), min(max(y, 110), 360), c) for x, y, c in pts]
    q = (285, 245)
    near = sorted(pts, key=lambda p: (p[0]-q[0])**2 + (p[1]-q[1])**2)[:4]
    for x, y, c in pts:
        b.append(f'<circle class="tw" cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="{c}" style="animation-delay:-{random.uniform(0, 4):.1f}s;animation-duration:{random.uniform(3, 6):.1f}s"/>')
    css = ".ln{stroke-dasharray:160;stroke-dashoffset:160;animation:dr 5s ease-in-out infinite}@keyframes dr{0%,15%{stroke-dashoffset:160}45%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-160}}"
    css += ".nd{animation:lu 5s linear infinite}@keyframes lu{0%{opacity:1}22%,100%{opacity:.3}}"
    for k, (x, y, c) in enumerate(near):
        b.append(f'<path class="ln" style="animation-delay:{k*.15:.2f}s" d="M{q[0]} {q[1]}L{x:.0f} {y:.0f}" stroke="{WHITE}" stroke-opacity=".75" stroke-width="1.3"/>'
                 f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="none" stroke="{c}" class="pulse" style="animation-delay:-{k*.3}s"/>')
    b.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="6" fill="none" stroke="{WHITE}"><animate attributeName="r" values="6;34" dur="2.4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;0" dur="2.4s" repeatCount="indefinite"/></circle>'
             f'<path d="M{q[0]} {q[1]-9}l3 6 6 3-6 3-3 6-3-6-6-3 6-3z" fill="{WHITE}" filter="url(#glow)"/>'
             f'<text x="{q[0]+14}" y="{q[1]+26}" font-size="12" fill="{WHITE}">query · top-k = 4</text>')
    b.append(f'<text x="678" y="74" font-size="13" fill="{CY}" letter-spacing="3">rag pipeline</text>')
    steps = [("Query", "someone asks a question"), ("Embed", "text becomes a vector"),
             ("Retrieve", "top-k nearest chunks"), ("Augment", "context stuffed into the prompt"),
             ("Generate", "the LLM answers, grounded (hopefully)")]
    x0, ys = 700, [116, 172, 228, 284, 340]
    b.append(f'<path id="pipe" d="M{x0} {ys[0]}V{ys[-1]}" stroke="url(#neonV)" stroke-width="2" stroke-opacity=".6"/>')
    for i, (t, s) in enumerate(steps):
        d = i * 1.25 - 5 if i else 0
        b.append(f'<circle class="nd" style="animation-delay:{d}s" cx="{x0}" cy="{ys[i]}" r="10" fill="{CY}" filter="url(#glow)"/>'
                 f'<circle cx="{x0}" cy="{ys[i]}" r="15" fill="none" stroke="#fff" stroke-opacity=".2"/>'
                 f'<text x="{x0+32}" y="{ys[i]+2}" font-family="{SANS}" font-size="18" font-weight="700" fill="{WHITE}">{t}</text>'
                 f'<text x="{x0+32}" y="{ys[i]+20}" font-size="12" fill="{TXT}">{esc(s)}</text>')
    b.append(f'<g><circle r="12" fill="#fff" opacity=".15"/><circle r="4.5" fill="#fff"/><animateMotion dur="5s" repeatCount="indefinite" path="M{x0} {ys[0]}V{ys[-1]}"/></g>')
    b.append(f'<text x="600" y="440" text-anchor="middle" font-size="12.5" fill="{DIM}">not claiming mastery. this is the take-it-apart-to-see-how-it-works stage, logged in public.</text>')
    svg("ai-lab.svg", W, H, "".join(b), css, "AI Lab — embeddings and a RAG pipeline")


# ───────────────────────── BUILD LOOP ─────────────────────────
def loop():
    W, H = 1200, 400
    spec = [(600, 200, 260, "orbV", "o1", .7), (160, 80, 180, "orbC", "o2", .5), (1060, 320, 180, "orbP", "o3", .4)]
    cx, cy, rx, ry = 600, 200, 440, 125
    path = f"M{cx} {cy-ry}A{rx} {ry} 0 1 1 {cx-.01} {cy-ry}Z"
    b = [backdrop(W, H, spec, 60)]
    b.append(f'<path d="{path}" fill="none" stroke="url(#neon)" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="3 7"/>')
    b.append(f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-family="{SANS}" font-size="110" font-weight="300" fill="#fff" opacity=".08">∞</text>'
             f'<text x="{cx}" y="{cy+6}" text-anchor="middle" font-size="14" fill="{TXT}">the loop that never really ends</text>')
    for k in range(10):
        b.append(f'<circle r="{7 - k*.6:.1f}" fill="{CY if k < 4 else VI}" opacity="{1 - k*.09:.2f}" filter="url(#glow)">'
                 f'<animateMotion dur="12s" repeatCount="indefinite" begin="-{1.2 - k*.09:.2f}s" path="{path}"/></circle>')
    stages = ["idea", "design", "code", "break it", "fix it", "ship", "learn"]
    n = len(stages)
    for i, s in enumerate(stages):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        w = len(s) * 9 + 44
        c = PK if s == "break it" else CY
        b.append(f'<g class="up" style="animation-delay:{i*.12:.2f}s"><rect x="{x-w/2:.0f}" y="{y-19:.0f}" width="{w:.0f}" height="38" rx="19" fill="#0B1226" fill-opacity=".85" stroke="{c}" stroke-opacity=".6"/>'
                 f'<text x="{x:.0f}" y="{y+5:.0f}" text-anchor="middle" font-size="15" fill="{WHITE}">{s}</text></g>')
    svg("build-loop.svg", W, H, "".join(b), "", "How I build: idea, design, code, break it, fix it, ship, learn, repeat")


# ───────────────────────── ROADMAP ─────────────────────────
def roadmap():
    W, H = 1200, 300
    spec = [(200, 150, 220, "orbC", "o1", .5), (1000, 150, 240, "orbV", "o2", .7)]
    P_ = [(170, 175), (380, 115), (600, 180), (815, 115), (1010, 175)]
    d = f"M{P_[0][0]} {P_[0][1]}"
    for (x1, y1), (x2, y2) in zip(P_, P_[1:]):
        dx = (x2 - x1) / 2
        d += f"C{x1+dx} {y1} {x2-dx} {y2} {x2} {y2}"
    css = ".rd{stroke-dasharray:1200;stroke-dashoffset:1200;animation:rd 3s cubic-bezier(.2,.8,.2,1) .3s forwards}@keyframes rd{to{stroke-dashoffset:0}}"
    b = [backdrop(W, H, spec, 40)]
    b.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="2" stroke-dasharray="4 6"/>'
             f'<path class="rd" d="{d}" fill="none" stroke="url(#neon)" stroke-width="2.5" filter="url(#glow)"/>')
    b.append(f'<g><circle r="12" fill="#fff" opacity=".15"/><circle r="4.5" fill="#fff"/><animateMotion dur="7s" repeatCount="indefinite" path="{d}"/></g>')
    items = [("Java & Spring Boot", "now"), ("Node.js & backend architecture", "now"), ("LLMs + RAG", "in the lab"),
             ("System design", "next"), ("AI-native software engineering", "eventually")]
    for i, ((x, y), (t, ph)) in enumerate(zip(P_, items)):
        last = i == len(P_) - 1
        c = VI if last else CY
        dash = ' stroke-dasharray="3 3"' if last else ""
        b.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#0B1226" stroke="{c}" stroke-width="2"{dash}/>'
                 f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
        if i == 0:
            b.append(f'<circle cx="{x}" cy="{y}" r="11" fill="none" stroke="{CY}"><animate attributeName="r" values="11;30" dur="2s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="1;0" dur="2s" repeatCount="indefinite"/></circle>')
        ty = y + 48 if i % 2 == 0 else y - 50
        b.append(f'<g class="up" style="animation-delay:{.5 + i*.35:.2f}s"><text x="{x}" y="{ty}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="700" fill="{WHITE}" opacity="{.6 if last else 1}">{esc(t)}</text>'
                 f'<text x="{x}" y="{ty+20}" text-anchor="middle" font-size="12" fill="{'#B69CFF' if c == VI else c}" letter-spacing="2">{ph}</text></g>')
    svg("roadmap.svg", W, H, "".join(b), css, "Learning roadmap")


# ───────────────────────── FOOTER ─────────────────────────
def footer():
    W, H = 1200, 300
    spec = [(300, 120, 240, "orbC", "o1", .5), (900, 140, 260, "orbV", "o2", .8), (600, 20, 160, "orbP", "o3", .35)]
    lines = ["thanks for scrolling this far", "code. break. fix. repeat.", "see you in the commit history"]
    css = cycle_css("f", 3, 10) + (".wv1{animation:wv 9s linear infinite}.wv2{animation:wv 14s linear infinite reverse}"
                                   "@keyframes wv{from{transform:translateX(0)}to{transform:translateX(-600px)}}")
    b = [backdrop(W, H, spec, 50), glass(150, 40, 900, 170, 26, spec)]
    b.append(f'<text x="600" y="90" text-anchor="middle" font-size="13" fill="{CY}" letter-spacing="6">end of transmission</text>')
    for i, t in enumerate(lines):
        b.append(f'<text class="f{i}" x="600" y="146" text-anchor="middle" font-family="{SANS}" font-size="32" font-weight="700" fill="{WHITE}">{t}</text>')
    b.append(f'<text x="600" y="184" text-anchor="middle" font-size="12" fill="{DIM}">— Sumit, probably debugging something right now</text>')

    def wave(amp, per, y0):
        d = f"M0 {y0}"
        for x in range(0, 1801, 20):
            d += f"L{x} {y0 + amp*math.sin(2*math.pi*x/per):.1f}"
        return d + f"L1800 {H}L0 {H}Z"
    b.append(f'<g clip-path="url(#frame)"><path class="wv1" d="{wave(10, 300, 252)}" fill="{CY}" opacity=".12"/>'
             f'<path class="wv2" d="{wave(14, 200, 262)}" fill="{VI}" opacity=".25"/></g>')
    svg("footer.svg", W, H, "".join(b), css, "End of transmission")


if __name__ == "__main__":
    hero(); divider(); dossier(); mission(); ailab(); loop(); roadmap(); footer()
    for f, g, t, s, h in [
        ("h-tldr.svg", "TL;DR", "Recruiter TL;DR", "the twenty-second version", CY),
        ("h-about.svg", "{ }", "About me", "class Sumit implements Learner, Builder", VI),
        ("h-mission.svg", "▲", "Current mission", "what I'm actively chasing", CY),
        ("h-stack.svg", "</>", "Tech I reach for", "the arsenal, sorted by layer", VI),
        ("h-projects.svg", "✓", "Things I've shipped", "deployed, broken, fixed, deployed again", CY),
        ("h-ai.svg", "∑", "AI lab", "taking LLMs apart to see how they work", VI),
        ("h-build.svg", "∞", "How I build things", "idea to ship, then back to idea", CY),
        ("h-roadmap.svg", "→", "Learning roadmap", "where the next commits are headed", VI),
        ("h-activity.svg", "◉", "GitHub activity", "live signal from the repos", CY),
        ("h-contact.svg", "@", "Let's talk", "internships, open source, AI and backend builds", VI)]:
        header(f, g, t, s, h)
    terminal("term-whoami.svg", "sumit@dev: ~", [
        P("whoami"), O("Sumit — B.Tech CSE, hunting a SWE internship"),
        P("stack --focus"), O("full-stack · backend/systems · AI · LLM/RAG", CY),
        P("uptime --coffee"), O("still standing, barely"),
        P("status"), O("[██████████████░░░░] 78% debugging", VI)], 11)
    terminal("term-deploy.svg", "deploy.log", [
        P('git commit -m "it works"'), P("git push"), O("✗ deploy failed", PK),
        P('git commit -m "it works fr"'), P("git push --force"), O("✓ deployed", GR),
        O("nobody touch anything.", DIM)], 10)
    card("card-tasks.svg", "Task Management App",
         "Full-stack task manager: REST APIs, auth, and a React front end talking to a Mongo-backed Express server.",
         ["React", "Node.js", "Express", "MongoDB"], icon_tasks(),
         [(60, 60, 150, "orbC", "o1", .5), (360, 260, 170, "orbV", "o2", .7)])
    card("card-backup.svg", "Multithreaded C++ Backup",
         "CLI tool that scans directories, takes timestamped snapshots, and processes files concurrently.",
         ["C++", "STL", "Multithreading"], icon_backup(),
         [(330, 40, 150, "orbV", "o1", .7), (60, 260, 170, "orbC", "o2", .5)])
    card("card-voice.svg", "Voice-Based Song Recommender",
         "Listens to speech and recommends songs from it. Speech processing meets recommendation in a simple web UI.",
         ["Python", "SpeechBrain", "HTML/CSS"], icon_voice(),
         [(60, 240, 150, "orbP", "o1", .5), (340, 60, 170, "orbC", "o2", .5)])
    print(sorted(os.listdir(OUT)))
