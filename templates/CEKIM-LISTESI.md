# <Seri adı> — Bölüm <N> çekim listesi

Dosya: `uretim/<seri>/bolumler/bolum-<NN>/cekim-listesi.md`. Kurguda `kurgu.json`'a çevrilir; klipler `klipler/` altında.

Kurgu sırasıyla. Her satır kurgudaki bir çekimdir (1.5–3 sn). Birden fazla çekim aynı klipten kesilebilir.

**Kaynak sütunu:** `YENİ <kod>` = üretilecek klip · `<klip-dosyası> (giriş–çıkış sn)` = var olan klipten kesit · `kurgu` = siyah kart / yazı.

| # | Zaman | Süre | Kadraj | Kim | Türkçe replik | Kaynak | Ses / kurgu |
|---|---|---|---|---|---|---|---|
| 1 | 0.0–2.4 | 2.4 | <yakın plan, mekân> | <Ad> | "<…>" | YENİ V1 (0.3–2.7) | "Bölüm <N>" 0–1 sn · BOOM · punch-in %6 |
| 2 | 2.4–3.6 | 1.2 | <karşı çekim yakın> | <Ad> (tepki, ağız kapalı) | — | YENİ V2 (0.0–1.2) | riser kısa |
| 3 | 3.6–4.6 | 1.0 | Siyah | — | "3 GÜN ÖNCE" | kurgu | WHOOSH |
| … | | | | | | | |
| <son> | <…> | 2.5 | Siyah | — | "Devamı için takip et" | kurgu | yankı söner |

**Darbe ritmi:** ~<…> · ~<…> · ~<…> · ~<…> sn
**Ortalama çekim:** ~<…> sn

## Üretim listesi

| Kod | Tür | Model | Süre | Başlangıç karesi | Bitiş karesi | Referanslar | Kullanıldığı çekimler | Tahmini kr |
|---|---|---|---|---|---|---|---|---|
| K1 | kare | nano_banana_2 | — | — | — | `@<Ad>`, `@<Mekan>` | V1, V2 | 2 |
| V1 | klip | veo3_1_lite | 6 sn | K1 | — | — | #1, #<…> | 9 |
| S1 | klip | seedance_2_5 720p | 30 sn | — | — | `@<Ad>`, `@<Ad>`, `@<Mekan>` | #<…>–#<…> | 210 |
| | | | | | | | **Toplam** | **<…>** |

**Tavan:** <…> kr

**Gönderim sırası (en fazla 4 eşzamanlı):**
1. <kareler + bağımsız klipler>
2. <karelere bağlı klipler, kareler onaylanınca>

## Ses planı

- Müzik: <nerede yükselir, nerede kesilir>
- 0.3 sn sessizlik öncesi replikler: #<…>, #<…>
- BOOM: #<…> · WHOOSH: #<…> · RISER: #<…>
- Son miks −15 LUFS
