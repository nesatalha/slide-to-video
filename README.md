# Slayttan Videoya

> Teknik ayrıntılar (kaynak koddan çalıştırma, paketleme, iç işleyiş) için: [TEKNIK.md](TEKNIK.md)

Slayttan Videoya, bir PowerPoint sunumunu sesli anlatımlı bir videoya çevirir. Her slaytın altına yazdığınız konuşmacı notları bir yapay zekâ sesiyle okunur ve slaytlar bu anlatımla birlikte bir video dosyasına (MP4) dönüşür.

Program sizin bilgisayarınızda çalışır. Sunumunuz yalnızca seslendirme için gereken notlar dışında hiçbir yere gönderilmez.

---

## Windows'a kurulum

Slaytları görüntüye çevirmek için bilgisayarınızda **PowerPoint** (Microsoft 365 veya Office) yüklü olmalıdır. Ayrıca bir şey kurmanız gerekmez. PowerPoint'i bu bilgisayarda hiç açmadıysanız bir kez açıp kapatın.

1. Bu sayfanın sağ tarafındaki **Releases** bölümüne tıklayın ve en üstteki sürümü açın.
2. **SlayttanVideoya-windows-x64.zip** dosyasına tıklayıp indirin.
3. İndirilenler klasöründe bu dosyaya sağ tıklayın, **Tümünü ayıkla...**'yı seçin ve **Ayıkla**'ya basın. Masaüstü veya Belgeler gibi kalıcı bir yer seçebilirsiniz.
4. Açılan **SlayttanVideoya** klasöründeki **SlayttanVideoya.exe** dosyasına çift tıklayın. (Yanındaki *_internal* klasörüne dokunmayın; programın parçasıdır.)
5. İlk açılışta mavi bir "Windows bilgisayarınızı korudu" penceresi çıkabilir. Bu, programın tanınmış bir yayıncıdan gelmediği anlamına gelir. **Ek bilgi**'ye, ardından **Yine de çalıştır**'a tıklayın. Bunu yalnızca bir kez yapmanız gerekir.
6. Siyah bir pencere açılır ve birkaç saniye içinde program tarayıcınızda görünür. **Siyah pencere program çalıştığı sürece açık kalmalıdır.** İşiniz bitince bu pencereyi sağ üstteki **X** ile kapatın.

<!-- Ekran görüntüsü: SmartScreen penceresi, "Ek bilgi" ve "Yine de çalıştır" işaretli -->
<!-- Ekran görüntüsü: siyah pencere ve tarayıcıda açılan program -->

Programı sonraki seferlerde açmak için yine **SlayttanVideoya.exe**'ye çift tıklamanız yeterlidir. Kolaylık için dosyaya sağ tıklayıp **Gönder > Masaüstü (kısayol oluştur)** diyebilirsiniz.

## Mac'e kurulum

1. Bu sayfanın sağ tarafındaki **Releases** bölümüne tıklayın ve en üstteki sürümü açın.
2. Mac'inize uygun dosyayı indirin:
   - Apple M1, M2, M3 veya daha yeni bir Mac için: **SlayttanVideoya-macos-arm64.zip**
   - Intel işlemcili eski bir Mac için: **SlayttanVideoya-macos-x64.zip**

   Hangisi olduğunu bilmiyorsanız ekranın sol üstündeki  menüsünden **Bu Mac Hakkında**'ya bakın: "Çip: Apple M…" yazıyorsa ilkini, "İşlemci: Intel" yazıyorsa ikincisini indirin.
