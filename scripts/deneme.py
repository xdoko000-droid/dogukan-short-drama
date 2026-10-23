"""Uctan uca deneme: test klipleri + ornek kurgu, tek komut.

UCRETSIZ: yalniz yerel ffmpeg ve Python kullanir; Higgsfield'a baglanmaz, kredi harcamaz, onay gerektirmez.
Altyazi icin faster-whisper modeli ilk calistirmada internetten (ucretsiz) indirilir. Internet yoksa
deneme durmaz: altyazi senaryo metninden tahmini zamanlamayla yazilir.

Ornek:
  python scripts/deneme.py
  python scripts/deneme.py --altyazisiz
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ORNEK = KOK / "examples" / "kurgu-ornek.json"


def adim(betik: str, *argv: str) -> None:
    komut = [sys.executable, str(KOK / "scripts" / betik), *argv]
    if subprocess.run(komut, cwd=KOK).returncode != 0:
        sys.exit(f"\n✗ {betik} hata verdi. Kurulumu kontrol et: python scripts/doctor.py")


def main() -> None:
    ap = argparse.ArgumentParser(description="Ucretsiz uctan uca deneme: ornek_klip.py + kurgu.py (Higgsfield yok)")
    ap.add_argument("--altyazisiz", action="store_true", help="whisper/altyazi adimini atla")
    a = ap.parse_args()

    print("== 1/2 test klipleri (ucretsiz, yerel ffmpeg) ==", flush=True)
    adim("ornek_klip.py", str(ORNEK))
    print("\n== 2/2 ornek kurgu ==", flush=True)
    adim("kurgu.py", str(ORNEK), "--temiz", *(["--altyazisiz"] if a.altyazisiz else []))
    cikti = KOK / "examples" / "output" / "bolum.mp4"
    if not cikti.is_file():
        sys.exit(f"\n✗ Cikti bulunamadi: {cikti}")
    print(f"\n✓ Deneme tamam: {cikti.relative_to(KOK)}")


if __name__ == "__main__":
    main()
