"""Klipten belirli saniyelerde PNG kare cikarir (kontrol kareleri, sonraki klibin baslangic karesi).

Ornek:
  python scripts/kare.py klipler/01.mp4 --sn 0.5 2 son
  python scripts/kare.py output/bolum.mp4 --sn 3.2 --cikti kontrol/

'son' = klibin son karesi (kare zinciri icin sonraki klibin baslangic karesi).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffmpeg_yol  # noqa: E402


def kare_al(klip: Path, an: str | float, cikti: Path) -> Path:
    cikti.parent.mkdir(parents=True, exist_ok=True)
    if str(an).lower() == "son":
        # sondan yarim saniyeyi coz, her kareyi ayni dosyaya yaz: geriye son kare kalir
        ffmpeg_yol.calistir(["-y", "-v", "error", "-sseof", "-0.5", "-i", str(klip), "-update", "1", str(cikti)])
    else:
        ffmpeg_yol.calistir(["-y", "-v", "error", "-ss", f"{float(an):.3f}", "-i", str(klip),
                             "-frames:v", "1", "-update", "1", str(cikti)])
    if not cikti.is_file():
        raise ffmpeg_yol.FfmpegHatasi(f"Kare cikmadi ({an} sn klip suresini asiyor olabilir)")
    return cikti


def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Klipten PNG kare cikarir")
    ap.add_argument("klip", type=Path)
    ap.add_argument("--sn", nargs="+", default=["son"], help="saniyeler ya da 'son' (varsayilan: son)")
    ap.add_argument("--cikti", type=Path, help="cikti klasoru (varsayilan: klibin klasoru)")
    a = ap.parse_args()
    klasor = a.cikti or a.klip.parent
    for an in a.sn:
        ek = "son" if str(an).lower() == "son" else f"{float(an):.2f}s"
        print(kare_al(a.klip, an, klasor / f"{a.klip.stem}-{ek}.png"))


if __name__ == "__main__":
    main()
