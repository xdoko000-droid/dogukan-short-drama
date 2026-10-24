# Çifte Davetiye — Bölüm 1: kullanılan promptlar

Bu promptlar bölümün son kurgusunda kullanılan gerçek promptlardır. Kendi dizinde kalıp olarak kullan;
sabit blokları kendi karakter ve mekân kartlarınla değiştir.

**Model ayarları**
- Kare: `nano_banana_2`, 9:16, referans olarak karakter sayfası + mekân/ışık karesi. ~2 kr.
- Klip: `veo3_1_lite`, 4/6 sn, 9:16, ses açık, yalnız başlangıç karesi. 4 sn = 6 kr, 6 sn = 9 kr.
- Bitiş karesi kullanılmadı: önceki denemede NSFW retlerini artırdı.

**Karakter sayfaları hakkında not:** Bu örnekteki sayfalar (`kareler/01-…`, `kareler/02-…`) eski yöntemle,
8 görünümlü ve yüzü her görünümde açık olarak üretildi. Önerilen yöntem artık: GPT Image 2, gri fon,
3 görünüm, ön boyda yüz silinmiş (`templates/prompt-kaliplari.md` → 3). Defne'nin sayfasındaki askılı
elbise de klip üretiminde sürekli filtreye takıldı; bu yüzden yeni çekimlerde kapalı yakalı elbiseye geçildi.

## Sabit bloklar (her klipte kelimesi kelimesine aynı)

**NERMIN VOICE:** speaks Turkish with a native, refined Istanbul accent; low alto pitch; slow, deliberate pace; smooth, cold, velvety timbre.

**DEFNE VOICE:** speaks Turkish with a native Istanbul accent; soft mezzo-soprano pitch; measured pace; warm, slightly breathy timbre.

**NERMIN:** late fifties elegant Turkish woman, silver-blonde hair in a low chignon, sharp dark eyes, fair skin, cream boucle tweed skirt suit, pearl necklace, pearl earrings.

**DEFNE:** late twenties Turkish woman, long voluminous wavy dark chestnut hair, hazel eyes, olive skin, small beauty mark on left cheek, soft glam makeup, champagne silk satin midi dress with thin long sleeves and an elegant, modest high neckline, thin gold necklace, small gold hoop earrings, diamond engagement ring.

**LOCATION:** Grand entrance hall of an old Bosphorus waterfront mansion (yali) at night. Black and white checkered marble floor, crystal chandelier, dark wood staircase on the left, tall carved wooden double doors at the back, a brass table lamp on the right. Same hall, same light throughout.

**CARD:** a cream invitation card with a thin gold edge; only its plain blank back side or its thin edge is ever visible to the camera.

**LOOK:** photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.

---

## K1 — Nermin yakın plan başlangıç karesi (nano_banana_2, 2 kr)

Referanslar: Nermin karakter sayfası (kimlik), yalı holünden bir kare (mekân ve ışık).
Kullanım: V1 ve V2'nin başlangıç karesi. Karşı çekimdeki Defne karesiyle aynı ölçek (85mm görünüm, 1.2 m).
Model orta plan verdi; kare ücretsiz kırpılıp yakın plana çevrildi.

```
Use image 1 (character sheet) for the woman's identity, 1:1 face similarity. Use image 2 only for the location, colors and light. Create ONE full-frame vertical 9:16 cinematic film still, no panels, no borders.
SUBJECT: Nermin: late fifties elegant Turkish woman, silver-blonde hair in a low chignon, sharp dark eyes, fair skin, cream boucle tweed skirt suit, pearl necklace, pearl earrings. She holds a cream invitation card with a thin gold edge flat against her chest with both hands; only its plain blank back side faces the camera.
FIRST FRAME / BLOCKING: close-up from mid-chest to just above the head. Nermin stands right of center (face at x 55%, eyes at y 33% of the frame), body three-quarter turned toward frame left, eyes looking just left of the lens toward someone off-screen left. Out-of-focus edge of a woman's long dark wavy hair and champagne satin shoulder fills the far left 12% of the frame, soft and blurred.
LOCATION: Grand entrance hall of an old Bosphorus waterfront mansion (yali) at night. Black and white checkered marble floor, crystal chandelier, dark wood staircase on the left, tall carved wooden double doors at the back, a brass table lamp on the right. The chandelier glows soft and blurred in the upper left background.
OPTICS: 85mm lens look, about 24 degrees horizontal field of view, eye-level camera at 1.2 m distance, background in creamy bokeh.
EXPRESSION: calm, composed, a faint cold closed-mouth smile, chin slightly raised, eyes steady.
LOOK: photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.
POSITIVE LOCKS: clean image with no writing anywhere; the card shows only its blank back; one person in focus.
```

