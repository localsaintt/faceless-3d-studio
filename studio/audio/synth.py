"""Procedural, fully original sound design (no samples, so nothing to license).

Every function returns a float32 numpy array at SR (mono unless noted). Filtering is done in the
frequency domain with smooth masks, which keeps everything fast in pure numpy.
"""
import numpy as np

SR = 48000


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _rng(seed):
    return np.random.default_rng(seed)


def bandpass(x, lo=None, hi=None, slope=1.5):
    """Smooth spectral band-pass (lo/hi in Hz; either may be None)."""
    n = len(x)
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(n, 1 / SR) + 1e-6
    g = np.ones_like(fr)
    if lo:
        g *= 1 / (1 + (lo / fr) ** (2 * slope))
    if hi:
        g *= 1 / (1 + (fr / hi) ** (2 * slope))
    return np.fft.irfft(X * g, n).astype(np.float32)


def pink(dur, seed=0):
    n = int(dur * SR)
    X = np.fft.rfft(_rng(seed).standard_normal(n))
    fr = np.fft.rfftfreq(n, 1 / SR)
    fr[0] = 1
    y = np.fft.irfft(X / np.sqrt(fr), n)
    return (y / (np.abs(y).max() + 1e-9)).astype(np.float32)


def brown(dur, seed=0):
    y = np.cumsum(_rng(seed).standard_normal(int(dur * SR)))
    y = bandpass(y.astype(np.float32), lo=20)
    return y / (np.abs(y).max() + 1e-9)


def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.where(t < a, t / max(a, 1e-4), 1.0)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / max(d, 1e-4), e)
    e = np.where((t >= a + d) & (t < dur - r), s, e)
    e = np.where(t >= dur - r, s * np.clip((dur - t) / max(r, 1e-4), 0, 1), e)
    return e.astype(np.float32)


def norm(x, peak=0.9):
    return (x / (np.abs(x).max() + 1e-9) * peak).astype(np.float32)


# ------------------------------------------------------------------ beds
def beach_bed(dur, seed=1):
    """Surf (slow swells of filtered pink noise), soft wind, distant crowd and the odd gull."""
    t = _t(dur)
    surf = bandpass(pink(dur, seed), 80, 1800)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * t / 7.3 + 1) ** 2 * (0.7 + 0.3 * np.sin(2 * np.pi * t / 11.1))
    wash = bandpass(pink(dur, seed + 1), 2500, 9000) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7.3 + 2.4) ** 6)
    crowd = murmur(dur, seed + 2, voices=10) * 0.35
    out = surf * swell * 0.8 + wash * 0.25 + crowd
    rng = _rng(seed + 3)
    for start in rng.uniform(0.5, max(dur - 1, 1), size=max(1, int(dur / 6))):
        g = gull(rng.integers(1e6))
        i = int(start * SR)
        out[i:i + len(g)] += g[:len(out) - i] * 0.18
    return norm(out, 0.5)


def street_bed(dur, seed=5):
    t = _t(dur)
    rumble = bandpass(brown(dur, seed), 30, 300) * 0.6
    hiss = bandpass(pink(dur, seed + 1), 800, 6000) * 0.12
    chatter = murmur(dur, seed + 2, voices=6) * 0.3
    out = rumble + hiss + chatter
    rng = _rng(seed + 3)
    for start in rng.uniform(0, max(dur - 2, 1), size=max(1, int(dur / 5))):
        p = passby(rng.integers(1e6))
        i = int(start * SR)
        out[i:i + len(p)] += p[:len(out) - i] * 0.35
    return norm(out * (0.9 + 0.1 * np.sin(2 * np.pi * t / 5)), 0.5)


def murmur(dur, seed=0, voices=12):
    """Crowd talk: band-limited noise with syllable-rate amplitude modulation per 'voice'."""
    t = _t(dur)
    rng = _rng(seed)
    out = np.zeros_like(t, dtype=np.float32)
    for v in range(voices):
        rate = rng.uniform(3.5, 6.0)
        centre = rng.uniform(350, 1400)
        n = bandpass(rng.standard_normal(len(t)).astype(np.float32), centre * 0.6, centre * 1.8)
        am = np.clip(np.sin(2 * np.pi * rate * t + rng.uniform(0, 6)) + rng.uniform(-0.2, 0.4), 0, None)
        phrase = (np.sin(2 * np.pi * t / rng.uniform(2, 4) + rng.uniform(0, 6)) > -0.3).astype(np.float32)
        out += n * am * phrase
    return norm(out, 0.6)


# ------------------------------------------------------------------ one-shots
def gull(seed=0):
    rng = _rng(seed)
    dur = rng.uniform(0.35, 0.6)
    t = _t(dur)
    f0 = rng.uniform(1400, 1900)
    f = f0 * (1 - 0.35 * t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph + 0.5 * np.sin(2 * np.pi * 30 * t))
    return norm(y * env_adsr(len(t), 0.02, 0.1, 0.6, 0.15), 0.5)


