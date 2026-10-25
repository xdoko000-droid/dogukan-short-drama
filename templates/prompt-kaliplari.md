# Prompt kalıpları

`<…>` alanlarını doldur. Kod bloğundaki metin doğrudan modele gider; bloğun içine yorum yazma.
Promptlar İngilizce, replikler Türkçe ve tırnak içinde.
Sabit bloklar (KARAKTER, SES, LOCATION, LOOK, eşya) karakter ve mekân kartlarından **aynen kopyalanır**.

Örnek sabitler (Çifte Davetiye):
```
LOOK: photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.
```

---

## 1. Yüz seçenekleri — Soul 2.0, 3:4, 4–6 adet

```
Close-up portrait of <Ad>, a <age> Turkish <woman/man>, <hair>, <eyes>, <skin>, <one distinguishing mark>, <makeup / grooming>, calm neutral expression, looking at the camera. Plain light grey studio background, soft even light, photorealistic live action, 35mm film grain, natural skin texture. Vertical 3:4.
```

## 2. Kıyafet — Soul 2.0, 3:4

```
Full outfit from the shoulders to the feet on an invisible standing figure against a plain light grey wall: <garment, colour, fabric>, thin long sleeves and an elegant, modest high neckline, <shoes>, <jewellery>. No bags, no hand-held props. Soft even studio light, photorealistic. Vertical 3:4.
```
Askı, açık omuz, derin dekolte yazma; filtreye takılıyor.

## 3. Karakter sayfası — GPT Image 2, 16:9

Referanslar: `@<Ad>Yuz`, `@<Ad>Kiyafet`.
```
Reference sheet for a single character. Take the identity strictly from image 1 and the clothing exactly from image 2. One uniform mid-grey backdrop behind everything. Lay out three views in a row: (1) standing front view showing the whole body from head to shoes; (2) standing back view, whole body; (3) head-and-shoulders portrait facing the camera. In the standing front view, render the head with no facial details at all, just plain skin where the features would be; the portrait in panel 3 carries the only visible face. Soft, even studio light. Photorealistic live action, 35mm film grain, muted tones. No text, no labels. Aspect ratio 16:9.
```

## 4. Görünüm değişikliği — Seedream (düzenleme), 16:9

Referans: `@<Ad>`.
```
Edit this character sheet. Change only: <örnek: the outfit to an ivory satin wedding gown with long lace sleeves and a high neckline>. Keep the face, hair, body proportions, grey background, three-panel layout and blank face on the full-body front view exactly the same. No text.
```

## 5. Mekân — Soul Location, 16:9

```
<Place>, <time of day>. Three-quarter view showing the whole layout: <entrance door position>, <main furniture>, <windows and what is outside>, <walking path>, <main light sources>. No people. Photorealistic live action, 35mm film grain, <colour mood>. Aspect ratio 16:9.
```

## 6. Storyboard (isteğe bağlı) — nano_banana_2 ya da GPT Image 2, 16:9

Yalnız kompozisyon referansı. Panel oranına model uymayabilir.
```
Cinematic storyboard sheet, 3x3 grid, nine sequential panels of ONE continuous scene in <place>. Sheet 16:9; each panel a tall vertical 9:16 frame. Thin clean separators, no numbers inside panels. Under each panel a thin off-white strip with three short uppercase lines in a clean sans-serif font: CAM, MOVE, VOICE. Characters identical in every panel: <ADI>: <one short sentence>. <ADI>: <one short sentence>. Same place, same light throughout. Smooth steady camera. No readable writing anywhere in the panels.
Panel 1: <framing>. <action>. CAM: <…>. MOVE: <…>. VOICE: "<replik>" or (BEAT. NO WORDS.)
Panel 2: …
Panel 9: <closest, most emotional frame>.
Photorealistic live action, 35mm film grain, muted tones.
```

## 7. Başlangıç karesi — nano_banana_2, 9:16