## V1 — Nermin: "Davetiyeleri ben bastırdım, Defne." (6 sn, 9 kr)

Başlangıç: K1. Kurguda iki kez: #1 (kanca) ve #23 (doruk).

```
6 seconds, one continuous shot, real time, vertical 9:16.
SCENE: Night, mansion entrance hall. Nermin reveals to the young woman in front of her that she printed the wedding invitations herself.
SUBJECT: Nermin: late fifties elegant Turkish woman, silver-blonde hair in a low chignon, sharp dark eyes, fair skin, cream boucle tweed skirt suit, pearl necklace, pearl earrings. Nermin speaks Turkish with a native, refined Istanbul accent; low alto pitch; slow, deliberate pace; smooth, cold, velvety timbre. Face, hair and outfit 100% match the first frame.
LOCATION MAP: Grand entrance hall of an old Bosphorus waterfront mansion (yali) at night. Black and white checkered marble floor, crystal chandelier upper left in soft bokeh, dark wood staircase on the left, carved wooden double doors at the back. Camera eye-level, 1.2 m from Nermin. Same hall, same light throughout.
FIRST FRAME: exactly the start image. Nermin right of center, eyes just left of the lens toward the off-screen listener; blurred dark hair edge at far left.
OPTICS / CAMERA: 85mm look, about 24 degrees field of view, locked framing with a very slow push-in of about 5 percent over the whole shot.
ACTING TASK: MOTIVE: she has waited for this moment. GOAL: make the young woman understand who holds the power. OBSTACLE: the young woman is still in shock and barely listening. TACTIC: speak slowly, softly, without blinking, as if stating the weather.
ACTION TIMING:
0.0-0.4s: Nermin holds still, a faint cold smile.
0.4-3.0s: Nermin says, calm and icy, each word separate: "Davetiyeleri ben bastırdım, Defne."
3.0-6.0s: silence; she keeps eye contact, lips closed, a slow single blink, the smile grows a little colder.
PHYSICS: the card stays flat against her chest in both hands; pearls catch the light with her breathing; no hair movement.
CARD: a cream invitation card with a thin gold edge; only its plain blank back side or its thin edge is ever visible to the camera.
AUDIO: large quiet hall room tone with a soft echo, a distant grandfather clock ticking. Only Nermin's voice.
LOOK: photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.
POSITIVE LOCKS: only the quoted line is spoken, once; lips move only during the quoted line; clean picture without on-screen text or subtitles; ambient sound only, without music; framing stays identical to the first frame.
```

## V2 — Nermin: "Asıl gelini şimdi göreceksin." (4 sn, 6 kr)

Başlangıç: K1 (V1 ile aynı kadraj; kesme görünmez). Kurguda #25.

```
4 seconds, one continuous shot, real time, vertical 9:16.
SCENE: Night, mansion entrance hall. Nermin promises the young woman she is about to see who the real bride is.
SUBJECT: Nermin: late fifties elegant Turkish woman, silver-blonde hair in a low chignon, sharp dark eyes, fair skin, cream boucle tweed skirt suit, pearl necklace, pearl earrings. Nermin speaks Turkish with a native, refined Istanbul accent; low alto pitch; slow, deliberate pace; smooth, cold, velvety timbre. Face, hair and outfit 100% match the first frame.
LOCATION MAP: Grand entrance hall of an old Bosphorus waterfront mansion (yali) at night. Black and white checkered marble floor, crystal chandelier upper left in soft bokeh, dark wood staircase on the left, carved wooden double doors at the back. Camera eye-level, 1.2 m from Nermin. Same hall, same light throughout.
FIRST FRAME: exactly the start image. Nermin right of center, eyes just left of the lens toward the off-screen listener; blurred dark hair edge at far left.
OPTICS / CAMERA: 85mm look, about 24 degrees field of view, locked-off, no camera movement.
ACTING TASK: MOTIVE: she enjoys the young woman's confusion. GOAL: plant the next shock. OBSTACLE: the young woman wants answers now. TACTIC: lean in a few centimeters, lower the voice almost to a whisper.
ACTION TIMING:
0.0-0.4s: Nermin tilts her head a little toward frame left.
0.4-2.8s: Nermin says, low and almost whispering, a cold smile: "Asıl gelini şimdi göreceksin."
2.8-4.0s: silence; her right hand slowly starts to lift the card away from her chest, its blank back still facing the camera.
PHYSICS: slow, controlled hand motion; the card stays rigid; pearls shift slightly as she leans.
CARD: a cream invitation card with a thin gold edge; only its plain blank back side or its thin edge is ever visible to the camera.
AUDIO: large quiet hall room tone with a soft echo, a distant grandfather clock ticking. Only Nermin's voice.
LOOK: photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.
POSITIVE LOCKS: only the quoted line is spoken, once; lips move only during the quoted line; clean picture without on-screen text or subtitles; ambient sound only, without music; framing stays identical to the first frame.
```