3. İndirilenler klasöründe ZIP dosyasına çift tıklayın. **Slayttan Videoya** uygulaması çıkar. Bu uygulamayı **Uygulamalar** klasörüne sürükleyin.
4. Uygulamaya **sağ tıklayın** (veya Control tuşuna basılı tutarak tıklayın) ve **Aç**'ı seçin. Çıkan pencerede yine **Aç**'a basın.
5. Mac "açılamıyor" deyip yalnızca **Bitti** ve **Çöp Sepetine Taşı** düğmelerini gösterirse **Bitti**'ye basın. Sonra  menüsü > **Sistem Ayarları** > **Gizlilik ve Güvenlik** bölümüne gidin, sayfanın altındaki "Slayttan Videoya engellendi" satırında **Yine de Aç**'a tıklayın ve parolanızı girin. Bunu yalnızca bir kez yapmanız gerekir.
6. Program tarayıcınızda açılır ve ekranda küçük bir "Slayttan Videoya çalışıyor" penceresi görünür. İşiniz bitince bu penceredeki **Kapat** düğmesine basın. Tarayıcıyı yanlışlıkla kapatırsanız **Tarayıcıda aç** ile geri getirebilirsiniz.

<!-- Ekran görüntüsü: sağ tık > Aç menüsü -->
<!-- Ekran görüntüsü: Gizlilik ve Güvenlik sayfasında "Yine de Aç" düğmesi -->
<!-- Ekran görüntüsü: "Slayttan Videoya çalışıyor" penceresi -->

Mac'te slaytlar **Keynote** ile görüntüye çevrilir. Keynote yüklü değilse App Store'dan ücretsiz indirebilirsiniz ya da sunumun PDF'ini yükleyebilirsiniz (bkz. "PowerPoint veya Keynote yoksa"). İlk videoda Mac, programın Keynote'u kullanması için izin ister; **İzin Ver**'e tıklayın.

---

## ElevenLabs anahtarı nasıl alınır

Seslendirmeyi ElevenLabs adlı bir hizmet yapar. Programın bu hizmeti sizin adınıza kullanabilmesi için bir "API anahtarı" gerekir. Anahtar, hesabınıza ait uzun bir şifre gibidir.

1. **https://elevenlabs.io** adresine gidin ve bir hesap açın (veya giriş yapın).
2. Seslendirme kredi harcar. Ücretsiz hesabın kredisi kısa bir sunum için yetebilir; daha fazlası için **Subscription** (Abonelik) sayfasından bir paket seçin.
3. Sol alttaki adınıza tıklayın ve **API Keys** bölümünü açın.
4. **Create API Key** (Anahtar oluştur) düğmesine basın. Anahtara "Slayttan Videoya" gibi bir ad verin.
5. İzinler listesinde **Text to Speech** için erişimi açın ve **Voices** için en az okuma (*Read*) izni verin. Sonra **Create**'e basın.
6. Ekranda görünen anahtarı kopyalayın ve güvenli bir yere (örneğin parola yöneticinize) kaydedin. **Bu anahtar bir daha gösterilmez.** Kimseyle paylaşmayın.

<!-- Ekran görüntüsü: ElevenLabs API Keys sayfası ve izinler -->

## Kısaca kullanım

1. Programı açın (yukarıdaki kurulum adımlarının son adımı).
2. **Slaytlar** bölümünde PowerPoint dosyanızı (**.pptx**) seçin. Program her slaytı ve notunu listeler. Notlar yalnızca seslendirilir, videoda yazı olarak görünmez.
3. **ElevenLabs** bölümüne anahtarınızı yapıştırın. Kalan krediniz hemen altında görünür. **Bu tarayıcıda hatırla** kutusunu işaretlerseniz anahtarı her seferinde yeniden girmeniz gerekmez; anahtar bilgisayarınızda başka hiçbir yere yazılmaz.
4. **Video** bölümünde konuşma hızını, çözünürlüğü (video kalitesi: 480p, 720p veya 1080p) ve slayt geçişini seçin. Emin değilseniz varsayılanları bırakın.
5. **Videoyu oluştur**'a basın. İlerleme çubuğu dolarken programı kapatmayın.
6. Video hazır olunca tarayıcıda izleyebilir ve **MP4 indir** ile bilgisayarınıza kaydedebilirsiniz.

<!-- Ekran görüntüsü: programın ana ekranı -->