Referanslar: `@<Ad>` (kimlik), mekân ya da önceki kare (ışık ve renk).
```
Use image 1 (character sheet) for the person's identity, 1:1 face similarity. Do not take the grey backdrop, the panel borders or the multi-view layout from image 1. Use image 2 only for the location, colours and light. Do not use any person from image 2. Create ONE full-frame vertical 9:16 cinematic film still, no panels, no borders.
SUBJECT: <KARAKTER sabit bloğu>. <what they hold, how>.
FIRST FRAME / BLOCKING: <shot size, from where to where>. <Ad> <left/right> of centre (face at x <…>%, eyes at y <…>% of the frame), body <three-quarter turned toward frame left/right>, eyes <just left/right of the lens> toward someone off-screen <left/right>. <Out-of-focus edge of the other person fills the far left/right 10–12% of the frame.>
LOCATION: <LOCATION sabit bloğu>.
OPTICS: <85mm lens look, about 24 degrees horizontal field of view>, eye-level camera at <1.2> m, background in soft bokeh.
EXPRESSION: <closed mouth, visible micro-expression>.
LOOK: <LOOK sabit bloğu>
POSITIVE LOCKS: clean image with no writing anywhere; <prop shows only its blank back>; one person in focus.
```

## 8. Veo 3.1 Lite klibi — tek çekim, 4/6/8 sn

Ayarlar: `veo3_1_lite`, süre 4/6/8, 9:16, ses açık, başlangıç karesi. Bitiş karesi verirsen süre 8 olmalı.
```
<N> seconds, one continuous shot, real time, vertical 9:16.
SCENE: <Time, place. What happens in one or two sentences.>
SUBJECT: <KARAKTER sabit bloğu> <SES sabit bloğu> The start image defines <Ad>'s face, hair and outfit; keep them unchanged.
LOCATION MAP: <LOCATION sabit bloğu>. Camera <eye-level>, <1.2> m from <Ad>. Same place, same light throughout.
FIRST FRAME: exactly the start image. <Ad> <position>, eyes <direction>.
OPTICS / CAMERA: <85mm look>, about <24> degrees field of view, <locked framing with a very slow push-in of about 5 percent | locked-off, no camera movement>. Smooth steady camera, no whip pans.
ACTING TASK: MOTIVE: <why>. GOAL: <what they want from the other person>. OBSTACLE: <what is in the way>. TACTIC: <how they try, physically>.
ACTION TIMING:
0.0-0.4s: <small movement before speaking>.
0.4-<t>s: <Ad> says, <tone>: "<Türkçe replik, en fazla 8 kelime>"
<t>-<N>s: silence; <reaction, lips closed>.
PHYSICS: <hair, fabric, prop behaviour>.
<EŞYA sabit bloğu, varsa>
DIALOGUE LANGUAGE: Turkish, native Istanbul accent, natural everyday speech. Every quoted line is spoken in Turkish, word for word.
AUDIO: <room tone, one or two ambient sounds>. Only <Ad>'s voice.
LOOK: <LOOK sabit bloğu>
POSITIVE LOCKS: only the quoted line is spoken, once; lips move only during the quoted line; clear diction, every final consonant pronounced; restrained emotion, no sobbing; clean picture without on-screen text or subtitles; ambient sound only, without music; framing stays identical to the first frame.
```

Sessiz tepki klibi için ACTION TIMING'de replik yok, LOCKS: `she stays silent with her mouth closed the whole shot`.

İki konuşmacı (8 sn, en fazla iki replik):
```
0:00-0:04: <framing> - <Ad1> says (<tone>): "<replik>"
0:04-0:08: <camera move onto Ad2> - She replies (<Ad2>, <tone>): "<replik>"
```

## 9. Seedance 2.5 çok kesmeli klip — 30 sn'ye kadar

