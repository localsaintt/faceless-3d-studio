"""On-screen text as an ASS subtitle file (burned in by FFmpeg/libass).

House text style: Space Mono labels + Archivo Black numbers/captions (both SIL OFL, in assets/fonts).
Key numbers in captions are tinted with the EVENT magenta. Layout respects phone UI safe areas:
HUD top-left (y 170-450), captions centred at y≈1230, nothing in the right-hand button column.
"""
import json
import re
from pathlib import Path

FPS = 24
W, H = 1080, 1920
WHITE, INK, MAGENTA = "&H00FFFFFF", "&H001E1A15", "&H007A21E0"
NUMBER_WORDS = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "sixty", "thousand",
                "hundred", "million", "seconds", "miles"}

HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Archivo Black,76,{WHITE},{WHITE},{INK},&H64000000,0,0,0,0,100,100,0,0,1,7,2,5,60,60,0,1
Style: Hud,Archivo Black,86,{WHITE},{WHITE},{INK},&H64000000,0,0,0,0,100,100,0,0,1,6,2,7,64,64,0,1
Style: Small,Space Mono,32,{WHITE},{WHITE},{INK},&H64000000,1,0,0,0,100,100,1,0,1,4,1,7,64,64,0,1
Style: Tag,Space Mono,30,{WHITE},{WHITE},{MAGENTA},&H00000000,1,0,0,0,100,100,1,0,3,10,0,7,64,64,0,1
Style: Callout,Space Mono,34,{WHITE},{WHITE},{MAGENTA},&H00000000,1,0,0,0,100,100,1,0,3,9,0,2,0,0,0,1
Style: Prompt,Archivo Black,60,{WHITE},{WHITE},&H40151A1E,&H00000000,0,0,0,0,100,100,0,0,3,22,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ts(sec):
    sec = max(0.0, sec)
    cs = int(round(sec * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ev(start, end, style, text, layer=0):
    return f"Dialogue: {layer},{ts(start)},{ts(end)},{style},,0,0,0,,{text}"


def fmt_num(v):
    return f"{int(round(v)):,}"


def ease_out(x):
    return 1 - (1 - x) ** 3


def counter_text(label, value, unit, note=None):
    u = f"{{\\fs40}} {unit}" if unit else ""
    n = f"{{\\fnSpace Mono\\fs26}}  {note}" if note else ""
    return f"{{\\fnSpace Mono\\fs34\\b1}}{label}\\N{{\\fnArchivo Black\\fs92\\b0}}{value}{u}{n}"


def hud_events(shot, start, slot_y):
    out = []
    end = start + shot["duration"]
    y = slot_y
    for h in shot.get("hud", []) or []:
        kind = h.get("kind", "counter")
        if kind == "counter":
            pos = f"{{\\pos(64,{y})}}"
            if "value" in h:
                out.append(ev(start, end, "Hud", pos + counter_text(h["label"], fmt_num(h["value"]), h.get("unit", ""),
                                                                   h.get("note"))))
            else:
                a = start + h.get("at", 0)
                b = a + h.get("dur", 1.0)
                v0, v1 = h["from"], h["to"]
                out.append(ev(start, a, "Hud", pos + counter_text(h["label"], fmt_num(v0), h.get("unit", ""))))
                frames = max(1, int((b - a) * FPS))
                for i in range(frames):
                    t0 = a + i / FPS
                    v = v0 + (v1 - v0) * ease_out((i + 1) / frames)
                    out.append(ev(t0, t0 + 1 / FPS, "Hud", pos + counter_text(h["label"], fmt_num(v), h.get("unit", ""),
                                                                              h.get("note"))))
                out.append(ev(b, end, "Hud", pos + counter_text(h["label"], fmt_num(v1), h.get("unit", ""), h.get("note"))))
            y += 150
        elif kind == "location":
            out.append(ev(start, end, "Small", f"{{\\pos(64,172)}}{h['text']}"))
        elif kind == "clock":
            t0 = sum(int(p) * m for p, m in zip(h["from"].split(":"), (3600, 60, 1)))
            t1 = sum(int(p) * m for p, m in zip(h["to"].split(":"), (3600, 60, 1)))
            stop = start + h.get("stop_at", shot["duration"])
            span = max(stop - start, 0.01)
            sec = t0
            cur = start
            while cur < end - 1e-6:
                frac = min((cur - start) / span, 1.0)
                sec = int(t0 + (t1 - t0) * frac)
                hh, rem = divmod(sec, 3600)
                mm, ss = divmod(rem, 60)
                nxt = min(end, cur + 0.25)
                out.append(ev(cur, nxt, "Small", f"{{\\pos(64,172)}}CLOCK {hh:02d}:{mm:02d}:{ss:02d}"))
                cur = nxt
        elif kind == "tag":
            a = start + h.get("at", 0)
            out.append(ev(a, min(end, a + h.get("dur", shot["duration"])), "Tag", f"{{\\pos(70,{y + 10})}}{h['text']}"))
        elif kind == "prompt":
            a = start + h.get("at", 0)
            out.append(ev(a, end, "Prompt", f"{{\\pos(540,780)\\fad(250,0)}}{h['text']}"))
    return out


def chunk_words(text, max_words=3, max_chars=16):
    words = text.split()
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or len(" ".join(cur + [w])) > max_chars):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if w.endswith((".", "?", "!", ",", ":")):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def styled_word(w):
    core = re.sub(r"[^\w']", "", w).lower()
    if re.search(r"\d", w) or core in NUMBER_WORDS:
        return f"{{\\c{MAGENTA}}}{w}{{\\c{WHITE}}}"
    return w


def caption_events(lines):
    out = []
    for ln in lines:
        chunks = chunk_words(ln["text"])
        weights = [sum(len(w) + 2 for w in c) for c in chunks]
        total = sum(weights)
        t = ln["start"]
        for c, wgt in zip(chunks, weights):
            d = ln["dur"] * wgt / total
            text = " ".join(styled_word(w) for w in c).upper()
            text = re.sub(r"\\C&H", r"\\c&H", text)  # keep override tags lower-case after upper()
            text = text.replace("\\C", "\\c")
            out.append(ev(t, t + max(d, 0.25), "Caption",
                          f"{{\\pos(540,1230)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{text}"))
            t += d
    return out


def callout_events(callouts_path, start):
    p = Path(callouts_path)
    if not p.exists():
        return []
    data = json.loads(p.read_text())
    out = []
    for actor in data.values():
        for fr, x, y, vis in actor["frames"]:
            if not vis:
                continue
            t = start + (fr - 1) / FPS
            out.append(ev(t, t + 1 / FPS, "Callout", f"{{\\pos({x * W:.0f},{(1 - y) * H - 12:.0f})}}{actor['label']}", 2))
    return out


def build(video, lines, callout_dirs, out_path):
    events = []
    t = 0.0
    for shot in video["shots"]:
        events += hud_events(shot, t, 225)
        if shot["id"] in callout_dirs:
            events += callout_events(Path(callout_dirs[shot["id"]]) / "callouts.json", t)
        t += shot["duration"]
    events += caption_events(lines)
    Path(out_path).write_text(HEADER + "\n".join(events) + "\n", encoding="utf-8")
    return len(events)
