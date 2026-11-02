"""Build the full soundtrack for a video from its spec: beds, effects, narration, ducking.

The "slow sound" window muffles the world (low-pass + quieter beds) between the drop and the snap,
because in-story sound is still crawling through the air.
"""
import math

import numpy as np
import soundfile as sf

from . import synth, tts

SR = synth.SR


def resample(y, sr_in, sr_out=SR):
    if sr_in == sr_out:
        return y.astype(np.float32)
    n_out = int(len(y) * sr_out / sr_in)
    return np.interp(np.linspace(0, len(y) - 1, n_out), np.arange(len(y)), y).astype(np.float32)


def place(track, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(track) or len(clip) == 0:
        return
    if i < 0:
        clip, i = clip[-i:], 0
    n = min(len(clip), len(track) - i)
    track[i:i + n] += clip[:n] * gain


def timeline(video):
    t, out = 0.0, []
    for s in video["shots"]:
        out.append((s, t))
        t += s["duration"]
    return out, t


def narration(video, report):
    """Synthesize every line, fitted to its shot. Returns list of (shot_id, start_s, samples, words)."""
    lines = []
    for shot, start in timeline(video)[0]:
        text = shot.get("vo")
        if not text:
            continue
        lead = shot.get("vo_delay", 0.2)
        y, sr, speed, fits = tts.fit_line(text, shot["duration"] - lead - 0.15, video.get("voice", "am_michael"),
                                          video.get("voice_speed", 1.0))
        y = resample(y, sr)
        lines.append({"shot": shot["id"], "start": start + lead, "dur": len(y) / SR, "text": text, "audio": y,
                      "speed": speed})
        if not fits:
            report.append(f"WARN narration for {shot['id']} is {len(y) / SR:.2f}s, longer than the shot allows")
        elif speed > video.get("voice_speed", 1.0):
            report.append(f"INFO narration for {shot['id']} sped up to {speed:.2f}x to fit")
    return lines


def kid_yell(voice="af_sky"):
    y, sr = tts.say("Mom!", voice, 1.0)
    y = resample(y, sr * 1.18)  # pitch/speed up -> younger voice
    return synth.bandpass(y, 250, 5000) * 0.8


def build(video, out_wav, report):
    shots, total = timeline(video)
    n = int(math.ceil(total * SR)) + SR
    beds = np.zeros(n, dtype=np.float32)
    fx = np.zeros(n, dtype=np.float32)
    vo = np.zeros(n, dtype=np.float32)

    # beds per shot with short crossfades at cuts
    bed_cache = {}
    for shot, start in shots:
        kit = video["sets"][shot["set"]]["kit"]
        if kit not in bed_cache:
            bed_cache[kit] = synth.beach_bed(total + 2) if kit == "beach" else synth.street_bed(total + 2)
        seg = bed_cache[kit][int(start * SR): int((start + shot["duration"]) * SR) + int(0.08 * SR)].copy()
        fade = int(0.08 * SR)
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
        place(beds, seg, start)

    # the slow window: from the drop (first 'drop_sweep') to the snap ('riser' end) the world is muffled
    drop = next((start + c["at"] for shot, start in shots for c in shot.get("sfx", []) if c["id"] == "drop_sweep"), None)
    snap = next((start + c.get("snap_after", 2.2) for shot, start in shots for c in shot.get("sfx", [])
                 if c["id"] == "riser"), None)
    if drop is not None and snap is not None and snap > drop:
        a, b = int(drop * SR), int(snap * SR)
        muffled = synth.bandpass(beds[a:b], None, 380) * 0.55
        ramp = min(int(0.6 * SR), (b - a) // 4)
        w = np.ones(b - a, dtype=np.float32)
        w[:ramp] = np.linspace(0, 1, ramp)
        beds[a:b] = beds[a:b] * (1 - w) + muffled * w

    # one-shot effects
    for shot, start in shots:
        for c in shot.get("sfx", []):
            sid = c["id"]
            t = start + c["at"]
            if sid == "big_boom":
                clip, pre = synth.big_boom()
                place(fx, clip, t - pre, c.get("gain", 1.0))
            elif sid == "kid_yell":
                place(fx, kid_yell(), t, c.get("gain", 0.9))
            elif sid in synth.ONE_SHOTS:
                place(fx, synth.ONE_SHOTS[sid](), t, c.get("gain", 1.0))
            else:
                report.append(f"WARN unknown sfx '{sid}' in {shot['id']}")

    lines = narration(video, report)
    for ln in lines:
        place(vo, ln["audio"], ln["start"])

    # duck beds under narration (-9 dB), smoothed
    env = np.abs(vo)
    k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = 1 - 0.65 * np.clip(env / (env.max() + 1e-9) * 6, 0, 1)
    mix = beds * 0.55 * duck + fx * 0.9 + vo * 1.0
    mix = np.tanh(mix * 1.1) / 1.1  # gentle safety saturation; final loudness is set by ffmpeg loudnorm
    stereo = np.stack([mix, np.roll(mix, int(0.0004 * SR)) * 0.98 + mix * 0.02], axis=1)
    sf.write(out_wav, stereo[: int(total * SR)], SR, subtype="FLOAT")
    return lines, total
