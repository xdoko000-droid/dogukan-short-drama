---
description: Kurulum sihirbazı. Python, ffmpeg, Git, paketler ve Higgsfield MCP girişini soru sorarak tamamlar.
---

# /kur: Kurulum sihirbazı

Kullanıcı teknik bilmiyor varsay. Komutları sen çalıştır. Onun yapması gerekenleri (tarayıcıda giriş,
Claude'u yeniden açmak gibi) adım adım söyle. Sohbette **tek seferde tek adım**, kısa Türkçe cümleler.
Her adım bitince bir satırlık özet ver ("✓ ffmpeg hazır") ve sonrakine geç.

Akış tekrar çalıştırılabilir: her adımda önce durumu kontrol et. Hazır olan adımı atla.

## Kurallar

- **Sistem yazılımı kurmak kullanıcının kararıdır.** `winget`, `brew` ya da `pip` komutunu
  çalıştırmadan önce ne kurulacağını tek cümleyle söyle ve **AskUserQuestion** ile onay al
  (seçenekler: "Evet, kur" / "Hayır, ben kurarım"). Onaysız kurulum yok.
- Ücretli Higgsfield üretimi bu akışta **yok**. Yalnız ücretsiz okuma araçları kullanılır.
- `scripts/` altındaki betiklerin hiçbiri ücretli API çağırmaz. `ornek_klip.py` yalnız yerel ffmpeg ile
  renkli test klipleri üretir: ücretsiz, internet gerekmez, Higgsfield'a bağlanmaz. Çalıştırmak için onay gerekmez.
- Windows'ta Claude Code komutları genelde Git Bash içinde çalıştırır. Yollarda `/` kullan.
- Bu dosyada **PY** şu demek:
  - Windows: `.venv/Scripts/python.exe`
  - Mac: `.venv/bin/python`
  Sanal ortamı `activate` etme; PY ile doğrudan çalıştır.
- Windows tuzakları için `CLAUDE.md` → "Windows tuzakları" bölümüne bak.

## 1. Repo burada mı?

Çalışma klasöründe `scripts/doctor.py` ve `CLAUDE.md` var mı bak.

- **Varsa:** 2. adıma geç.
- **Yoksa:** önce `git --version` ile Git'i kontrol et.
  - Git yoksa: Windows'ta `winget install --id Git.Git -e`, Mac'te `xcode-select --install`
    ya da `brew install git` (onay al).
  - Sonra klonla:
    ```
    git clone https://github.com/xdoko000-droid/dogukan-short-drama.git
    ```
  - Klasörün tam yolunda ğ, ü, ş, ı, ö, ç ya da boşluk varsa uyar ve kısa bir yola klonlamayı öner
    (Windows: `C:\drama\`). Bkz. "Windows tuzakları".
  - Kurulumun geri kalanını `dogukan-short-drama/` içinde sürdür. Higgsfield bağlantısı için
    kullanıcı Claude Code'u bu klasörde yeniden açacak (5. adım); bunu şimdiden haber ver.

## 2. Durum kontrolü

```
py scripts/doctor.py          # Windows
python3 scripts/doctor.py     # Mac
```
`.venv` varsa PY ile çalıştır. Çıktıdaki ✗ satırlarını kullanıcıya sade bir listeyle söyle
("Eksik: Python, ffmpeg"). Hepsi ✓ ise 4. adıma geç.

## 3. Eksikleri kur (her biri için ayrı onay)

Sırayla, her eksik için: ne olduğunu tek cümleyle söyle → AskUserQuestion ile onay → kur → kontrol et.

| Eksik | Windows | Mac |
|---|---|---|
| Python 3.10+ | `winget install --id Python.Python.3.12 -e` | `brew install python@3.12` ya da uv (aşağıya bak) |
| ffmpeg | `winget install --id Gyan.FFmpeg -e` | `brew install ffmpeg` |
| Git | `winget install --id Git.Git -e` | `xcode-select --install` |

- Mac'te `brew` yoksa: kullanıcıya https://brew.sh adresindeki tek satırlık komutu Terminal'e
  yapıştırmasını söyle (şifre ister; bunu o yapar). Bitince haber versin.
- winget sonrası komut hâlâ bulunamıyorsa: PATH yenilenmemiştir. Kullanıcıdan Claude Code'u kapatıp
  aynı klasörde yeniden açmasını iste, sonra "kur" yazsın; akış kaldığı yerden sürer.
- ffmpeg kurulamazsa sorun değil: `requirements.txt` içindeki `imageio-ffmpeg` yedek ffmpeg getirir.

### Python < 3.10 ise (ör. Mac sistem Python'u 3.9.6, Homebrew yok)

AskUserQuestion ile sor: hangi yolla kuralım?
- **Homebrew**: `brew install python@3.12` (brew yoksa önce https://brew.sh; şifreyi kullanıcı girer).
- **uv** (Homebrew gerektirmez, şifre istemez): kurulum komutu için resmi sayfa
  https://docs.astral.sh/uv/getting-started/installation/ ; sonra `uv python install 3.12`.
- **python.org yükleyicisi**: https://www.python.org/downloads/ (kullanıcı indirip kurar).
- Windows: `winget install --id Python.Python.3.12 -e`.

Seçime göre kur. Sonra `.venv`'i yeni Python ile **yeniden oluştur** (eski `.venv` 3.9 ise sil) ve paketleri kur:
```
# uv ile
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt   # ya da: .venv/bin/python -m pip install -r requirements.txt

# Homebrew / python.org ile
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```
Not: `uv venv` ile oluşan `.venv`'de pip olmayabilir; o durumda `uv pip install` kullan.
Sonra doctor'ı PY ile tekrar çalıştır.

## 4. Sanal ortam ve paketler

`.venv` yoksa onay al, sonra:
```
# Windows
py -m venv .venv
.venv/Scripts/python.exe -m pip install --upgrade pip
.venv/Scripts/python.exe -m pip install -r requirements.txt

# Mac
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```
Kurulum birkaç dakika sürebilir; kullanıcıya söyle. Sonra doctor'ı PY ile tekrar çalıştır.
Zorunlu ✗ kalmadıysa devam et.

## 5. Higgsfield MCP bağlantısı

Önce araç listende Higgsfield araçları var mı bak (adında `higgsfield` geçen MCP araçları).

**Yoksa**, durum şunlardan biridir:

- **Claude Code repo klasöründe açık değil** (1. adımda klonladıysan böyledir). Kullanıcıya söyle:
  1. Claude Code'u kapat.
  2. Masaüstü uygulaması: klasör olarak `dogukan-short-drama`'yı seç.
     Terminal: `cd dogukan-short-drama` sonra `claude`.
  3. "Bu projedeki higgsfield MCP sunucusunu onaylıyor musun?" sorusuna **onayla**.
  4. "kur" yaz. Kaldığımız yerden devam ederiz.
- **Klasör doğru, giriş yapılmamış.** Adımları tek tek söyle, her birinde bekle:
  1. Bu sohbete `/mcp` yaz ve Enter'a bas.
  2. Listeden `higgsfield`'ı seç.
  3. **Authenticate**'i seç. Tarayıcı açılır.
  4. Tarayıcıda Higgsfield hesabınla giriş yap, izin ver.
  5. Claude Code'a dön, "tamam" yaz.
  Tarayıcı açılmazsa ekrandaki bağlantıyı kopyalayıp tarayıcıya yapıştırsın.
- `/mcp` listesinde `higgsfield` hiç yoksa: `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`
  komutunu (onay alarak) çalıştır, sonra Claude Code'u yeniden açtır. Ayrıntı: `docs/05-higgsfield-mcp-kurulum.md`.

Not: Kullanıcı Claude masaüstü/web uygulamasını soruyorsa aynı bağlantı orada da kurulabilir
(Settings → Connectors → + → Ad `Higgsfield`, URL `https://mcp.higgsfield.ai/mcp`; ayrıntı `docs/05`).
Ama bu repo dosya ve betik kullandığı için asıl çalışma yeri Claude Code'dur; kurulumu burada sürdür.

**Higgsfield hesabı yoksa:**
1. Kayıt için şu bağlantıyı ver: https://higgsfield.ai/s/higgsfield-mcp-general-yt-dogukanlive-CTCNCG
   (sponsorlu bağlantı olduğunu belirt; README'deki `SPONSOR_LINK` satırıyla aynı).
2. Kayıt olsun, kredili bir plan seçsin. Hangi planın uygun olduğunu kendisi seçer; sen yalnız bölüm başı
   tahmini söyle (Ekonomik ~140, Dengeli ~375, Premium ~950 kredi; 22 Eki 2026 fiyatı).
3. Kazanç ya da gelir vaadi verme.
4. Bitince yukarıdaki giriş adımlarına dön.

**Doğrulama:** Bağlantıyı ücretsiz bir okuma aracıyla doğrula. Araç adını **tahmin etme**: mevcut Higgsfield
araç listesinden bakiye, kredi, hesap ya da kullanıcı bilgisi döndüren bir araç seç (ör. adında
balance, credits, account, me, profile geçen). Üretim, gönderim ya da maliyet doğuran araç çağırma.
Kalan krediyi kullanıcıya söyle. Böyle bir araç yoksa model listesi gibi başka bir okuma aracını kullan.

## 6. Deneme çıktısı (ücretsiz)

**Bu adım ücretsizdir, onay gerektirmez; Higgsfield'a dokunmaz.** Yalnız yerel ffmpeg ve Python kullanır.
Tek komut:
```
PY scripts/deneme.py
```
(`ornek_klip.py` test kliplerini üretir, ardından `kurgu.py examples/kurgu-ornek.json` çalışır.
Elle yapmak istersen bu iki komutu sırayla çalıştır.)

`faster-whisper` altyazı modeli ücretsizdir ama ilk çalıştırmada internetten indirilir (birkaç yüz MB,
birkaç dakika sürebilir; kullanıcıya söyle). İnternet yoksa deneme durmaz: altyazı senaryo metninden
tahmini zamanlamayla yazılır.
Çıktı: `examples/output/bolum.mp4`. Kullanıcıya dosyanın yerini söyle, açıp izlemesini öner
(Windows: `start examples/output/bolum.mp4`, Mac: `open examples/output/bolum.mp4`).

## 7. Bitiş

Kısa özet:
```
✓ Python  ✓ ffmpeg  ✓ paketler  ✓ Higgsfield (kalan kredi: …)  ✓ deneme kurgusu
```
Sonra: "Kurulum tamam. İlk dizini yapalım mı?" diye sor (AskUserQuestion: "Evet, başlayalım" / "Sonra").
Evet derse `/ilk-dizi` akışına geç (`.claude/commands/ilk-dizi.md`).
