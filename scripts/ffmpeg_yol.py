"""Ortak ffmpeg yardimcilari: dogru ffmpeg'i bulur, komut calistirir, sure/LUFS olcer.

Kurallar:
- PATH'teki ffmpeg once denenir; subtitles (libass) filtresi yoksa imageio-ffmpeg'in
  ffmpeg'i kullanilir. `FFMPEG` ortam degiskeni ile elle yol verilebilir.
- Butun subprocess cagrilari liste bicimindedir, shell=False.
- ffprobe yoksa sure, `ffmpeg -i` ciktisindan okunur.
"""
from __future__ import annotations

import functools
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


class FfmpegHatasi(RuntimeError):
    pass


def konsol_utf8() -> None:
    """Windows konsolunda Turkce karakter ve isaretler (✓ ✗) hata vermesin."""
    for akim in (sys.stdout, sys.stderr):
        try:
            akim.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def _cmd(args: list[str], cwd: Path | None = None, timeout: float | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(a) for a in args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
        cwd=str(cwd) if cwd else None,
        timeout=timeout,
    )


@functools.lru_cache(maxsize=None)
def filtreler(exe: str) -> frozenset[str]:
    try:
        r = _cmd([exe, "-hide_banner", "-filters"], timeout=30)
    except (OSError, subprocess.SubprocessError):
        return frozenset()
    adlar = set()
    for satir in r.stdout.splitlines():
        p = satir.split()
        if len(p) >= 3 and "->" in p[2]:
            adlar.add(p[1])
    return frozenset(adlar)


def altyazi_destekli(exe: str) -> bool:
    return "subtitles" in filtreler(exe)


def imageio_ffmpeg_yolu() -> str | None:
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


@functools.lru_cache(maxsize=None)
def ffmpeg() -> str:
    """Kullanilacak ffmpeg yolu (libass destekli olani tercih eder)."""
    adaylar = []
    if os.environ.get("FFMPEG"):
        adaylar.append(os.environ["FFMPEG"])
    yol = shutil.which("ffmpeg")
    if yol:
        adaylar.append(yol)
    ii = imageio_ffmpeg_yolu()
    if ii:
        adaylar.append(ii)
    for a in adaylar:
        if altyazi_destekli(a):
            return a
    if adaylar:
        return adaylar[0]
    raise FfmpegHatasi(
        "ffmpeg bulunamadi. Kur: Windows `winget install Gyan.FFmpeg`, macOS `brew install ffmpeg` "
        "ya da `pip install imageio-ffmpeg`."
    )


@functools.lru_cache(maxsize=None)
def ffprobe() -> str | None:
    """ffmpeg ile ayni klasordeki ya da PATH'teki ffprobe; yoksa None."""
    f = Path(ffmpeg())
    yan = f.with_name("ffprobe" + (".exe" if f.suffix.lower() == ".exe" else ""))
    if yan.is_file():
        return str(yan)
    return shutil.which("ffprobe")


def calistir(args: list, cwd: Path | None = None, kontrol: bool = True) -> subprocess.CompletedProcess:
    """ffmpeg'i verilen argumanlarla calistirir. args ffmpeg'den sonraki kisimdir."""
    r = _cmd([ffmpeg(), "-hide_banner", "-nostdin"] + list(args), cwd=cwd)
    if kontrol and r.returncode != 0:
        son = "\n".join(r.stderr.strip().splitlines()[-25:])
        raise FfmpegHatasi(f"ffmpeg hata verdi ({r.returncode}):\n{son}")
    return r


def sure(yol: Path | str) -> float:
    """Medya suresi (sn). ffprobe yoksa ffmpeg ciktisindan okunur."""
    pr = ffprobe()
    if pr:
        r = _cmd([pr, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(yol)])
        try:
            return float(r.stdout.strip())
        except ValueError:
            pass
    r = _cmd([ffmpeg(), "-hide_banner", "-i", str(yol)])
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        raise FfmpegHatasi(f"Sure okunamadi: {yol}")
    h, d, s = m.groups()
    return int(h) * 3600 + int(d) * 60 + float(s)


def akislar(yol: Path | str) -> dict:
    """{'video': bool, 'ses': bool, 'fps': float|None, 'genislik': int|None, 'yukseklik': int|None}"""
    r = _cmd([ffmpeg(), "-hide_banner", "-i", str(yol)])
    bilgi = {"video": False, "ses": False, "fps": None, "genislik": None, "yukseklik": None}
    for satir in r.stderr.splitlines():
        if "Stream #" not in satir:
            continue
        if "Video:" in satir and not bilgi["video"]:
            bilgi["video"] = True
            m = re.search(r"(\d{2,5})x(\d{2,5})", satir)
            if m:
                bilgi["genislik"], bilgi["yukseklik"] = int(m.group(1)), int(m.group(2))
            m = re.search(r"([\d.]+) fps", satir)
            if m:
                bilgi["fps"] = float(m.group(1))
        elif "Audio:" in satir:
            bilgi["ses"] = True
    return bilgi


def lufs(yol: Path | str, cwd: Path | None = None) -> float:
    """Entegre ses yuksekligi (LUFS). Sessiz/cok kisa dosyada -70 doner."""
    r = calistir(["-i", str(yol), "-af", "ebur128=peak=none", "-f", "null", "-"], cwd=cwd, kontrol=False)
    bul = re.findall(r"\bI:\s+(-?[\d.]+) LUFS", r.stderr)
    try:
        return float(bul[-1])
    except (IndexError, ValueError):
        return -70.0


def loudnorm_olc(args_girdi: list, filtre: str, hedef: float, sure_sn: float, cwd: Path | None = None) -> str:
    """Iki gecisli loudnorm'un 1. gecisi. `filtre` [mx] etiketli sesi uretmeli.
    Donus: 2. geciste kullanilacak loudnorm filtre metni."""
    r = calistir(
        args_girdi
        + ["-filter_complex", filtre + f";[mx]loudnorm=I={hedef}:TP=-1.5:LRA=11:print_format=json[o]",
           "-map", "[o]", "-t", f"{sure_sn:.3f}", "-f", "null", "-"],
        cwd=cwd,
    )
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)
    if not m:
        raise FfmpegHatasi("loudnorm olcumu okunamadi")
    j = json.loads(m.group(0))
    return (
        f"loudnorm=I={hedef}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
        f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
    )


def filtre_yolu(yol: Path | str) -> str:
    """Bir dosya yolunu ffmpeg filtre argumani icinde (ornegin subtitles=...) kullanilabilir hale getirir.

    Windows tuzagi: `C:\\x\\alt.ass` icindeki `\\` ve `:` filtre sozdiziminde ozel anlamlidir.
    Ters bolu ileri boluya cevrilir, `:` kacirilir, yol tek tirnaga alinir. En guvenlisi yine de ffmpeg'i dosyanin
    klasorunde (cwd) calistirip yalnizca dosya adini vermektir; kurgu.py bunu yapar.
    """
    s = Path(yol).as_posix()          # C:\\x\\alt.ass -> C:/x/alt.ass
    if "'" in s:
        raise ValueError(f"Filtre yolunda tek tirnak desteklenmiyor: {s}")
    return "'" + s.replace(":", "\\:") + "'"   # -> 'C\\:/x/alt.ass'


if __name__ == "__main__":
    konsol_utf8()
    print("ffmpeg :", ffmpeg())
    print("ffprobe:", ffprobe() or "(yok, ffmpeg ile olculur)")
    print("subtitles filtresi:", "var" if altyazi_destekli(ffmpeg()) else "YOK")
