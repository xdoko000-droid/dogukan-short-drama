# Kanca kontrolü (Virality Predictor)

Kurgu bittikten sonra bölümün açılışını Higgsfield'ın **Virality Predictor** modeliyle ölç.
Model adı `brain_activity`, çıktı tipi metin. Parametreler: `medias` (zorunlu, video), `folder_id` (opsiyonel).

## Ücret

Şu an kredisiz olduğu söyleniyor; **doğrulanmadı**. Önceden maliyet ölçülemiyor:
`higgsfield generate cost brain_activity` "does not support alpha v2 cost estimation" hatası veriyor.

- Çalıştırmadan **önce ve sonra** bakiyeyi kontrol et (MCP hesap aracı ya da `higgsfield account status`).
- Bakiye düşerse bu adımı ücretli say: harcamayı `harcama.txt`'ye yaz, bir sonraki seferde önce onay iste.
- `/tek-prompt` modunda bakiye düşerse dur ve sor.

## Adımlar

1. İlk ≤ 15 sn'yi ücretsiz kes:
   ```
   PY scripts/kanca_kes.py uretim/<seri>/bolumler/bolum-01/bolum-01.mp4 --sn 15
   ```
   Çıktı: `bolum-01-kanca.mp4` (aynı klasörde).
2. Kesilen klibi Virality Predictor'a ver:
   - **MCP (önerilen):** Higgsfield araç listesinde `brain_activity` / Virality Predictor üretim aracını seç,
     kanca klibini `medias` olarak ver. Araç adını tahmin etme; listeden bak.
   - **CLI:** `higgsfield generate create brain_activity --video bolum-01-kanca.mp4`, sonra
     `higgsfield generate wait <id>`. Not: CLI 1.1.26 bu modelde "Model type "text" is not supported by
     generate create yet" hatası veriyor; bu durumda MCP yolunu kullan.
3. Sonucu kısaca özetle:
   - **Kanca puanı** (genel puan).
   - **Kalma oranı:** izleyicinin hangi saniyeye kadar kaldığı, en büyük düşüşün olduğu an.
   - **Dikkat haritası:** dikkatin yükseldiği ve düştüğü anlar.
   Ham çıktıyı kullanıcıya yapıştırma; 3–5 satırla anlat.
4. Puan düşükse 1–2 kurgu önerisi ver (yeniden üretim gerektirmeyenler önce):
   - Doruk anını ilk 1 sn'ye çek; "3 GÜN ÖNCE" kartını daha erken koy.
   - Düşüş anındaki çekimi 1.5 sn'ye kısalt ya da punch-in ekle.
   - İlk replikten önce 0.3 sn sessizlik + BOOM; ilk karede yüz yerine el, gözler ya da yazılı nesne.
   - "Bölüm X" yazısını kısalt ya da kaldır.
   Öneriyi `kurgu.json`'a uygula, `kurgu.py` ile yeniden kurgula. Yeniden ölçmek ayrı bir çalıştırmadır;
   yukarıdaki ücret kuralı yine geçerli.

## Gerçek deney (Çifte Davetiye 1. bölüm, 24 Eki 2026)

Aynı bölümün ilk 15 sn'si üç kez ölçüldü (puanlar 0–100, Higgsfield'ın tahmini; garanti değildir):

| Versiyon | Değişiklik | Maliyet | Kanca | İlgi | Genel | Viral |
|---|---|---|---|---|---|---|
| v1 | Açılış: sakin konuşma yakın planı + "BÖLÜM 1" yazısı | — | 24 | 33 | 44 | 50 |
| v2 | İlk kare şok yüzü, replik dış ses (J-cut), BOOM + punch-in, yazı kaldırıldı | 0 kredi (yalnız kurgu) | 30 | 39 | 47 | 47 |
| v3 | v2 + açılışa 4 sn'lik aksiyon klibi (davetiye yırtılıyor) | 6 kredi | 32 | 40 | 48 | 48 |

Çıkan dersler:
- **En büyük kazanç kurgudan gelir ve bedavadır.** İlk karede hareket/duygu, ilk 2 sn'de yazı yok, sessizlik yok.
- Yeni aksiyon klibi az ekledi (+2). Önce kurguyu düzelt, sonra gerekirse çekim ekle.
- "Viral" puanı ölçümler arasında ±3 oynuyor; tek ölçümle karar verme.
- Kalan zayıf an: ilk saniyeden sonra kıpırtısız konuşma yakın planına geçiş. Konuşma çekimlerini kısa tut ya da hareket ekle.
- Asıl ölçüm platformdur: iki versiyonu yayınlayıp izlenme süresini karşılaştır.
