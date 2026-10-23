---
name: short-drama-tr
description: >
  Türkçe AI short-drama (dikey mikro dizi, 9:16, bölüm başı ~60 sn) üretim yöntemi: fikir puanlama,
  sezon planı, kancalı bölüm yapısı, karakter/mekân varlıkları, Veo 3.1 Lite ve Seedance 2.5 klip
  promptları, kare zinciri, maliyet onayı ve kurgu (altyazı, ses efekti, -15 LUFS). Şu isteklerde
  kullan: "mini dizi yap", "dikey dizi", "short drama", "bölüm yaz", "senaryo yaz", "sezon planla",
  "karakter sayfası", "Higgsfield ile üret", "klip promptu", "Veo promptu", "Seedance promptu",
  "kurgu yap", "altyazı ekle", "TikTok dizisi". English triggers: "make a short drama",
  "vertical micro drama", "AI series episode", "write a Seedance prompt", "Veo prompt",
  "character sheet", "storyboard", "season plan", "cliffhanger", "edit the episode".
---

# Türkçe AI Short-Drama Üretimi

Bu skill, Higgsfield MCP ile Türkçe dikey mikro dizi üretmenin baştan sona yöntemidir.
Hedef: konuşan karakterler, tutarlı yüzler, ilk saniyede kanca, sonunda cliffhanger.

Ayrıntılar `references/` altında:

| Dosya | Ne zaman oku |
|---|---|
| `references/fikir-bankasi.md` | Kullanıcının fikri yoksa ya da fikir seçilecekse |
| `references/varliklar.md` | Yüz, kıyafet, karakter sayfası, mekân üretilecekse |
| `references/klip-promptu.md` | Veo veya Seedance klip promptu yazılacaksa |
| `references/kurgu-ses.md` | Kurgu, altyazı, ses efekti, müzik, son miks |
| `references/maliyet.md` | Bütçe, tarif seçimi, kredi hesabı |

Doldurulacak şablonlar repo kökünde `templates/` altında. Tam bir örnek: `examples/cifte-davetiye/`.

---

## 0. Değişmez kurallar (her adımda geçerli)

1. **Maliyet önce, onay sonra.** Her ücretli üretimden önce tahmini krediyi göster.
   MCP'de maliyet aracı varsa onu kullan. Yoksa CLI ile aynı parametrelerle sor:
   ```
   higgsfield generate cost <model> --prompt "..." [diğer parametreler]
   ```
   Kullanıcı "evet" demeden gönderme. Toplu gönderimde toplamı göster, tek onay al.
2. **Tavan.** Bölüm başında toplam kredi tavanı belirle (örnek: tahmin × 1.5). Harcamayı
   `uretim/<seri>/harcama.txt` dosyasına satır satır yaz (`etiket kredi`). Tavanı aşacaksan dur, sor.
3. **Çift gönderim yok.** Bir iş zaman aşımına uğradıysa yeniden göndermeden önce iş listesine bak
   (MCP iş listesi ya da `higgsfield generate list`). Aynı promptu iki kez ödeme.
4. **Eşzamanlı iş sınırı: 4.** Aynı anda en fazla 4 iş kuyrukta olsun.
5. **Gerçek kişi yok.** Ünlüye ya da tanıdık birine benzeyen yüz üretme, kullanma.
   Karakter adlarının gerçek bir ünlüye ait olmadığını kontrol et.
6. **Platform güvenli.** Çıplaklık, cinsellik, kanlı şiddet yok. Herkes yetişkin.
7. **TikTok'ta AI etiketi açık.** Açıklamada "Kurgudur, AI ile üretildi." yazar.
8. **Gelir vaadi yok.** Ne README'de, ne açıklamada, ne kullanıcıya önerilerde "şu kadar kazanırsın" yok.
9. **Fiyatlar 22 Eki 2026 tarihli.** Değişmiş olabilir; her zaman canlı maliyet aracına güven.

---

## 1. Fikir

Kullanıcının fikri yoksa `references/fikir-bankasi.md` içinden aday seç.
Her adayı 6 ölçütle 1–5 arası puanla:

