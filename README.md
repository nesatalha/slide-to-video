# Slayttan Videoya

PowerPoint sunumunu seslendirilmiş bir MP4 videoya çeviren, bilgisayarınızda çalışan bir web uygulaması. Her slaytın konuşmacı notları ElevenLabs ile seslendirilir.

## Gereksinimler
- **Python 3.10 veya üstü**: https://www.python.org/downloads/ (Windows'ta kurulumda "Add python.exe to PATH" seçeneğini işaretleyin.)
- Slaytları görüntüye çevirmek için şunlardan biri:
  - **macOS:** **Keynote** (App Store'da ücretsiz). Slaytlar orijinal görünümleriyle dışa aktarılır. Keynote yoksa LibreOffice da kullanılabilir.
  - **Windows / Linux:** **LibreOffice** (ücretsiz): https://www.libreoffice.org/download/. Linux'ta paket yöneticisinden de kurabilirsiniz (örneğin `sudo apt install libreoffice-impress`).
- Bir **ElevenLabs API anahtarı**. Anahtarı ElevenLabs'te Profile > API Keys bölümünden alabilirsiniz. Anahtarın *Text to Speech* ve *Voices (read)* izinleri olmalı.

| İşletim sistemi | Slayt dışa aktarımı | Başlatma |
|---|---|---|
| macOS | Keynote, yoksa LibreOffice | `./run.sh` |
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

İlk çalıştırmada gerekli paketler kurulur ve tarayıcıda **http://127.0.0.1:8765** açılır. Uygulamaya yalnızca sizin bilgisayarınızdan erişilebilir.

macOS'ta Keynote kullanılıyorsa ilk videoda macOS, uygulamanın Keynote'u kontrol etmesi için izin isteyecek. **İzin Ver**'e tıklayın. İzni kaçırırsanız Sistem Ayarları > Gizlilik ve Güvenlik > Otomasyon bölümünden açabilirsiniz.

Keynote yüklü bir Mac'te LibreOffice'i zorlamak için: `SLIDE2VIDEO_RENDERER=libreoffice ./run.sh`. LibreOffice standart bir yerde değilse `soffice` komutunun PATH'te olduğundan emin olun.

## Kullanım
1. **Slaytlar:** `.pptx` dosyasını yükleyin. Konuşmacı notları seslendirme metni olur. Gizli slaytlar atlanır. Notu olmayan slaytlar seslendirme olmadan 3 saniye gösterilir. Notlara `[calmly]`, `[short pause]` gibi ses etiketleri yazabilirsiniz.
2. **API anahtarı:** anahtar yalnızca çalışan işlem süresince bellekte tutulur, diske yazılmaz. İsterseniz tarayıcınızda hatırlanabilir. Anahtarı girdiğinizde kalan krediniz de gösterilir.
3. **Hız:** 0,8× ile 2× arası. Ses hızlanır ama tonu değişmez.
4. **Çözünürlük:** 480p, 720p veya 1080p.
5. **Ses:** varsayılan ses Fatih Yıldırım'dır (`7VqWGAWwo2HMrylfKrcm`). "Seslerimi yükle" düğmesi hesabınızdaki sesleri listeler. Başka bir ses kimliği de yapıştırabilirsiniz. Varsayılan ses kendi hesabınızda yoksa listeden başka bir ses seçin.

Gelişmiş bölümünde model (varsayılan `eleven_v4`) ve dil (varsayılan Türkçe) değiştirilebilir.

## Kredi
Üretilen seslendirmeler `data/tts-cache` klasöründe saklanır. Aynı sunumu farklı hız veya çözünürlükte yeniden oluşturmak kredi harcamaz. Kredi biterse kredi yükleyip tekrar başlatın; yalnızca eksik slaytlar ücretlendirilir.

Uygulamanın ürettiği her şey `data/` klasöründedir. Yer açmak için bu klasörü silebilirsiniz.

## Nasıl çalışır
- Keynote (yoksa LibreOffice, `soffice --headless --convert-to pdf`) sunumu PDF olarak dışa aktarır, PyMuPDF her sayfayı seçilen çözünürlükte görüntüye çevirir.
- Her slayt için tek bir ElevenLabs isteği yapılır. Model yalnızca Text-to-Dialogue ile sunuluyorsa uygulama otomatik olarak ona geçer.
- Ses seviyesi -16 LUFS'a normalize edilir. Her slaytın başına 200 ms, sonuna en az 600 ms sessizlik eklenir ve klip uzunluğu kare sayısıyla birebir eşlenir.
- Klipler birleştirilir. Her slayt için bir bölüm (chapter) içeren tek bir MP4 oluşur ve dosyanın tamamı bir kez çözülerek kontrol edilir.

Çevrimdışı test için `SLIDE2VIDEO_FAKE_TTS=1 ./run.sh` komutu ElevenLabs yerine macOS'un `say` sesini kullanır (yalnızca macOS).
