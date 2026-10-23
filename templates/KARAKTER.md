# Karakter kartı: <Ad>

| Alan | Değer |
|---|---|
| Ad | <Ad> (gerçek bir ünlüye ait değil, kontrol edildi) |
| Yaş | <…> |
| Rol | <ana karakter / karşı karakter / yan> |
| Ne istiyor | <…> |
| Baskı altında | <…> |
| Bölümler | <…> |

## Varlıklar

| Ad | Dosya | Model | İş / MCP kimliği | Not |
|---|---|---|---|---|
| `@<Ad>Yuz` | `varliklar/<Ad>Yuz.png` | Soul 2.0 | <…> | 4–6 seçenekten seçildi |
| `@<Ad>Kiyafet` | `varliklar/<Ad>Kiyafet.png` | Soul 2.0 | <…> | kol/yaka kapalı, askı yok |
| `@<Ad>` | `varliklar/<Ad>.png` | GPT Image 2 | <…> | gri fon, 3 görünüm, ön boyda yüz silinmiş |
| `@<Ad><Durum>` | `varliklar/<Ad><Durum>.png` | Seedream | <…> | görünüm değişikliği |

## Sabit bloklar (her klipte kelimesi kelimesine aynı)

**KARAKTER** (30–60 kelime, İngilizce):
```
<Ad>: <age> Turkish <woman/man>, <hair>, <eyes>, <skin>, <distinguishing mark>, <makeup>, <outfit with modest neckline / long sleeves>, <jewellery / key prop>.
```

**SES** (aksan, perde, tempo, tını):
```
<Ad> speaks Turkish with a native <Istanbul> accent; <pitch>; <pace>; <timbre>.
```

O anki ton (fısıltı, titreyen, soğuk) buraya değil, klibin ACTION TIMING satırına yazılır.

## Görünüm durumları

| Bölüm / sahne | Görünüm | Varlık |
|---|---|---|
| <…> | <…> | `@<Ad>` |

## Hazır promptlar

Yüz, kıyafet ve karakter sayfası kalıpları: `templates/prompt-kaliplari.md`.