### PowerPoint veya Keynote yoksa
Sunumu PowerPoint'i olan bir bilgisayarda **Dosya > Farklı Kaydet** ile **PDF** olarak kaydedin. Programa **.pptx** dosyasını ve bu **PDF**'i birlikte sürükleyip bırakın (ya da önce .pptx'i yükleyip sonra **PDF ekle**'ye basın). Slayt görüntüleri PDF'ten, notlar .pptx'ten alınır. PDF'in aynı sunumdan kaydedilmiş olması gerekir.

Aynı sunumu farklı hızda veya kalitede yeniden oluşturmak ek kredi harcamaz; daha önce okunan notlar tekrar kullanılır.

## Konuşmacı notları nasıl anlatıma dönüşür

- PowerPoint'te her slaytın altında **"Notlar"** alanı bulunur (görmüyorsanız alt çubuktaki **Notlar** düğmesine basın). Bu alana slayt ekrandayken söylenmesini istediğiniz metni yazın.
- Program notları doğrudan **.pptx** dosyasından okur ve seslendirir. **Notlar videoda yazı olarak görünmez**; videoda yalnızca slaytın kendisi görünür ve notlar sesli olarak duyulur.
- Notu boş olan slayt, sessiz olarak 3 saniye gösterilir.
- PowerPoint'te **gizlenmiş** slaytlar videoya alınmaz.
- Notları noktalama işaretleriyle, normal cümleler halinde yazın. Kısaltmaları (ör. "KVKK") okunmasını istediğiniz gibi yazmanız daha doğal bir sonuç verir.
- İsterseniz **"Notlara ifade etiketleri ekle"** seçeneği anlatıma doğal duraklamalar ve vurgular ekler. Notlarınızın metni değişmez.

<!-- Ekran görüntüsü: PowerPoint'te notlar alanı -->

---

## Sorun giderme

**Program açılmıyor, "bağlantı noktası kullanılıyor" (port) diyor.**
Program büyük olasılıkla zaten açık. Tarayıcınızda **http://127.0.0.1:8765** adresini deneyin. Açılmazsa bilgisayarı yeniden başlatıp programı tekrar açın.

**Antivirüs programı dosyayı engelledi veya sildi.**
Program imzasız olduğu için bazı antivirüs programları onu yanlışlıkla şüpheli bulabilir. Dosyayı yalnızca bu sayfadaki **Releases** bölümünden indirdiyseniz antivirüs programınızın "karantina" bölümünden geri yükleyip izin verebilirsiniz. Şirket bilgisayarında bu işlemi bilgi işlem biriminiz yapabilir.

**"ElevenLabs isteği reddetti", "kota" veya "kredi" içeren bir hata aldım.**
ElevenLabs hesabınızdaki kredi bitmiştir. ElevenLabs'te **Subscription** sayfasından kredi ekleyin ve **Videoyu oluştur**'a yeniden basın. Daha önce seslendirilen slaytlar için tekrar kredi harcanmaz.

**"Anahtar geçersiz" veya "izin yok" hatası aldım.**
Anahtarı eksiksiz kopyaladığınızdan emin olun. Anahtarın **Text to Speech** ve **Voices** izinleri açık olmalıdır (bkz. "ElevenLabs anahtarı nasıl alınır").

**Slaytlar dışa aktarılamadı (görüntüye çevrilemedi) ya da "PDF gerekli" yazıyor.**
Windows'ta PowerPoint, Mac'te Keynote yüklü olmalıdır. PowerPoint açıksa ekranda bekleyen bir uyarı veya oturum açma penceresi olup olmadığına bakın, kapatıp tekrar deneyin. Olmuyorsa sunumu PDF olarak kaydedip .pptx ile birlikte yükleyin (bkz. "PowerPoint veya Keynote yoksa").

**"PDF'te ... sayfa var" hatası aldım.**
PDF başka bir sunumdan ya da sunumun eski bir halinden kaydedilmiş. Sunumu PowerPoint'te yeniden PDF olarak kaydedip tekrar yükleyin.

**Video yarıda kaldı.**
Program kapatıldıysa yeniden açın ve aynı sunumda **Videoyu oluştur**'a tekrar basın. Tamamlanan seslendirmeler yeniden kullanılır.
