"""Make a complete video from videos/<id>/video.yaml.

    .venv/bin/python -m studio.make_video slow-sound-miami                  # preview (half-res, fast)
    .venv/bin/python -m studio.make_video slow-sound-miami --profile final  # needs status: script-approved
    .venv/bin/python -m studio.make_video slow-sound-miami --shots s03 s04  # re-render only these shots

Pipeline: note sync -> narration + sound mix -> render each shot (cached) -> join shots ->
captions/counters/callouts -> loudness-normalised mux -> QC -> Obsidian note updated.
Nothing is ever posted. Final renders require the owner's approval in the note.
"""
import argparse
import json
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

from studio import notes, overlays, qc
from studio.audio import mix
from studio.render_shot import contact_sheet

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "blender"))
from scenekit.render import FPS, PROFILES  # noqa: E402  (pure Python, no bpy)

MIN_FREE_GB = 15


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, **kw)
    if r.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-3000:]}")
    return r


def render_shot(video_yaml, shot, profile, shot_dir, keep_frames):
    frames = shot_dir / "frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir(parents=True)
    cmd = [sys.executable, str(ROOT / "blender" / "build_shot.py"), "--video", str(video_yaml), "--shot", shot["id"],
           "--profile", profile, "--out", str(frames)]
    if platform.system() == "Darwin" and shutil.which("caffeinate"):
        cmd = ["caffeinate", "-i", *cmd]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    rep = next((json.loads(l[14:]) for l in r.stdout.splitlines() if l.startswith("RENDER_REPORT ")), None)
    if r.returncode != 0 or rep is None:
        (shot_dir / "blender_error.log").write_text(r.stdout[-20000:] + "\n--- stderr ---\n" + r.stderr[-20000:])
        raise SystemExit(f"Shot {shot['id']} failed. See {shot_dir / 'blender_error.log'}")
    step = PROFILES[profile]["frame_step"]
    mp4 = shot_dir / f"{shot['id']}.mp4"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS / step), "-pattern_type", "glob",
        "-i", str(frames / "frame_*.png"), "-vf", "tpad=stop_mode=clone:stop_duration=1,format=yuv420p",
        "-t", f"{shot['duration']:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "17", str(mp4)])
    for f in ("callouts.json", "render_report.json"):
        if (frames / f).exists():
            shutil.copy(frames / f, shot_dir / f)
    if not keep_frames:
        shutil.rmtree(frames)
    return mp4, rep


def loudnorm_args(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, cwd=ROOT)
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    return (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_id")
    ap.add_argument("--profile", default="preview", choices=list(PROFILES))
    ap.add_argument("--shots", nargs="*", help="re-render only these shots (others are reused if present)")
    ap.add_argument("--fresh", action="store_true", help="re-render every shot")
    ap.add_argument("--keep-frames", action="store_true")
    a = ap.parse_args()

    vdir = ROOT / "videos" / a.video_id
    vyaml = vdir / "video.yaml"
    video = yaml.safe_load(vyaml.read_text())
    final = a.profile.startswith("final")
    st = notes.status(a.video_id)
    if final and st not in ("script-approved", "rendering", "ready-for-review", "approved"):
        raise SystemExit(f"Final render blocked: the note's status is '{st}'. Review the script in Obsidian "
                         f"(videos/{a.video_id}/{a.video_id}.md) and set status: script-approved.")
    free_gb = shutil.disk_usage(ROOT).free / 1e9
    if free_gb < MIN_FREE_GB and final:
        raise SystemExit(f"Only {free_gb:.0f} GB free; need {MIN_FREE_GB} GB. Free some space and re-run.")
    notes.write_note(video)
    if final:
        notes.set_status(a.video_id, "rendering")

    out = ROOT / "output" / "videos" / a.video_id / a.profile
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    report = []

    print("1/6 narration + sound design")
    lines, total = mix.build(video, out / "mix.wav", report)

    print(f"2/6 rendering {len(video['shots'])} shots ({a.profile})")
    shot_dirs, renders = {}, {}
    for shot in video["shots"]:
        sdir = out / "shots" / shot["id"]
        sdir.mkdir(parents=True, exist_ok=True)
        shot_dirs[shot["id"]] = sdir
        mp4 = sdir / f"{shot['id']}.mp4"
        wanted = a.fresh or not mp4.exists() or (a.shots is not None and shot["id"] in a.shots)
        if wanted:
            ts = time.time()
            _, rep = render_shot(vyaml, shot, a.profile, sdir, a.keep_frames)
            renders[shot["id"]] = rep
            print(f"   {shot['id']}: {rep['frames']} frames, {rep['steady_s_per_frame']}s/frame, {time.time() - ts:.0f}s")
        else:
            print(f"   {shot['id']}: reused")

    print("3/6 joining shots")
    lst = out / "concat.txt"
    lst.write_text("".join(f"file '{shot_dirs[s['id']] / (s['id'] + '.mp4')}'\n" for s in video["shots"]))
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
        str(out / "picture.mp4")])

    print("4/6 captions, counters and labels")
    n_events = overlays.build(video, lines, shot_dirs, out / "overlays.ass")

    print("5/6 final mix + export (1080x1920, -14 LUFS)")
    final_mp4 = out / f"{a.video_id}_{a.profile}.mp4"
    fonts = (ROOT / "assets" / "fonts").relative_to(ROOT)
    ass = (out / "overlays.ass").relative_to(ROOT)
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out / "picture.mp4"), "-i", str(out / "mix.wav"),
        "-filter_complex",
        f"[0:v]scale=1080:1920:flags=lanczos,ass={ass}:fontsdir={fonts},format=yuv420p[v];[1:a]{loudnorm_args(out / 'mix.wav')},alimiter=limit=0.79:attack=2:release=50:level=false,aresample=48000[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final_mp4)])
    sheet = out / f"{a.video_id}_{a.profile}_sheet.png"
    contact_sheet(final_mp4, sheet, cols=6, rows=3)

    print("6/6 quality check")
    result = qc.run(final_mp4, video, a.profile, report)
    (out / "qc.json").write_text(json.dumps(result, indent=2))
    media_dir = vdir / "media"
    media_dir.mkdir(exist_ok=True)
    shutil.copy(final_mp4, media_dir / final_mp4.name)
    shutil.copy(sheet, media_dir / sheet.name)
    qc_md = qc.to_markdown(result) + f"\n_Profile: {a.profile} · overlay events: {n_events} · built in {(time.time() - t0) / 60:.1f} min_\n"
    notes.write_note(video, qc_md, {"video": f"media/{final_mp4.name}", "sheet": f"media/{sheet.name}"})
    if final:
        notes.set_status(a.video_id, "ready-for-review" if result["verdict"] != "FAIL" else "script-approved")

    print(f"\n{result['verdict']} - {final_mp4.relative_to(ROOT)} ({result['duration']} s) in {(time.time() - t0) / 60:.1f} min")
    for c in result["checks"]:
        if c["status"] != "PASS":
            print(f"  [{c['status']}] {c['check']}: {c['detail']}")
    if platform.system() == "Darwin":
        subprocess.run(["open", str(final_mp4)])


if __name__ == "__main__":
    main()