## V3 — Defne: "Siz mi?" (4 sn, 6 kr)

Başlangıç: önceki bir klibin son karesi (Defne yakın plan, ücretsiz çıkarıldı). Kurguda #24.

```
4 seconds, one continuous shot, real time, vertical 9:16.
SCENE: Night, mansion entrance hall. The young woman cannot believe the older woman in front of her printed the wedding invitations.
SUBJECT: Defne: late twenties Turkish woman, long voluminous wavy dark chestnut hair, hazel eyes, olive skin, small beauty mark on left cheek, soft glam makeup, champagne silk satin midi dress with thin long sleeves and an elegant, modest high neckline, thin gold necklace, small gold hoop earrings, diamond engagement ring. Defne speaks Turkish with a native Istanbul accent; soft mezzo-soprano pitch; measured pace; warm, slightly breathy timbre. Face, hair and outfit 100% match the first frame.
LOCATION MAP: Grand entrance hall of an old Bosphorus waterfront mansion (yali) at night. Crystal chandelier glowing above her in soft bokeh, the older woman in a cream suit blurred in the right background, dark wood and lamp light behind. Camera eye-level, 1.2 m from Defne. Same hall, same light throughout.
FIRST FRAME: exactly the start image. Defne left of center, eyes toward frame right just past the lens.
OPTICS / CAMERA: 85mm look, about 24 degrees field of view, locked framing, no camera movement.
ACTING TASK: MOTIVE: the person she trusted is part of the betrayal. GOAL: hear that it is not true. OBSTACLE: the older woman's calm smile. TACTIC: a broken half-whisper, then hold the stare.
ACTION TIMING:
0.0-0.6s: Defne stays frozen, eyes wide, a short sharp breath.
0.6-1.8s: Defne says, half-whisper, voice cracking: "Siz mi?"
1.8-4.0s: silence; lips close and press together, chin trembles slightly, eyes glisten, she does not blink.
PHYSICS: tiny tremor in the chin; hair still; satin catches the light with her breathing.
AUDIO: large quiet hall room tone with a soft echo, a short sharp inhale. Only Defne's voice.
LOOK: photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.
POSITIVE LOCKS: only the quoted line is spoken, once; lips move only during the quoted line; restrained emotion, no sobbing; clean picture without on-screen text or subtitles; ambient sound only, without music; framing stays identical to the first frame.
```

## V4 — Defne'nin sessiz tepkisi (4 sn, 6 kr)

Başlangıç: V3 ile aynı kare. Kurguda iki kez: #2 (kanca tepkisi) ve #26 (cliffhanger).

```
4 seconds, one continuous shot, real time, vertical 9:16.
SCENE: Night, mansion entrance hall. The young woman sees the face of the invitation held up off-screen in front of her and is struck silent.
SUBJECT: Defne: late twenties Turkish woman, long voluminous wavy dark chestnut hair, hazel eyes, olive skin, small beauty mark on left cheek, soft glam makeup, champagne silk satin midi dress with thin long sleeves and an elegant, modest high neckline, thin gold necklace, small gold hoop earrings, diamond engagement ring. Face, hair and outfit 100% match the first frame.
LOCATION MAP: Grand entrance hall of an old Bosphorus waterfront mansion (yali) at night. Crystal chandelier glowing above her in soft bokeh, the older woman in a cream suit blurred in the right background, dark wood and lamp light behind. Camera eye-level, 1.2 m from Defne. Same hall, same light throughout.
FIRST FRAME: exactly the start image. Defne left of center, eyes toward frame right just past the lens.
OPTICS / CAMERA: 85mm look, about 24 degrees field of view, slow steady push-in toward her eyes, about 10 percent over the shot.
ACTING TASK: MOTIVE: she is about to discover the truth. GOAL: understand what she is reading. OBSTACLE: what she sees is impossible. TACTIC: no words, only the eyes.
ACTION TIMING:
0.0-1.2s: Defne's eyes drop slightly to something at chest height off-screen right, she reads.
1.2-2.4s: her eyes widen sharply, a silent sharp inhale through the nose, lips stay closed.
2.4-4.0s: she freezes completely, eyes wet and wide, not blinking.
PHYSICS: a single small shiver through the shoulders at 1.2s; hair still; satin catches the light.
AUDIO: large quiet hall room tone with a soft echo, one sharp inhale. No dialogue.
LOOK: photorealistic live action, 35mm film grain, muted warm tones, warm 2700K tungsten key light from the chandelier upper right, cool 5600K moonlight rim from behind, shallow depth of field, vertical 9:16.
POSITIVE LOCKS: she stays silent with her mouth closed the whole shot; clean picture without on-screen text or subtitles; ambient sound only, without music.
```

