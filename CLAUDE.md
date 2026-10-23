# Doğukan Short Drama — Claude talimatı

Bu repo, Türkçe AI short-drama (dikey mikro dizi, 9:16, bölüm başı ~60 sn) üretmek için bir şablondur.
Üretim Higgsfield MCP üzerinden yapılır. Kurgu, ses ve altyazı yerel Python betikleriyle yapılır.

Kullanıcıyla **Türkçe**, kısa ve sade konuş. Kullanıcı teknik olmayabilir: komutları sen çalıştır,
kod bloğunda göster, ne yaptığını tek cümleyle söyle.

## Kullanıcı ilk kez geldiyse

- Kullanıcı "kur", "kurulum", "başla", "install" derse **ya da** ortam hazır değilse (`.venv` yok ya da
  Higgsfield MCP araçları listende yok) `/kur` akışını uygula: `.claude/commands/kur.md`.
- Kurulum bittiyse ve "dizi yapalım", "ilk dizi" denirse `/ilk-dizi` akışını uygula: `.claude/commands/ilk-dizi.md`.
- Kullanıcı teknik bilmiyor varsay. Komutları sen çalıştır. Onun yapması gerekenleri (tarayıcıda giriş,
  Claude'u yeniden açmak) adım adım söyle. Sistem yazılımı (winget/brew/pip) kurmadan önce onay al.
- Değişmez kural aynen geçerli: **her ücretli üretim ve yeniden deneme öncesi maliyet gösterilir, onay alınır.**
- Windows'ta önce aşağıdaki "Windows tuzakları"na bak.

## İlk açılışta (her yeni oturumda bir kez)

1. Ortamı kontrol et:
   ```
   py scripts/doctor.py              # Windows
   python3 scripts/doctor.py         # Mac
   ```
   Eksik varsa (Python 3.10+, ffmpeg, paketler) kullanıcıya kurulum adımını göster: `README.md` → Elle kurulum (ya da `/kur` akışı).
   Paketler için (önerilen: önce sanal ortam):
   ```
   # Windows (activate gerekmez; execution policy engeline takılmaz)
   py -m venv .venv
   .venv/Scripts/python.exe -m pip install -r requirements.txt

   # Mac
   python3 -m venv .venv
   source .venv/bin/activate
   python3 -m pip install -r requirements.txt
   ```
   Sanal ortam etkinken iki platformda da `python` komutu o ortamın Python'unu çalıştırır.
   Sen komut çalıştırırken activate etme; doğrudan `.venv/Scripts/python.exe` (Windows) ya da
   `.venv/bin/python` (Mac) kullan.
2. Higgsfield MCP bağlı mı bak: Higgsfield araçları listende var mı? Yoksa kullanıcıyı
   `docs/05-higgsfield-mcp-kurulum.md` adımlarına yönlendir. Bağlıysa hesap/kredi bilgisini MCP'den oku
   (varsa) ve kalan krediyi söyle.
3. Kullanıcıya sor: "Bir fikrin var mı, yoksa fikir bankasından önereyim mi?" Sonra `short-drama-tr`
   skill'inin akışını izle.

## Değişmez kurallar

1. **Her ücretli üretimden önce maliyeti göster ve onay al.** MCP'nin maliyet aracı varsa onu kullan;
   yoksa `higgsfield generate cost <model> ...`. Onaysız gönderim yok. Yeniden üretim ve filtre reti
   sonrası yapılan deneme de ayrı maliyet onayı ister.
2. **Toplam tavan belirle** (bölüm başında, kullanıcıyla). Harcamayı `uretim/<seri>/harcama.txt`'ye yaz.
   Tavanı aşacaksan dur ve sor.
3. **Çift gönderim yapma.** Zaman aşımında yeniden göndermeden önce iş listesine bak.
4. **Eşzamanlı iş sınırı 4.** Aynı anda en fazla 4 Higgsfield işi.
5. **Gerçek kişiye benzeyen yüz kullanma.** Ünlü, tanıdık, kamuya mal olmuş kişi yok.
6. **TikTok'ta AI etiketi açık**, açıklamada "Kurgudur, AI ile üretildi."
7. **Kâr ya da gelir vaadi yazma.** Hiçbir metinde, hiçbir öneride.
8. Platform güvenli içerik: çıplaklık, cinsellik, kanlı şiddet yok; herkes yetişkin.
9. Sonuçları `result_url` alanından indir. Dönen ilk URL giriş görseli olabilir.
10. Fiyatlar 22 Eki 2026 tarihlidir; canlı maliyet aracına güven.

## İş akışı

```
fikir (6 ölçüt) → SEZON.md → senaryo.md → cekim-listesi.md
→ varlıklar (yüz, kıyafet, karakter sayfası, mekân) → klip promptları (promptlar.md)
→ maliyet + onay → üretim (≤4 eşzamanlı) → kurgu, ses, altyazı → kontrol kareleri → yayın metni
```
Her adımın sonunda kullanıcıya göster, onay al, sonra devam et.
Yöntemin tamamı: `.claude/skills/short-drama-tr/SKILL.md`.

## Dosya haritası

| Yol | Ne işe yarar |
|---|---|
| `.claude/commands/` | `/kur` (kurulum sihirbazı) ve `/ilk-dizi` (rehberli ilk dizi) akışları |
| `.claude/skills/short-drama-tr/` | Yöntemin çekirdeği (skill). `references/` altında ayrıntılar |
| `templates/` | Doldurulacak şablonlar: SEZON, BOLUM-SENARYO, CEKIM-LISTESI, KARAKTER, MEKAN, prompt-kaliplari |
| `examples/cifte-davetiye/` | Tam örnek: sezon planı, 1. bölüm senaryosu, kullanılan promptlar, kareler |
| `docs/01-yontem.md` | Yöntemin insan için anlatımı |
| `docs/02-maliyet.md` | Fiyatlar ve 3 bütçe tarifi |
| `docs/03-dersler.md` | Gerçek üretimden dersler (filtre, ses, kare zinciri) |
| `docs/04-tiktok-yayin.md` | Yayın metni ve kuralları |
| `docs/05-higgsfield-mcp-kurulum.md` | Higgsfield MCP ve CLI kurulumu |
| `scripts/` | `doctor.py`, `kare.py`, `zincir.py`, `sfx.py`, `altyazi.py`, `kurgu.py`, `ornek_klip.py` (örnek kurgu için test klipleri), `ffmpeg_yol.py` (ortak modül). Kullanım: `scripts/README.md` ve `--help` |
| `examples/kurgu-ornek.json` | `scripts/kurgu.py` için örnek kurgu dosyası (çekim listesinin makine hâli) |
| `uretim/` | Kullanıcının üretimleri (git'e girmez) |

## Üretim klasörü düzeni

Her seri için:
```
uretim/<seri-adi>/
  SEZON.md
  harcama.txt
  varliklar/                # @Ad görselleri, karakter ve mekân kartları
  bolumler/
    bolum-01/
      senaryo.md            # templates/BOLUM-SENARYO.md'den
      cekim-listesi.md      # templates/CEKIM-LISTESI.md'den
      promptlar.md          # klip promptları
      kareler/              # başlangıç ve kontrol kareleri (scripts/kare.py)
      klipler/              # indirilen klipler: 01.mp4, 02.mp4 …
      kurgu.json            # scripts/kurgu.py girdisi; "klip": "klipler/01.mp4", "cikti": "bolum-01.mp4"
      bolum-01.mp4          # son kurgu (kurgu.json'daki "cikti")
      bolum-01.srt
      .kurgu-tmp/           # kurgu.py ara dosyaları; --temiz yalnız bunu siler
```
Kurgu: `python scripts/kurgu.py uretim/<seri-adi>/bolumler/bolum-01/kurgu.json --temiz`.
`kurgu.json` içindeki göreli yollar kendi klasörüne göredir (örnek: `examples/kurgu-ornek.json`).
Şablonları `templates/`'ten kopyala, doldur. `examples/` klasörünü değiştirme.

## Platform notları

- Windows'ta yollar için `/` kullan ya da tırnak içine al. Windows'ta `py`, Mac'te `python3` kullan
  (sanal ortam etkinse ikisinde de `python`).
- Uzun üretimlerde işleri bekle (MCP bekleme aracı ya da `higgsfield generate wait <id>`); döngüde sürekli yeniden gönderme.

### Windows tuzakları

- **PATH yenilenmez:** `winget` ile Python, ffmpeg ya da Git kurduktan sonra komut "bulunamadı" diyebilir.
  Kullanıcıdan terminali ya da Claude Code'u kapatıp aynı klasörde yeniden açmasını iste.
- **`py` komutu:** Windows'ta `python` yerine `py` kullan. `python` yazınca Microsoft Store açılıyorsa bu,
  Store kısayoludur; `py` ile devam et. `py --version` 3.10+ göstermeli.
- **Execution policy:** PowerShell'de `.venv\Scripts\Activate.ps1` "betik çalıştırma devre dışı" hatası verebilir.
  Activate etme; `.venv\Scripts\python.exe` (Git Bash'te `.venv/Scripts/python.exe`) ile doğrudan çalıştır.
- **Türkçe karakterli kullanıcı klasörü:** Kullanıcı klasörünün adında ğ, ü, ş, ı, ö, ç ya da boşluk varsa
  ffmpeg altyazı filtresi ve bazı paketler sorun çıkarabilir. Repoyu kısa, ASCII bir yola klonla (ör. `C:\drama\`).
  Konsolda bozuk karakter görürsen `PYTHONUTF8=1` ortam değişkeniyle çalıştır.
- Claude Code Windows'ta komutları çoğunlukla Git Bash ile çalıştırır: yollarda `/` kullan.
