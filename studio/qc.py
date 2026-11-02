"""Automated quality control for a finished video. Produces qc.json + a Markdown report.

Checks: format (1080x1920, 24 fps, H.264 + AAC), length (>= 61 s for TikTok Creator Rewards),
black frames, frozen video, loudness (-14 LUFS +/-1, true peak <= -1 dBTP), long silences,
narration fit, and originality versus this studio's own other videos (script overlap, reused camera paths).
"""
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(mp4):
    r = _run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(mp4)])
    return json.loads(r.stdout)


def _filters(mp4):
    r = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4),
              "-vf", "blackdetect=d=0.1:pix_th=0.08,freezedetect=n=0.0005:d=1.5",
              "-af", "silencedetect=n=-45dB:d=1.2,ebur128=peak=true", "-f", "null", "-"])
    log = r.stderr
    black = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)
    frozen = re.findall(r"freeze_start: ([\d.]+)", log)
    silence = re.findall(r"silence_start: ([\d.]+)", log)
    summary = log[log.rfind("Summary:"):] if "Summary:" in log else ""
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    peak = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    return {
        "black": [(float(a), float(b)) for a, b in black],
        "frozen_starts": [float(x) for x in frozen],
        "silence_starts": [float(x) for x in silence],
        "lufs": float(lufs.group(1)) if lufs else None,
        "true_peak": float(peak.group(1)) if peak and peak.group(1) != "-inf" else None,
    }


def _trigrams(text):
    w = re.findall(r"[a-z']+", text.lower())
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}


def originality(video, videos_dir=ROOT / "videos"):
    me = video["id"]
    my_script = " ".join(s.get("vo", "") for s in video["shots"])
    my_tri = _trigrams(my_script)
    my_cams = {json.dumps(s["camera"], sort_keys=True) for s in video["shots"]}
    findings = []
    for other in videos_dir.glob("*/video.yaml"):
        o = yaml.safe_load(other.read_text())
        if o.get("id") == me:
            continue
        tri = _trigrams(" ".join(s.get("vo", "") for s in o["shots"]))
        if my_tri and tri:
            overlap = len(my_tri & tri) / len(my_tri)
            if overlap > 0.15:
                findings.append(f"script overlaps {overlap:.0%} with {o['id']}")
        same = my_cams & {json.dumps(s["camera"], sort_keys=True) for s in o["shots"]}
        if same:
            findings.append(f"{len(same)} camera path(s) identical to {o['id']}")
        if video["shots"][0]["camera"] == o["shots"][0]["camera"]:
            findings.append(f"opening shot identical to {o['id']}")
    return findings


def run(mp4, video, profile, notes):
    info = probe(mp4)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    num, den = map(int, v["r_frame_rate"].split("/"))
    fl = _filters(mp4)
    checks = []

    def add(name, ok, detail, level="FAIL"):
        checks.append({"check": name, "status": "PASS" if ok else level, "detail": detail})

    final = profile.startswith("final")
    add("resolution", (v["width"], v["height"]) == (1080, 1920), f"{v['width']}x{v['height']}",
        "FAIL" if final else "INFO")
    add("frame rate", abs(num / den - 24) < 0.01, f"{num / den:.2f} fps")
    add("codecs", v["codec_name"] == "h264" and a is not None and a["codec_name"] == "aac",
        f"{v['codec_name']} / {a['codec_name'] if a else 'no audio'}")
    add("length >= 61 s", dur >= 61.0, f"{dur:.2f} s (TikTok Creator Rewards needs > 1 min)", "WARN")
    add("no black frames", not fl["black"], f"{fl['black'] or 'none'}")
    add("no frozen video", not fl["frozen_starts"], f"{fl['frozen_starts'] or 'none'}", "WARN")
    lufs, tp = fl["lufs"], fl["true_peak"]
    add("loudness -14 LUFS", lufs is not None and -15.5 <= lufs <= -12.5, f"{lufs} LUFS integrated", "WARN")
    add("true peak <= -1 dBTP", tp is not None and tp <= -0.9, f"{tp} dBTP", "WARN")
    add("no long silences", not fl["silence_starts"], f"{fl['silence_starts'] or 'none'}", "WARN")
    narr = [n for n in notes if n.startswith("WARN")]
    add("narration fits shots", not narr, "; ".join(narr) or "all lines fit", "WARN")
    orig = originality(video)
    add("originality vs own videos", not orig, "; ".join(orig) or "no overlap with other videos", "WARN")
    verdict = "FAIL" if any(c["status"] == "FAIL" for c in checks) else (
        "PASS with warnings" if any(c["status"] == "WARN" for c in checks) else "PASS")
    return {"verdict": verdict, "duration": round(dur, 2), "checks": checks, "notes": notes}


def to_markdown(qc):
    rows = "\n".join(f"| {c['check']} | {c['status']} | {c['detail']} |" for c in qc["checks"])
    return f"**Verdict: {qc['verdict']}** · length {qc['duration']} s\n\n| Check | Result | Detail |\n|---|---|---|\n{rows}\n"
