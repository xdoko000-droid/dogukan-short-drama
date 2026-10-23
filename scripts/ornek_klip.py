"""ÜCRETSİZ: yalnız yerel ffmpeg ile test klipleri üretir; internet ve Higgsfield kullanmaz, kredi harcamaz.

Ornek kurgu icin test klipleri uretir. Onay gerektirmez.

examples/kurgu-ornek.json'daki her `klip` icin 1080x1920, sesli (sinus), ustunde "KLİP N" yazan
birkac saniyelik bir mp4 yazar: examples/klipler/01.mp4, 02.mp4 ...
Bu dosyalar yalniz denemelik; git'e girmez.

Ornek:
  python scripts/ornek_klip.py
  python scripts/kurgu.py examples/kurgu-ornek.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffmpeg_yol  # noqa: E402
from altyazi import font_bul  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
RENKLER = ["0x1f3a5f", "0x5f1f3a", "0x2f5f1f", "0x5f4a1f", "0x3a1f5f", "0x1f5f5a"]


def klipleri_oku(yapilandirma: Path) -> list[tuple[Path, float]]:
    """(hedef yol, en az sure) listesi; ayni klip birden cok gecerse en uzun cikis alinir."""
    cfg = json.loads(yapilandirma.read_text(encoding="utf-8"))
    sureler: dict[Path, float] = {}
    for c in cfg.get("cekimler", []):
        if "klip" not in c:
            continue
        p = Path(c["klip"])
        yol = (p if p.is_absolute() else yapilandirma.parent / p).resolve()
        cikis = float(c.get("cikis") or 0)
        sureler[yol] = max(sureler.get(yol, 0.0), cikis)
    return list(sureler.items())


def klip_yaz(hedef: Path, no: int, sure: float, font: Path | None) -> None:
    renk = RENKLER[(no - 1) % len(RENKLER)]
    frekans = 220 + 55 * no
    vf = "format=yuv420p"
    with tempfile.TemporaryDirectory() as td:
        if font and "drawtext" in ffmpeg_yol.filtreler(ffmpeg_yol.ffmpeg()):
            # Windows tuzagi: fontfile'a mutlak yol yerine gecici klasordeki goreli adi ver.
            shutil.copyfile(font, Path(td) / "font.ttf")
            vf = (f"drawtext=fontfile=font.ttf:text='KLİP {no}':fontsize=160:fontcolor=white:"
                  f"borderw=8:bordercolor=black:x=(w-tw)/2:y=(h-th)/2,{vf}")
        ffmpeg_yol.calistir([
            "-y", "-v", "error",
            "-f", "lavfi", "-i", f"color=c={renk}:s=1080x1920:r=30:d={sure:.2f}",
            "-f", "lavfi", "-i", f"sine=frequency={frekans}:sample_rate=48000:duration={sure:.2f}",
            "-vf", vf, "-map", "0:v", "-map", "1:a", "-shortest",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-ac", "2", str(hedef),
        ], cwd=Path(td))


def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Ornek kurgu icin sesli 1080x1920 test klipleri uretir")
    ap.add_argument("yapilandirma", type=Path, nargs="?", default=KOK / "examples" / "kurgu-ornek.json",
                    help="klip adlarinin okunacagi kurgu.json (varsayilan: examples/kurgu-ornek.json)")
    ap.add_argument("--sure", type=float, default=5.0, help="en kisa klip suresi, sn (varsayilan 5)")
    a = ap.parse_args()

    klipler = klipleri_oku(a.yapilandirma.resolve())
    if not klipler:
        sys.exit("Yapilandirmada 'klip' alani olan cekim yok")
    font, _ = font_bul()
    if not font:
        print("  ! Font bulunamadi; klipler yazisiz uretilecek")
    for no, (hedef, cikis) in enumerate(klipler, 1):
        hedef.parent.mkdir(parents=True, exist_ok=True)
        klip_yaz(hedef, no, max(a.sure, cikis + 0.5), font)
        print(f" ✓ {hedef.relative_to(KOK) if hedef.is_relative_to(KOK) else hedef}")
    print(f"\n{len(klipler)} klip hazir (ucretsiz, yerel). Simdi: python scripts/kurgu.py examples/kurgu-ornek.json")


if __name__ == "__main__":
    main()
