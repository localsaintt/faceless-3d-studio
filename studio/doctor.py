"""Environment check + speed test. Run after setup, and whenever something seems off:

    .venv/bin/python -m studio.doctor            # checks + one timed preview frame
    .venv/bin/python -m studio.doctor --quick    # checks only

Writes logs/doctor_<timestamp>.json so render speed on this machine is on record.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / "shots" / "proto" / "s01_beach_establishing.yaml"
results = []


def check(name, status, detail):
    results.append({"check": name, "status": status, "detail": detail})
    print(f"[{status:4}] {name}: {detail}")


def ram_gb():
    try:
        if platform.system() == "Darwin":
            return int(subprocess.check_output(["sysctl", "-n", "hw.memsize"])) / 1e9
        for line in open("/proc/meminfo"):
            if line.startswith("MemTotal"):
                return int(line.split()[1]) / 1e6
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()

    check("machine", "OK" if (platform.system(), platform.machine()) == ("Darwin", "arm64") else "INFO",
          f"{platform.system()} {platform.machine()} {platform.mac_ver()[0] or platform.release()}")
    v = sys.version_info
    check("python", "OK" if (v.major, v.minor) == (3, 13) else "FAIL", f"{v.major}.{v.minor}.{v.micro} (bpy 5.2 needs 3.13)")
    try:
        import bpy  # noqa: F401
        check("blender (bpy)", "OK" if bpy.app.version[:2] == (5, 2) else "WARN", bpy.app.version_string)
    except Exception as e:  # pragma: no cover
        check("blender (bpy)", "FAIL", f"cannot import bpy: {e}")
    try:
        import yaml  # noqa: F401
        check("pyyaml", "OK", "installed")
    except ImportError:
        check("pyyaml", "FAIL", "missing: pip install pyyaml")
    for tool in ("ffmpeg", "ffprobe"):
        path = shutil.which(tool)
        if path:
            ver = subprocess.run([tool, "-version"], capture_output=True, text=True).stdout.split("\n")[0]
            check(tool, "OK", ver[:60])
        else:
            check(tool, "FAIL", "not found (macOS: brew install ffmpeg)")
    ram = ram_gb()
    check("memory", "OK" if ram and ram >= 15 else "WARN" if ram else "INFO",
          f"{ram:.0f} GB" + (" - fine with the lightweight render profiles" if ram and ram < 15 else "") if ram else "unknown")
    free = shutil.disk_usage(ROOT).free / 1e9
    check("disk free", "OK" if free >= 30 else "WARN" if free >= 15 else "FAIL", f"{free:.0f} GB (need ~20-30 GB)")
    home = str(Path.home())
    synced = any(str(ROOT).startswith(os.path.join(home, d)) for d in ("Desktop", "Documents", "Library/Mobile Documents"))
    check("iCloud", "WARN" if synced else "OK",
          f"{ROOT} " + ("may be synced to iCloud - move it to ~/Projects" if synced else "is outside iCloud-synced folders"))

    if not a.quick and not any(r["status"] == "FAIL" for r in results):
        print("\nSpeed test: building the prototype beach shot and rendering one preview frame...")
        from studio.render_shot import run_blender
        out = ROOT / "output" / "doctor"
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True)
        t = time.time()
        rep = run_blender(PROTO, "preview", out, stills=[1])
        spf = rep["s_per_frame"]
        # rough scaling to a final frame: 4x pixels, 3x samples; EEVEE scales sub-linearly, so use x6
        final_spf = spf * 6
        est_h = final_spf * 70 * 24 / 3600
        check("speed test", "OK", f"preview frame {spf:.1f}s, peak memory {rep['peak_mem_mb']} MB, "
                                  f"wall {time.time() - t:.0f}s")
        check("estimate", "INFO", f"~{final_spf:.0f}s per final 1080x1920 frame -> ~{est_h:.1f} h for a 70 s video "
                                  f"(rough; replaced by real measurements in Stage C)")

    log = ROOT / "logs" / f"doctor_{time.strftime('%Y%m%d_%H%M%S')}.json"
    log.parent.mkdir(exist_ok=True)
    log.write_text(json.dumps(results, indent=2))
    fails = sum(r["status"] == "FAIL" for r in results)
    print(f"\n{'ALL GOOD' if not fails else f'{fails} problem(s) to fix'} - report saved to {log.relative_to(ROOT)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
