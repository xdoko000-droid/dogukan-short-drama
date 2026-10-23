"""Ana kurgu: klipleri TikTok'a hazir 1080x1920 enerjik bir bolume cevirir.

Akis: kirp -> olcekle (+punch-in) -> birlestir -> efekt + muzik karisimi -> loudnorm (2 gecis)
      -> whisper ile kelime altyazisi (altyazi.py) -> gom -> output/bolum.mp4
Cikti 30 MB'i asarsa bitrate dusurulerek yeniden kodlanir.

Ornek:
  python scripts/kurgu.py examples/kurgu-ornek.json
  python scripts/kurgu.py kurgu.yaml --cikti output/bolum-2.mp4 --temiz

Yapilandirmadaki goreli yollar yapilandirma dosyasinin klasorune goredir.
Ara dosyalar <cikti klasoru>/.kurgu-tmp altindadir; --temiz yalniz bu klasoru siler.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import altyazi  # noqa: E402
import ffmpeg_yol  # noqa: E402
import sfx  # noqa: E402
from ffmpeg_yol import calistir  # noqa: E402

VARSAYILAN = {
    "genislik": 1080,
    "yukseklik": 1920,
    "fps": 30,
    "bolum_basligi": "",          # ornek: "BÖLÜM 1"
    "baslik_suresi": 1.0,
    "muzik": True,
    "muzik_bpm": 100,
    "muzik_seviyesi_db": -15,     # konusmaya gore (dB)
    "hedef_lufs": -15,
    "diyalog_lufs": -19,          # karistirma oncesi cekim basina
    "ortam_lufs": -30,
    "max_mb": 30,
    "altyazi": True,
    "whisper_model": "small",
    "dil": "tr",
    "font": None,                 # ozel kalin font dosyasi
    "kontrast": 1.07,
    "doygunluk": 1.06,
    "crf": 21,
}
EFEKT_SEVIYE = {"boom": 0.9, "whoosh": 0.6, "riser": 0.5, "hit": 0.8}
ARA_KLASOR = ".kurgu-tmp"         # cikti klasorunde; --temiz yalniz bunu siler
SES_AF = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"


# ---------------------------------------------------------------- yapilandirma
def yukle(yol: Path) -> dict:
    metin = yol.read_text(encoding="utf-8")
    if yol.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError:
            sys.exit("YAML icin: pip install pyyaml (ya da kurgu.json kullan)")
        return yaml.safe_load(metin)
    return json.loads(metin)


def cekimleri_hazirla(cfg: dict, kok: Path) -> list[dict]:
    out = []
    for i, c in enumerate(cfg.get("cekimler", []), 1):
        c = dict(c)
        c["no"] = i
        efekt = c.get("efekt") or []
        c["efekt"] = [e for e in ([efekt] if isinstance(efekt, str) else efekt) if e and e != "yok"]
        for e in c["efekt"]:
            if e not in EFEKT_SEVIYE:
                sys.exit(f"Cekim {i}: bilinmeyen efekt '{e}' (boom/whoosh/riser/hit/yok)")
        if "kart" in c:
            c["tip"] = "kart"
            c["sure"] = float(c.get("sure", 1.0))
            c.setdefault("ses", "sessiz")
        else:
            c["tip"] = "klip"
            if "klip" not in c:
                sys.exit(f"Cekim {i}: 'klip' ya da 'kart' alani gerekli")
            p = Path(c["klip"])
            c["yol"] = (p if p.is_absolute() else kok / p).resolve()
            if not c["yol"].is_file():
                sys.exit(f"Cekim {i}: klip bulunamadi: {c['yol']}")
            bilgi = ffmpeg_yol.akislar(c["yol"])
            c["kaynak_sesli"] = bilgi["ses"]
            giris = float(c.get("giris", 0.0))
            cikis = float(c["cikis"]) if c.get("cikis") is not None else ffmpeg_yol.sure(c["yol"])
            if cikis <= giris:
                sys.exit(f"Cekim {i}: cikis ({cikis}) giristen ({giris}) buyuk olmali")
            c["giris"], c["sure"] = giris, cikis - giris
            c.setdefault("ses", "diyalog" if c.get("replik") else "ortam")
        if c["ses"] not in ("diyalog", "ortam", "sessiz"):
            sys.exit(f"Cekim {i}: ses alani diyalog/ortam/sessiz olmali")
        out.append(c)
    if not out:
        sys.exit("Yapilandirmada cekim yok ('cekimler' listesi bos)")
    return out


# ---------------------------------------------------------------- 1) cekimler
def cekim_isle(c: dict, ay: dict, tmp: Path) -> None:
    W, H, fps = ay["genislik"], ay["yukseklik"], ay["fps"]
    n = max(1, round(c["sure"] * fps))
    d = n / fps
    c["sure"] = d
    cikti = f"n/{c['no']:02d}.mov"
    sessiz_ses = ["-f", "lavfi", "-t", f"{d:.4f}", "-i", "anullsrc=r=48000:cl=stereo"]
    kod = ["-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le"]
    if c["tip"] == "kart":
        renk = c.get("renk", "black")
        args = ["-f", "lavfi", "-i", f"color=c={renk}:s={W}x{H}:r={fps}:d={d:.4f}"] + sessiz_ses
        fc = f"[0:v]setsar=1,format=yuv420p[v];[1:a]{SES_AF},apad,atrim=0:{d:.4f}[a]"
    else:
        args = ["-ss", f"{c['giris']:.3f}", "-t", f"{d + 0.2:.4f}", "-i", str(c["yol"])]
        if c["kaynak_sesli"] and c["ses"] != "sessiz":
            ses_kaynak = "0:a"
        else:
            args += sessiz_ses
            ses_kaynak = "1:a"
        z0 = 1 + float(c.get("punch_bas", 0)) / 100
        z1 = 1 + float(c.get("punch_in", 0)) / 100
        renk = f"eq=contrast={ay['kontrast']}:saturation={ay['doygunluk']},"
        if abs(z1 - 1) < 1e-6 and abs(z0 - 1) < 1e-6:
            vf = (f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},")
        else:  # 2x ust ornekleme ile titremesiz yumusak punch-in
            z = f"{z0}+({z1}-{z0})*on/{max(n - 1, 1)}"
            vf = (f"fps={fps},scale={2 * W}:{2 * H}:force_original_aspect_ratio=increase:flags=lanczos,crop={2 * W}:{2 * H},"
                  f"zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={fps},")
        fc = (f"[0:v]{vf}{renk}setsar=1,format=yuv420p[v];"
              f"[{ses_kaynak}]{SES_AF},apad,atrim=0:{d:.4f},afade=t=in:d=0.02,"
              f"afade=t=out:st={max(d - 0.03, 0):.4f}:d=0.03[a]")
    calistir(["-y", "-v", "error"] + args + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                                             "-frames:v", str(n), "-t", f"{d:.4f}"] + kod + [cikti], cwd=tmp)
    c["dosya"] = cikti
    c["kazanc"] = 0.0
    if c["tip"] == "klip" and c["ses"] in ("diyalog", "ortam"):
        L = ffmpeg_yol.lufs(cikti, cwd=tmp)
        if L > -60:
            hedef = ay["diyalog_lufs"] if c["ses"] == "diyalog" else ay["ortam_lufs"]
            c["kazanc"] = max(min(hedef - L, 14.0), -30.0)


def birlestir(cekimler: list[dict], tmp: Path) -> float:
    girdi, fc = [], []
    for i, c in enumerate(cekimler):
        girdi += ["-i", c["dosya"]]
        fc.append(f"[{i}:a]volume={c['kazanc']:.2f}dB[a{i}]")
    fc.append("".join(f"[{i}:v][a{i}]" for i in range(len(cekimler))) + f"concat=n={len(cekimler)}:v=1:a=1[v][a]")
    calistir(["-y", "-v", "error"] + girdi + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                                              "-c:v", "libx264", "-crf", "14", "-preset", "veryfast",
                                              "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "ham.mov"], cwd=tmp)
    t = 0.0
    for c in cekimler:
        c["bas"] = t
        t += c["sure"]
    return t


# ---------------------------------------------------------------- 2) ses karisimi
def _carpim(pencereler: list[tuple[float, float]]) -> str:
    return "*".join(f"(1-between(t,{a:.3f},{b:.3f}))" for a, b in pencereler if b > a) or "1"


def ses_karistir(cekimler: list[dict], ay: dict, tmp: Path, D: float) -> None:
    sfx_k = tmp / "sfx"
    sfx_k.mkdir(exist_ok=True)
    sfx.wav_yaz(sfx_k / "boom.wav", sfx.boom())
    sfx.wav_yaz(sfx_k / "whoosh.wav", sfx.whoosh())
    sfx.wav_yaz(sfx_k / "hit.wav", sfx.hit())

    girdi = ["-i", "ham.mov"]
    fc = []
    karisim = ["[0:a]"]
    sessizlik = []
    for c in cekimler:
        s = float(c.get("sessizlik_once", 0) or 0)
        if s > 0:
            sessizlik.append((max(c["bas"] - s, 0), c["bas"] - 0.01))

    if ay["muzik"]:
        sfx.wav_yaz(sfx_k / "muzik.wav", sfx.muzik(D + 1.0, float(ay["muzik_bpm"])))
        Lm = ffmpeg_yol.lufs("sfx/muzik.wav", cwd=tmp)
        kazanc = ay["diyalog_lufs"] + ay["muzik_seviyesi_db"] - Lm
        kapali = [(c["bas"], c["bas"] + c["sure"]) for c in cekimler if c.get("muzik") is False]
        girdi += ["-i", "sfx/muzik.wav"]
        fc.append(f"[1:a]{SES_AF},volume={kazanc:.2f}dB,afade=t=in:d=0.3,"
                  f"afade=t=out:st={max(D - 0.8, 0):.3f}:d=0.8,volume='{_carpim(kapali)}':eval=frame[mu]")
        karisim.append("[mu]")

    k = 0
    for c in cekimler:
        bas, son = c["bas"], c["bas"] + c["sure"]
        an = c.get("efekt_an")
        for e in c["efekt"]:
            if e == "riser":
                rs = min(max(c["sure"], 0.6), 6.0)
                dosya = f"sfx/riser_{c['no']:02d}.wav"
                sfx.wav_yaz(tmp / dosya, sfx.riser(rs))
                t = bas + float(an) if an is not None else max(son - rs, 0)
            else:
                dosya = f"sfx/{e}.wav"
                if an is not None:
                    t = bas + float(an)
                elif e == "whoosh":
                    t = bas - 0.2           # tepe noktasi kesmeye denk gelir
                elif e == "boom" and c["ses"] == "diyalog":
                    t = son - 0.25          # son hecede
                else:
                    t = bas
            seviye = float(c.get("efekt_seviye", EFEKT_SEVIYE[e]))
            j = len(girdi) // 2
            girdi += ["-i", dosya]
            fc.append(f"[{j}:a]{SES_AF},volume={seviye},adelay={int(max(t, 0) * 1000)}:all=1[f{k}]")
            karisim.append(f"[f{k}]")
            k += 1

    fc.append("".join(karisim) + f"amix=inputs={len(karisim)}:duration=first:normalize=0,"
              f"volume='{_carpim(sessizlik)}':eval=frame[mx]")
    filtre = ";".join(fc)
    ln = ffmpeg_yol.loudnorm_olc(girdi, filtre, ay["hedef_lufs"], D, cwd=tmp)
    calistir(["-y", "-v", "error"] + girdi + ["-filter_complex", filtre + f";[mx]{ln},aresample=48000[o]",
                                              "-map", "[o]", "-t", f"{D:.3f}", "-c:a", "pcm_s16le", "miks.wav"], cwd=tmp)


# ---------------------------------------------------------------- 3) altyazi
def kelimeleri_cikar(cekimler: list[dict], ay: dict, tmp: Path) -> list[altyazi.Kelime]:
    diyalog = [c for c in cekimler if c["tip"] == "klip" and c["ses"] == "diyalog"]
    if not diyalog:
        return []
    # whisper yalniz diyalog cekimlerini duysun (muzik/efekt/ortam yok)
    calistir(["-y", "-v", "error", "-i", "ham.mov", "-vn", "-ac", "1", "-ar", "16000", "ses16k.wav"], cwd=tmp)
    import numpy as np

    with wave.open(str(tmp / "ses16k.wav"), "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).copy()
    maske = np.zeros(len(x), bool)
    for c in diyalog:
        maske[int(c["bas"] * 16000): int((c["bas"] + c["sure"]) * 16000)] = True
    x[~maske] = 0
    with wave.open(str(tmp / "whisper.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(x.tobytes())

    replikler = [c["replik"] for c in diyalog if c.get("replik")]
    try:
        duyulan = altyazi.whisper_kelimeler(tmp / "whisper.wav", ay["whisper_model"], ay["dil"],
                                            ipucu=" ".join(replikler) or None)
    except Exception as e:  # paket yok, model indirilemedi (internet yok) vb.
        print(f"  ! Whisper calismadi: {type(e).__name__}: {str(e)[:200]}\n"
              "  ! Altyazi senaryo metninden, tahmini zamanlamayla uretilecek.")
        duyulan = []
    rapor = []
    kelimeler: list[altyazi.Kelime] = []
    for c in diyalog:
        a, b = c["bas"], c["bas"] + c["sure"]
        icerde = [w for w in duyulan if a <= (w.bas + w.bit) / 2 < b]
        if c.get("replik"):
            ws = altyazi.replikle_duzelt(icerde, [c["replik"]], grup_ofset=c["no"], pencere=(a, b))
        else:
            ws = [altyazi.Kelime(w.bas, w.bit, w.metin, c["no"]) for w in icerde]
        for w in ws:
            w.bas, w.bit = max(w.bas, a), min(w.bit, b)
        kelimeler += [w for w in ws if w.bit > w.bas]
        rapor.append({"cekim": c["no"], "replik": c.get("replik"), "duyulan": " ".join(w.metin for w in icerde)})
    (tmp / "replik-rapor.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")
    return kelimeler


def ekleri_hazirla(cekimler: list[dict], ay: dict, D: float) -> list[dict]:
    ekler = []
    if ay["bolum_basligi"]:
        ekler.append({"bas": 0, "bit": min(float(ay["baslik_suresi"]), D), "stil": "Bolum",
                      "metin": altyazi.tr_buyuk(ay["bolum_basligi"])})
    for c in cekimler:
        a, b = c["bas"], c["bas"] + c["sure"]
        if c["tip"] == "kart" and c.get("kart"):
            ekler.append({"bas": a, "bit": b, "stil": "Kart", "metin": c["kart"]})
        if c.get("ekran_yazisi"):
            ekler.append({"bas": a, "bit": b, "stil": "Yazi", "metin": c["ekran_yazisi"]})
    return ekler


# ---------------------------------------------------------------- 4) son kodlama
def son_kodla(tmp: Path, cikti: Path, D: float, ay: dict, altyazili: bool, font_var: bool,
              video_kbps: int | None = None) -> None:
    vf = []
    if altyazili:
        # Windows tuzagi: subtitles filtresine mutlak yol (C:\...) vermek yerine ffmpeg'i .kurgu-tmp
        # klasorunde calistirip goreli ad veriyoruz; ':' ve '\' kacisina gerek kalmiyor.
        vf.append("subtitles=alt.ass" + (":fontsdir=fonts" if font_var else ""))
    vf.append("format=yuv420p")
    if video_kbps:
        oran = ["-b:v", f"{video_kbps}k", "-maxrate", f"{int(video_kbps * 1.3)}k", "-bufsize", f"{video_kbps * 2}k"]
    else:
        oran = ["-crf", str(ay["crf"]), "-maxrate", "3500k", "-bufsize", "7000k"]
    calistir(["-y", "-v", "error", "-i", "ham.mov", "-i", "miks.wav", "-vf", ",".join(vf),
              "-map", "0:v", "-map", "1:a", "-t", f"{D:.3f}", "-c:v", "libx264", "-preset", "slow"] + oran
             + ["-profile:v", "high", "-r", str(ay["fps"]), "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart", str(cikti)], cwd=tmp)


# ---------------------------------------------------------------- ana akis
def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Klipleri TikTok'a hazir 1080x1920 bolume cevirir")
    ap.add_argument("yapilandirma", type=Path, help="kurgu.json ya da kurgu.yaml")
    ap.add_argument("--cikti", type=Path, help="cikti mp4 (varsayilan: yapilandirmadaki 'cikti' ya da output/bolum.mp4)")
    ap.add_argument("--temiz", action="store_true", help="bitince ara dosyalari (.kurgu-tmp) sil")
    ap.add_argument("--altyazisiz", action="store_true", help="whisper/altyazi adimini atla")
    a = ap.parse_args()

    yap = a.yapilandirma.resolve()
    cfg = yukle(yap)
    kok = yap.parent
    ay = {**VARSAYILAN, **(cfg.get("ayarlar") or {})}
    if a.altyazisiz:
        ay["altyazi"] = False
    cikti = (a.cikti.resolve() if a.cikti else (kok / cfg.get("cikti", "output/bolum.mp4")).resolve())
    cikti.parent.mkdir(parents=True, exist_ok=True)
    tmp = cikti.parent / ARA_KLASOR
    (tmp / "n").mkdir(parents=True, exist_ok=True)
    print(f"ffmpeg: {ffmpeg_yol.ffmpeg()}")
    if ay["altyazi"] and not ffmpeg_yol.altyazi_destekli(ffmpeg_yol.ffmpeg()):
        sys.exit("Bu ffmpeg'de subtitles (libass) filtresi yok. `pip install imageio-ffmpeg` kur ya da "
                 "--altyazisiz kullan. Ayrinti: python scripts/doctor.py")

    cekimler = cekimleri_hazirla(cfg, kok)
    print(f"1/5 {len(cekimler)} cekim isleniyor...")
    for c in cekimler:
        cekim_isle(c, ay, tmp)
    D = birlestir(cekimler, tmp)
    print(f"    toplam sure {D:.2f} sn")

    print("2/5 efekt + muzik karisimi, loudnorm...")
    ses_karistir(cekimler, ay, tmp, D)

    font_yol, aile = altyazi.font_bul(ay["font"])
    font_var = False
    if font_yol:
        (tmp / "fonts").mkdir(exist_ok=True)
        shutil.copyfile(font_yol, tmp / "fonts" / font_yol.name)
        font_var = True
    else:
        print("  ! Kalin font bulunamadi; libass sistem fontuna dusecek (python scripts/doctor.py)")

    kelimeler = []
    if ay["altyazi"]:
        print(f"3/5 altyazi (whisper {ay['whisper_model']})...")
        kelimeler = kelimeleri_cikar(cekimler, ay, tmp)
    else:
        print("3/5 altyazi atlandi")
    grup_bitis = {c["no"]: c["bas"] + c["sure"] for c in cekimler}
    ekler = ekleri_hazirla(cekimler, ay, D)
    altyazili = bool(kelimeler or ekler)
    altyazi.ass_yaz(kelimeler, tmp / "alt.ass", D, aile, ekler, ay["genislik"], ay["yukseklik"], grup_bitis)
    srt = cikti.with_suffix(".srt")
    altyazi.srt_yaz(kelimeler, srt, D, grup_bitis)

    print("4/5 son kodlama...")
    son_kodla(tmp, cikti, D, ay, altyazili, font_var)
    mb = cikti.stat().st_size / 1024 / 1024
    if mb > ay["max_mb"]:
        kbps = int(ay["max_mb"] * 8 * 1024 * 0.92 / D) - 160
        print(f"    {mb:.1f} MB > {ay['max_mb']} MB, {kbps} kbps ile yeniden kodlaniyor...")
        son_kodla(tmp, cikti, D, ay, altyazili, font_var, video_kbps=max(kbps, 300))
        mb = cikti.stat().st_size / 1024 / 1024

    L = ffmpeg_yol.lufs(cikti)
    print(f"5/5 bitti: {cikti}\n    {D:.2f} sn, {mb:.1f} MB, {L:.1f} LUFS, altyazi: {srt.name}")
    if a.temiz:
        shutil.rmtree(tmp, ignore_errors=True)
        print("    ara dosyalar silindi")
    else:
        print(f"    ara dosyalar: {tmp} (replik-rapor.json: whisper ne duydu)")


if __name__ == "__main__":
    main()
