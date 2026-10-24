# 03 — Dersler

Örnek dizi "Çifte Davetiye" üretilirken yaşanan gerçek sorunlar ve çözümleri.

## Filtre (NSFW) retleri

- **Sorun:** Askılı saten elbise sürekli reddedildi. Kareler geçse bile klip üretiminde takıldı.
  Bir sahnede ~15 deneme reddedildi.
- **Bilgi:** Retler genelde ücretsiz iade ediliyor ama her deneme zaman yiyor.
- **Çözüm:** Kıyafeti baştan güvenli seç: ince uzun kol ya da kapalı yaka; askı, açık omuz, derin dekolte yok.
  "elegant, modest high neckline, thin long sleeves" işe yaradı. Gerekirse üstüne palto ekle.
- **Ek:** "leans in close", "crushes", "slip dress" gibi ifadeler ve bitiş karesi (end image) ret oranını artırdı.
  Bitiş karesini kaldırınca geçti.
- **Kurgu hilesi:** Eski (askılı) kıyafetli çekimleri kullanmak istiyorsan zaman atlaması ile açıkla:
  "3 gün önce" bir kıyafet, "bu gece" başka kıyafet.

## Yazılı nesneler (davetiye kartı)

- **Sorun:** Model kartın yazılı yüzünü kameraya çevirebiliyor; anlamsız harfler çıkıyor.
- **Çözüm:** Kartı her klipte aynı cümleyle tarif et: yalnız boş arka yüzü ya da ince kenarı görünür.
  Kart yine dönerse o çekimi kurgudan çıkar. Seyirci içeriği karakterin yüzünden okusun.

## Veo bitiş karesi

- **Sorun:** Veo bitiş karesini birkaç kare aşıyor; birleşimde zıplama oluyor.
- **Çözüm:** Birleştirirken SSIM ile bitiş karesine en yakın kareyi bul, orada kes (`scripts/zincir.py`).

## Kamera

- **Sorun:** "slightly handheld" ile "steady" birlikte yazılınca kamera savruldu.
- **Çözüm:** `smooth steady camera, slow controlled movement, no whip pans`. Handheld ifadesini sil.

## Ses

- **Sorun:** Kelime sonu ünsüzleri yutulabiliyor.
- **Çözüm:** Replikleri kısa tut (≤ 8 kelime), `clear diction, every final consonant pronounced` yaz.
- **Sorun:** Riser efekti "Nermin" ismini "Dermin" gibi duyurdu.
- **Çözüm:** Efektleri replik altında kıs; kritik replikten önce 0.3 sn sessizlik bırak.
- Son miksten konuşma tanıma ile replikleri kontrol et.

## Storyboard

- **Sorun:** Panellerin 9:16 olması istense de model yatay ya da farklı düzende çizebiliyor.
- **Çözüm:** Storyboard'u yalnız kompozisyon referansı say. Başlangıç karelerini ayrıca üret.

## İndirme

- **Sorun:** Dönen ilk URL bazen giriş görseli oluyor.
- **Çözüm:** Sonucu `result_url` alanından indir.

## Higgsfield kredisi

- Abonelikle gelen kalan kredi 30 günde bir siliniyor. Hesabındaki işlem geçmişinde görebilirsin.
  Üretimi dönem sonuna sıkıştırma; düzenli üret.

## ffmpeg

- **Sorun:** macOS Homebrew'un ffmpeg'inde libass yok; altyazı gömülemiyor.
- **Çözüm:** `imageio-ffmpeg` paketinin getirdiği ffmpeg altyazı gömmeyi destekliyor.
  `python scripts/doctor.py` uygun ffmpeg'i bulur.

## Ücretsiz görsel servisleri

- Pollinations gibi ücretsiz katmanlar denendi: çok yavaş ve kalitesiz. Karakter tutarlılığı için yeterli değil.

## Hikâye

- **Sorun:** 16 ayrı, birbirinden kopuk klip "kopuk" hissettirdi.
- **Çözüm:** 3–4 sürekli sahne (kare zinciri) + kurguda kanca ve hızlı kesme. En iyi sonuç bu birleşimle geldi.
- **Sorun:** Anlatıcılı fotoroman (durağan görsel + dış ses) "yeterince gerçek değil" dedirtti.
- **Çözüm:** Karakterler konuşmalı. Her konuşmalı çekimde tek kişi konuşur, dinleyenin ağzı kapalı.

## Marka ve logo

- Promptlarda ve ekranda marka ve logo adı kullanma. Kamera, film, moda ya da platform markası yerine
  markasız tarif yaz: "cinema camera look", "35mm film look", "luxury handbag".

## Higgsfield MCP ile dosya yükleme

- Yerel bir videoyu ya da görseli MCP'ye vermek için: `media_upload` → dönen `upload_url`'e PUT → `media_confirm`.
- PUT isteğinde **`If-None-Match: *`** başlığı da gönderilmeli (imzalı adresin parçası). Yoksa yükleme reddedilir.
  ```
  curl -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" --data-binary @kanca.mp4 "<upload_url>"
  ```
- Virality Predictor işi kuyrukta birkaç dakika bekleyebilir; sonucu `jobs_wait` ile ya da `virality_predictor` (action: preview) ile sonra açabilirsin. Gönderimde kredi düşmedi (24 Eki 2026 denemesi).
- MCP'de `get_cost: true` ile maliyet önceden öğrenilebilir (ör. nano_banana_2 görsel: 1,5 kredi).

## Kısa özet

1. Kıyafet güvenli.
2. Yazı kameraya dönmez.
3. Kamera sabit.
4. Replik kısa, ünsüz net.
5. Sahne sürekli, kurgu hızlı.
6. Karakterler konuşur.