Ayarlar: `seedance_2_5`, mod `omni_reference`, 720p, ses açık, 9:16. Yalnız bu klipte görünen referansları ekle.
```
SCENE CONTEXT: <Place, time. Who is where. What happens and where the emotion turns, 2–4 sentences.>

ACTIVE REFERENCES:
@<Ad1> defines <Ad1>'s face, hair, body and outfit; keep all of it unchanged. Do not take the grey backdrop, the panel borders or the multi-view layout. <Ad1>: <age>, <role>, <state now>, <prop>, <SES sabit bloğu>.
@<Ad2> defines <Ad2>'s face, hair, body and outfit; keep all of it unchanged. Do not take the grey backdrop, the panel borders or the multi-view layout. <Ad2>: <…>.
@<Mekan> defines the room, its furniture and its light only. Do not use any person in the image.
@<Kare> defines only where everyone stands and the light at the start. Do not take faces or clothing from it; identity comes from the character references above.

LOCATION MAP: <foreground / midground / background, doors, windows, light sources, camera positions>.

FIRST FRAME / BLOCKING: <who is where, screen left/right, facing where, eye-lines>.

FORMAT MODE: timed multishot, <N> seconds total; cuts only at the stated seconds, the camera does not cut on its own.

OPTICS: <per segment: shot size + field of view in degrees>; no drift mid-segment.

DIALOGUE LANGUAGE: Turkish, native Istanbul accent, natural everyday speech. Every quoted line is spoken in Turkish, word for word.

ACTION TIMING:
0.0s to 2.5s — <hook: the peak moment, close-up, line or reaction>
2.5s HARD CUT
2.5s to 5.0s — <Ad1> says (<tone>): "<replik>"
5.0s REVERSE CUT
5.0s to 7.5s — She replies (<Ad2>, <tone>): "<replik>"
7.5s HARD CUT
7.5s to 9.0s — <reaction close-up, lips closed>
…
<N-2>s to <N>s — <cliffhanger: the moment right before the answer; hold>.

PERFORMANCE: <muscle-level emotion per character: jaw, eyes, breath; restraint; living eyes with catch-lights>.

PHYSICS: <fabric, hair, prop behaviour>.

LIGHTING: <sources, direction, colour temperature; the same logic in every segment>.

AUDIO: <room tone, key sounds>. Only the quoted lines are spoken. No music.

STYLE: photorealistic live action, 35mm film grain, <colour mood>, vertical 9:16.

POSITIVE LOCKS: the same characters, outfits, props and room in every segment; screen direction and eye-lines stay consistent across cuts; listeners keep their mouths closed; <prop shows only its blank back>; clean picture without on-screen text or subtitles.
```

### Referans rolleri ve dil satırı

- **Her `@ad` bir rol cümlesiyle girer:** neyi verdiği (kimlik, kıyafet, mekân, ışık, konum) ve aynı cümlede neyi **vermediği**. Dışlama yazılmazsa referansın başka parçası sızar: karakter sayfasının gri fonu set olur, mekân görselindeki kişi sahneye girer.
- **Ne kadarı korunacak, açık yaz:** "keep all of it unchanged" (tamamı), "only the coat and the scar; the hair may change" (yalnız sayılan parçalar), "mood and colours only" (yalnız hava). Görünüm değişikliğinde yalnız değişen parçayı serbest bırak.
- **`@<Kare>` (önceki klibin son karesi) kimlik kaynağı değildir.** Yalnız konum ve ışık verir; yüz her zaman karakter sayfasından gelir. Bu satır yalnız kare zincirinde kullanılır, yoksa sil.
- **ACTION TIMING ve PERFORMANCE satırlarında `@ad` değil isim yazılır** (`Defne says`, `@Defne says` değil). Etiket cümlenin öznesi olunca model aynı kişiyi iki kez çizebiliyor. Etiketler yalnız ACTIVE REFERENCES'ta durur.
- **DIALOGUE LANGUAGE satırı replikten önce gelir.** Dil, aksan, konuşma biçimi; replik yine tırnakta. Veo klibinde (§8) aynı satır AUDIO'dan önce gelir.
- **`{}` söz dizimi:** Seedance 2.5 repliği `{…}`, müziği `(…)`, efekti `<…>`, altyazıyı `【…】` içinde de okur. Bu kit tırnak kullanır: bizim kalıplarda `<…>` doldurulacak alan demektir, gönderilen promptta `<…>` kalmamalı. İki biçimi aynı promptta karıştırma. "No music" ifadesini `(…)` içine yazma; parantez müzik kanalı sayılır, düz cümle olarak AUDIO satırında kalsın.
- **Okunabilen her söz seslendirilir.** `a look that says "…"` gibi alt metin cümleleri sesli çıkar. Duyguyu eylemle yaz (`her jaw sets, her eyes hold`), replik yalnız ACTION TIMING'de tırnakta dursun.

