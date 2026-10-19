# Slayttan Videoya: teknik belge

Kurulum ve kullanım için sade anlatım: [README.md](README.md). Bu belge kaynak koddan çalıştırma, paketleme ve iç işleyiş içindir.

PowerPoint sunumunu seslendirilmiş bir MP4 videoya çeviren, bilgisayarınızda çalışan bir web uygulaması. Her slaytın konuşmacı notları ElevenLabs ile seslendirilir.

## Gereksinimler
- **Python 3.10 veya üstü**: https://www.python.org/downloads/ (Windows'ta kurulumda "Add python.exe to PATH" seçeneğini işaretleyin.)
- Slaytları görüntüye çevirmek için şunlardan biri:
  - **macOS:** **Keynote** (App Store'da ücretsiz). Slaytlar orijinal görünümleriyle dışa aktarılır. Keynote yoksa LibreOffice da kullanılabilir.
  - **Windows / Linux:** **LibreOffice** (ücretsiz): https://www.libreoffice.org/download/. Linux'ta paket yöneticisinden de kurabilirsiniz (örneğin `sudo apt install libreoffice-impress`).
- Bir **ElevenLabs API anahtarı**. Anahtarı ElevenLabs'te Profile > API Keys bölümünden alabilirsiniz. Anahtarın *Text to Speech* ve *Voices (read)* izinleri olmalı.

| İşletim sistemi | Slayt dışa aktarımı | Başlatma |
|---|---|---|
| macOS | Keynote, yoksa LibreOffice | `./run.sh` veya `run.command` (çift tıklayın) |
| Windows | LibreOffice | `run.bat` (çift tıklayın) |
| Linux | LibreOffice | `./run.sh` |

LibreOffice slaytları kendi motoruyla çizer. Yazı tipleri ve bazı efektler PowerPoint'tekinden biraz farklı görünebilir. Sunumdaki yazı tipleri bilgisayarınızda yüklü değilse benzerleriyle değiştirilir.

## Çalıştırma
**macOS / Linux:**
```bash
git clone <repo-adresi>
cd slide-to-video
./run.sh
```
**Windows:** depoyu klonlayın (veya ZIP olarak indirip açın) ve klasördeki `run.bat` dosyasına çift tıklayın.

**macOS (Finder'dan):** `run.command` dosyasına çift tıklayın. Terminal penceresi açılır ve `run.sh` çalışır. İlk seferde Gatekeeper uyarı verirse dosyaya sağ tıklayıp **Aç**'ı seçin.

İlk çalıştırmada gerekli paketler kurulur ve tarayıcıda **http://127.0.0.1:8765** açılır. Uygulamaya yalnızca sizin bilgisayarınızdan erişilebilir.

macOS'ta Keynote kullanılıyorsa ilk videoda macOS, uygulamanın Keynote'u kontrol etmesi için izin isteyecek. **İzin Ver**'e tıklayın. İzni kaçırırsanız Sistem Ayarları > Gizlilik ve Güvenlik > Otomasyon bölümünden açabilirsiniz.

Keynote yüklü bir Mac'te LibreOffice'i zorlamak için: `SLIDE2VIDEO_RENDERER=libreoffice ./run.sh`. LibreOffice standart bir yerde değilse `soffice` komutunun PATH'te olduğundan emin olun.

## Kullanım
1. **Slaytlar:** `.pptx` dosyasını yükleyin. Konuşmacı notları seslendirme metni olur. Gizli slaytlar atlanır. Notu olmayan slaytlar seslendirme olmadan 3 saniye gösterilir. Notlara `[calmly]`, `[short pause]` gibi ses etiketleri yazabilirsiniz.
2. **API anahtarı:** anahtar yalnızca çalışan işlem süresince bellekte tutulur, diske yazılmaz. İsterseniz tarayıcınızda hatırlanabilir. Anahtarı girdiğinizde kalan krediniz de gösterilir.
3. **Hız:** 0,8× ile 2× arası. Ses hızlanır ama tonu değişmez.
4. **Çözünürlük:** 480p, 720p veya 1080p.
5. **Slayt geçişi:** *Kesme* (slayt anında değişir) veya *Yumuşak geçiş* (slaytlar 0,4 saniyede birbirine karışır, konuşma geçiş bitince başlar).
6. **Ses:** varsayılan ses Fatih Yıldırım'dır (`7VqWGAWwo2HMrylfKrcm`). "Seslerimi yükle" düğmesi hesabınızdaki sesleri listeler. Başka bir ses kimliği de yapıştırabilirsiniz. Varsayılan ses kendi hesabınızda yoksa listeden başka bir ses seçin.

Gelişmiş bölümünde model (varsayılan `eleven_v4`) ve dil (varsayılan Türkçe) değiştirilebilir.

## İfade etiketleri
"Notlara ifade etiketleri ekle" seçeneği notların arasına ElevenLabs ses etiketleri yerleştirir: `[short pause]`, `[slowly]`, `[calmly]`, `[warmly]`, `[thoughtful]`, `[inhales]`, `[exhales]` gibi. Böylece anlatım duraklamalı, vurgulu ve daha doğal olur. Not metninin kendisi hiçbir zaman değişmez; yalnızca etiketler eklenir.

- **OpenAI veya Anthropic API anahtarı girerseniz** etiketleri yapay zekâ yerleştirir. `sk-ant-` ile başlayan anahtarlar Claude (`claude-opus-5-5`), diğerleri OpenAI (`gpt-5.6`, yoksa `gpt-5.5`) ile kullanılır. Bu, o hesaptan küçük bir ücret düşer. Anahtar diske yazılmaz.
- **Anahtar yoksa** etiketler kural tabanlı eklenir: liste maddelerinden önce kısa duraklama, "temel kural şudur" gibi önemli cümlelerde yavaşlama, soru cümlelerinde düşünceli ton, açılış ve kapanışta sıcak ton. Ücretsizdir ve internet gerektirmez. Kural tabanlı ekleme nefes etiketleri kullanmaz.
- Model bir slaytta metni değiştirirse ya da yanıt veremezse, o slayt için otomatik olarak kurallar kullanılır. İçinde zaten etiket bulunan notlara dokunulmaz.
- **Etiketleri oluştur ve göster** düğmesiyle sonucu video oluşturmadan önce görebilir, her slaytın metnini elle düzenleyebilirsiniz. Önizleme yapmadan videoyu başlatırsanız etiketler video sırasında eklenir.

Etiketli metin yeni bir metin sayıldığı için ilk seferde yeniden seslendirilir ve etiket karakterleri de krediye dahil olabilir. OpenAI modelini değiştirmek için `SLIDE2VIDEO_OPENAI_MODEL=<model> ./run.sh` kullanabilirsiniz.

## Kredi
Üretilen seslendirmeler `data/tts-cache` klasöründe saklanır. Aynı sunumu farklı hız veya çözünürlükte yeniden oluşturmak kredi harcamaz. Kredi biterse kredi yükleyip tekrar başlatın; yalnızca eksik slaytlar ücretlendirilir.

Uygulamanın ürettiği her şey `data/` klasöründedir. Yer açmak için bu klasörü silebilirsiniz. Paketlenmiş uygulamada (aşağıya bakın) bu klasör kullanıcı klasöründedir; `SLIDE2VIDEO_DATA` ortam değişkeniyle her iki durumda da başka bir yer seçilebilir.

## Nasıl çalışır
- Keynote (yoksa LibreOffice, `soffice --headless --convert-to pdf`) sunumu PDF olarak dışa aktarır, PyMuPDF her sayfayı seçilen çözünürlükte görüntüye çevirir.
- İsteğe bağlı olarak notlara ifade etiketleri eklenir (yapay zekâ veya kurallarla).
- Her slayt için tek bir ElevenLabs isteği yapılır. Model yalnızca Text-to-Dialogue ile sunuluyorsa uygulama otomatik olarak ona geçer.
- Ses seviyesi -16 LUFS'a normalize edilir. Her slaytın başına 200 ms (yumuşak geçişte 450 ms), sonuna en az 600 ms sessizlik eklenir ve klip uzunluğu kare sayısıyla birebir eşlenir.
- Klipler birleştirilir. Her slayt için bir bölüm (chapter) içeren tek bir MP4 oluşur ve dosyanın tamamı bir kez çözülerek kontrol edilir.

Çevrimdışı test için `SLIDE2VIDEO_FAKE_TTS=1 ./run.sh` komutu ElevenLabs yerine macOS'un `say` sesini kullanır (yalnızca macOS).

## Paketlenmiş uygulama (Python gerektirmez)
Teknik olmayan kullanıcılar için Python, bağımlılıklar, `static/` ve ffmpeg (imageio-ffmpeg'in ikili dosyası) PyInstaller ile tek klasörlük bir pakete konur. Slaytları görüntüye çevirmek için Keynote veya LibreOffice yine bilgisayarda yüklü olmalıdır; paket bunları içermez.

| Platform | Paket | İçerik |
|---|---|---|
| Windows | `SlayttanVideoya-windows-x64.zip` | `SlayttanVideoya/SlayttanVideoya.exe` ve `_internal/` |
| macOS Apple Silicon | `SlayttanVideoya-macos-arm64.zip` | `Slayttan Videoya.app` |
| macOS Intel | `SlayttanVideoya-macos-x64.zip` | `Slayttan Videoya.app` |

Paketin giriş noktası `launcher.py`'dır (`app.py` değil):
- Veriyi (`jobs/`, `tts-cache/`) kullanıcının yazabildiği bir klasöre koyar: Windows'ta `%LOCALAPPDATA%\SlayttanVideoya`, macOS'ta `~/Library/Application Support/SlayttanVideoya`, Linux'ta `~/.local/share/SlayttanVideoya`. Bunu `SLIDE2VIDEO_DATA` ortam değişkeni ile `app.py`'a iletir.
- Sunucuyu `127.0.0.1:8765`'te başlatır ve tarayıcıyı açar. Port zaten bu uygulama tarafından kullanılıyorsa yalnızca tarayıcıyı açıp çıkar; başka bir program kullanıyorsa kullanıcıya bir hata mesajı gösterir.
- **Windows:** konsol penceresi açık kalır ve "İşiniz bitince bu pencereyi kapatın" der. Pencereyi kapatmak uygulamayı kapatır.
- **macOS:** `.app` pencere göstermez. Bunun yerine `osascript` ile "Tarayıcıda aç / Kapat" düğmeli bir iletişim kutusu açılır; **Kapat** sunucuyu durdurur. Standart çıktı olmadığı için günlük `log.txt` dosyasına (veri klasöründe) yazılır.
- `Info.plist` içinde `NSAppleEventsUsageDescription` bulunur; Keynote otomasyon izni istendiğinde bu metin gösterilir.

Paketler imzasız (macOS'ta yalnızca ad-hoc imzalı) olduğu için Windows SmartScreen ve macOS Gatekeeper ilk açılışta uyarı verir. Kullanıcıya yönelik adımlar README'dedir.

### Yerelde derleme
```bash
python3 -m venv .venv && .venv/bin/pip install -r packaging/requirements-build.txt
.venv/bin/python packaging/build.py 0.1.0
.venv/bin/python packaging/smoke.py "dist/Slayttan Videoya.app/Contents/MacOS/SlayttanVideoya"
```
Windows'ta: `python packaging\build.py 0.1.0` ve `python packaging\smoke.py dist\SlayttanVideoya\SlayttanVideoya.exe`.

- `packaging/SlayttanVideoya.spec`: PyInstaller tanımı. `onnxruntime` ve `networkx` (PyMuPDF'nin OCR/yerleşim özellikleri için çektiği, uygulamanın kullanmadığı paketler) ve `tkinter` dışarıda bırakılır. Paket yaklaşık 165 MB, ZIP'i yaklaşık 80 MB'tır.
- `packaging/build.py`: PyInstaller'ı çalıştırır, `dist/` altında ZIP oluşturur. macOS'ta ZIP `ditto` ile yapılır, böylece paketin sembolik bağlantıları ve imzası korunur. Sürüm numarası ilk argümandan (veya `SLIDE2VIDEO_VERSION`) alınır.
- `packaging/smoke.py`: paketi geçici bir veri klasörüyle başlatır, sunucunun açılmasını bekler, küçük bir sunum yükler, notların okunduğunu ve verinin doğru klasöre yazıldığını kontrol eder.
- Paket, derlendiği işletim sistemi ve işlemci için çalışır; Windows paketi Windows'ta, Intel Mac paketi Intel bir Mac'te derlenmelidir.

### Sürüm yayınlama (GitHub Actions)
`.github/workflows/release.yml` bir `v*` etiketi gönderildiğinde `windows-latest`, `macos-latest` (Apple Silicon) ve `macos-15-intel` üzerinde paketi derler, smoke testi çalıştırır ve üç ZIP'i aynı adlı GitHub Release'e ekler (Release yoksa oluşturur, varsa dosyaları değiştirir).
```bash
git tag v0.1.0
git push origin v0.1.0
```
İş akışı Actions sekmesinden elle de çalıştırılabilir (*Run workflow*); bu durumda Release oluşturulmaz, ZIP'ler çalıştırmanın *Artifacts* bölümünden indirilir.

## Planlanan
- Windows'ta LibreOffice yerine PowerPoint ile slayt dışa aktarma ve `.pptx` ile birlikte PDF yükleme (görüntüler PDF'ten, notlar `.pptx`'ten).