| Ölçüt | 5 puan | 1 puan |
|---|---|---|
| Anında anlaşılır durum | Tek karede anlaşılır | Arka plan anlatısı ister |
| Tanıdık duygu | Herkes yaşamıştır | Nadir, soyut |
| Görünür doruk | Fiziksel olay: tokat, ifşa, düşen kadeh | İç ses, düşünce |
| Tepki zıtlığı | İki kişi aynı anı zıt okur | Kimse tepki vermez |
| Üretim kolaylığı | 2–4 konuşan kişi, 1–2 mekân | Kalabalık, araç, kavga, dans |
| Seri potansiyeli | 10+ bölüm taşır | Tek hikâye |

En yüksek 3 adayı tek cümlelik tanıtımla göster, birini öner. Kullanıcı "sen seç" derse en yükseği al.

Türk izleyicisinde iyi çalışan motorlar: dedikodu, magazin, sosyete, aldatma, kayınvalide,
intikam, saklı kimlik, miras, düğün/nişan/kına. Hikâyeyi bir **duyguya** bağla
("en yakın arkadaşım beni sırtımdan vurdu"), mekâna değil.

## 2. Sezon planı

Şablon: `templates/SEZON.md`. Sezon 8–10 bölüm.

- **Logline:** tek cümle. Kim, neyi keşfeder, ne yapar.
- **Ana sır:** sezon boyunca açılmayan büyük soru. Son bölümde açılır ya da 2. sezona devreder.
- **Bölüm başına twist:** her bölüm bir yeni bilgi verir.
- **Cliffhanger haritası:** her bölümün son 3 saniyesi bir soru bırakır. Sonraki bölüm o soruyla açılır.
- Karakter sayısı: 3–5 konuşan kişi. Mekân: 3–4 sabit mekân. Az varlık = az kredi, çok tutarlılık.

## 3. Bölüm yapısı (~60 sn)

Şablonlar: `templates/BOLUM-SENARYO.md`, `templates/CEKIM-LISTESI.md`.

| Bölüm | Süre | Ne olur |
|---|---|---|
| **Kanca** | 0–5 sn | Bölümün doruk anıyla aç. Sonra siyah kart "3 GÜN ÖNCE" ile geri dön. |
| **Bağlam** | 5–25 sn | Kim, ne istiyor. Duygu dalgası: başlangıç → umut → darbe → şans. |
| **Tırmanış** | 25–45 sn | Yeni karakter ya da ters köşe. Tepki çekimleri: aynı anı iki kişi zıt okur. |
| **Doruk + cliffhanger** | 45–60 sn | Cevaba bir adım kala kes. "Söz ver, gösterme." Siyah ekran, "Devamı için takip et". |

Kurallar:
- **Darbe ritmi:** her 13–30 sn'de bir darbe (yeni bilgi, ihanet, ifşa). Örnek bölümde darbeler ~7, ~20, ~34, ~46. sn.
- **Önemli yüzü geç göster.** Önce sırtı, eli, kıyafeti, gözleri; yüz en son. Kancada bir kez görünen yüz,
  bağlamda saklanır, dorukta geri gelir.
- **Replik ≤ 8 kelime.** Ünsüzleri net kelimeler seç. Kelime sonu ünsüzleri yutulabiliyor.
- **Anlatıcı yok, karakterler konuşur.** Anlatıcılı fotoroman "yeterince gerçek değil" hissi veriyor.
- **Sürekli sahne.** Birbirinden kopuk 16 klip yerine 3–4 sürekli sahne. Sahne içinde kare zinciri,
  kurguda hızlı kesme (bkz. §6, §7).
- **Yazılı nesneler.** Davetiye, mektup, telefon ekranı: yazılı yüz kameraya hiç dönmez.
  Seyirci içeriği karakterin yüzünden okur.

Senaryoyu yazınca kullanıcıya göster, onay al. Sonra çekim listesine geç.

## 4. Varlıklar

Ayrıntı ve hazır promptlar: `references/varliklar.md`, `templates/KARAKTER.md`, `templates/MEKAN.md`.

| Varlık | Model | Kural | Ad |
|---|---|---|---|
| Yüz | Soul 2.0 | 4–6 portre üret, kullanıcı birini seçer | `@DefneYuz` |
| Kıyafet | Soul 2.0 | Omuzdan ayağa, düz duvar. İnce kol ya da kapalı yaka; askı yok, derin dekolte yok | `@DefneKiyafet` |
| Karakter sayfası | GPT Image 2 | Gri fon, 3 görünüm: ön boy, arka boy, yakın yüz. Ön boy görünümde yüz silinmiş | `@Defne` |
| Görünüm değişikliği | Seedream (düzenleme) | Sayfayı düzenle; yüz, oran, düzen aynı kalsın | `@DefneGelinlik` |
| Mekân | Soul Location | 3/4 açı, insansız, tüm hareket yolları görünür | `@YaliHol` |