def passby(seed=0, dur=2.2):
    t = _t(dur)
    n = bandpass(_rng(seed).standard_normal(len(t)).astype(np.float32), 120, 2500)
    e = np.exp(-((t - dur / 2) / (dur / 5)) ** 2)
    return norm(n * e, 0.6)


def whistle(dur=0.7):
    """Pea whistle: bright tone with a fast trill."""
    t = _t(dur)
    trill = 1 + 0.06 * np.sign(np.sin(2 * np.pi * 34 * t))
    ph = 2 * np.pi * np.cumsum(2950 * trill) / SR
    y = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.05 * _rng(3).standard_normal(len(t))
    return norm(y * env_adsr(len(t), 0.01, 0.05, 0.85, 0.08), 0.6)


def sonic_boom(strength=1.0, seed=0):
    """N-wave double crack followed by a low rumble tail."""
    dur = 1.6 + 1.2 * strength
    t = _t(dur)
    y = np.zeros_like(t, dtype=np.float32)
    nlen = int(0.11 * SR)
    nwave = np.linspace(1, -1, nlen).astype(np.float32)
    y[:nlen] += nwave
    y[nlen:nlen + 400] += np.linspace(-1, 0, 400)
    crack = bandpass(_rng(seed).standard_normal(len(t)).astype(np.float32), 1500, 9000) * np.exp(-t / 0.02)
    crack2 = np.roll(crack, nlen)
    rumble = bandpass(brown(dur, seed + 1), 25, 140) * np.exp(-t / (0.5 + 0.4 * strength)) * 1.6
    out = y * 0.9 + (crack + crack2) * 0.5 + rumble
    return norm(np.tanh(out * 1.5), min(0.95, 0.6 + 0.25 * strength))


def big_boom():
    """Everything arriving at once: reverse swell into a huge layered impact."""
    pre = 0.8
    swell = bandpass(pink(pre, 9), 200, 6000) * np.linspace(0, 1, int(pre * SR)) ** 3
    hit = sonic_boom(2.2, 11)
    voices = murmur(1.0, 12, voices=30) * np.exp(-_t(1.0) / 0.25)
    out = np.zeros(int(pre * SR) + len(hit), dtype=np.float32)
    out[:len(swell)] += swell * 0.6
    out[int(pre * SR):] += hit
    out[int(pre * SR):int(pre * SR) + len(voices)] += voices * 0.7
    return norm(np.tanh(out * 1.3), 0.98), pre  # pre: seconds before the impact point


def drop_sweep(dur=1.6):
    """'Sound slows down': tape-stop style falling tone over a filtered whoosh."""
    t = _t(dur)
    f = 900 * (60 / 900) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-t / (dur * 0.7))
    whoosh = bandpass(pink(dur, 21), 100, 3000) * np.sin(np.pi * t / dur)
    return norm(tone * 0.7 + whoosh * 0.4, 0.7)


def riser(dur=2.2):
    t = _t(dur)
    f = 120 * (900 / 120) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) * (t / dur) ** 2
    noise = bandpass(pink(dur, 31), 400, 9000) * (t / dur) ** 3
    return norm(tone * 0.5 + noise * 0.6, 0.7)


def ringing(dur=5.0):
    t = _t(dur)
    y = np.sin(2 * np.pi * 4100 * t) * np.exp(-t / 2.2) + 0.3 * np.sin(2 * np.pi * 3950 * t) * np.exp(-t / 1.4)
    return norm(y, 0.25)


def pop():
    dur = 0.18
    t = _t(dur)
    f = 900 * np.exp(-t / 0.04) + 250
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    return norm(y, 0.5)


def engine(dur=2.5):
    t = _t(dur)
    f = 55 + 35 * np.clip(t / 1.5, 0, 1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = sum(np.sin(k * ph) / k for k in range(1, 9))
    y = saw * (0.6 + 0.4 * np.clip(t / 0.4, 0, 1)) * np.clip((dur - t) / 0.6, 0, 1)
    y += bandpass(brown(dur, 41), 40, 400) * 0.3
    return norm(y, 0.55)


ONE_SHOTS = {
    "whistle": lambda: whistle(),
    "boom": lambda: sonic_boom(1.0, 1),
    "boom_small": lambda: sonic_boom(0.45, 2) * 0.7,
    "drop_sweep": lambda: drop_sweep() * 0.5,
    "riser": lambda: riser(),
    "ringing": lambda: ringing(),
    "pop": lambda: pop(),
    "engine": lambda: engine() * 0.4,
    "murmur": lambda: murmur(6.0, 51, voices=24) * 0.6,
}
