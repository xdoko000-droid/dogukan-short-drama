# Kurgu, ses ve altyazı

Kurgu ücretsizdir ve bölümün enerjisini asıl o belirler. Aynı klipler, yavaş kurguda sıkıcı,
hızlı kurguda sürükleyici olur.

Betikler `scripts/` altında. Ayrıntılı kullanım `scripts/README.md`; her biri `python scripts/<ad>.py --help` ile de kullanımını gösterir.
Çekim listesi (`cekim-listesi.md`) bölüm klasöründe `kurgu.json` dosyasına çevrilir; alanlar `scripts/README.md`de.
Klipler `klipler/` altında (`"klip": "klipler/01.mp4"`), son dosya json'daki `"cikti"` (ör. `bolum-01.mp4`),
ara dosyalar `.kurgu-tmp/` altında (`--temiz` yalnız bu klasörü siler).

| Betik | İş |
|---|---|
| `scripts/doctor.py` | Python, ffmpeg (altyazı desteğiyle), paketler, Higgsfield erişimi kontrolü |
| `scripts/kare.py` | Klipten kare çıkarma (son kare, belirli saniye); kare zinciri ve kontrol kareleri |
| `scripts/zincir.py` | Kare zinciri birleşimi: SSIM ile en yakın kareyi bulur, kesim noktası önerir |
| `scripts/sfx.py` | BOOM, WHOOSH, RISER efektleri ve gerilim müziği sentezi |
| `scripts/altyazi.py` | Kelime zamanlamalı altyazı: kelime kelime, aktif kelime sarı |
| `scripts/kurgu.py` | `kurgu.json`dan kurgu: kesme, punch-in, siyah kartlar, efekt, müzik, altyazı, −15 LUFS. Örnek: `examples/kurgu-ornek.json` |

## Ritim

- Çekim süresi **1.5–3 sn**. Ortalama ~2.2 sn iyi çalıştı (58 sn'de 24 çekim + 3 siyah kart).
- Sürekli bir klibi kurguda 2–4 parçaya böl: replik, tepki, insert.
- **Tepki çekimi** her darbeden sonra: dinleyenin donmuş yüzü, ağız kapalı.
- **Punch-in:** darbe anında %6–10 kırpıp yakınlaştır. Yeni çekim gibi hissettirir, ücretsizdir.
- **Eşleşme kesmesi:** telefondaki yüzük → başka bir eldeki aynı yüzük. Twisti tek kesmeyle anlatır.
- Kancadaki doruk çekimini cliffhanger öncesi aynı kadrajla tekrar kullan. Seyirci "işte o an" der.

## Ses tasarımı

Hepsi sentez; telifli ses yok.

| Efekt | Ne zaman | Tarif |
|---|---|---|
| BOOM | Darbe anı, replik son hecesinden hemen sonra | Düşük frekanslı sinüs + gürültü patlaması, ~1.2 sn sönüm |
| WHOOSH | Geçiş, siyah kart | Bant geçirgen gürültü süpürmesi, ~0.4 sn |
| RISER | Darbe öncesi gerilim | 1.5–3 sn yükselen ton + gürültü |
| Müzik | Bölüm boyunca | Sert gerilim: ~100 BPM nabız, düşük ostinato; darbe öncesi bir ölçü boşluk |

Kurallar:
- Kritik replikten önce **0.3 sn tam sessizlik**. Replik böyle "çarpar".
- Efektleri **replik altında kıs**. Bir riser, "Nermin" ismini "Dermin" gibi duyurdu.
- Şans anında (kahramanın karar verdiği an) müziği kes. Sessizlik en güçlü efekt.
- Son miks **−15 LUFS** (ffmpeg `loudnorm I=-15`).

## Altyazı

- Kelime zamanlaması konuşma tanıma ile (whisper benzeri) çıkarılır.
- Kelime kelime ya da 2–3 kelimelik bloklar. **Aktif kelime sarı**, diğerleri **kalın beyaz**, **siyah kontur**.
- Konum: ekranın alt-orta üçte biri. Yüzü ve ağzı kapatma.
- Türkçe karakterleri (ç, ğ, ı, İ, ö, ş, ü) destekleyen kalın bir yazı tipi kullan.
- Son miksten tanıma yapıp replikleri senaryoyla karşılaştır. Yanlış duyulan replik varsa yeniden üret ya da sesi düzelt.

## Ekran yazıları

| Yazı | Yer | Süre |
|---|---|---|
| "Bölüm X" | İlk çekimin üstünde, küçük, üst orta | 0–1 sn |
| "3 GÜN ÖNCE" | Siyah kart, ortada | ~1 sn |
| "Devamı için takip et" | Son siyah kart, ortada | ~2.5 sn |

## Teknik

- Klipler 720x1280 gelir; 1080x1920'ye ölçekle.
- **ffmpeg ve altyazı:** Altyazı gömmek için ffmpeg'in libass desteği gerekir. Bazı paket yöneticisi
  sürümlerinde (örnek: macOS Homebrew'un varsayılan ffmpeg'i) yok. `imageio-ffmpeg` paketinin getirdiği
  ffmpeg bunu destekliyor; `scripts/doctor.py` hangisini kullanacağını söyler.
- Veo bitiş karesini birkaç kare aşabilir. Birleşimde SSIM ile en yakın kareyi bulup orada kes (`scripts/zincir.py`).
- Kurgudan sonra 5–7 **kontrol karesi** çıkar (kanca, her darbe, cliffhanger) ve kullanıcıya göster.

## Kontrol listesi (teslimden önce)

- [ ] İlk 1 sn'de yüz ve ses var, siyah açılış yok.
- [ ] Darbeler 13–30 sn arayla.
- [ ] Hiçbir karede okunur anlamsız yazı yok (kart, ekran, tabela).
- [ ] Dinleyenlerin ağzı kapalı; yanlış kişi konuşmuyor.
- [ ] Altyazı replikle birebir.
- [ ] Son kart "Devamı için takip et".
- [ ] −15 LUFS, 1080x1920, 9:16.
