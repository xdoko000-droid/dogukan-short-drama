# Maliyet ve bütçe

Tüm fiyatlar Higgsfield kredisi (kr) cinsindendir ve **22 Eki 2026** tarihlidir. Değişebilir.
Her üretimden önce canlı maliyeti sor: MCP maliyet aracı ya da `higgsfield generate cost`.

## Birim fiyatlar

| Model | Birim | Örnek |
|---|---|---|
| Veo 3.1 Lite (`veo3_1_lite`, sesli) | 1.5 kr/sn | 4 sn = 6, 6 sn = 9, 8 sn = 12 |
| Seedance 2.5 (`seedance_2_5`) 720p sesli | 7 kr/sn | 30 sn = 210 |
| Seedance 2.5 480p | 3 kr/sn | |
| Seedance 2.5 1080p | 16 kr/sn | |
| Seedance 2.0 (`seedance_2_0`) 720p | 4.5 kr/sn | |
| Seedance 2.0 Mini (`seedance_2_0_mini`) 720p | 1 kr/sn | |
| nano_banana_2 (kare) | 2 kr | |
| GPT Image 2 (`gpt_image_2`, karakter sayfası) | 6.5 kr | |
| Soul 2.0 (`text2image_soul_v2`) | 0.12 kr | |
| Seedream 5 Pro (`seedream_v5_pro`) | 2.5 kr | |
| Virality Predictor (`brain_activity`) | şu an kredisiz (doğrula) | maliyet aracı desteklemiyor; önce/sonra bakiyeye bak |

Seedance 2.5: tek üretimde 30 sn'ye kadar çok kesme, 50'ye kadar referans.

## 3 bütçe tarifi (bölüm ~60 sn)

| Tarif | Nasıl | Bölüm başı | 30 bölüm |
|---|---|---|---|
| **Ekonomik** | Veo 3.1 Lite, 4/6/8 sn tek çekim klipler, başlangıç karesiyle | ~140 kr | ~4.200 |
| **Dengeli** | Kanca, yüzleşme, cliffhanger için toplam ~30 sn Seedance 2.5 720p; gerisi Veo Lite | ~375 kr | ~11.000 |
| **Premium** | Tamamı Seedance 2.5 720p | ~950 kr | ~29.000 |

Tahminler yeniden çekim payı ve başlangıç karelerini içerir. Karakter sayfaları ve mekânlar
sezon başında bir kez üretilir (karakter başına ~7–10 kr) ve bölüm maliyetine eklenmez.

Kaba hesap:
- **Ekonomik:** ~12–15 Veo klibi (~80–90 sn ham) ≈ 120–135 kr + birkaç kare ≈ 140.
- **Dengeli:** 30 sn Seedance 2.5 ≈ 210 kr + ~100 sn Veo ≈ 150 kr + kareler ≈ 375.
- **Premium:** ~4 adet 30 sn Seedance 2.5 üretimi + yeniden çekimler ≈ 950.

Kurgu, ses, altyazı ücretsizdir (yerel betikler).

## Tasarruf

- Kurguda yeniden kullan: bir klibin replik, tepki ve insert kısımları ayrı çekim olur.
- Aynı başlangıç karesinden birden fazla replik üret (çekim/karşı çekim).
- Son kareyi ücretsiz çıkar, yeni kare üretme.
- Orta plan kareyi kırpıp yakın plan yap; yeni üretim gerekmez.
- Yanlış giden tek anı insert klip ile düzelt, bütün sahneyi yeniden üretme.
- NSFW retleri genelde iade ediliyor ama zaman yiyor. Kıyafeti baştan güvenli seç.

## Harcama kaydı

`uretim/<seri>/harcama.txt`, her satır: `<etiket> <kredi>`. Gönderimden önce toplamı topla,
tavanı aşacaksa gönderme. Örnek:
```
b1-K1 2
b1-V1 9
b1-V2 6
```

## Hatırlatma

- Abonelikle gelen kalan kredi dönem sonunda (30 günde bir) silinebiliyor. Hesap sayfasındaki
  işlem geçmişinden kontrol et, üretimi buna göre planla.
- Gelir hesabı yapma, kazanç vaadi verme.
