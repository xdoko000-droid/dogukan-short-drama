"""Kelime zamanlamali TikTok tarzi altyazi (ASS + SRT).

faster-whisper (yoksa openai-whisper) ile kelime zamanlari cikarilir. `--replikler` verilirse
whisper'in yanlis duydugu kelimeler senaryodaki metinle degistirilir (zamanlama whisper'dan,
yazim senaryodan). ASS: 2-3 kelimelik bloklar, aktif kelime sari, kalin beyaz yazi, siyah kontur,
alt-orta konum.

Ornek:
  python scripts/altyazi.py output/bolum.mp4 --replikler replik.json
  python scripts/altyazi.py ses.wav --model large-v3-turbo --ass alt.ass --srt alt.srt

replik.json: ["Davetiyeleri ben bastirdim, Defne.", "Siz mi?"]  (ya da {"replikler": [...]})
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import struct
import sys
import tempfile
import unicodedata
import wave
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffmpeg_yol  # noqa: E402

SARI = r"{\c&H0000FFFF&}"   # ASS renkleri &HBBGGRR
BEYAZ = r"{\c&H00FFFFFF&}"


@dataclass
class Kelime:
    bas: float
    bit: float
    metin: str
    grup: int = 0   # ayni replik/cekim; bloklar grup sinirini asmaz


# ---------------------------------------------------------------- metin yardimcilari
def tr_buyuk(s: str) -> str:
    return s.replace("i", "İ").replace("ı", "I").upper()


def _norm(s: str) -> str:
    s = s.lower().replace("ı", "i").replace("i̇", "i")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^\w]", "", s)


def replikleri_oku(yol: Path) -> list[str]:
    veri = json.loads(Path(yol).read_text(encoding="utf-8"))
    if isinstance(veri, dict):
        veri = veri.get("replikler", [])
    return [x["metin"] if isinstance(x, dict) else str(x) for x in veri]


# ---------------------------------------------------------------- font
def ttf_aile_adi(yol: Path) -> str | None:
    """TTF/OTF name tablosundan aile adini (nameID 1) okur."""
    try:
        b = Path(yol).read_bytes()
        n_tablo = struct.unpack(">H", b[4:6])[0]
        for i in range(n_tablo):
            kayit = b[12 + 16 * i: 28 + 16 * i]
            if kayit[:4] == b"name":
                off = struct.unpack(">I", kayit[8:12])[0]
                _, sayi, str_off = struct.unpack(">HHH", b[off:off + 6])
                adaylar = []
                for k in range(sayi):
                    pid, eid, lid, nid, uz, so = struct.unpack(">HHHHHH", b[off + 6 + 12 * k: off + 18 + 12 * k])
                    if nid != 1:
                        continue
                    ham = b[off + str_off + so: off + str_off + so + uz]
                    metin = ham.decode("utf-16-be", "ignore") if pid in (0, 3) else ham.decode("latin-1", "ignore")
                    adaylar.append((0 if (pid == 3 and lid == 0x409) else 1, metin))
                if adaylar:
                    return sorted(adaylar)[0][1]
    except Exception:
        return None
    return None


def font_adaylari() -> list[Path]:
    win = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    return [
        win / "arialbd.ttf",
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        Path("/Library/Fonts/Arial Bold.ttf"),
        Path.home() / "Library/Fonts/Arial Bold.ttf",
        Path("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        win / "verdanab.ttf",
    ]


def font_bul(ozel: str | Path | None = None) -> tuple[Path | None, str]:
    """(font dosyasi, aile adi). Bulunamazsa (None, 'Arial')."""
    adaylar = [Path(ozel)] if ozel else []
    adaylar += font_adaylari()
    for p in adaylar:
        if p.is_file():
            return p, ttf_aile_adi(p) or p.stem
    return None, "Arial"


# ---------------------------------------------------------------- whisper
def _wav16k(girdi: Path, klasor: Path) -> Path:
    cikti = klasor / "whisper16k.wav"
    ffmpeg_yol.calistir(["-y", "-v", "error", "-i", str(girdi), "-vn", "-ac", "1", "-ar", "16000", str(cikti)])
    return cikti


def whisper_kelimeler(girdi: Path, model: str = "small", dil: str = "tr", ipucu: str | None = None) -> list[Kelime]:
    """Ses/video dosyasindan kelime zamanlari. faster-whisper > openai-whisper."""
    import numpy as np

    with tempfile.TemporaryDirectory() as td:
        wav = _wav16k(Path(girdi), Path(td))
        with wave.open(str(wav), "rb") as w:
            ses = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    # Ses numpy dizisi olarak verilir: PyAV/ffmpeg surum uyumsuzluklarindan bagimsiz.
    prompt = (ipucu or "")[-600:] or None
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError:
        WhisperModel = None
    if WhisperModel is not None:
        m = WhisperModel(model, device="cpu", compute_type="int8")
        parcalar, _ = m.transcribe(ses, language=dil, word_timestamps=True, beam_size=5,
                                   condition_on_previous_text=False, initial_prompt=prompt)
        return [Kelime(w.start, w.end, w.word.strip()) for p in parcalar for w in (p.words or []) if w.word.strip()]
    try:
        import whisper  # type: ignore
    except ImportError as e:
        raise RuntimeError("faster-whisper ya da openai-whisper kurulu degil: pip install faster-whisper") from e
    sonuc = whisper.load_model(model).transcribe(ses, language=dil, word_timestamps=True, initial_prompt=prompt)
    return [Kelime(w["start"], w["end"], w["word"].strip())
            for s in sonuc["segments"] for w in s.get("words", []) if w["word"].strip()]


# ---------------------------------------------------------------- senaryo ile duzeltme
def _dagit(bas: float, bit: float, kelimeler: list[tuple[str, int]]) -> list[Kelime]:
    toplam = sum(max(len(k), 1) for k, _ in kelimeler) or 1
    bit = max(bit, bas + 0.12 * len(kelimeler))
    t, out = bas, []
    for k, g in kelimeler:
        d = (bit - bas) * max(len(k), 1) / toplam
        out.append(Kelime(t, t + d, k, g))
        t += d
    return out


def replikle_duzelt(duyulan: list[Kelime], replikler: list[str], grup_ofset: int = 0,
                    pencere: tuple[float, float] | None = None) -> list[Kelime]:
    """Duyulan kelime dizisini senaryo replikleriyle hizalar.
    Zamanlama whisper'dan, metin senaryodan gelir. Senaryoda olmayan duyulan kelimeler atilir,
    duyulmayan senaryo kelimeleri komsu zamanlar arasina dagitilir."""
    ref = [(k, gi + grup_ofset) for gi, r in enumerate(replikler) for k in r.split()]
    if not ref:
        return []
    if not duyulan:
        a, b = pencere if pencere else (0.0, 0.4 * len(ref))
        return _dagit(a + 0.1, max(a + 0.2, b - 0.2), ref)
    sm = difflib.SequenceMatcher(None, [_norm(w.metin) for w in duyulan], [_norm(k) for k, _ in ref], autojunk=False)
    out: list[Kelime] = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            out += [Kelime(duyulan[i1 + k].bas, duyulan[i1 + k].bit, ref[j1 + k][0], ref[j1 + k][1]) for k in range(i2 - i1)]
        elif op == "replace":
            out += _dagit(duyulan[i1].bas, duyulan[i2 - 1].bit, ref[j1:j2])
        elif op == "insert":
            once = duyulan[i1 - 1].bit if i1 > 0 else (pencere[0] + 0.1 if pencere else max(0.0, duyulan[0].bas - 0.4 * (j2 - j1)))
            sonra = duyulan[i1].bas if i1 < len(duyulan) else (pencere[1] - 0.1 if pencere else duyulan[-1].bit + 0.4 * (j2 - j1))
            out += _dagit(once, max(sonra, once + 0.15 * (j2 - j1)), ref[j1:j2])
        # "delete": senaryoda olmayan duyulan kelime, atlanir
    # tekdüze artan zaman
    for i in range(1, len(out)):
        if out[i].bas < out[i - 1].bit:
            out[i].bas = out[i - 1].bit
        if out[i].bit < out[i].bas + 0.08:
            out[i].bit = out[i].bas + 0.08
    return out


# ---------------------------------------------------------------- ASS / SRT
def bloklar(kelimeler: list[Kelime], en_cok: int = 3, max_harf: int = 18) -> list[list[Kelime]]:
    out, cur = [], []
    for w in kelimeler:
        if cur and (
            cur[-1].grup != w.grup or len(cur) == en_cok or re.search(r"[,.?!…:;]$", cur[-1].metin)
            or (len(cur) >= 2 and sum(len(x.metin) + 1 for x in cur) + len(w.metin) > max_harf)
            or w.bas - cur[-1].bit > 0.6
        ):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def _ts(t: float, ass: bool) -> str:
    t = max(0.0, t)
    if ass:
        cs = int(round(t * 100))
        return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _blok_bitisleri(bl: list[list[Kelime]], sure: float, grup_bitis: dict[int, float] | None) -> list[float]:
    bitler = []
    for i, c in enumerate(bl):
        sonraki = bl[i + 1][0].bas if i + 1 < len(bl) else sure
        b = min(c[-1].bit + 0.25, sonraki - 0.02)
        if grup_bitis and c[0].grup in grup_bitis:
            b = min(b, grup_bitis[c[0].grup])
        bitler.append(max(b, c[-1].bit))
    return bitler


def ass_yaz(kelimeler: list[Kelime], yol: Path, sure: float, font_aile: str = "Arial",
            ekler: list[dict] | None = None, genislik: int = 1080, yukseklik: int = 1920,
            grup_bitis: dict[int, float] | None = None) -> Path:
    """ekler: [{"bas":0,"bit":1,"stil":"Bolum|Kart|Yazi","metin":"..."}] (ekran yazilari, kartlar)."""
    f = font_aile
    sx = genislik / 1080
    ust = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {genislik}", f"PlayResY: {yukseklik}",
        "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        f"Style: Alt,{f},{round(80*sx)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,{round(7*sx)},3,2,{round(70*sx)},{round(70*sx)},{round(560*sx)},1",
        f"Style: Bolum,{f},{round(46*sx)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,4,0,1,{round(4*sx)},2,8,60,60,{round(150*sx)},1",
        f"Style: Kart,{f},{round(100*sx)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,4,0,1,{round(7*sx)},3,5,60,60,0,1",
        f"Style: Yazi,{f},{round(70*sx)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,{round(6*sx)},3,8,70,70,{round(380*sx)},1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    olay = []
    for e in ekler or []:
        metin = str(e["metin"]).replace("\r", "").replace("\n", r"\N")
        efekt = {"Bolum": r"{\fad(0,250)}",
                 "Kart": r"{\fad(80,150)\fscx118\fscy118\t(0,250,\fscx100\fscy100)}",
                 "Yazi": r"{\fad(120,120)}"}.get(e["stil"], "")
        olay.append(f"Dialogue: 1,{_ts(e['bas'], True)},{_ts(e['bit'], True)},{e['stil']},,0,0,0,,{efekt}{metin}")
    bl = bloklar(kelimeler)
    for c, cbit in zip(bl, _blok_bitisleri(bl, sure, grup_bitis)):
        for k, w in enumerate(c):
            a = c[0].bas if k == 0 else w.bas
            b = c[k + 1].bas if k + 1 < len(c) else cbit
            if b <= a:
                continue
            metin = " ".join(SARI + tr_buyuk(x.metin) + BEYAZ if i == k else tr_buyuk(x.metin) for i, x in enumerate(c))
            pop = r"{\fscx112\fscy112\t(0,90,\fscx100\fscy100)}" if k == 0 else ""
            olay.append(f"Dialogue: 0,{_ts(a, True)},{_ts(b, True)},Alt,,0,0,0,,{pop}{metin}")
    Path(yol).write_text("\n".join(ust + olay) + "\n", encoding="utf-8")
    return Path(yol)


def srt_yaz(kelimeler: list[Kelime], yol: Path, sure: float, grup_bitis: dict[int, float] | None = None) -> Path:
    bl = bloklar(kelimeler)
    satirlar = []
    for i, (c, b) in enumerate(zip(bl, _blok_bitisleri(bl, sure, grup_bitis)), 1):
        satirlar.append(f"{i}\n{_ts(c[0].bas, False)} --> {_ts(b, False)}\n{' '.join(x.metin for x in c)}\n")
    Path(yol).write_text("\n".join(satirlar), encoding="utf-8")
    return Path(yol)


# ---------------------------------------------------------------- CLI
def main() -> None:
    ffmpeg_yol.konsol_utf8()
    ap = argparse.ArgumentParser(description="Kelime zamanlamali TikTok tarzi altyazi (ASS + SRT)")
    ap.add_argument("girdi", type=Path, help="video ya da ses dosyasi")
    ap.add_argument("--model", default="small", help="whisper modeli: small (varsayilan), medium, large-v3-turbo")
    ap.add_argument("--dil", default="tr")
    ap.add_argument("--replikler", type=Path, help="senaryo replikleri (JSON liste); yanlis duyulan kelimeleri duzeltir")
    ap.add_argument("--ass", type=Path, help="ASS cikti yolu (varsayilan: girdi adi .ass)")
    ap.add_argument("--srt", type=Path, help="SRT cikti yolu (varsayilan: girdi adi .srt)")
    ap.add_argument("--font", help="kalin font dosyasi (varsayilan: Arial Bold)")
    a = ap.parse_args()

    replikler = replikleri_oku(a.replikler) if a.replikler else []
    print(f"whisper ({a.model}) calisiyor...")
    duyulan = whisper_kelimeler(a.girdi, a.model, a.dil, ipucu=" ".join(replikler) or None)
    kelimeler = replikle_duzelt(duyulan, replikler) if replikler else duyulan
    sure = ffmpeg_yol.sure(a.girdi)
    _, aile = font_bul(a.font)
    ass = a.ass or a.girdi.with_suffix(".ass")
    srt = a.srt or a.girdi.with_suffix(".srt")
    ass_yaz(kelimeler, ass, sure, aile)
    srt_yaz(kelimeler, srt, sure)
    print("duyulan :", " ".join(w.metin for w in duyulan))
    if replikler:
        print("duzeltme:", " ".join(w.metin for w in kelimeler))
    print(f"ASS -> {ass}\nSRT -> {srt}")


if __name__ == "__main__":
    main()
