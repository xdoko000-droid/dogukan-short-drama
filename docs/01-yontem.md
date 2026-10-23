# 01 — Yöntem

Bu belge, repodaki yöntemi insan için anlatır. Claude aynı yöntemi
`.claude/skills/short-drama-tr/SKILL.md` dosyasından okur.

## Short-drama nedir?

Dikey (9:16), bölüm başı ~60 saniyelik, her bölümü bir cliffhanger ile biten mikro dizi.
İzleyici kaydırarak gelir; ilk saniyede yakalanmazsa gider. Bu yüzden yapı katıdır.

## 1. Fikir

İyi bir fikir tek karede anlaşılır ve herkesin bildiği bir duyguya dokunur.
Fikirleri 6 ölçütle 1–5 arası puanlıyoruz:

1. **Anında anlaşılır durum** — tek karede ne olduğu belli mi?
2. **Tanıdık duygu** — izleyici bunu yaşamış mı?
3. **Görünür doruk** — en güçlü an kamerada görülebilen bir olay mı?
4. **Tepki zıtlığı** — iki kişi aynı anı zıt mı okuyor?
5. **Üretim kolaylığı** — az kişi, az mekân, gündelik hareket mi?
6. **Seri potansiyeli** — 10 bölüm taşır mı?

Türk izleyicisinde dedikodu, magazin, sosyete, aldatma, kayınvalide, intikam ve saklı kimlik
temaları güçlü. 15 özgün fikir ve puanları: `.claude/skills/short-drama-tr/references/fikir-bankasi.md`.

## 2. Sezon

8–10 bölüm. Bir **ana sır** sezon boyunca taşınır. Her bölüm bir **twist** verir ve bir **soru** ile biter.
Sonraki bölüm o soruyla açılır. Şablon: `templates/SEZON.md`.

## 3. Bölüm

| Parça | Süre | İş |
|---|---|---|
| Kanca | 0–5 sn | Doruk anıyla aç. "3 GÜN ÖNCE" ile geri dön. |
| Bağlam | 5–25 sn | Kim, ne istiyor. Başlangıç → umut → darbe → şans. |
| Tırmanış | 25–45 sn | Yeni karakter ya da ters köşe. Tepki çekimleri. |
| Cliffhanger | 45–60 sn | Cevaba bir adım kala kes. Söz ver, gösterme. Siyah ekran. |

- Her 13–30 sn'de bir darbe.
- Önemli yüzü geç göster: önce sırt, eller, gözler.
- Replikler 8 kelimeyi geçmez, ünsüzleri net kelimeler seçilir.
- Anlatıcı yok; karakterler konuşur.

Şablonlar: `templates/BOLUM-SENARYO.md`, `templates/CEKIM-LISTESI.md`.

## 4. Varlıklar

Yüz tutarlılığı için her karakterin bir **karakter sayfası** olur:

1. **Yüz** — Soul 2.0 ile 4–6 portre, birini seç → `@DefneYuz`
2. **Kıyafet** — Soul 2.0 → `@DefneKiyafet` (ince kol ya da kapalı yaka; askı ve derin dekolte yok)
3. **Karakter sayfası** — GPT Image 2: gri fon; ön boy, arka boy, yakın yüz; ön boyda yüz silinmiş → `@Defne`
4. **Görünüm değişikliği** — Seedream ile sayfayı düzenle → `@DefneGelinlik`
5. **Mekân** — Soul Location, 3/4 açı, insansız → `@YaliHol`

Şablonlar: `templates/KARAKTER.md`, `templates/MEKAN.md`.

## 5. Sabitler

Tutarlılığın asıl sırrı: aynı metni her klipte **kelimesi kelimesine** tekrar etmek.

- **Ses tarifi:** aksan, perde, tempo, tını.
- **Stil bloğu:** ışık, film dokusu, renk, 9:16.
- **ACTING TASK:** motivasyon, hedef, engel, taktik.
- **POSITIVE LOCKS:** yalnız tırnaktaki replik konuşulur, dinleyenin ağzı kapalı, ekranda yazı yok.
- **Konuşma sırası:** ikinci konuşan "She replies:" ile başlar.
- **Mekân haritası ve ilk kare yerleşimi:** kim solda, kim sağda, yüz yüzde kaçta.

## 6. Klipler

İki yol var:

- **Veo 3.1 Lite** — 4/6/8 sn tek çekim, başlangıç karesiyle. Ucuz. Sahneyi **kare zinciri** ile
  sürdürürsün: bir klibin son karesi, sonrakinin ilk karesi olur.
- **Seedance 2.5** — tek üretimde 30 sn'ye kadar, içinde kesmeler. Pahalı ama tek seferde tam sahne.

Çekim/karşı çekimde iki taraf aynı lens, aynı mesafe, aynı göz hizasında. Aynı kişinin replikleri
aynı başlangıç karesinden üretilir. Kalıplar: `templates/prompt-kaliplari.md`.

## 7. Kurgu

Enerjinin çoğu kurgudan gelir:

- Çekimler 1.5–3 sn, darbelerde punch-in.
- BOOM, WHOOSH, RISER efektleri ve sert gerilim müziği (sentez, telifsiz).
- Kritik replikten önce 0.3 sn sessizlik.
- Kelime kelime altyazı, aktif kelime sarı.
- "Bölüm X", "3 GÜN ÖNCE", "Devamı için takip et".
- Son miks −15 LUFS.

Betikler: `scripts/kurgu.py`, `scripts/altyazi.py`, `scripts/sfx.py`, `scripts/kare.py`, `scripts/zincir.py`, `scripts/doctor.py`, `scripts/ornek_klip.py`. Kullanım: `scripts/README.md`.

## 8. Kurallar

- Her ücretli üretimden önce maliyet ve onay. Toplam tavan.
- Çift gönderim yok; aynı anda en fazla 4 iş.
- Gerçek kişiye benzeyen yüz yok.
- TikTok'ta AI etiketi açık.
- Gelir vaadi yok.

## Kaynaklar ve teşekkür

Fikir puanlama, dört parçalı bölüm yapısı, karakter sayfası ve klip promptu blok yapısı gibi
tekniklerin bir kısmı Higgsfield'ın short-drama rehberinden esinlenmiştir:
https://higgsfield.ai/@adilinthewildtempo/blogs/how-to-make-ai-short-drama

Metinler kopyalanmamış, kendi deneyimimizle sınanıp kendi cümlelerimizle yazılmıştır.
Türkçe uyarlamalar, kare zinciri, ses tasarımı ve dersler bu reponun kendi üretiminden gelir.
