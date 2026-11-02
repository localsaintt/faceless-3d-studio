"""Stage C benchmark: real render speed on this machine, plus a native-vs-upscaled A/B clip.

    .venv/bin/python -m studio.benchmark            # 48 frames (2 s) at each resolution
    .venv/bin/python -m studio.benchmark --frames 96

Renders the prototype beach shot at final 1080x1920 and at 720x1280 (upscaled to 1080x1920),
prints seconds per frame, how much the Mac slowed down during the run (fanless Macs throttle),
and the estimated time for a 70-second video. Writes logs/benchmark_<time>.json.
"""
import argparse
import json
import shutil
import subprocess
import time

from studio.doctor import PROTO, ROOT
from studio.render_shot import assemble, run_blender

FRAMES_70S = 70 * 24


def one(profile, frames):
    out = ROOT / "output" / "benchmark" / profile
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    rep = run_blender(PROTO, profile, out, frames=frames)
    mp4 = ROOT / "output" / "benchmark" / f"benchmark_{profile}.mp4"
    assemble(out, mp4, 1, (1080, 1920) if profile == "final_720" else None)
    shutil.rmtree(out)
    rep["video"] = str(mp4.relative_to(ROOT))
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=48)
    a = ap.parse_args()
    results = {}
    for profile in ("final", "final_720"):
        print(f"Rendering {a.frames} frames at {profile}... (the Mac will get warm; that's expected)")
        t = time.time()
        r = one(profile, a.frames)
        r["wall_min"] = round((time.time() - t) / 60, 1)
        results[profile] = r
        slow = r["last5_s_per_frame"] / max(r["steady_s_per_frame"], 0.01)
        print(f"  {profile}: {r['steady_s_per_frame']}s/frame (first {r['first_frame_s']}s, last five "
              f"{r['last5_s_per_frame']}s -> {'slowing down ' + format(slow, '.1f') + 'x' if slow > 1.15 else 'steady'}), "
              f"peak memory {r['peak_mem_mb']} MB")
        print(f"  70 s video at this speed: ~{r['last5_s_per_frame'] * FRAMES_70S / 3600:.1f} h")
    log = ROOT / "logs" / f"benchmark_{time.strftime('%Y%m%d_%H%M%S')}.json"
    log.write_text(json.dumps(results, indent=2))
    print(f"\nCompare the two clips (native vs 720p upscaled):\n  open {results['final']['video']}\n"
          f"  open {results['final_720']['video']}\nReport saved to {log.relative_to(ROOT)}")
    try:
        subprocess.run(["open", str(ROOT / results["final"]["video"]), str(ROOT / results["final_720"]["video"])],
                       check=False)
    except FileNotFoundError:
        pass  # not on a Mac


if __name__ == "__main__":
    main()