## 10. İki karakterli sahne — karşı çekim tutarlılığı

§9'un FIRST FRAME / BLOCKING bölümünün yerine geçer. Veo'da her karşı çekim ayrı klip olur; BETWEEN THEM ve REVERSE ANGLES satırları o sahnenin her klibine **aynen kopyalanır**.
```
FIRST FRAME / BLOCKING: two characters in frame.
<Ad1> — <one visible marker: hair, outfit colour>. Screen <left>, face at x <30>%, eyes at y <38>% of the frame. Midground. Body three-quarter turned toward <Ad2>, screen <right>. <Pose>. Eyes on <Ad2>'s eyes. <Contact: left hand on the chair back>. State: <controlled, cold>.
<Ad2> — <one visible marker>. Screen <right>, face at x <70>%, eyes at y <42>% of the frame. <Depth: half a metre behind Ad1>. Body three-quarter turned toward <Ad1>, screen <left>. <Pose>. Eyes <drop to the card, come back to Ad1>. <Contact>. State: <cornered, holding back>.
BETWEEN THEM: about <1.5> m apart. <Ad1> stays screen <left> and <Ad2> stays screen <right> in every shot. Neither crosses the centre line of the frame; the camera never crosses the line between them. Empty space between them <narrows as Ad1 steps in>.
REVERSE ANGLES: over <Ad1>'s <right> shoulder onto <Ad2>, <Ad2> faces screen <left>. Over <Ad2>'s <left> shoulder onto <Ad1>, <Ad1> faces screen <right>. Same distance, same light direction, same props in the same hands in every angle.
CONTINUITY LOCKS: <who holds what, in which hand>; <what stays where>; <hair and fabric state>.
```
- İlk görünüşte isim + tek görünür işaret (`Defne — ivory gown`) yazmak iki karakterin yer değiştirmesini azaltır.
- 9:16'da iki kişiyi aynı karede uzun tutma; yüzler küçülür. İkili kareyi kurmak için kullan, sonra karşı çekimlere kes. Karşı çekimde diğer kişinin bulanık kenarı karenin dış %10–12'sinde kalır (§7).
- Her konuşmalı segmentte tek kişi konuşur, dinleyenin ağzı kapalı (POSITIVE LOCKS).

---

## Hızlı kontrol (göndermeden önce)

- [ ] Sabit bloklar kartlardan aynen kopyalandı mı?
- [ ] Replik ≤ 8 kelime, tırnakta, Türkçe mi?
- [ ] İlk karede kim nerede, nereye bakıyor yazıyor mu?
- [ ] Bu klipte olmayan karakter ya da `@ad` var mı? (Olmamalı.)
- [ ] Müzik yok, ekranda yazı yok yazıyor mu?
- [ ] Kıyafet filtre güvenli mi?
- [ ] Maliyet gösterildi, onay alındı mı?
- [ ] Her `@ad`ın rol cümlesi ve "Do not take / Do not use" dışlaması var mı? ACTION TIMING'de etiket değil isim mi yazıyor?
- [ ] Replikten önce DIALOGUE LANGUAGE satırı var mı?
- [ ] İki karakterli sahnede taraf (screen left/right) ve bakış yönü her klipte aynı mı (§10)?
- [ ] Bu çekimin deneme bütçesi ve "yeterince iyi" çıtası yazıldı mı (aşağıda)?

