# scripts/

Saf Python kurgu ve yardımcı betikleri. Windows ve macOS'ta aynı şekilde çalışır.
Kurulum (Python 3.10+): Windows `py -m pip install -r requirements.txt`, Mac `python3 -m pip install -r requirements.txt`.
Sanal ortam (`.venv`) etkinse iki platformda da aşağıdaki `python` komutları çalışır; değilse Windows'ta `py`, Mac'te `python3` yaz.
Her betikte `--help` var.

| Betik | Ne yapar | Örnek |
|---|---|---|
| `doctor.py` | Kurulumu kontrol eder (Python, ffmpeg/ffprobe, libass, whisper, font, Higgsfield CLI); eksik için winget/brew komutu verir | `python scripts/doctor.py` |
| `kurgu.py` | Ana kurgu: kırp, 1080x1920 ölçekle, punch-in, birleştir, efekt + müzik, loudnorm (−15 LUFS), kelime altyazısı, gömme → json'daki `"cikti"` | `python scripts/ornek_klip.py` ardından `python scripts/kurgu.py examples/kurgu-ornek.json` |
| `ornek_klip.py` | Örnek kurgu için test klipleri üretir (1080x1920, sinüs sesli, "KLİP N" yazılı) → `examples/klipler/01.mp4` … (git'e girmez) | `python scripts/ornek_klip.py` |
| `altyazi.py` | faster-whisper ile kelime zamanlaması; senaryo replikleriyle düzeltme; TikTok tarzı ASS (aktif kelime sarı) + SRT | `python scripts/altyazi.py output/bolum.mp4 --replikler replik.json` |
| `sfx.py` | BOOM, WHOOSH, RISER, HIT ve BPM ayarlı gerilim müziği sentezler (harici ses dosyası yok) | `python scripts/sfx.py --cikti output/sfx --bpm 100` |
| `zincir.py` | Kare zinciri: A klibinin sonunda B'nin ilk karesine en benzeyen kareyi SSIM ile bulur, kesim noktası önerir | `python scripts/zincir.py klipler/01.mp4 klipler/02.mp4` |
| `kare.py` | Klipten belirli saniyelerde (ya da `son`) PNG kare çıkarır | `python scripts/kare.py klipler/01.mp4 --sn 1.5 son` |
| `ffmpeg_yol.py` | Ortak modül: libass'li ffmpeg'i seçer (yoksa imageio-ffmpeg), süre/LUFS ölçer | `python scripts/ffmpeg_yol.py` |

## kurgu.json / kurgu.yaml

Göreli yollar yapılandırma dosyasının klasörüne göredir. Ara dosyalar `<çıktı klasörü>/.kurgu-tmp` altına yazılır;
`--temiz` yalnız bu klasörü siler. `--altyazisiz` whisper adımını atlar. `.kurgu-tmp/replik-rapor.json` whisper'ın ne duyduğunu gösterir.
Whisper hiçbir şey duymazsa (ör. `ornek_klip.py`'nin sinüs sesi) altyazı replik metninden tahmini zamanlamayla yazılır.

Bölüm başına düzen: `uretim/<seri>/bolumler/bolum-01/{senaryo.md, cekim-listesi.md, promptlar.md, kareler/, klipler/, kurgu.json}`;
`kurgu.json` içinde `"klip": "klipler/01.mp4"` ve `"cikti": "bolum-01.mp4"`.

**`ayarlar`** (hepsi opsiyonel): `bolum_basligi` ("Bölüm 1"), `baslik_suresi` (sn), `genislik`/`yukseklik` (1080x1920),
`fps` (30), `muzik` (true/false), `muzik_bpm` (100), `muzik_seviyesi_db` (konuşmaya göre, −15), `hedef_lufs` (−15),
`max_mb` (30; aşılırsa bitrate düşürülüp yeniden kodlanır), `altyazi` (true), `whisper_model` ("small";
daha doğru ama yavaş: "large-v3-turbo"), `dil` ("tr"), `font` (özel kalın .ttf yolu), `kontrast`, `doygunluk`, `crf`.

**`cekimler`** listesi, sırayla. Her öğe ya bir klip ya bir karttır:

| Alan | Klip | Kart | Açıklama |
|---|---|---|---|
| `klip` | ✓ | | kaynak dosya (`klipler/01.mp4`) |
| `giris`, `cikis` | ✓ | | kaynakta saniye (varsayılan: başı ve sonu) |
| `kart` | | ✓ | kart metni (`"3 GÜN ÖNCE"`, `"Devamı için\ntakip et"`; boş = düz siyah) |
| `sure` | | ✓ | kart süresi (sn) |
| `renk` | | ✓ | kart rengi (varsayılan `black`) |
| `punch_in` | ✓ | | çekim sonunda yakınlaştırma yüzdesi (10 = %110) |
| `punch_bas` | ✓ | | çekim başındaki yakınlaştırma yüzdesi (varsayılan 0) |
| `efekt` | ✓ | ✓ | `boom` / `whoosh` / `riser` / `hit` / `yok` ya da liste |
| `efekt_an`, `efekt_seviye` | ✓ | ✓ | efektin çekim başından saniyesi ve seviyesi (varsayılanlar otomatik) |
| `sessizlik_once` | ✓ | ✓ | çekimden hemen önce tüm sesi kesen sessizlik (sn, ör. 0.3) |
| `ekran_yazisi` | ✓ | ✓ | üst-orta ekran yazısı |
| `replik` | ✓ | | senaryodaki replik; altyazı yazımı buradan alınır |
| `ses` | ✓ | | `diyalog` (replik varsa varsayılan), `ortam` (kısık), `sessiz` |
| `muzik` | ✓ | ✓ | `false` = bu çekimde müzik susar |

Efekt zamanları: `whoosh` kesmeye ortalanır, `boom` diyalog çekiminde son hecede (yoksa çekim başında),
`riser` çekim sonunda biter, `hit` çekim başında.

## Windows notları

- Altyazı gömülürken ffmpeg `.kurgu-tmp` klasöründe çalıştırılır ve ASS dosyası göreli adla verilir; böylece
  `C:\...` yolundaki `:` ve `\` kaçış sorunu oluşmaz. Mutlak yol gerekirse `ffmpeg_yol.filtre_yolu()` kullan.
- Font `.kurgu-tmp/fonts` altına kopyalanır ve `fontsdir` ile verilir (Windows'ta varsayılan `C:\Windows\Fonts\arialbd.ttf`).
- PATH'teki ffmpeg'de libass yoksa imageio-ffmpeg'in ffmpeg'i otomatik kullanılır. `FFMPEG` ortam değişkeniyle elle yol verilebilir.
