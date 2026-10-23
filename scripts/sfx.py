"""Ses efekti ve gerilim muzigi sentezi (numpy + wave; harici ses dosyasi yok).

Uretilenler (48 kHz, stereo, 16 bit WAV):
  boom.wav    alcak frekansli darbe (sub kick + gurultu patlamasi)
  whoosh.wav  gecis supurmesi (filtrelenmis gurultu)
  riser.wav   yukselen gerilim (glissando + gurultu), --riser-sure ile
  hit.wav     kisa sert vurus
  muzik.wav   BPM ayarli nabiz + ostinato + drone, --muzik-sure ile

Ornek:
  python scripts/sfx.py --cikti output/sfx
  python scripts/sfx.py --cikti output/sfx --bpm 110 --muzik-sure 60
"""
from __future__ import annotations

import argparse
import wave
from pathlib import Path

import numpy as np

SR = 48000
_RNG_TOHUM = 7


def _t(sure: float) -> np.ndarray:
    return np.arange(int(round(sure * SR))) / SR


def _gurultu(n: int, tohum: int = _RNG_TOHUM) -> np.ndarray:
    return np.random.default_rng(tohum).uniform(-1.0, 1.0, n)


def _alcak_geciren(x: np.ndarray, kesim_hz: np.ndarray | float) -> np.ndarray:
    """Tek kutuplu alcak geciren; kesim frekansi ornek bazinda degisebilir."""
    k = np.broadcast_to(np.asarray(kesim_hz, dtype=float), x.shape)
    a = 1.0 - np.exp(-2.0 * np.pi * k / SR)
    y = np.empty_like(x)
    onceki = 0.0
    for i in range(len(x)):  # efektler kisa; dongu yeterince hizli
        onceki += a[i] * (x[i] - onceki)
        y[i] = onceki
    return y


def _yumusat(x: np.ndarray, giris: float = 0.003, cikis: float = 0.01) -> np.ndarray:
    n1, n2 = int(giris * SR), int(cikis * SR)
    if n1:
        x[:n1] *= np.linspace(0, 1, n1)
    if n2:
        x[-n2:] *= np.linspace(1, 0, n2)
    return x


def boom(sure: float = 2.0) -> np.ndarray:
    t = _t(sure)
    frek = 38 + 70 * np.exp(-t * 9)
    faz = 2 * np.pi * np.cumsum(frek) / SR
    govde = 0.9 * np.sin(faz) * np.exp(-t * 2.2)
    patlama = 0.35 * _gurultu(len(t)) * np.exp(-t * 18)
    return _yumusat(govde + patlama)


def whoosh(sure: float = 0.45) -> np.ndarray:
    t = _t(sure)
    zarf = np.sin(np.pi * t / sure) ** 3
    kesim = 400 + 5000 * np.sin(np.pi * t / sure) ** 2
    x = _alcak_geciren(_gurultu(len(t), 11), kesim) * 2.2
    return _yumusat(0.55 * x * zarf)


def riser(sure: float = 2.0) -> np.ndarray:
    t = _t(sure)
    faz = 2 * np.pi * (180 * t + 260 * t * t / sure)
    ton = 0.35 * np.sin(faz) + 0.12 * np.sin(2 * faz)
    kesim = 300 + 7000 * (t / sure) ** 2
    hisirti = 0.5 * _alcak_geciren(_gurultu(len(t), 13), kesim)
    return _yumusat((ton + hisirti) * (t / sure) ** 2.2, cikis=0.02)


def hit(sure: float = 0.8) -> np.ndarray:
    t = _t(sure)
    govde = 0.8 * np.sin(2 * np.pi * (60 + 120 * np.exp(-t * 30)) * t) * np.exp(-t * 6)
    tok = 0.45 * _gurultu(len(t), 17) * np.exp(-t * 35)
    metal = 0.12 * np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 9)
    return _yumusat(govde + tok + metal)


def muzik(sure: float = 60.0, bpm: float = 100.0) -> np.ndarray:
    """Gerilim yatagi: vurus basina kalp atisi nabzi, sekizlik ostinato, alcak drone."""
    t = _t(sure)
    vurus = 60.0 / bpm
    yarim = vurus / 2

    def kalp(ofset: float, sonum: float) -> np.ndarray:
        m = np.mod(t + ofset, vurus)
        return np.sin(2 * np.pi * (48 + 90 * np.exp(-m * 28)) * m) * np.exp(-m * sonum)

    nabiz = 0.55 * kalp(0, 7) + 0.35 * kalp(yarim, 9) * (np.mod(t, 4 * vurus) < 2 * vurus)
    drone = 0.10 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t)) \
        + 0.07 * np.sin(2 * np.pi * 82.41 * t)
    adim = np.floor(t / yarim).astype(int) % 4
    notalar = np.array([220.0, 233.08, 220.0, 246.94])[adim]   # A - Bb - A - B
    m = np.mod(t, yarim)
    ostinato = 0.09 * np.sin(2 * np.pi * notalar * t) * np.exp(-m * 10)
    tik = 0.06 * _gurultu(len(t), 19) * np.exp(-np.mod(t + yarim / 2, yarim) * 70)
    x = nabiz + drone + ostinato + tik
    return _yumusat(x, giris=0.5, cikis=1.0)


def wav_yaz(yol: Path, x: np.ndarray) -> Path:
    yol = Path(yol)
    yol.parent.mkdir(parents=True, exist_ok=True)
    tepe = float(np.max(np.abs(x))) or 1.0
    if tepe > 0.98:
        x = x * (0.98 / tepe)
    veri = (np.clip(x, -1, 1) * 32767).astype("<i2")
    stereo = np.repeat(veri[:, None], 2, axis=1)
    with wave.open(str(yol), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    return yol


def hepsini_uret(klasor: Path, bpm: float = 100.0, muzik_sure: float = 60.0, riser_sure: float = 2.0) -> dict[str, Path]:
    klasor = Path(klasor)
    return {
        "boom": wav_yaz(klasor / "boom.wav", boom()),
        "whoosh": wav_yaz(klasor / "whoosh.wav", whoosh()),
        "riser": wav_yaz(klasor / "riser.wav", riser(riser_sure)),
        "hit": wav_yaz(klasor / "hit.wav", hit()),
        "muzik": wav_yaz(klasor / "muzik.wav", muzik(muzik_sure, bpm)),
    }


def main() -> None:
    from ffmpeg_yol import konsol_utf8

    konsol_utf8()
    ap = argparse.ArgumentParser(description="Ses efekti ve gerilim muzigi sentezi")
    ap.add_argument("--cikti", type=Path, default=Path("output/sfx"), help="cikti klasoru")
    ap.add_argument("--bpm", type=float, default=100.0, help="muzik temposu (vurus/dk)")
    ap.add_argument("--muzik-sure", type=float, default=60.0, help="muzik suresi (sn)")
    ap.add_argument("--riser-sure", type=float, default=2.0, help="riser suresi (sn)")
    a = ap.parse_args()
    for ad, yol in hepsini_uret(a.cikti, a.bpm, a.muzik_sure, a.riser_sure).items():
        print(f"{ad:7s} -> {yol}")


if __name__ == "__main__":
    main()
