# Klip promptu yazma

Promptlar **İngilizce** yazılır, replikler **Türkçe** ve tırnak içinde kalır.
Video modelleri İngilizce yönergeyi daha iyi izliyor; Türkçe repliği ise tırnaktan aynen okuyor.

Tekniklerin bir kısmı Higgsfield'ın short-drama rehberinden ve herkese açık AI film yapım rehberlerinden
uyarlandı, kendi deneyimimizle sınandı:
https://higgsfield.ai/@adilinthewildtempo/blogs/how-to-make-ai-short-drama

## Temel ilkeler

1. **Görüneni yaz.** "Gergin" değil: "eli kartı sıkıyor, gözleri yere iniyor, çenesi kasılıyor".
2. **Olumlu yaz.** "Kameraya dönmesin" yerine "only its blank back faces the camera".
3. **Sol/sağ kameraya göre.** "Screen left", "x 25%".
4. **Her prompt kendi başına bir belgedir.** Model önceki klibi hatırlamaz. "Yukarıdaki gibi", sahne numarası,
   önceki sahne özeti yazma. Bu klipte olmayan karakteri ya da `@ad`ı ekleme.
5. **Sabit bloklar kopyalanır.** Karakter, ses, mekân, stil blokları her klipte kelimesi kelimesine aynı.
6. **Kısa ve yoğun.** Kritik yerde ayrıntılı, önemsiz yerde kısa. Her önemli şeyi bir kez, net söyle.
7. **Müzik yok.** Müziği kurguda ekleriz; klipte pişmiş müzik temizlenmez. Yalnız ortam sesi.
8. **Ekranda yazı yok.** Altyazıyı kurguda ekleriz.

## Veo 3.1 Lite iskeleti (tek çekim, 4/6/8 sn)

Parametreler: `veo3_1_lite`, süre 4/6/8, en-boy 9:16, ses açık, başlangıç karesi.
Hem başlangıç hem bitiş karesi verilirse süre 8 sn olmak zorunda.
CLI karşılığı:
```
higgsfield generate create veo3_1_lite --prompt "<prompt>" --duration 6 --aspect_ratio 9:16 --generate_audio true --start-image kareler/K1.png --wait
```

Blok sırası:
```
<N> seconds, one continuous shot, real time, vertical 9:16.
SCENE: 1–2 cümle: ne oluyor, nerede, ne zaman.
SUBJECT: <karakter tarifi, sabit>. <Ad> <SES tarifi, sabit>. Face, hair and outfit 100% match the first frame.
LOCATION MAP: <mekân tarifi, sabit>. Kamera nerede, kime ne kadar uzak. Same place, same light throughout.
FIRST FRAME: exactly the start image. Kim nerede (x/y %), nereye bakıyor.
OPTICS / CAMERA: lens görünümü, yaklaşık görüş açısı (derece), hareket (çok yavaş push-in / locked-off).
ACTING TASK: MOTIVE … GOAL … OBSTACLE … TACTIC …
ACTION TIMING:
0.0-0.4s: konuşmadan önceki küçük hareket.
0.4-3.0s: <Ad> says, <o anki ton>: "<Türkçe replik, ≤ 8 kelime>"
3.0-N s: sessizlik; ağız kapalı, tepki.
PHYSICS: saç, kumaş, eşya nasıl davranır.
<EŞYA bloğu, sabit>
AUDIO: ortam sesi. Only <Ad>'s voice.
LOOK: <stil bloğu, sabit>
POSITIVE LOCKS: only the quoted line is spoken, once; lips move only during the quoted line; clean picture without on-screen text or subtitles; ambient sound only, without music; framing stays identical to the first frame.
```

Notlar:
- Replikten önce 0.3–0.6 sn boşluk bırak. Model ilk kareden hemen konuşursa ilk hece kayboluyor.
- Replikten sonra en az 1 sn sessiz tepki yaz. Kurguda tepki çekimi olarak işe yarar.
- Konuşan yüz kameraya dönük ya da 3/4 olsun. Profil konuşma dudak senkronunu zayıflatır.
- Kamera: `smooth steady camera, slow controlled movement, no whip pans`. "slightly handheld" ile birlikte yazma.
- Diksiyon: `clear diction, every final consonant pronounced`. Türkçede kelime sonu ünsüzleri yutulabiliyor.
- Duygu: `restrained emotion, no sobbing`. Hıçkırık, dudakları bozuyor ve filtreye yaklaşıyor.

## İki kişilik konuşma (tek klipte)

İkinci konuşanı "She replies:" / "He replies:" ile başlat. Model bu kelimeden sırayı anlar,
iki ses birbirine karışmaz.
```
0:00-0:04: Medium two-shot, slow push-in - Defne says (voice trembling, jaw tight): "Davetiyede gelin olarak senin adın var."
0:04-0:08: Camera drifts over Defne's shoulder onto Selin - She replies (cool, slow smirk): "Kerem seni hiç sevmedi, Defne."
```
Veo'da 8 sn'ye iki replikten fazlasını sığdırma.

