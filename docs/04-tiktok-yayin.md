# 04 — TikTok'ta yayın

## Zorunlu

- **AI etiketi açık.** Yüklerken "Yapay zekâ ile oluşturulmuş içerik" (AI-generated content) ayarını aç.
- **Açıklamada:** "Kurgudur, AI ile üretildi."
- Gerçek kişi, marka ya da kurum adı kullanma. Karakterler hayal ürünü.
- Gelir, kazanç, "zengin ol" türü vaat yok.

## Başlık ve açıklama

| Alan | Kalıp | Örnek |
|---|---|---|
| Başlık | `Bölüm N \| <kanca cümlesi>` | Bölüm 1 \| Davetiyede gelin ben değildim |
| Açıklama | 1–2 cümle merak + izleyiciye soru + uyarı | Düğüne üç gün kala ikinci davetiyeyi buldum… Sence ikinci isim kimin? 👇 Kurgudur, AI ile üretildi. |
| Hashtag | 3–5 adet | #dizi #minidizi #aldatma #düğün #yapayzeka |

Kanca cümlesi bölümün ilk replikiyle ya da twistiyle aynı duyguyu taşısın. Cevabı verme.

**Soru şart.** Açıklamasında soru olmayan bölümlere hiç yorum gelmedi. Soru bölüme özel olsun ve tahmin
istesin ("Sence mektubun ikinci sayfasında ne yazıyor?"), evet/hayır değil. 2. bölümden itibaren
"1. bölüm profilde 📌" satırını ekle. Paketi `scripts/yayin_paketi.py` hazırlar.

## Video

- 1080x1920, 9:16, ~60 sn.
- İlk saniyede yüz ve ses. Siyah açılış yok. İlk replik 0,3 sn içinde.
- İlk 2,5 sn üstte dizinin konu cümlesi (`kurgu.json` → `ayarlar.acilis_yazisi`). Diziye ilk kez rastlayan kişi
  neyi izlediğini anlamazsa ilk saniyede geçiyor.
- Altyazı gömülü (kelime kelime). Seslerin kapalı izlendiği durumlar için şart.
- Son: siyah kart **yok**. Cliffhanger karesi 0,8 sn donar, üstünde "Devamı yarın" (`scripts/bitis_duzelt.py`).
  Siyah "Devamı için takip et" kartında izleyicinin çoğu çıktı; donan kareden sonra video başa sarar.
- Kapak: kancadaki en güçlü yüz ifadesi. Kapakta okunur yazı varsa yalnız dizi adı ve "Bölüm N".
  Kareyi altyazısız **ham** klipten al; altyazılı son videodan alınan karede yazılar üst üste biner.

## Seri düzeni

- Bölümleri bir **oynatma listesine** (playlist) ekle: "<Seri adı> — Sezon 1".
- Her bölümün altına sabit yorum: yeni geleni 1. bölüme yönlendir + soru (`sabit-yorum.txt`).
- 1, 2, 3. bölümleri profilin en üstüne sabitle (önce 3, sonra 2, en son 1). Instagram ve TikTok'ta
  sabitleme ve oynatma listesi yalnız **mobil uygulamada** var; web'de yok.
- Önceki bölümü izlemeyen için 2. bölümden itibaren ilk 2–3 sn'de kısa hatırlatma ya da doğrudan önceki cliffhanger'ın cevabıyla aç.
- Düzenli yayın: örneğin her gün aynı saat ya da haftada 3 bölüm. Düzen, sayıdan önemli.

## Yayından önce kontrol

- [ ] AI etiketi açık
- [ ] Açıklamada "Kurgudur, AI ile üretildi."
- [ ] Başlık "Bölüm N | …"
- [ ] Ekranda anlamsız yazı yok
- [ ] Ses −15 LUFS, altyazı birebir
- [ ] Açıklamada bölüme özel soru var
- [ ] Siyah son kart yok; ilk 2,5 sn'de konu cümlesi var
- [ ] Oynatma listesine eklendi
- [ ] Yayından sonra sabit yorum yazıldı

## Ölçüm

Bölüm başına izlenme süresi, tamamlama oranı ve **geçme oranına** (Instagram: "Geçme oranı", ilk saniyede
kaydıranlar) bak. Hedef: geçme < %25. Yorumlama örnekleri: `docs/03-dersler.md` → "Yayın verisi". Düşüş nerede başlıyorsa
o saniyeyi incele: darbe geç mi geldi, sahne uzun mu kaldı? Bir sonraki bölümün çekim listesini buna göre düzelt.

## Tarayıcıdan yükleme (Claude in Chrome)

- Dosya yükleme sınırı **10 MB**: `scripts/yayin_paketi.py --max-mb 9.3`.
- Yüklemeden önce oturum açık hesabın doğru hesap olduğunu doğrula (kullanıcı adı ekranda).
- Instagram'da kırpmayı **9:16** seç; varsayılan kare kırpma videoyu keser.
- Şifre girme, hesap ayarı değiştirme; giriş ekranı ya da passkey önerisi çıkarsa kullanıcıya bırak.
