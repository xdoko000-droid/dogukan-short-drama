"""Kurulum kontrolu: Python, ffmpeg/ffprobe, libass, whisper, font, Higgsfield CLI.

Ornek:
  python scripts/doctor.py        (Windows'ta gerekirse: py scripts/doctor.py)
"""
from __future__ import annotations

import importlib.util
import platform
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

WIN = platform.system() == "Windows"
MAC = platform.system() == "Darwin"
sorunlar = 0


def satir(ok: bool, ad: str, ayrinti: str = "", kur_win: str = "", kur_mac: str = "", zorunlu: bool = True) -> None:
    global sorunlar
    isaret = "✓" if ok else ("✗" if zorunlu else "–")
    print(f" {isaret} {ad}" + (f"  ({ayrinti})" if ayrinti else ""))
    if not ok:
        if zorunlu:
            sorunlar += 1
        if kur_win:
            print(f"     Windows: {kur_win}")
        if kur_mac:
            print(f"     macOS  : {kur_mac}")


def main() -> None:
    try:
        from ffmpeg_yol import konsol_utf8
    except Exception:
        konsol_utf8 = None
    if konsol_utf8:
        konsol_utf8()
    print(f"AI Short Drama Kit - kurulum kontrolu ({platform.system()} {platform.machine()})\n")

    v = sys.version_info
    satir(v >= (3, 10), f"Python {v.major}.{v.minor}.{v.micro} (>= 3.10 gerekli)", "",
          "winget install Python.Python.3.12",
          "brew install python@3.12\n"
          "              ya da Homebrew yoksa uv: https://docs.astral.sh/uv/getting-started/installation/\n"
          "              sonra: uv python install 3.12 && uv venv --python 3.12 .venv")
    if v < (3, 10):
        print("     Sonra .venv'i yeni Python ile yeniden olustur ve requirements.txt'yi kur"
              " (python3.12 -m venv .venv  ya da  uv venv --python 3.12 .venv).")

    paket = {m: importlib.util.find_spec(m) is not None for m in ("numpy", "imageio_ffmpeg", "faster_whisper", "whisper", "yaml")}
    pip_w, pip_m = "py -m pip install -r requirements.txt", "python3 -m pip install -r requirements.txt"
    satir(paket["numpy"], "numpy", "", pip_w, pip_m)
    satir(paket["imageio_ffmpeg"], "imageio-ffmpeg (libass'li yedek ffmpeg)", "", pip_w, pip_m, zorunlu=False)

    import ffmpeg_yol

    yol_ffmpeg = shutil.which("ffmpeg")
    satir(bool(yol_ffmpeg), "ffmpeg (PATH)", yol_ffmpeg or "bulunamadi",
          "winget install Gyan.FFmpeg", "brew install ffmpeg", zorunlu=not paket["imageio_ffmpeg"])
    yol_ffprobe = shutil.which("ffprobe")
    satir(bool(yol_ffprobe), "ffprobe (PATH)", yol_ffprobe or "yok; sure ffmpeg ile olculur",
          "winget install Gyan.FFmpeg", "brew install ffmpeg", zorunlu=False)

    if yol_ffmpeg:
        var = ffmpeg_yol.altyazi_destekli(yol_ffmpeg)
        satir(var, "PATH ffmpeg'de subtitles (libass) filtresi", "",
              "" if var else "sorun degil, imageio-ffmpeg kullanilir: " + pip_w,
              "" if var else "sorun degil, imageio-ffmpeg kullanilir: " + pip_m, zorunlu=False)
    try:
        secilen = ffmpeg_yol.ffmpeg()
        lib = ffmpeg_yol.altyazi_destekli(secilen)
        satir(lib, "Kurguda kullanilacak ffmpeg (altyazi gomme destekli)", secilen,
              pip_w + "  (imageio-ffmpeg libass'li ffmpeg getirir)", pip_m)
    except ffmpeg_yol.FfmpegHatasi as e:
        satir(False, "Kurguda kullanilacak ffmpeg", str(e), "winget install Gyan.FFmpeg", "brew install ffmpeg")

    w = paket["faster_whisper"] or paket["whisper"]
    satir(w, "Whisper (faster-whisper ya da openai-whisper)",
          "faster-whisper" if paket["faster_whisper"] else ("openai-whisper" if paket["whisper"] else "yok"),
          "py -m pip install faster-whisper", "python3 -m pip install faster-whisper")
    satir(paket["yaml"], "pyyaml (kurgu.yaml icin; json kullanirsan gerekmez)", "",
          "py -m pip install pyyaml", "python3 -m pip install pyyaml", zorunlu=False)

    from altyazi import font_bul

    font, aile = font_bul()
    satir(font is not None, "Turkce karakterli kalin font", f"{aile}: {font}" if font else "bulunamadi",
          r"C:\Windows\Fonts\arialbd.ttf olmali; yoksa kurgu ayarlarinda \"font\" ile bir .ttf ver",
          "Arial Bold macOS ile gelir; yoksa kurgu ayarlarinda \"font\" ile bir .ttf ver")

    hf = shutil.which("higgsfield")
    satir(bool(hf), "Higgsfield CLI (opsiyonel; MCP yeterli)", hf or "yok",
          "docs/05-higgsfield-mcp-kurulum.md", "docs/05-higgsfield-mcp-kurulum.md", zorunlu=False)

    print()
    if sorunlar:
        print(f"{sorunlar} zorunlu eksik var. Yukaridaki kurulum komutlarini calistirip tekrar dene.")
        sys.exit(1)
    print("Her sey hazir. Deneme (ucretsiz, yerel test; Higgsfield'a dokunmaz):\n"
          "  python scripts/deneme.py                         (ucretsiz, yerel test)\n"
          "  ya da: python scripts/ornek_klip.py              (ucretsiz, yerel test)\n"
          "         python scripts/kurgu.py examples/kurgu-ornek.json  (ucretsiz, yerel test)")


if __name__ == "__main__":
    main()
