"""Kare zinciri birlesimi: A klibinin sonunda, B'nin ilk karesine en cok benzeyen kareyi bulur (SSIM).

B klibi A'nin son karesinden uretildiyse, A'yi bu karede kesip B'yi 1. kareden baslatmak
gorunmez bir birlesim verir. ffmpeg'in ssim filtresi kullanilir.

Ornek:
  python scripts/zincir.py klipler/01.mp4 klipler/02.mp4
  python scripts/zincir.py a.mp4 b.mp4 --son 3 --ilk 5
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffmpeg_yol  # noqa: E402


def benzerlik(a: Path, b: Path, son: float = 2.5, olcek: int = 270) -> tuple[list[tuple[float, float]], float]:
    """A'nin son `son` saniyesindeki her kare icin (A'daki zaman, SSIM). Donus: (liste, fps)."""
    sure_a = ffmpeg_yol.sure(a)
    fps = ffmpeg_yol.akislar(a)["fps"] or 24.0
    bas = max(sure_a - son, 0.0)
    h = olcek * 16 // 9
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        ffmpeg_yol.calistir(["-y", "-v", "error", "-i", str(b), "-frames:v", "1", "b0.png"], cwd=td)
        fc = (f"[0:v]scale={olcek}:{h},format=gray,setsar=1[a];"
              f"[1:v]scale={olcek}:{h},format=gray,setsar=1[b];"
              f"[a][b]ssim=stats_file=ssim.log:shortest=1:repeatlast=1")
        ffmpeg_yol.calistir(["-y", "-v", "error", "-ss", f"{bas:.3f}", "-i", str(a), "-loop", "1", "-i", "b0.png",
                             "-filter_complex", fc, "-f", "null", "-"], cwd=td)
        satirlar = (td / "ssim.log").read_text(encoding="utf-8").splitlines()
    out = []
    for s in satirlar:
        m = re.search(r"n:(\d+).*All:([\d.]+)", s)
        if m:
            out.append((bas + (int(m.group(1)) - 1) / fps, float(m.group(2))))
    return out, fps


def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Iki klip arasinda SSIM ile kesim noktasi onerir")
    ap.add_argument("a", type=Path, help="onceki klip")
    ap.add_argument("b", type=Path, help="sonraki klip (A'nin son karesinden uretilmis)")
    ap.add_argument("--son", type=float, default=2.5, help="A'nin son kac saniyesine bakilsin (varsayilan 2.5)")
    ap.add_argument("--ilk", type=int, default=5, help="en iyi kac aday listelensin")
    a = ap.parse_args()

    skor, fps = benzerlik(a.a, a.b, a.son)
    if not skor:
        sys.exit("SSIM hesaplanamadi")
    sirali = sorted(skor, key=lambda x: -x[1])
    print(f"A: {a.a.name}  B: {a.b.name}  ({fps:g} fps)\nEn benzer kareler (A zamani, SSIM):")
    for t, s in sirali[: a.ilk]:
        print(f"  {t:7.3f} sn  kare {round(t * fps):4d}  SSIM {s:.4f}")
    t, s = sirali[0]
    print(f"\nOneri: A'yi {t + 1 / fps:.3f} sn'de kes (kare {round(t * fps)} dahil), "
          f"B'yi {1 / fps:.3f} sn'den (2. kare) baslat.")
    if s < 0.6:
        print("Uyari: benzerlik dusuk; B, A'nin son karesinden uretilmemis olabilir.")


if __name__ == "__main__":
    main()
