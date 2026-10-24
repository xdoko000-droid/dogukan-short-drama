"""Bolumun ilk N saniyesini (varsayilan 15) ayri bir mp4 olarak keser: kanca kontrolu icin.

UCRETSIZ: yalniz yerel ffmpeg kullanir; Higgsfield'a baglanmaz, onay gerektirmez.

Ornek:
  python scripts/kanca_kes.py uretim/seri/bolumler/bolum-01/bolum-01.mp4
  python scripts/kanca_kes.py bolum-01.mp4 --sn 10 --cikti kanca.mp4

Cikti varsayilani: girdinin yaninda <ad>-kanca.mp4.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffmpeg_yol  # noqa: E402


def kanca_kes(klip: Path, sn: float, cikti: Path) -> Path:
    if not klip.is_file():
        raise ffmpeg_yol.FfmpegHatasi(f"Dosya yok: {klip}")
    if sn <= 0:
        raise ValueError("--sn 0'dan buyuk olmali")
    sn = min(sn, ffmpeg_yol.sure(klip))
    cikti.parent.mkdir(parents=True, exist_ok=True)
    # yeniden kodla: kesim tam N. saniyede olsun, anahtar kareye kaymasin
    ffmpeg_yol.calistir(["-y", "-v", "error", "-i", str(klip), "-t", f"{sn:.3f}",
                         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                         "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(cikti)])
    if not cikti.is_file():
        raise ffmpeg_yol.FfmpegHatasi("Kanca klibi olusmadi")
    return cikti


def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Bolumun ilk N saniyesini ayri mp4 olarak keser (ucretsiz)")
    ap.add_argument("klip", type=Path)
    ap.add_argument("--sn", type=float, default=15.0, help="kesilecek sure, saniye (varsayilan 15)")
    ap.add_argument("--cikti", type=Path, help="cikti dosyasi (varsayilan: <ad>-kanca.mp4)")
    a = ap.parse_args()
    cikti = a.cikti or a.klip.with_name(f"{a.klip.stem}-kanca.mp4")
    try:
        yol = kanca_kes(a.klip, a.sn, cikti)
    except (ffmpeg_yol.FfmpegHatasi, ValueError) as e:
        sys.exit(f"✗ {e}")
    print(f"{yol}  ({ffmpeg_yol.sure(yol):.2f} sn)")


if __name__ == "__main__":
    main()
