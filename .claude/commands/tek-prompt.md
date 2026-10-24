---
description: Tek prompt otomatik modu. Tek cümlelik istekten, baştan onaylanan kredi tavanı içinde fikirden kurguya ve yayın metnine kadar durmadan ilerler.
---

# /tek-prompt: Tek cümleden bölüme

Kullanıcı tek cümle yazar, sen bir kez onay alırsın, sonra bölümü baştan sona üretirsin.
Yöntem aynıdır: `.claude/skills/short-drama-tr/SKILL.md` ve `references/`. Fark yalnız onay biçimindedir:
her ücretli iş için ayrı onay yerine, kullanıcı baştan **toplam bir kredi tavanını** açıkça onaylar.

**PY:** Windows'ta `.venv/Scripts/python.exe`, Mac'te `.venv/bin/python`.

## 0. Hazırlık

`.venv` var mı ve Higgsfield araçları listende mi bak. Eksikse önce `/kur` akışını öner (`.claude/commands/kur.md`).
Kalan krediyi ücretsiz bir okuma aracıyla oku.

## 1. İstek

Kullanıcı tek cümleyle yazar. Örnek:
```
aldatma temalı 1 bölümlük dizi, Ekonomik tarif, tavan 200 kredi
```
Cümleden tür, tarif, bölüm sayısı ve tavanı çıkar. Eksik olanı makul bir varsayılanla doldur
(tarif yoksa Ekonomik, bölüm sayısı yoksa 1).

## 2. Tek onay

**Tek bir AskUserQuestion** çağrısında dört soruyu birlikte sor; çıkardığın değerleri ilk seçenek yap:

1. **Tür:** ör. Aldatma · Kayınvalide · İntikam · Saklı kimlik ("Diğer" serbest yazı).
2. **Tarif:** Ekonomik ~140 · Dengeli ~375 · Premium ~950 kr/bölüm (22 Eki 2026 fiyatı).
3. **Bölüm sayısı:** 1 · 2 · 3.
4. **Toplam kredi tavanı:** kullanıcının yazdığı değer · tahmin × 1.3 · tahmin × 1.5.

Seçeneklerin yanında tahmini toplamı göster:
`tahmin = tarif × bölüm sayısı + varlıklar (karakter başına ~7–10 kr)`.
Tavan tahminden düşükse ya da kalan krediden yüksekse bunu soruda açıkça yaz.

Onaylanan tavanı `uretim/<seri>/harcama.txt` dosyasının ilk satırına yaz:
```
# tavan 200 (tek-prompt, onay: <tarih>)
```
Tavan onayı yoksa bu akış çalışmaz; normal akışa (`/ilk-dizi`) dön.

## 3. Durmadan üretim

Onaydan sonra aşamaları sırayla yap, aralarda kullanıcıya soru sorma; her aşamadan sonra tek satır durum yaz
(`✓ senaryo · harcanan 18 / 200`):

1. Fikir: 6 ölçütle puanla, en yükseği seç (SKILL.md §1).
2. Kısa sezon notu: `uretim/<seri>/SEZON.md` (logline, ana sır, cliffhanger haritası; kısa tut).
3. Senaryo ve çekim listesi: `bolumler/bolum-01/senaryo.md`, `cekim-listesi.md`.
4. Varlıklar: yüz, kıyafet, karakter sayfası, mekân (SKILL.md §4). Yüzü sen seç; gerçek kişiye benzemesin.
5. Kareler ve klipler: `promptlar.md`, başlangıç kareleri, klipler (≤ 4 eşzamanlı iş, çift gönderim yok).
   Kare zinciri için son kareyi ücretsiz çıkar: `PY scripts/kare.py`.
6. `kurgu.json` yaz, sonra:
   ```
   PY scripts/kurgu.py uretim/<seri>/bolumler/bolum-01/kurgu.json --temiz
   ```
7. Kanca kontrolü (araç varsa): `references/kanca-kontrolu.md`.
8. TikTok metni: `docs/04-tiktok-yayin.md` (başlık, açıklamada "Kurgudur, AI ile üretildi.", 3–5 hashtag).

Birden çok bölümde 3–8. adımları her bölüm için tekrarla; varlıklar bir kez üretilir.

### Her ücretli işten önce

- Maliyeti yine sorgula (MCP maliyet aracı ya da `higgsfield generate cost`). Kullanıcıya sorma.
- `harcanan + bu işin maliyeti ≤ tavan` ise gönder. Sonra satırı `harcama.txt`'ye yaz (`etiket kredi`).
- Yeniden deneme de aynı kurala bağlıdır: yalnız tavanın içinde kalıyorsa yapılır.

## 4. Dur ve sor

Şu durumlardan biri olursa üretimi durdur, AskUserQuestion ile ne yapılacağını sor:

- Bir sonraki iş tavanı aşacaksa.
- Gerçek harcama ilk tahminden **%20'den fazla** saptıysa (o ana kadarki aşamaların tahminine göre).
- Aynı çekim filtreye **ikinci kez** takıldıysa (tekrarlanan ret).
- Bakiye beklenmedik biçimde düştüyse ya da bir araç bilinmeyen maliyet döndürdüyse.

Seçenekler: "Tavanı artır" · "Ucuzlatarak devam et" · "Burada dur".

## 5. Son özet

```
Dosyalar : uretim/<seri>/bolumler/bolum-01/bolum-01.mp4, .srt, senaryo.md, promptlar.md
Harcama  : 164 / 200 kr (tahmin 150)
Kareler  : kareler/kontrol-*.png (3–4 kontrol karesi göster)
Kanca    : puan, kalma oranı (varsa)
Yayın    : başlık + açıklama + hashtag
```
Hatırlat: TikTok'ta AI etiketini aç. Kazanç ya da gelir vaadi yazma.