- Her varlığa **sabit bir ad** ver ve her yerde aynı adı kullan.
- Varlıkları `uretim/<seri>/varliklar/` altına kaydet, `templates/KARAKTER.md` kartına işle.
- Askılı saten elbise sürekli filtreye takıldı. Kıyafeti baştan güvenli seç.

## 5. Sabitler (her klipte kelimesi kelimesine aynı)

Karakter kartında bir kez yaz, her klip promptuna **kopyala**. Asla yeniden ifade etme.

- **SES tarifi:** aksan + perde + tempo + tını. Örnek:
  `speaks Turkish with a native Istanbul accent; soft mezzo-soprano pitch; measured pace; warm, slightly breathy timbre.`
  O anki ruh hâli (fısıltı, titreyen) ses tarifine değil ACTION TIMING satırına yazılır.
- **Karakter tarifi:** 30–60 kelime. Yaş, saç, göz, ten, ayırt edici iz, kıyafet, takı.
- **STİL bloğu (LOOK):** ışık, film dokusu, renk, alan derinliği, 9:16. Tüm bölümde aynı.
- **ACTING TASK:** MOTIVE (neden) · GOAL (ne istiyor) · OBSTACLE (ne engelliyor) · TACTIC (nasıl deniyor).
- **POSITIVE LOCKS:** yalnız tırnaktaki replik bir kez konuşulur; dinleyenin ağzı kapalı; ekranda yazı yok;
  müzik yok (müziği kurguda ekleriz).
- **Konuşma sırası:** ikinci konuşan "She replies:" / "He replies:" ile başlar. Model sırayı böyle anlar.
- **Mekân haritası + ilk kare yerleşimi:** kim ekranın solunda/sağında, yüz x/y yüzdesi, bakış yönü.
  Sol/sağ her zaman kameraya göre.

## 6. Klip üretimi

Promptun tam iskeleti ve örnekleri: `references/klip-promptu.md`, `templates/prompt-kaliplari.md`.

**Ekonomik yol: Veo 3.1 Lite** (`veo3_1_lite`, 4/6/8 sn, ses açık, 9:16).
- Her klip **tek çekim**, tek konuşan. Başlangıç karesi (`--start-image`) zorunlu.
- **Kare zinciri:** bir sonraki klibin başlangıç karesi, öncekinin son karesidir (`scripts/kare.py` ile ücretsiz çıkar).
  Böylece sahne kopmadan sürer.
- Bitiş karesi (`end image`) isteğe bağlı. Dikkat: NSFW retlerini artırdı ve Veo bitiş karesini birkaç kare aşıyor.
  Birleşimde en yakın kareyi SSIM ile bul, orada kes (`scripts/zincir.py`).
- **Çekim/karşı çekim kadraj kilidi:** iki taraf aynı lens, aynı mesafe, aynı göz hizası. Konuşan ekranın
  bir yanında (x %55), karşısındaki öbür yanında (x %45), bakışlar lensin hemen yanından birbirine.
  Aynı kişinin farklı replikleri **aynı başlangıç karesinden** üretilir; kesme görünmez olur.
- Kamera: `smooth steady camera, no whip pans`. "slightly handheld" ile "steady"yi birlikte yazma.

**Premium yol: Seedance 2.5** (`seedance_2_5`, 720p sesli).
- Tek üretimde 30 sn'ye kadar, içinde zamanlı HARD CUT'larla çok kesme; 50'ye kadar referans.
- Karakter sayfaları ve mekân `@ad` ile eklenir (mod `omni_reference`). Ses tarifini yine her klipte aynen yaz.
- Yalnız o klipte görünen referansları ekle. Görünmeyen `@ad` modele "bunu kadraja sok" der.

**Dengeli yol:** kanca, yüzleşme ve cliffhanger için toplam ~30 sn Seedance 2.5; gerisi Veo Lite.

