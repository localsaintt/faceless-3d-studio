"""Obsidian integration: the video note is the owner's control panel.

- The note's frontmatter `status` is the approval gate the studio obeys.
- The block between STUDIO markers is regenerated from video.yaml (script, storyboard, QC, preview).
- Everything outside the markers (e.g. "## Your notes") belongs to the owner and is never touched.
"""
import datetime as dt
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- STUDIO:BEGIN (generated from video.yaml - edits here are overwritten) -->", "<!-- STUDIO:END -->"
STATUSES = ["idea", "script-review", "script-approved", "rendering", "ready-for-review", "approved", "archived", "posted"]


def note_path(video_id):
    return ROOT / "videos" / video_id / f"{video_id}.md"


def read_front(path):
    if not path.exists():
        return {}, ""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, text)


def status(video_id):
    return read_front(note_path(video_id))[0].get("status", "script-review")


def set_status(video_id, new):
    assert new in STATUSES, new
    path = note_path(video_id)
    front, body = read_front(path)
    front["status"] = new
    front["updated"] = dt.date.today().isoformat()
    path.write_text("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n" + body, encoding="utf-8")


def _fmt_t(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def generated_block(video, qc_md=None, media=None):
    shots = video["shots"]
    total = sum(s["duration"] for s in shots)
    lines = [BEGIN, "",
             f"> **Premise:** {video['premise'].strip()}", "",
             f"**Format:** {video['format']} · **Length:** {total:.1f} s · **Shots:** {len(shots)} · "
             f"**Voice:** {video.get('voice')} (local Kokoro) · **Audience:** {video.get('audience')}", "",
             f"**Comment prompt:** {video.get('comment_prompt', '')}  ", f"**Running gag:** {video.get('running_gag', '')}", "",
             "## Script", "", "| # | Time | Narration | On screen |", "|---|---|---|---|"]
    t = 0.0
    for s in shots:
        hud = "; ".join(h.get("text") or f"{h.get('label')}: {h.get('value', str(h.get('from')) + ' → ' + str(h.get('to')))} {h.get('unit', '')}".strip()
                        for h in s.get("hud", []) or [])
        lines.append(f"| {s['id']} | {_fmt_t(t)}–{_fmt_t(t + s['duration'])} | {s.get('vo', '')} | {hud} |")
        t += s["duration"]
    lines += ["", "## Storyboard", "", "| # | Set | Camera | Action / effects | Sound |", "|---|---|---|---|---|"]
    for s in shots:
        acts = ", ".join(f"{a['id']} ({a['type']})" for a in s.get("actors", []) or [])
        fx = ", ".join(e["type"] for e in s.get("effects", []) or [])
        snd = ", ".join(c["id"] for c in s.get("sfx", []) or [])
        lines.append(f"| {s['id']} | {s['set']} | {s['camera']['move']} | {'; '.join(x for x in (acts, fx) if x)} | {snd} |")
    lines += ["", "## Science check", "", video.get("science", "").strip(), ""]
    if media:
        lines += ["## Latest render", "", f"![[{media['video']}]]", "", f"![[{media['sheet']}]]", ""]
    if qc_md:
        lines += ["## Quality check", "", qc_md, ""]
    lines += [END]
    return "\n".join(lines)


def write_note(video, qc_md=None, media=None):
    path = note_path(video["id"])
    front, body = read_front(path)
    front.setdefault("status", "script-review")
    front.update({"title": video["title"], "format": video["format"],
                  "length_s": round(sum(s["duration"] for s in video["shots"]), 1),
                  "updated": dt.date.today().isoformat()})
    block = generated_block(video, qc_md, media)
    if BEGIN in body and END in body:
        body = body[:body.index(BEGIN)] + block + body[body.index(END) + len(END):]
    else:
        body = (f"\n# {video['title']}\n\n**How approval works:** change `status` above. "
                "`script-review` → `script-approved` lets the studio render the final video; after watching it, "
                "`ready-for-review` → `approved` lets it archive the file. The studio never posts anything.\n\n"
                + block + "\n\n## Your notes\n\n- \n")
    path.write_text("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n" + body, encoding="utf-8")
    return path
