# Mekân kartı: <Mekân adı>

| Alan | Değer |
|---|---|
| Ad | `@<MekanAdi>` |
| Dosya | `varliklar/<MekanAdi>.png` |
| Model | Soul Location (3/4 açı, insansız) |
| İş / MCP kimliği | <…> |
| Zaman | <gece / gündüz / akşam> |
| Bölümler | <…> |

## Sabit blok (her klipte kelimesi kelimesine aynı)

**LOCATION** (İngilizce):
```
<Place description: architecture, floor, main furniture, doors, windows, key light sources>. Same place, same light throughout.
```

## Mekân haritası (kamera görüşüne göre)

| Bölge | Ne var |
|---|---|
| Sol | <örnek: koyu ahşap merdiven> |
| Orta arka | <örnek: oymalı çift kanatlı kapı> |
| Sağ | <örnek: pirinç masa lambası> |
| Tavan | <örnek: kristal avize> |
| Ana ışık | <yön, renk sıcaklığı: sıcak 2700K avizeden sağ üstten> |
| Dolgu / kontur | <örnek: soğuk 5600K ay ışığı arkadan> |

## Hareket yolları

- Giriş: <nereden girilir>
- Karakterlerin durduğu yerler: <…>
- Kamera konumları: <yakın planlar için 1.2 m, göz hizası; iki kişilik için 2.5 m, göğüs hizası>

## Üretim promptu

Kalıp: `templates/prompt-kaliplari.md` → "Mekân".
