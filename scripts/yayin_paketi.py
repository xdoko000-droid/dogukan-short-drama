"""Bir bolum icin yayin paketi hazirlar: video (istenirse boyut sinirli), kapak, aciklama, sabit yorum.

UCRETSIZ: yalniz yerel ffmpeg kullanir; Higgsfield'a baglanmaz, onay gerektirmez.

Ornek:
  python scripts/yayin_paketi.py uretim/seri/bolumler/bolum-02/bolum-02.mp4 --no 2 --seri "ÇİFTE DAVETİYE" \\
      --kapak-klibi uretim/seri/bolumler/bolum-02/klipler/S2.mp4 --kapak-sn 1.5 \\
      --kanca "Gelinliği başkası giyecekti" --merak "Davetiyedeki ikinci isim kimin?" \\
      --soru "Sence ikinci isim kimin?" --etiket aldatma

Cikti (varsayilan <bolum klasoru>/yayin/): video.mp4, kapak.jpg, aciklama.txt, sabit-yorum.txt

Dersler (docs/03-dersler.md -> "Yayin verisi"):
- Kapak karesini altyazisiz HAM klipten al; altyazili son videodan alinan karede yazilar ust uste biner.
- Aciklamaya bolume ozel bir soru koy: soru yoksa yorum gelmiyor.
- Yeni gelen izleyiciyi 1. bolume yonlendir (aciklama satiri + sabit yorum).
- Tarayici eklentisiyle (Claude in Chrome) yuklemede dosya siniri 10 MB: --max-mb 9.3 ver.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import altyazi  # noqa: E402
import ffmpeg_yol  # noqa: E402


def video_hazirla(kaynak: Path, cikti: Path, max_mb: float | None) -> None:
    if not max_mb:
        ffmpeg_yol.calistir(["-y", "-v", "error", "-i", str(kaynak), "-c", "copy", "-movflags", "+faststart",
                             str(cikti)])
        return
    # 2 gecisli x264: boyut hedefe oturur, kalite tek gecisli dusuk bitrate'ten iyi
    video_kbps = int(max_mb * 8 * 1024 / ffmpeg_yol.sure(kaynak) - 128)
    log = str(cikti.with_name("x264"))
    for gecis in (1, 2):
        son = (["-an", "-f", "null", "-"] if gecis == 1 else
               ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(cikti)])
        ffmpeg_yol.calistir(["-y", "-v", "error", "-i", str(kaynak), "-c:v", "libx264", "-preset", "slow",
                             "-b:v", f"{video_kbps}k", "-pass", str(gecis), "-passlogfile", log,
                             "-pix_fmt", "yuv420p", "-r", "30", *son], cwd=cikti.parent)
    for f in cikti.parent.glob("x264*"):
        f.unlink()


def kapak_hazirla(klip: Path, sn: float, cikti: Path, seri: str, no: int, font: Path | None) -> None:
    font = font or altyazi.font_bul(None)[0]   # kurgu ile ayni kalin font
    fnt = f"fontfile={ffmpeg_yol.filtre_yolu(font)}:" if font else ""
    # alt yariyi karart, yazi okunsun
    koyu = "r(X,Y)*if(gt(Y,1000),max(0.3,1-(Y-1000)/700),1)"
    seri_aralikli = " ".join(altyazi.tr_buyuk(seri))
    filt = (f"scale=1080:1920,geq=r='{koyu}':g='{koyu.replace('r(', 'g(')}':b='{koyu.replace('r(', 'b(')}',"
            f"drawtext={fnt}text='{seri_aralikli}':fontsize=62:fontcolor=0xD8B25A:x=(w-tw)/2:y=1250:"
            f"shadowcolor=black@0.8:shadowx=3:shadowy=3,"
            f"drawtext={fnt}text='BÖLÜM {no}':fontsize=190:fontcolor=white:x=(w-tw)/2:y=1340:"
            f"borderw=6:bordercolor=black@0.7")
    ffmpeg_yol.calistir(["-y", "-v", "error", "-ss", str(sn), "-i", str(klip), "-frames:v", "1", "-vf", filt,
                         "-q:v", "2", str(cikti)])


def aciklama_yaz(a: argparse.Namespace, klasor: Path) -> None:
    sonraki = (f"Bölüm {a.no + 1} {a.sonraki} 🔔" if a.no < a.son_bolum
               else "Sezon finali 🎬 Takipte kal, yeni sezon geliyor.")
    profil = " · 1. bölüm profilde 📌" if a.no > 1 else ""
    soru = f"{a.soru} 👇\n" if a.soru else ""
    etiketler = " ".join(f"#{e.lstrip('#')}" for e in ["dizi", "minidizi", *a.etiket, "yapayzeka"])
    (klasor / "aciklama.txt").write_text(
        f"Bölüm {a.no} | {a.kanca}\n{a.merak}\n{soru}{sonraki}{profil}\nKurgudur, AI ile üretildi.\n{etiketler}\n",
        encoding="utf-8")
    # yayindan hemen sonra ilk yorum olarak yazilip sabitlenir
    (klasor / "sabit-yorum.txt").write_text(
        f"Diziye yeni mi katıldın? 1. bölüm profilde en üstte 📌{(' ' + a.soru) if a.soru else ''}\n",
        encoding="utf-8")


def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Bolum icin yayin paketi: video, kapak, aciklama (ucretsiz)")
    ap.add_argument("video", type=Path, help="son kurgu (bolum-NN.mp4)")
    ap.add_argument("--no", type=int, required=True, help="bolum numarasi")
    ap.add_argument("--seri", required=True, help="dizi adi (kapakta)")
    ap.add_argument("--kanca", required=True, help='baslik kancasi: "Bölüm N | <kanca>"')
    ap.add_argument("--merak", required=True, help="1-2 cumle merak (cevabi verme)")
    ap.add_argument("--soru", default="", help="izleyiciye bolume ozel soru (yorum getirir)")
    ap.add_argument("--etiket", nargs="*", default=[], help="ek hashtag'ler (# olmadan), 2-3 adet")
    ap.add_argument("--kapak-klibi", type=Path, help="altyazisiz ham klip (varsayilan: video)")
    ap.add_argument("--kapak-sn", type=float, default=1.0, help="kapak karesinin saniyesi")
    ap.add_argument("--font", type=Path, help="kapak icin kalin .ttf (varsayilan: altyaziyla ayni font)")
    ap.add_argument("--sonraki", default="yarın", help='sonraki bolum zamani (ör. "yarın 20:30\'da")')
    ap.add_argument("--son-bolum", type=int, default=10, help="sezondaki son bolum no")
    ap.add_argument("--max-mb", type=float, help="video boyut siniri, MB (Chrome eklentisi icin 9.3)")
    ap.add_argument("--cikti", type=Path, help="paket klasoru (varsayilan: <video klasoru>/yayin)")
    a = ap.parse_args()

    klasor = (a.cikti or a.video.parent / "yayin").resolve()
    klasor.mkdir(parents=True, exist_ok=True)
    try:
        video_hazirla(a.video.resolve(), klasor / "video.mp4", a.max_mb)
        kapak_hazirla((a.kapak_klibi or a.video).resolve(), a.kapak_sn, klasor / "kapak.jpg", a.seri, a.no, a.font)
    except ffmpeg_yol.FfmpegHatasi as e:
        sys.exit(f"✗ {e}")
    aciklama_yaz(a, klasor)
    mb = (klasor / "video.mp4").stat().st_size / 1024 / 1024
    print(f"✓ {klasor}: video {mb:.2f} MB, kapak.jpg, aciklama.txt, sabit-yorum.txt")


if __name__ == "__main__":
    main()