---

## Eski deneme: iki kişilik yüzleşme (Veo 8 sn, "She replies:" kalıbı)

Yüzleşme sahnesi (#15–#19) bu klipten ve devamından kesildi. "She replies:" kalıbıyla iki konuşmacının
sırası korundu.

Dikkat: Bu prompt iki hata içeriyor ve dersler bundan çıktı:
1. "slip dress with thin straps" ve "off-the-shoulder" → devam klibi filtreye takıldı. Yeni çekimlerde kapalı yaka.
2. "slightly handheld" → kamera zaman zaman savruldu. Yeni çekimlerde `smooth steady camera, no whip pans`.

Başlangıç karesi: iki kişilik profil; bitiş karesi: Defne'nin omzu üstünden Selin.

```
8 seconds / ONE CONTINUOUS TAKE / intimate cinematic micro-drama / NO MUSIC
SUBJECT 1: Defne: late twenties Turkish woman, long voluminous wavy dark chestnut hair, hazel eyes, olive skin, small beauty mark on left cheek, soft glam makeup, champagne silk satin slip dress with thin straps, thin gold necklace, small gold hoop earrings, diamond engagement ring.
SUBJECT 2: Selin: late twenties Turkish woman, long straight honey-blonde hair parted at the side, green eyes, fair skin, bold red lipstick, fitted deep red satin off-the-shoulder dress, gold hoop earrings, red manicured nails.
ENVIRONMENT: Grand Bosphorus waterfront mansion (yali) salon at night. Dark carved wood, marble floor, warm table lamps, tall arched windows with Bosphorus water and city lights behind. Same room, same light throughout.
AUDIO: NO MUSIC. Quiet salon room tone, soft distant Bosphorus waves through the windows, faint satin rustle. Dialogue in Turkish only. No subtitles, no text on screen.
TIMELINE (0:00-0:08):
0:00-0:04: Medium two-shot, slow push-in - Defne says (voice trembling, jaw tight, card raised): "Davetiyede gelin olarak senin adın var."
0:04-0:08: Camera drifts over Defne's shoulder onto Selin - She replies (Selin, cool, slow smirk, steady eyes): "Kerem seni hiç sevmedi, Defne."
Restrained emotion, subtle tears, clear diction, every final consonant pronounced, no sobbing, nuanced facial micro-expressions, coherent character consistency, one continuous take, photorealistic, life-like live action, 35mm film, subtle grain, muted tones, shallow depth of field, slightly handheld, 9:16.
```

## Kurguda çıkarılan klip

Planda Nermin'in kartı Defne'ye çevirdiği 4 sn'lik bir profil klibi vardı (6 kr). Kart, yazılı yüzünü
kameraya döndü ve anlamsız yazı göründü. Kurgudan çıkarıldı. Ders: yazılı nesneyi hareket ettiren
çekimden kaçın; tepkiyi göster.

## Bu bölümün yeni üretim maliyeti

| Kod | Ne | Kredi |
|---|---|---|
| K1 | Nermin yakın kare | 2 |
| K2 | Profil iki kişilik kare (kullanılmayan klip için) | 2 |
| V1 | 6 sn | 9 |
| V2 | 4 sn | 6 |
| V3 | 4 sn | 6 |
| V4 | 4 sn | 6 |
| V5 | 4 sn (kurgudan çıkarıldı) | 6 |
| | **Toplam** | **37** |

Diğer çekimler önceki denemelerden yeniden kullanıldı.