---

## Sorun giderme

Maliyet kuralı değişmez: her yeniden deneme de ayrı maliyet onayı ister. Aşağıdakiler onayın yerine geçmez, neyi onaylayacağını belirler.

**Deneme bütçesi.** İlk üretimden önce çekim başına bir sayı yaz: Veo tek çekim en fazla 3, Seedance çok kesmeli en fazla 2 ücretli deneme. Filtre reti bütçeyi doldurmaz ama aynı promptla yeniden gönderilmez; önce kıyafeti ve ifadeyi düzelt (`docs/03-dersler.md` → "Filtre (NSFW) retleri").

**"Yeterince iyi" çıtası.** Çekimin ana işini bir cümleyle yaz: replik doğru kişide, doğru ve net; yüz tanınıyor; bakış yönü doğru. Bu tutuyorsa arka plan ayrıntısı, kumaş kıvrımı gibi ikincil kusurlar yayına girer; gerekirse kurguda kısalt. Çıta yazılmazsa sessizce "kusursuz"a döner ve hiçbir bütçe yetmez.

**Durma kuralı.** Bütçenin yarısında aynı kusur sürüyorsa yeniden üretme, yolu değiştir: çekimi ikiye böl, Seedance yerine Veo tek çekime geç, referansı değiştir ya da çekimi kurgudan çıkar (davetiye kartı örneği: `docs/03-dersler.md` → "Yazılı nesneler"). Denemeler arasında **tek şeyi** değiştir ve `harcama.txt`'ye bir satır yaz: ne değişti, sonuç ne oldu. İki satırda aynı kusur varsa promptu yeniden yaz.

**Kare zinciri hataları** (her satırda tek değişiklik):

| Belirti | Olası neden | Değiştir |
|---|---|---|
| Kimlik kayıyor, zincir uzadıkça yüz başkalaşıyor | Önceki klibin son karesi kimlik kaynağı olmuş | Kimliği karakter sayfasından (`@<Ad>`) yeniden al; son kare yalnız konum ve ışık verir (§9). 2–3 halkadan sonra zinciri karakter sayfasından yeniden başlat |
| Eksen dönüyor, birleşimde karakterler taraf değiştiriyor | Ekran yönü yazılmamış | Tarafı ve bakış yönünü açık yaz; §10'un BETWEEN THEM satırını her klipte aynen kopyala |
| Replik tekrar ediliyor | Önceki klipte söylenen replik promptta kalmış | Söyleneni promptdan çıkar, "she has already said it" yaz; tırnakta yalnız yeni replik kalsın |
| Eylem baştan başlıyor | Biten eylem bitmiş olarak yazılmamış | Bitmiş hâli yaz ("the door already stands open"), yalnız sonrasını iste |
| Sonraki an erken geliyor | Sonraki klibin eylemi bu prompta sızmış | Bir klip, bir an; gelecek eylemleri sil |
| Eşya önceki klibe uymuyor | Eşyanın kimde, nerede, hangi durumda olduğu yazılmamış | CONTINUITY LOCKS'a eşya satırı ekle |
| Gri fon ya da referanstaki başka kişi sahneye giriyor | Dışlama cümlesi yok | §9'daki rol + "Do not take / Do not use" cümlesini ekle |
| Birleşimde kare zıplıyor (Veo bitiş karesi) | Model bitiş karesini birkaç kare aşıyor | `scripts/zincir.py` ile en yakın karede kes (`docs/03-dersler.md` → "Veo bitiş karesi") |

---

Bu bölümdeki teknikler (referans rolleri, dil satırı, iki karakterli yerleşim, sorun giderme) [OSideMedia/higgsfield-ai-prompt-skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill) (MIT, © 2026 O-Side Media) çalışmasından uyarlanmıştır.
