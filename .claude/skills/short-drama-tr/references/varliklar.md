# Varlıklar: yüz, kıyafet, karakter sayfası, mekân

Amaç: aynı kişi her çekimde aynı görünsün. Yüz kayması, AI dizisini ilk bozan şeydir.
Çözüm iki katmanlı: **referans görsel** (sayfa) + **kelimesi kelimesine aynı metin tarifi**.

Model adları CLI'daki iş tipleridir. MCP'de farklı adla görünebilir; MCP'nin model listesine bak.

| Adım | Model (CLI iş tipi) | Oran | Yaklaşık kredi |
|---|---|---|---|
| Yüz seçenekleri | Soul 2.0 (`text2image_soul_v2`) | 3:4 | 0.12 / görsel |
| Kıyafet | Soul 2.0 (`text2image_soul_v2`) | 3:4 | 0.12 / görsel |
| Karakter sayfası | GPT Image 2 (`gpt_image_2`) | 16:9 | 6.5 |
| Görünüm değişikliği | Seedream 5 Pro (`seedream_v5_pro`) | 16:9 | 2.5 |
| Mekân | Soul Location (`soul_location`) | 16:9 | canlı maliyete bak |
| Tek kare / başlangıç karesi | nano_banana_2 | 9:16 | 2 |

Fiyatlar 22 Eki 2026 tarihli; değişebilir. Her üretimden önce canlı maliyeti göster.

## 1. Yüz (`@<Ad>Yuz`)

- 4–6 portre üret, kullanıcı birini seçer.
- Tarif: yaş, saç, göz, ten, ayırt edici iz (ben, kaş), genel hava. Işık nötr, arka plan sade.
- Gerçek bir ünlüye benziyorsa ele. Kullanıcıya "tanıdık birine benziyor mu?" diye sor.

## 2. Kıyafet (`@<Ad>Kiyafet`)

- Omuzdan ayağa, düz duvar önünde, elde çanta ya da eşya yok.
- **Filtre kuralı:** ince uzun kol ya da kapalı yaka. Askı yok, derin dekolte yok, sırt dekoltesi yok.
  "elegant, modest high neckline, thin long sleeves" gibi ifadeler işe yarar.
- Hikâyede çıkarılacak bir parça (palto, gözlük) varsa başlangıç kıyafetine dahil et.

## 3. Karakter sayfası (`@<Ad>`)

GPT Image 2 ile, yüz ve kıyafet referanslarını birleştir. Üç kural:

1. **Gri fon.** Beyaz ya da siyah değil; düz orta gri.
2. **Üç görünüm:** ön boy (baştan ayağa), arka boy, yakın yüz.
3. **Ön boy görünümde yüz silinmiş.** Pürüzsüz, özelliksiz bir oval. Böylece video modeli yüzü
   yalnız yakın plandan alır; iki farklı yüz kaynağı arasında gidip gelmez.
   Model yine yüz çizerse görsel düzenleyici ile sil.

Işık nötr ve stüdyo gibi olsun. Sahneye özel ışık (ay ışığı, mum, neon) sayfaya girmez; o sahne promptunun işi.

## 4. Görünüm değişikliği (`@<Ad><Durum>`)

Saç açık, gelinlik, gözlük çıkmış gibi değişiklikler için Seedream ile sayfayı **düzenle**.
Yüz, oran, fon ve düzen aynı kalsın. Yeni ad ver: `@DefneGelinlik`. Bir sayfa tek görünüm taşır.

## 5. Mekân (`@<MekanAdi>`)

Soul Location ile. 3/4 açı, **insansız**, sahnenin ihtiyaç duyduğu her şey görünür:
giriş kapısı, pencere, oturulacak yer, yürüme yolu, ana ışık kaynağı.
Tek çekimlik ikinci mekân için ayrı görsel üretme; ana mekânı stil referansı yap, yeniyi metinle tarif et.

## 6. Küçük detaylar ve hikâye eşyaları

Yüzük, davetiye, dosya gibi her klipte aynı görünmesi gereken eşya için ya ayrı referans üret
ya da her klipte aynı kelimelerle tarif et. Örnek:
`CARD: a cream invitation card with a thin gold edge; only its plain blank back side or its thin edge is ever visible to the camera.`

## 7. Başlangıç kareleri (Veo yolu)

Veo 3.1 Lite klibi bir başlangıç karesinden başlar. Kareyi nano_banana_2 ile üret:
karakter sayfası (kimlik) + mekân (ışık ve renk) referans, prompt ilk karenin yerleşimini tarif eder.
Kalıp: `templates/prompt-kaliplari.md` → "Başlangıç karesi".

Ücretsiz kare kaynakları:
- Önceki klibin son karesi (`scripts/kare.py`). Kare zinciri bununla kurulur.
- Var olan bir karenin kırpımı (orta planı yakın plana çevirmek).

## Storyboard (isteğe bağlı)

3x3 storyboard sayfası kompozisyon fikri verir. Ama model "her panel 9:16 olsun" isteğine
çoğu zaman uymaz. Storyboard'u yalnız **kompozisyon referansı** say; panelden kare kesip
doğrudan başlangıç karesi yapma, onu ayrıca üret.

## Adlandırma ve kayıt

`uretim/<seri>/varliklar/` altında:
```
DefneYuz.png  DefneKiyafet.png  Defne.png  DefneGelinlik.png  YaliHol.png
```
Her varlığı `templates/KARAKTER.md` / `templates/MEKAN.md` kartına işle: ad, dosya, MCP/iş kimliği, tarif metni.
