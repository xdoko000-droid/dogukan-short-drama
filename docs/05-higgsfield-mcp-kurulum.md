# 05 — Higgsfield MCP kurulumu

Claude'un Higgsfield ile görsel ve video üretebilmesi için iki yol var:

1. **MCP (önerilen)** — Claude, Higgsfield araçlarını doğrudan çağırır.
2. **CLI (yedek yol)** — Claude, terminalde `higgsfield` komutunu çalıştırır.

İkisi de aynı Higgsfield hesabını ve kredisini kullanır. API anahtarı gerekmez; giriş tarayıcıdan yapılır.

## Bulunan resmi bilgi

Kaynak: https://higgsfield.ai/mcp (23 Eki 2026'da kontrol edildi)

- Resmi MCP sunucu adresi: **`https://mcp.higgsfield.ai/mcp`**
- Sunucu türü: HTTP (uzak MCP). Giriş OAuth ile, tarayıcıda yapılır. Sunucunun kendi yetkilendirme
  bilgisinde Claude Code desteklenen istemciler arasında listeleniyor.
- Sayfa, claude.ai / Claude masaüstü için bu adresi "özel bağlayıcı" (custom connector) olarak eklemeyi anlatıyor.
- Sayfanın "Claude Code" sekmesi ise CLI yolunu öneriyor (`npm i -g @higgsfield/cli`, `higgsfield auth login`).

Aşağıdaki Claude Code komutları, Claude Code'un standart uzak MCP ekleme yöntemidir. Adres değişirse
güncel adresi https://higgsfield.ai/mcp sayfasındaki "Copy connector URL" düğmesinden al.

---

## Yol 1: Claude Code + Higgsfield MCP

### A. Repo ile gelen ayar (en kolay)

Repo kökünde `.mcp.json` var:
```json
{
  "mcpServers": {
    "higgsfield": {
      "type": "http",
      "url": "https://mcp.higgsfield.ai/mcp"
    }
  }
}
```
1. Repo klasöründe Claude Code'u aç:
   ```
   claude
   ```
2. Claude Code bu projedeki MCP sunucusunu onaylamanı ister. **Onayla.**
3. Claude Code içinde yaz:
   ```
   /mcp
   ```
4. Listeden `higgsfield` → **Authenticate** seç. Tarayıcı açılır, Higgsfield hesabınla giriş yap.
5. Claude Code'a dön. `/mcp` ekranında `higgsfield` bağlı görünmeli.

### B. Elle ekleme (Windows ve Mac aynı)

PowerShell (Windows) ya da Terminal (Mac) aç:
```
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
```
Tüm projelerde kullanmak istersen:
```
claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp
```
Kontrol:
```
claude mcp list
```
Sonra Claude Code içinde `/mcp` → `higgsfield` → **Authenticate** → tarayıcıda giriş.

### Test

Claude Code'a yaz:
```
Higgsfield'a bağlı mısın? Kalan kredimi ve kullanılabilir video modellerini listele. Hiçbir şey üretme.
```

---

## Yol 2: Claude masaüstü / claude.ai (sohbet için)

Claude masaüstü uygulamasında ya da claude.ai'de aynı Higgsfield bağlantısını kurabilirsin:

1. Claude'u aç → **Settings** → **Connectors**.
2. **+** düğmesine bas.
3. Ad: `Higgsfield`
4. URL: `https://mcp.higgsfield.ai/mcp` (güncel adres: https://higgsfield.ai/mcp sayfasındaki "Copy connector URL").
5. **Add** de.
6. Açılan pencerede Higgsfield hesabınla giriş yap, izin ver.

Menü adı sürüme göre farklı görünebilir: **Customize → Connectors** ya da **Add custom connector**.

Not: Claude uygulamasında bağlantı sohbet için yeterlidir. Bu repo dosya ve betik (kurgu, altyazı,
kare çıkarma) kullandığı için asıl çalışma yeri **Claude Code**'dur.

---

## Yol 3: CLI (yedek yol)

MCP bağlanmazsa ya da maliyet aracı MCP'de yoksa CLI kullan.

### Gereken: Node.js
- Windows: https://nodejs.org adresinden LTS sürümünü kur (ya da `winget install OpenJS.NodeJS.LTS`).
- Mac: https://nodejs.org ya da `brew install node`.

### Kurulum
```
npm i -g @higgsfield/cli
higgsfield auth login
```
`auth login` tarayıcıyı açar; giriş yap ve terminale dön.

Higgsfield'ın kendi skill paketleri var; kurmadan önce içeriğini incele, sürüm sabitle.

### Windows notu
PowerShell "betik çalıştırma devre dışı" hatası verirse (`higgsfield.ps1 cannot be loaded`):
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Sonra PowerShell'i kapatıp yeniden aç.

### Kullanışlı komutlar
```
higgsfield model list                                   # modeller
higgsfield model get veo3_1_lite                        # bir modelin parametreleri
higgsfield generate cost veo3_1_lite --prompt "..." --duration 6 --aspect_ratio 9:16 --generate_audio true --start-image kare.png
higgsfield generate create <model> ... --wait           # üret ve bekle
higgsfield generate list                                # son işler (çift gönderimi önlemek için)
higgsfield generate wait <job_id>                       # bir işi bekle
```

---

## Sorun giderme

| Belirti | Çözüm |
|---|---|
| `/mcp` listesinde higgsfield yok | Repo kökünde mi açtın? `.mcp.json` orada. Değilse Yol 1-B ile ekle. |
| "Needs authentication" | `/mcp` → higgsfield → Authenticate. Tarayıcıda girişi tamamla. |
| Tarayıcı açılmıyor | Gösterilen bağlantıyı elle kopyalayıp tarayıcıya yapıştır. |
| `higgsfield` komutu bulunamadı | Node.js kurulu mu? `npm i -g @higgsfield/cli` sonrası terminali yeniden aç. |
| Kredi yetersiz | Higgsfield hesabından plan/kredi durumuna bak. Claude üretimden önce maliyeti gösterir. |
