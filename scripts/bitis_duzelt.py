"""Bolum sonundaki siyah "Devami icin takip et" kartini kaldirir; yerine son cekimin son karesini kisa sure
dondurup ustune ekran yazisi koyar ("Devami yarin").

Neden: yayin verisinde izleyicinin buyuk kismi siyah son kartta cikti (izlenme grafigi son 2 sn'de dikey dusuyor).
Donan cliffhanger karesi izleyiciyi gerilimin tepesinde birakir; video da hemen basa sarar.

UCRETSIZ: yalniz yerel ffmpeg kullanir; Higgsfield'a baglanmaz, onay gerektirmez.

Ornek:
  python scripts/bitis_duzelt.py uretim/seri/bolumler/bolum-02/kurgu.json
  python scripts/bitis_duzelt.py kurgu.json --dondur 0.8 --yazi "Devamı yarın 20:30"
Sonra: python scripts/kurgu.py <ayni kurgu.json> --temiz

kurgu.json yerinde guncellenir (yedegi kurgu.onceki.json). Dondurulmus klip: klipler/<ad>-son.mp4.
Ikinci kez calistirilirsa durur (son cekim zaten -son klibi).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffmpeg_yol  # noqa: E402


def bitis_duzelt(kj: Path, dondur: float, yazi: str) -> dict:
    d = json.loads(kj.read_text(encoding="utf-8"))
    cek = d.get("cekimler") or []
    if cek and "kart" in cek[-1]:
        cek.pop()
    if not cek or "klip" not in cek[-1]:
        raise ValueError("Son cekim bir klip olmali (karttan once klip yok)")
    son = cek[-1]
    kaynak = kj.parent / son["klip"]
    if kaynak.stem.endswith("-son"):
        raise ValueError(f"Zaten duzeltilmis: {son['klip']} (geri almak icin {kj.stem}.onceki.json)")
    hedef = kaynak.with_name(kaynak.stem + "-son.mp4")
    sure = ffmpeg_yol.sure(kaynak)
    cikis = min(float(son.get("cikis", sure)), sure)
    shutil.copy(kj, kj.with_name(kj.stem + ".onceki.json"))
    # klibi cikis noktasinda kes, son kareyi dondur; ses sessizlikle uzar
    ffmpeg_yol.calistir(["-y", "-v", "error", "-i", str(kaynak), "-t", f"{cikis:.3f}",
                         "-vf", f"tpad=stop_mode=clone:stop_duration={dondur}", "-af", f"apad=pad_dur={dondur}",
                         "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                         str(hedef)])
    son["klip"] = hedef.relative_to(kj.parent).as_posix()
    son["cikis"] = round(cikis + dondur, 3)
    son["ekran_yazisi"] = yazi
    kj.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return son


def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Siyah son karti kaldirir, son kareyi dondurup yazi ekler (ucretsiz)")
    ap.add_argument("kurgu", type=Path, help="kurgu.json")
    ap.add_argument("--dondur", type=float, default=0.8, help="son karenin donma suresi, sn (varsayilan 0.8)")
    ap.add_argument("--yazi", default="Devamı yarın", help='ekran yazisi (varsayilan "Devamı yarın")')
    a = ap.parse_args()
    try:
        son = bitis_duzelt(a.kurgu, a.dondur, a.yazi)
    except (ffmpeg_yol.FfmpegHatasi, ValueError, FileNotFoundError) as e:
        sys.exit(f"✗ {e}")
    print(f"✓ son cekim {son['klip']} {son.get('giris', 0)}–{son['cikis']} + '{a.yazi}'")


if __name__ == "__main__":
    main()
