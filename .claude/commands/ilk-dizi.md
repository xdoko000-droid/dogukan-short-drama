---
description: Rehberli ilk dizi. Fikirden sezon planına, karakterlerden 1. bölümün kurgusuna kadar soru sorarak götürür.
---

# /ilk-dizi: Rehberli ilk dizi

Yöntemin tamamı `.claude/skills/short-drama-tr/SKILL.md` ve `references/` altında. Bu akış onu adım adım uygular.
Kullanıcı teknik bilmiyor varsay. Komutları sen çalıştır. Kısa Türkçe cümleler, tek seferde tek aşama.

**PY:** Windows'ta `.venv/Scripts/python.exe`, Mac'te `.venv/bin/python`.

## Değişmez kurallar

- **Her ücretli üretimden ve her yeniden denemeden önce maliyeti göster, onay al.** MCP maliyet aracı varsa
  onu kullan; yoksa `higgsfield generate cost`. Filtre reti sonrası deneme de ayrı onay ister.
- Toplam tavanı aşma; aşacaksan dur, sor. Harcamayı `uretim/<seri>/harcama.txt`'ye yaz.
- Aynı anda en fazla 4 Higgsfield işi. Çift gönderim yok.
- Gerçek kişiye benzeyen yüz yok. Platform güvenli içerik. Kazanç vaadi yok.

Her aşamanın sonunda: 2–4 satırlık özet + AskUserQuestion ile "Devam edelim mi?"
(seçenekler: "Devam" / "Değiştirmek istiyorum" / "Burada duralım").

## 0. Hazırlık kontrolü

`.venv` var mı ve Higgsfield araçları listende mi bak. Biri eksikse önce `/kur` akışını öner
(`.claude/commands/kur.md`).

## 1. Sorular

Tek AskUserQuestion çağrısında dört soru sor (her biri 2–4 seçenek; "Diğer" alanı serbest yazı içindir):

1. **Tür:** Aldatma · Kayınvalide · İntikam · Saklı kimlik. Kendi fikri varsa "Diğer" alanına yazsın.
2. **Bütçe tarifi** (bölüm başı, 22 Eki 2026 fiyatı):
   - Ekonomik ~140 kredi (Veo 3.1 Lite)
   - Dengeli ~375 kredi (kritik anlar Seedance 2.5)
   - Premium ~950 kredi (tamamı Seedance 2.5)
   Karakter ve mekân varlıkları sezon başında bir kez, karakter başına ~7–10 kredi.
3. **Bölüm sayısı (sezon planı):** 8 bölüm · 10 bölüm · Şimdilik yalnız 1. bölüm (deneme).
   Hangisi seçilirse seçilsin bu akışta yalnız 1. bölüm üretilir.
4. **Ton:** Ağır dram · Gerilim · Magazin/dedikodu tadında · Duygusal.

Cevaplardan sonra kalan krediyi MCP'den oku (ücretsiz okuma aracı) ve tarifle karşılaştır. Yetmiyorsa söyle.

## 2. Fikir

- Kendi fikri varsa onu, yoksa `references/fikir-bankasi.md`'den türe uyan adayları al.
- 6 ölçütle puanla (SKILL.md §1). En iyi 3'ü puanlarıyla ve tek cümleyle göster.
- AskUserQuestion ile seçtir (3 aday + "Sen seç"). Seri için ASCII bir klasör adı belirle (ör. `cifte-davetiye`).

## 3. Sezon planı

- `templates/SEZON.md`'den `uretim/<seri>/SEZON.md` yaz: logline, ana sır, bölüm başı twist, cliffhanger haritası,
  3–5 karakter, 3–4 mekân.
- Kullanıcıya kısa hâlini göster (logline + bölüm listesi). Özet + "Devam edelim mi?"

## 4. Tavan ve varlıklar

- Bölüm tavanını öner: tarif tahmini × 1.5 + varlık maliyeti. Onaylat, `harcama.txt`'nin başına yaz.
- Varlık listesini çıkar (SKILL.md §4, `references/varliklar.md`): her karakter için yüz (Soul 2.0, 4–6 seçenek),
  kıyafet, karakter sayfası (GPT Image 2); her mekân için Soul Location.
- **Önce toplam maliyeti göster, onay al**, sonra en fazla 4 eşzamanlı işle üret.
- Yüz seçeneklerini göster, kullanıcı seçsin. Varlıkları `uretim/<seri>/varliklar/` altına indir,
  sabit adlar ver (`@Defne`), `templates/KARAKTER.md` ve `templates/MEKAN.md` kartlarına işle.
- Özet + "Devam edelim mi?"

## 5. 1. bölüm senaryosu ve çekim listesi

- `uretim/<seri>/bolumler/bolum-01/senaryo.md` (`templates/BOLUM-SENARYO.md`) ve
  `cekim-listesi.md` (`templates/CEKIM-LISTESI.md`) yaz. Kanca → bağlam → tırmanış → doruk + cliffhanger, ~60 sn,
  replikler ≤ 8 kelime.
- Kullanıcıya replikleri ve çekim sırasını kısa bir tabloyla göster. Özet + "Devam edelim mi?"

## 6. Klipler

- Seçilen tarife göre `promptlar.md` yaz (`references/klip-promptu.md`, `templates/prompt-kaliplari.md`).
  Sabitleri (ses, karakter tarifi, stil) her klipte kelimesi kelimesine aynı kullan.
- Başlangıç kareleri ve klipler için **toplam maliyeti göster, onay al**. Tavanı kontrol et.
- En fazla 4 eşzamanlı işle üret. Sonuçları `result_url` alanından `bolum-01/klipler/01.mp4, 02.mp4 …` olarak indir.
- Kare zinciri için son kareyi ücretsiz çıkar: `PY scripts/kare.py --help`.
- Bozuk klipte sorunu açık sözle söyle, yeniden deneme maliyetini göster, ayrı onay al.
- Her harcamayı `harcama.txt`'ye yaz. Özet (harcanan / tavan) + "Devam edelim mi?"

## 7. Kurgu

- Çekim listesini `bolum-01/kurgu.json`'a çevir (örnek: `examples/kurgu-ornek.json`, alanlar: `scripts/README.md`),
  `"cikti": "bolum-01.mp4"`.
- Çalıştır:
  ```
  PY scripts/kurgu.py uretim/<seri>/bolumler/bolum-01/kurgu.json --temiz
  ```
- Kontrol kareleri çıkar (`PY scripts/kare.py`), kullanıcıya göster. Son dosya:
  `uretim/<seri>/bolumler/bolum-01/bolum-01.mp4`. İzlemesini öner.
- Özet + "Devam edelim mi?"

## 8. Yayın metni

`docs/04-tiktok-yayin.md`'ye göre öner:
- Başlık: `Bölüm 1 | <kanca cümlesi>`
- Açıklama: 1–2 cümle merak + "Kurgudur, AI ile üretildi."
- 3–5 hashtag
- Hatırlat: TikTok'ta **AI etiketini aç**.

Son özet: harcanan kredi, dosya yolu, sıradaki adım ("2. bölüme geçelim mi?").
