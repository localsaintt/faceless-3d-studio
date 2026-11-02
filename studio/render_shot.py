"""Render one shot spec and assemble it into an MP4 (plus a contact sheet for QC).

    .venv/bin/python -m studio.render_shot shots/proto/s01_beach_establishing.yaml --profile preview
    .venv/bin/python -m studio.render_shot shots/proto/s01_beach_establishing.yaml --still 1 72

Blender runs in a separate process (one shot per process keeps memory low on an 8 GB Mac).
On macOS the render is wrapped in `caffeinate -i` so the Mac does not sleep mid-render.
"""
import argparse
import json
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 24


def run_blender(spec, profile, out, stills=None, save_blend=False, frames=None):
    cmd = [sys.executable, str(ROOT / "blender" / "build_shot.py"),
           "--spec", str(spec), "--profile", profile, "--out", str(out)]
    if frames:
        cmd += ["--frames", str(frames)]
    if stills:
        cmd += ["--still", *map(str, stills)]
    if save_blend:
        cmd.append("--save-blend")
    if platform.system() == "Darwin" and shutil.which("caffeinate"):
        cmd = ["caffeinate", "-i", *cmd]
    t = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    report = None
    for line in proc.stdout.splitlines():
        if line.startswith("RENDER_REPORT "):
            report = json.loads(line[len("RENDER_REPORT "):])
    if proc.returncode != 0 or report is None:
        log = out / "blender_error.log"
        log.write_text(proc.stdout[-20000:] + "\n--- stderr ---\n" + proc.stderr[-20000:])
        raise SystemExit(f"Blender failed (exit {proc.returncode}). See {log}")
    report["wall_s"] = round(time.time() - t, 1)
    return report


def assemble(frames_dir, mp4, frame_step=1, upscale_to=None):
    """PNG sequence -> H.264 MP4. Preview profiles render every Nth frame, so the rate is divided."""
    rate = FPS / frame_step
    vf = []
    if upscale_to:
        vf.append(f"scale={upscale_to[0]}:{upscale_to[1]}:flags=lanczos")
    vf.append("format=yuv420p")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", f"{rate}", "-pattern_type", "glob",
           "-i", str(frames_dir / "frame_*.png"), "-vf", ",".join(vf), "-r", str(FPS),
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-movflags", "+faststart", str(mp4)]
    subprocess.run(cmd, check=True)


def contact_sheet(mp4, png, cols=6, rows=2):
    """One image of evenly spaced frames, used by Claude (and you) to review a shot at a glance."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                           capture_output=True, text=True, check=True)
    dur = float(probe.stdout.strip())
    n = cols * rows
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    f"fps={n / dur:.4f},scale=270:-1,tile={cols}x{rows}:padding=4:color=white",
                    "-frames:v", "1", str(png)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--profile", default="preview", choices=["preview", "final", "final_720"])
    ap.add_argument("--still", type=int, nargs="*")
    ap.add_argument("--fresh", action="store_true", help="delete previous frames for this shot/profile first")
    ap.add_argument("--save-blend", action="store_true")
    ap.add_argument("--keep-frames", action="store_true",
                    help="keep the PNG frames of final renders (deleted by default to save disk space)")
    a = ap.parse_args()

    spec = Path(a.spec).resolve()
    out = ROOT / "output" / spec.parent.name / spec.stem / a.profile
    if a.fresh and out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    report = run_blender(spec, a.profile, out, a.still, a.save_blend)
    if not a.still:
        sys.path.insert(0, str(ROOT / "blender"))
        from scenekit.render import PROFILES  # pure-Python module; safe to import without bpy
        p = PROFILES[a.profile]
        mp4 = out.parent / f"{spec.stem}_{a.profile}.mp4"
        assemble(out, mp4, p["frame_step"], (1080, 1920) if a.profile == "final_720" else None)
        contact_sheet(mp4, out.parent / f"{spec.stem}_{a.profile}_sheet.png")
        report["video"] = str(mp4.relative_to(ROOT))
    (out.parent / f"{spec.stem}_{a.profile}_report.json").write_text(json.dumps(report, indent=2))
    if not a.still and a.profile != "preview" and not a.keep_frames:
        shutil.rmtree(out)  # the MP4 is assembled; frames are several GB per video
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
