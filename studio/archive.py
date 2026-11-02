"""Archive an APPROVED video to iCloud Drive and free local space.

    .venv/bin/python -m studio.archive slow-sound-miami

Only runs when the note's status is `approved`. Moves the final MP4 to
iCloud Drive/Faceless Studio Archive/ (finished files are fine in iCloud; renders in progress are not),
deletes that video's intermediate render files, and sets status: archived.
"""
import argparse
import shutil
from pathlib import Path

from studio import notes

ROOT = Path(__file__).resolve().parent.parent
ICLOUD = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Faceless Studio Archive"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_id")
    a = ap.parse_args()
    st = notes.status(a.video_id)
    if st != "approved":
        raise SystemExit(f"Not archived: status is '{st}'. Watch the video and set status: approved in the note first.")
    media = ROOT / "videos" / a.video_id / "media"
    finals = sorted(media.glob(f"{a.video_id}_final*.mp4"))
    if not finals:
        raise SystemExit("No final render found in the note's media folder. Run make_video with --profile final.")
    if not ICLOUD.parent.exists():
        raise SystemExit(f"iCloud Drive not found at {ICLOUD.parent}. Is iCloud Drive turned on?")
    ICLOUD.mkdir(exist_ok=True)
    for f in finals:
        dest = ICLOUD / f.name
        shutil.copy2(f, dest)
        if dest.stat().st_size == f.stat().st_size:
            f.unlink()
            print(f"Archived {f.name} -> {dest}")
    work = ROOT / "output" / "videos" / a.video_id
    freed = sum(p.stat().st_size for p in work.rglob("*") if p.is_file()) / 1e9 if work.exists() else 0
    shutil.rmtree(work, ignore_errors=True)
    notes.set_status(a.video_id, "archived")
    print(f"Freed {freed:.1f} GB of intermediate files. Status: archived.")


if __name__ == "__main__":
    main()
