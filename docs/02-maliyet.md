# 02 — Maliyet

Fiyatlar Higgsfield kredisi (kr) cinsindendir ve **22 Eki 2026** tarihlidir. **Değişebilir.**
Claude her üretimden önce canlı maliyeti gösterir ve onayını ister.

## Birim fiyatlar

| Model | Ne için | Fiyat |
|---|---|---|
| Veo 3.1 Lite (sesli) | Ekonomik klip | 1.5 kr/sn → 4 sn = 6, 6 sn = 9, 8 sn = 12 |
| Seedance 2.5 720p sesli | Çok kesmeli sahne | 7 kr/sn |
| Seedance 2.5 480p | Taslak | 3 kr/sn |
| Seedance 2.5 1080p | Yüksek çözünürlük | 16 kr/sn |
| Seedance 2.0 720p | Ara seçenek | 4.5 kr/sn |
| Seedance 2.0 Mini 720p | Deneme | 1 kr/sn |
| nano_banana_2 | Başlangıç karesi | 2 kr |
| GPT Image 2 | Karakter sayfası | 6.5 kr |
| Soul 2.0 | Yüz, kıyafet | 0.12 kr |
| Seedream 5 Pro | Görünüm düzenleme | 2.5 kr |
| Virality Predictor (`brain_activity`) | Kanca kontrolü | Şu an kredisiz (doğrula: önce ve sonra bakiyeye bak) |

Seedance 2.5 tek üretimde 30 sn'ye kadar çok kesme ve toplam 50'ye kadar referans alır (en fazla 30'u görsel).

## 3 tarif

| Tarif | Nasıl | Bölüm başı | 30 bölüm |
|---|---|---|---|
| **Ekonomik** | Veo 3.1 Lite, 4/6/8 sn klipler, başlangıç karesiyle | ~140 kr | ~4.200 |
| **Dengeli** | Kanca, yüzleşme ve cliffhanger için ~30 sn Seedance 2.5 720p; gerisi Veo Lite | ~375 kr | ~11.000 |
| **Premium** | Tamamı Seedance 2.5 720p | ~950 kr | ~29.000 |

### Hangisini seçmeli?

- **İlk deneme:** Ekonomik. Yöntemi öğren, kurguyu otur.
- **Seri yayında ilgi görüyorsa:** Dengeli. Kanca ve cliffhanger en çok izlenen anlar; parayı oraya koy.
- **Tek bir vitrin bölümü:** Premium.

### Bölüm başı nereden çıkıyor?

- **Ekonomik:** ~12–15 Veo klibi (~80–90 sn ham görüntü, yeniden çekimlerle) ≈ 120–135 kr + başlangıç kareleri ≈ 140 kr.
- **Dengeli:** 30 sn Seedance 2.5 ≈ 210 kr + ~100 sn Veo ≈ 150 kr + kareler ≈ 375 kr.
- **Premium:** 30 sn'lik ~4 Seedance 2.5 üretimi ve yeniden çekimler ≈ 950 kr.

Karakter sayfaları ve mekânlar sezon başında **bir kez** üretilir (karakter başına ~7–10 kr).
Kurgu, ses ve altyazı yerel betiklerle yapılır, **ücretsizdir**.

## Gerçek örnek

Örnek dizinin 1. bölümünün "enerji" kurgusu (`examples/cifte-davetiye/`): 5 yeni Veo klibi ve 2 kare
için **37 kr** harcandı, geri kalan çekimler önceki denemelerden yeniden kullanıldı. Sıfırdan yapılsa
ekonomik tarife yakın bir maliyet çıkar.

## Kurallar

1. Her üretimden önce maliyet: MCP maliyet aracı ya da
   ```
   higgsfield generate cost veo3_1_lite --prompt "..." --duration 6 --aspect_ratio 9:16 --generate_audio true --start-image kare.png
   ```
2. Bölüm başında tavan belirle (tahmin × 1.5 iyi bir başlangıç).
3. Harcamayı `uretim/<seri>/harcama.txt` dosyasına yaz.
4. Aynı anda en fazla 4 iş; çift gönderim yok.

## Tasarruf ipuçları

- Bir klibi kurguda 2–4 çekime böl (replik, tepki, insert).
- Son kareyi ücretsiz çıkar (`scripts/kare.py`), yeni kare üretme.
- Orta plan kareyi kırpıp yakın plan yap.
- Bozuk tek anı insert klip ile düzelt; bütün sahneyi yeniden üretme.
- Kıyafeti baştan güvenli seç; filtre retleri genelde iade edilir ama saatler yer.
- Kalan abonelik kredisi dönem sonunda silinebiliyor; hesabındaki işlem geçmişinden takip et.
