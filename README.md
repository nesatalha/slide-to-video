# Slayttan Videoya

PowerPoint sunumunu seslendirilmiş bir MP4 videoya çeviren, bilgisayarınızda çalışan bir web uygulaması. Her slaytın konuşmacı notları ElevenLabs ile seslendirilir.

## Gereksinimler
- **macOS** ve **Keynote**. Keynote, App Store'da ücretsizdir; slaytlar orijinal görünümleriyle Keynote üzerinden dışa aktarılır.
- **Python 3.10 veya üstü**
- Bir **ElevenLabs API anahtarı**. Anahtarı ElevenLabs'te Profile > API Keys bölümünden alabilirsiniz. Anahtarın *Text to Speech* ve *Voices (read)* izinleri olmalı.

## Çalıştırma
```bash
git clone <repo-adresi>
cd slide-to-video
./run.sh
```
İlk çalıştırmada gerekli paketler kurulur ve tarayıcıda **http://127.0.0.1:8765** açılır. Uygulamaya yalnızca sizin bilgisayarınızdan erişilebilir.

İlk videoda macOS, uygulamanın Keynote'u kontrol etmesi için izin isteyecek. **İzin Ver**'e tıklayın. İzni kaçırırsanız Sistem Ayarları > Gizlilik ve Güvenlik > Otomasyon bölümünden açabilirsiniz.

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
- Keynote sunumu PDF olarak dışa aktarır, PyMuPDF her sayfayı seçilen çözünürlükte görüntüye çevirir.
- Her slayt için tek bir ElevenLabs isteği yapılır. Model yalnızca Text-to-Dialogue ile sunuluyorsa uygulama otomatik olarak ona geçer.
- Ses seviyesi -16 LUFS'a normalize edilir. Her slaytın başına 200 ms, sonuna en az 600 ms sessizlik eklenir ve klip uzunluğu kare sayısıyla birebir eşlenir.
- Klipler birleştirilir. Her slayt için bir bölüm (chapter) içeren tek bir MP4 oluşur ve dosyanın tamamı bir kez çözülerek kontrol edilir.

Çevrimdışı test için `SLIDE2VIDEO_FAKE_TTS=1 ./run.sh` komutu ElevenLabs yerine macOS'un `say` sesini kullanır.
