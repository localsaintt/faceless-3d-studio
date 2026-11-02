"""Local narration with Kokoro-82M (Apache-2.0) via kokoro-onnx. No account, no API, no cost.

Lines are cached by (text, voice, speed), so re-running a video only synthesises changed lines.
"""
import hashlib
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "models" / "kokoro" / "kokoro-v1.0.onnx"
VOICES = ROOT / "models" / "kokoro" / "voices-v1.0.bin"
CACHE = ROOT / "output" / "cache" / "tts"
_engine = None


def _kokoro():
    global _engine
    if _engine is None:
        if not MODEL.exists():
            raise SystemExit("Narration model missing. Run: bash setup/mac_setup.sh (downloads models/kokoro/)")
        from kokoro_onnx import Kokoro
        _engine = Kokoro(str(MODEL), str(VOICES))
    return _engine


def say(text, voice="am_michael", speed=1.0, lang="en-us"):
    """Return (samples float32 mono, sample_rate). Cached on disk."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha1(f"{voice}|{speed:.3f}|{lang}|{text}".encode()).hexdigest()[:16]
    path = CACHE / f"{key}.wav"
    if path.exists():
        y, sr = sf.read(path, dtype="float32")
        return y, sr
    y, sr = _kokoro().create(text, voice=voice, speed=speed, lang=lang)
    y = np.asarray(y, dtype=np.float32)
    # trim leading/trailing near-silence so timing is tight
    idx = np.where(np.abs(y) > 0.01)[0]
    if len(idx):
        y = y[max(0, idx[0] - int(0.03 * sr)): idx[-1] + int(0.08 * sr)]
    sf.write(path, y, sr)
    return y, sr


def fit_line(text, max_seconds, voice, base_speed=1.0, max_speed=1.18):
    """Synthesize a line; if it is longer than the shot allows, speak a little faster (up to max_speed)."""
    y, sr = say(text, voice, base_speed)
    speed = base_speed
    while len(y) / sr > max_seconds and speed < max_speed - 1e-6:
        speed = min(max_speed, speed + 0.06)
        y, sr = say(text, voice, speed)
    return y, sr, speed, len(y) / sr <= max_seconds