Her klipten sonra izle, sorunu açık sözle adlandır ("vurgu Ankara'lı çıktı", "kart yazılı yüzünü çevirdi"),
yalnız bozuk kısmı değiştir, yeniden üret. Bir an bozuksa sahneyi değil o anı yeniden çek (insert klip).
Yeniden üretim ve filtre reti sonrası yapılan deneme de ayrı maliyet onayı ister.

## 7. Kurgu ve ses

Ayrıntı: `references/kurgu-ses.md`. Betikler `scripts/` altında; her biri `--help` ile kullanım gösterir.

- Çekimler **1.5–3 sn**. Sürekli klipleri kurguda parçala. Darbe anlarında **punch-in** (%6–10 yakınlaştırma).
- Ses tasarımı (`scripts/sfx.py`): sentez BOOM (darbe), WHOOSH (geçiş), RISER (gerilim), sert gerilim müziği.
  Kritik replikten önce **0.3 sn tam sessizlik**. Efektleri replik altında kıs.
- Altyazı (`scripts/altyazi.py`): kelime kelime, aktif kelime **sarı**, kalın beyaz, siyah kontur.
- Ekran yazıları: "Bölüm X" (ilk 1 sn), "3 GÜN ÖNCE" (siyah kart), "Devamı için takip et" (son siyah kart).
- Son miks **−15 LUFS**. Çıkış 1080x1920.
- Kurgu: çekim listesini `kurgu.json`a çevir (örnek `examples/kurgu-ornek.json`), `scripts/kurgu.py` ile işle.
  Kare çıkarma: `scripts/kare.py`. Kare zinciri kesimi: `scripts/zincir.py`. Ortam kontrolü: `scripts/doctor.py`.
  Alanlar ve örnekler: `scripts/README.md`.

## 8. Yayın

`docs/04-tiktok-yayin.md`: başlık "Bölüm N | <kanca cümlesi>", açıklamada "Kurgudur, AI ile üretildi.",
AI etiketi açık, 3–5 hashtag, aynı seri için oynatma listesi.

---

## Akış özeti (kullanıcıya bunu uygula)

1. `python scripts/doctor.py` (sanal ortam yoksa Windows'ta `py`, Mac'te `python3`) → eksik varsa kurdur. Higgsfield MCP bağlı mı bak.
2. Fikir → 6 ölçüt puanı → seçim.
3. `uretim/<seri>/SEZON.md` → onay.
4. `uretim/<seri>/bolumler/bolum-01/senaryo.md` + `cekim-listesi.md` → onay.
5. Varlık listesi + maliyet → onay → üret → kullanıcı seçer → adlandır.
6. Klip promptları (`promptlar.md`) + toplam maliyet + tavan → onay → en fazla 4 iş eşzamanlı.
7. Her sonucu `result_url` alanından `bolumler/bolum-01/klipler/` altına indir (01.mp4, 02.mp4 …). İlk URL giriş görseli olabilir.
8. Kurgu → kontrol kareleri → kullanıcıya göster → `kurgu.json` (`"cikti": "bolum-01.mp4"`) → `python scripts/kurgu.py uretim/<seri>/bolumler/bolum-01/kurgu.json --temiz`
   → son dosya `uretim/<seri>/bolumler/bolum-01/bolum-01.mp4`. Ara dosyalar `bolum-01/.kurgu-tmp/` altında.
9. Yayın metni (başlık, açıklama, hashtag).

Her adımın sonunda kısa durum ver: ne üretildi, ne harcandı, kalan tavan.

Klasör düzeni:
```
uretim/<seri-adi>/
  SEZON.md
  harcama.txt
  varliklar/                # @Ad görselleri, karakter ve mekân kartları
  bolumler/
    bolum-01/
      senaryo.md            # templates/BOLUM-SENARYO.md'den
      cekim-listesi.md      # templates/CEKIM-LISTESI.md'den
      promptlar.md          # klip promptları
      kareler/              # başlangıç ve kontrol kareleri (scripts/kare.py)
      klipler/              # indirilen klipler: 01.mp4, 02.mp4 …
      kurgu.json            # scripts/kurgu.py girdisi; "klip": "klipler/01.mp4", "cikti": "bolum-01.mp4"
      bolum-01.mp4          # son kurgu (kurgu.json'daki "cikti")
      bolum-01.srt
      .kurgu-tmp/           # kurgu.py ara dosyaları; --temiz yalnız bunu siler
```