## Seedance 2.5 iskeleti (çok kesmeli, 30 sn'ye kadar)

Parametreler: `seedance_2_5`, 720p, ses açık, 9:16. Referanslar `@ad` ile.
Referanslı üretimde mod `omni_reference` olmalı. Toplam 50 referans, en fazla 30 görsel.
CLI karşılığı (referanslar sırayla `@image1`, `@image2`… olur; MCP'de kayıtlı adları kullan):
```
higgsfield generate create seedance_2_5 --mode omni_reference --duration 30 --resolution 720p --aspect_ratio 9:16 --image-references Defne.png --image-references Nermin.png --image-references YaliHol.png --prompt "<prompt>" --wait
```

Blok sırası (yalnız gerekenleri kullan):
```
SCENE CONTEXT: 2–4 cümle, duygusal dönüş dahil. Kim nerede.
ACTIVE REFERENCES:
@Defne: yaş, rol, şu anki durumu, elindeki eşya, ses tarifi. Face, hair and outfit 100% match the reference.
@Nermin: …
@YaliHol: the room is identical to the reference.
LOCATION MAP: ön plan / orta plan / arka plan, kapılar, ışık kaynakları, kamera yeri.
FIRST FRAME / BLOCKING: ilk karede kim nerede, nereye bakıyor.
FORMAT MODE: timed multishot; cuts only at the stated seconds, the camera does not cut on its own.
OPTICS: her kesim için çekim boyu ve görüş açısı (derece); no drift mid-segment.
ACTION TIMING:
0.0s to 2.5s — …
2.5s HARD CUT
2.5s to 5.0s — <Ad> says (ton): "…"
5.0s HARD CUT
…
PERFORMANCE: kas düzeyinde duygu, bakış yönü, nefes.
PHYSICS: kumaş, saç, eşya.
LIGHTING: kaynak, yön, renk sıcaklığı. Tüm kesimlerde aynı mantık.
AUDIO: ortam sesi, replikler, müzik yok.
STYLE: photoreal, film dokusu, 9:16.
POSITIVE LOCKS: aynı karakterler, aynı mekân, aynı ışık; yalnız tırnaktaki replikler; ekranda yazı yok.
```

Notlar:
- Kesim türleri: HARD CUT, MATCH CUT, INSERT CUT, REVERSE CUT. Geçiş efektini kurguda yap.
- Kesimler arasında aynı karakter seti, aynı ekran yönü, aynı ışık, aynı kıyafet ve eşya durumu.
- 30 sn'lik tek üretim tam bir duygusal yay taşıyabilir: kanca + bağlam ya da yüzleşmenin tamamı.
- Kesim başına 2–4 sn hedefle; kurgu ritmine zaten yakın gelir.
- Görüş açısı rehberi (yaklaşık): aşırı yakın ~15°, yakın ~24°, orta yakın ~30°, orta ~40°, geniş ~60°.

## Kare zinciri (Veo yolu)

Bir sahne birden fazla Veo klibi ise:
1. Klip 1: başlangıç karesi A.
2. Klip 1'in son karesini çıkar: `scripts/kare.py` (ücretsiz).
3. Klip 2: başlangıç karesi = klip 1'in son karesi.
4. Bitiş karesi verdiysen Veo onu birkaç kare aşabilir. Birleştirirken SSIM ile en yakın kareyi bul, orada kes (`scripts/zincir.py`).

## Çekim / karşı çekim kilidi

- İki taraf **aynı lens görünümü** (örnek 85mm, ~24°), **aynı mesafe** (1.2 m), **aynı göz hizası**.
- Konuşan sağdaysa yüzü x %55, bakışı lensin hemen soluna; karşısındaki solda x %45, bakışı lensin hemen sağına.
- Karşı tarafın saçı/omzu ön planda flu kenar olarak görünsün (ekranın %10–12'si).
- Aynı kişinin bütün replikleri **aynı başlangıç karesinden**. Kurguda iki replik arası kesme fark edilmez.

## Revizyon

Sorunu somut adlandır, yalnız onu değiştir:
- "Kart yazılı yüzünü kameraya çevirdi" → kart bloğunu güçlendir, o anı kurgudan çıkar.
- "Kamera savruldu" → `smooth steady camera, no whip pans`, handheld ifadesini sil.
- "İsim yanlış duyuldu" → repliği kısalt, ünsüzü net kelime seç, efekti replik altında kıs.
- NSFW reti → kıyafeti kapat, "leans in close", "crushes", "slip dress" gibi ifadeleri çıkar, bitiş karesini kaldır.
