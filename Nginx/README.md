# Nginx

## Mimari ve Temel Mantık

### Nginx Nedir?

En basit haliyle Nginx, sunucunun kapısında duran inanılmaz hızlı ve yetenekli bir karşılama görevlisi veya resepsiyonisttir.

Bir web sitesine veya uygulamaya tarayıcıdan istek geldiğinde, bu isteği ilk karşılayan Nginx'tir. Arka plandaki asıl uygulamanın (Node.js, Python, PHP vb.) gereksiz yere yorulmasını ve çökmesini engeller.

Yüksek performanslı bir web sunucusu, reverse proxy ve yük dengeleyicidir (load balancer).

Çıkış noktası ve asıl ünü, C10K problemini (tek bir sunucuda aynı anda 10.000 bağlantıyı idare edebilme) çözmesinden gelir.

### Nginx'ten Önce Ne Vardı?

**Apache HTTP Server:** 90'ların sonu ve 2000'lerin başında web sunucusu dünyasının en yaygın çözümlerinden biriydi. Apache'nin özellikle geleneksel prefork MPM (Multi-Processing Module) modeli, yüksek sayıda eşzamanlı bağlantıda her bağlantı için ayrı process kullanabilmesi nedeniyle ciddi kaynak tüketimine yol açabiliyordu. Daha sonra worker ve event gibi thread tabanlı MPM'ler geliştirilerek bu sorunların bir kısmı azaltıldı.

**C10K Problemi:** İnternetin büyümesiyle birlikte tek bir sunucunun aynı anda on binlerce bağlantıyı verimli şekilde yönetmesi önemli bir problem haline geldi. "C10K", tek bir makinede yaklaşık 10.000 eşzamanlı bağlantıyı yönetebilme problemini ifade eder. Sorun yalnızca bağlantı sayısı değil, bu bağlantıları yönetirken CPU, RAM ve işletim sistemi kaynaklarının verimli kullanılabilmesiydi.

**Nginx'in Doğuşu (2004):** Rus geliştirici Igor Sysoev tarafından geliştirilen Nginx, özellikle çok sayıda eşzamanlı bağlantıyı düşük kaynak tüketimiyle yönetebilmek amacıyla event-driven ve non-blocking bir mimari kullandı. Bu yaklaşım, yüksek eşzamanlı bağlantı sayısının geleneksel process/thread tabanlı yapılara göre daha verimli yönetilmesini sağladı ve Nginx'in yüksek performanslı web sunucuları arasında öne çıkmasına yardımcı oldu.

|Alternatif|Öne Çıkan Özelliği|Neden Tercih Edilir?|Nginx ile Temel Farkı|
|---|---|---|---|
|Apache|.htaccess desteği ve modüler yapı|Geleneksel paylaşımlı hostingler (cPanel vb.) için hala vazgeçilmezdir. Ayarların klasör bazında kolayca ezilmesine olanak tanır.|Nginx özellikle yüksek eşzamanlı bağlantı sayısı ve statik içerik sunumu gibi senaryolarda güçlü performans avantajları sağlayabilir. Apache ise kullandığı MPM modeline bağlı olarak process veya thread tabanlı çalışabilir; özellikle yüksek eşzamanlı bağlantılarda Nginx'in event-driven mimarisi kaynak kullanımı açısından avantaj sağlayabilir.|
|Caddy|Otomatik SSL ve minimal konfigürasyon|Yeni neslin favorisidir. Nginx'te manuel yapılan HTTPS/Sertifika ayarlarını otomatik halleder. Konfigürasyon dosyası Nginx'in onda biri kadardır.|Nginx'in HTTPS yapılandırması daha manuel ve ayrıntılıdır. Let's Encrypt sertifikalarının otomatik alınması ve yenilenmesi için Certbot veya başka bir ACME istemcisi gibi ek araçlar kullanılabilir. Caddy ise bu süreci yerleşik olarak otomatikleştirir.|
|Traefik|Konteyner (Docker/Kubernetes) dostu|Mikroservisler için biçilmiş kaftandır. Sisteme yeni bir Docker ayağa kalktığında Traefik bunu otomatik tanır, Nginx gibi ayar dosyasını manuel güncellemeye gerek kalmaz.|Nginx statik ayar dosyalarıyla çalışır, arkaya yeni bir uygulama eklendiğinde dosyayı düzenleyip Nginx'e "reload" atmak gerekir. Traefik ise arkadaki değişiklikleri anlık olarak algılayıp trafiği kesintisiz yönlendirir.|
|HAProxy|Saf Yük Dengeleme (Load Balancing)|Nginx gibi statik dosya (HTML/CSS) sunmaz, sadece trafiği dağıtmaya odaklanır.|Nginx web sunucusu işini de yapar, HAProxy yapmaz. Saf yük dengeleme algoritmalarında ve sunucu sağlık kontrollerinde (health checks) ücretsiz Nginx'ten çok daha yetenekli ve incedir.|
|Envoy|Bulut tabanlı (Cloud-native) mimari|Özellikle Kubernetes ortamlarında (Service Mesh) Nginx'in yerini almaya başlayan, mikroservisler arası iletişimi yöneten modern C++ tabanlı vekildir.|Nginx genellikle dışarıdan gelen isteği karşılayan ana kapı (Edge Proxy) olarak kullanılırken, Envoy daha çok sistemin içindeki onlarca uygulamanın kendi aralarındaki devasa veri trafiğini yönetmek için tercih edilir.|

### Event-Driven Mimari
Nginx'i standart haline getiren temel özellik, gelen bağlantıları ele alış biçimidir:

**Geleneksel Model (Thread-Based):** Bazı geleneksel web sunucusu mimarilerinde eşzamanlı bağlantıları yönetmek için process veya thread'ler kullanılır. Bağlantı sayısı arttıkça bu yapıların oluşturduğu bellek ve CPU maliyeti de artabilir.

**Nginx Modeli (Asenkron ve Non-blocking):** Nginx her bağlantı için yeni bir process veya thread oluşturmak yerine, worker process'ler içerisindeki event loop mekanizmasıyla çok sayıda bağlantıyı yönetir. Bir bağlantı I/O beklerken worker başka bağlantıların olaylarını işleyebilir.

**Sonuç:** Çok düşük RAM tüketimi ile devasa trafikleri eritebilme gücü.

### Process Hiyerarşisi
Nginx arka planda iki temel yapıyla çalışır:

**Master Process:** Patron görevindedir. Konfigürasyon dosyalarını okur ve Worker süreçlerini başlatıp yönetir. Kullanıcılardan gelen ağ istekleriyle doğrudan ilgilenmez.

**Worker Process:** Gerçek istemci bağlantılarını ve isteklerini işleyen process'lerdir. Performans için worker sayısı çoğu durumda CPU çekirdeği sayısıyla ilişkilendirilir. `worker_processes auto`, kullanıldığında Nginx uygun worker sayısını otomatik olarak belirleyebilir ancak bu, her durumda "bir çekirdek = bir worker" şeklinde değişmez bir kural değildir.

<p align="center">
  <img src="process_hiyerarsisi.jpg" alt="Process Hiyerarşisi">
</p>

## Konfigürasyon Anatomisi

**nginx.conf (Ana Yönetim Merkezi)**

- İşlevi: Nginx'in kalbi ve beynidir. Tüm sistemi etkileyen global ayarlar burada barındırılır.

- İçeriği: Kaç adet Worker Process çalışacağı, genel güvenlik kuralları, bağlantı limitleri ve en önemlisi diğer parçalı ayar dosyalarını sisteme dahil eden include komutları bu dosyada yer alır.

**sites-available Klasörü (Bekleme Odası / Depo)**

- İşlevi: Sunucuda barındırmak istenilen her bir farklı web sitesi veya uygulama (Domain A, Domain B vb.) için oluşturulan özel ayar dosyalarının saklandığı yerdir.

- Özelliği: Nginx bu klasörü doğrudan okumaz. Buraya bir dosya koyulması, sitenin anında yayına gireceği anlamına gelmez. Pasif bir arşiv alanıdır.

- sites-available klasöründeki bir dosyanın aktif hale gelmesi için genellikle bu dosyaya sites-enabled altında bir sembolik link oluşturulur.

**sites-enabled Klasörü (Vitrin / Aktif Alan)**

- İşlevi: Debian/Ubuntu gibi sistemlerde yaygın olarak kullanılan bir organizasyon yöntemidir. Aktif olarak kullanılacak site konfigürasyonlarının sembolik linkleri burada bulunur. Nginx'in bu dosyaları okuması, ana konfigürasyondaki `include /etc/nginx/sites-enabled/*;` gibi bir include directive'i sayesinde gerçekleşir. Nginx'in kendisi `sites-enabled` klasörünü özel olarak tanımaz.

- Çalışma Mantığı (Symlink): Dosyaların orijinalleri bu klasöre kopyalanmaz. Bunun yerine, sites-available içindeki orijinal dosyaya işaret eden bir kısayol (symlink) oluşturulur.

```
sites-available/example.com
            ↑
            │ symlink
            │
sites-enabled/example.com
```

**Bu Hiyerarşinin Sağladığı Avantaj:**
Bir site geçici olarak kapatılmak veya bakıma alınmak istendiğinde, uzun ayar dosyalarını silmeye gerek kalmaz. Sadece sites-enabled (vitrin) içindeki kısayol silinir ve Nginx'e ayarlar yeniden okutulur. Sitenin asıl ayarları sites-available içinde dokunulmamış halde kalır. Site geri açılmak istendiğinde kısayolu tekrar oluşturmak yeterlidir.

## Bloklar (Contexts)

**http Bloğu (Ana Kapsayıcı)**

- Nginx'in web ile ilgili tüm işlemlerini kapsayan en dış çerçevedir.

- Log formatları, dosya sıkıştırma ayarları gibi tüm siteleri etkileyecek genel kurallar burada tanımlanır. Sistemdeki bütün web siteleri bu bloğun kurallarına tabidir.

**server Bloğu (Virtual Host)**

- http bloğunun içinde yer alır. Kiralanan sunucudaki her bir farklı web sitesini veya uygulamayı temsil eder.

- Hangi domain'e ve hangi porta yanıt verileceği burada, `server_name` ve `listen` komutlarıyla belirlenir.

- Aynı sunucuda 3 farklı site varsa, bu bloğun içine yazılmış 3 farklı server bloğu var demektir. Nginx gelen isteğin domainine bakar ve doğru server bloğunu seçer.

**location Bloğu (URL Yönlendirici)**

- server bloğunun içinde yer alır. İşin en detaylı, milimetrik ayarlarının yapıldığı yerdir.

- Kullanıcının girdiği URL yoluna göre ne yapılacağına karar verir.

- Örneğin; `/ (ana sayfa)` isteği geldiğinde Node.js'e git, `/resimler` isteği geldiğinde arka plana gitme doğrudan şu klasördeki resimleri göster gibi spesifik yönlendirmeler bu blokların içine yazılır.

## Reverse Proxy

**Forward Proxy:** Kullanıcıyı (istemciyi) gizler ve korur. Örneğin VPN bir Forward Proxy'dir. İnternetteki bir siteye girildiğinde istek önce VPN sunucusuna yollanır, siteye kullanıcı yerine o girer ve sonucu getirir. Karşıdaki web sitesi kullanıcının kim olduğunu (gerçek IP'yi) bilmez, sadece VPN sunucusunu görür.

**Reverse Proxy:** Client ile backend sunucuları arasında duran ve client'ın isteklerini backend adına karşılayıp uygun arka uç servisine ileten proxy türüdür. Backend sunucularının doğrudan internete açılmasını gerektirmediği için mimarinin dışarıya karşı soyutlanmasına ve merkezi güvenlik, TLS, caching ve load balancing gibi işlemlerin uygulanmasına olanak sağlar. Sunucuyu gizler.

<p align="center">
  <img src="reverse_proxy.jpg" alt="Proxy">
</p>

### Reverse Proxy Olarak Nginx

Eğer kullanıcı sitedeki bir logoyu (logo.png) görmek istiyorsa, bu isteği asıl uygulamaya kadar götürmek büyük bir performans israfıdır. Nginx, diskteki dosyaları okuyup doğrudan ağ kartına iletme konusunda inanılmaz optimize edilmiştir. Statik dosyalar Nginx üzerinden sunulduğunda, uygulama gereksiz yere yorulmaz ve sadece asıl yapması gereken işlere odaklanır. Fakat kullanıcı veritabanı sorgusu gerektiren dinamik bir şey isterse o zaman Nginx topu arka plandaki asıl uygulamaya atar.

**Temel Mekanizma:**
Nginx, location bloğu içerisine yazılan `proxy_pass` komutu ile bu yönlendirmeyi yapar.
Örneğin Nginx'e dışarıdan `/api` ile başlayan bir istek gelirse, buna cevap vermez, bu isteği alır ve sunucunun kendi içindeki http://localhost:3000 adresine fırlatır.

### Başlıkları (Headers) Taşımak
Nginx reverse proxy olarak çalışırken backend bağlantıyı Nginx'ten gelen bir bağlantı olarak görür. Nginx ve backend aynı makinedeyse bu adres genellikle 127.0.0.1 gibi bir localhost adresidir, farklı makinelerde ise Nginx sunucusunun IP adresi görülür. Bu nedenle gerçek istemci IP'si ve diğer istemci bilgileri `X-Real-IP, X-Forwarded-For, X-Forwarded-Proto` gibi HTTP header'ları üzerinden backend'e aktarılabilir.

Bunu çözmek için Nginx'te `proxy_set_header` komutları kullanılır. Nginx, isteği arka plana fırlatırken gerçek kullanıcının IP adresini ve tarayıcı bilgilerini bir HTTP Headers'a koyarak arka plandaki uygulamaya iletir. Böylece uygulama (hangi dilde yazılmış olursa olsun) aslında kiminle muhatap olduğunu bilir.

## Önbellekleme (Caching)

**Amacı:** Nginx, arka plandaki uygulamanın oluşturduğu dinamik sayfaları veya API yanıtlarını diskte/hafızada tutabilir. Aynı sayfaya yönelik bir istek tekrar geldiğinde, Nginx arka plana (Node.js, PHP vb.) hiç sormadan cevabı doğrudan kendi önbelleğinden verir. Bu, yanıt sürelerini milisaniyelere düşürür ve uygulamanın gereksiz yere yorulmasını engeller.

Nginx mimarisinde önbellek yönetimi için iki özel süreç (process) arka planda bağımsız olarak çalışır:
- **Cache Manager:** Nginx proxy cache'inin disk üzerindeki alanını yönetir. Cache boyutunun ve kullanılmayan cache nesnelerinin kontrol edilmesine ve gerektiğinde eski nesnelerin temizlenmesine yardımcı olur.
- **Cache Loader:** Nginx yeniden başlatıldığında disk üzerinde daha önceden oluşturulmuş cache nesnelerini tarayarak bunların metadata bilgisini bellekteki cache indeksine yükler. Cache içeriğinin tamamı RAM'e yüklenmez.

**Kullanımı:** Genel `http` bloğu içinde `proxy_cache_path` komutu ile önbelleğin nereye kaydedileceği ve kapasitesi tanımlanır. Ardından, önbelleğe alınması istenen yolların `location` bloğu içinde `proxy_cache` komutuyla aktif edilir.

## Load Balancing

**Amacı:** Load balancing yalnızca trafiği dağıtmak için değil, backend'lerden birinin başarısız olması durumunda sistemin dayanıklılığını artırmak için de kullanılabilir. Nginx, upstream sunucuların başarısızlıklarını belirli durumlarda pasif olarak algılayarak başarısız backend'i geçici olarak devre dışı bırakabilir. Daha gelişmiş aktif health-check mekanizmaları ise kullanılan Nginx sürümüne ve ürününe göre ayrıca değerlendirilmelidir.

**Çalışma Mantığı (upstream Bloğu):** Nginx ayarlarında bir upstream (kaynak) bloğu tanımlanır. Bu blok, arka plandaki sunucuların bir listesidir. Ardından `proxy_pass` komutu tek bir IP veya porta değil, doğrudan bu upstream grubunun ismine yönlendirilir.

<p align="center">
  <img src="load_balancing.jpg" alt="Load Balancing">
</p>

### Yük Dağıtım Algoritmaları
Nginx'in trafiği dağıtırken kullandığı temel stratejiler şunlardır:

**Round Robin (Varsayılan):** İskambil kağıdı dağıtır gibi sırayla verir. Birinci istek A sunucusuna, ikinci istek B'ye, üçüncü istek C'ye gider ve sonra tekrar başa döner.

**Least Connections (least_conn):** Hangi sunucunun o an en az aktif bağlantısı varsa, yeni gelen isteği ona yönlendirir. Bazı işlemlerin uzun, bazılarının kısa sürdüğü sistemler için dengeli bir yöntemdir.

**IP Hash (ip_hash):** Aynı IP adresine sahip bir kullanıcı siteye her girdiğinde hep aynı arka plan sunucusuna yönlendirilir. (Örneğin sepet veya kullanıcı giriş verileri ortak bir veritabanında değil de uygulamanın kendi belleğinde tutuluyorsa, kullanıcının hep aynı sunucuya düşmesi gerekir; aksi halde hesaptan çıkış yapmış gibi görünür).

**Weight:** Arka plandaki sunucuların donanımları eşit değilse kullanılır. B sunucusunun işlemcisi daha güçlüyse, oraya A sunucusunun 2 katı trafik gönderen manuel bir oran belirlenmesini sağlar.

## Güvenlik ve SSL/TLS

Amacı kullanıcının tarayıcısı ile sunucu arasındaki trafiği şifrelemektir. Nginx bu aşamada şifreleme ve şifre çözme işlemini üstlenerek arka plandaki uygulamaları büyük bir yükten kurtarır.

İnternetten gelen şifreli istek Nginx'e ulaşır. Nginx TLS bağlantısını sonlandırır ve isteği backend'e iletir. Backend bağlantısı ayrıca HTTP veya HTTPS olarak yapılandırılabilir. Böylece TLS şifreleme işlemi Nginx üzerinde sonlandırılabilir; backend ile Nginx arasındaki bağlantının ayrıca şifrelenip şifrelenmeyeceği mimariye göre belirlenir.

<p align="center">
  <img src="ssl_tls.jpg" alt="SSL/TLS">
</p>

Nginx'te güvenli bir bağlantı kurarken genellikle şu iki kural uygulanır:

- HTTP'yi HTTPS'e Zorlama: Eski usul güvensiz port olan 80'e (HTTP) gelen tüm istekler yakalanır ve anında güvenli porta (443) yönlendirilir. Kullanıcı `http://` yazsa bile Nginx onu zorla `https://` adresine atar.

- Sertifika Tanımlamaları: Nginx, TLS bağlantısını sonlandırarak client ile güvenli HTTPS iletişimini sağlayabilir. Bu durumda client ile Nginx arasındaki trafik TLS ile korunurken, Nginx ile backend arasındaki bağlantı ayrıca HTTP veya HTTPS olarak yapılandırılabilir.
  - ssl_certificate, sunucunun kimliğini doğrulamak için kullanılan TLS sertifikasını belirtir. Sertifika, sunucunun public key'ini ve sertifika otoritesi (CA) tarafından imzalanmış kimlik bilgilerini içerir.
  - ssl_certificate_key ise sertifikadaki public key'e karşılık gelen ve yalnızca sunucuda gizli tutulması gereken private key'i belirtir.

|Dosya|Görevi|
|---|---|
|ssl_certificate|TLS sertifikasını belirtir|
|ssl_certificate_key|Sunucunun private key'ini belirtir|

## Gözlem ve Loglama

Amaç sistemde ne olup bittiğini görmek, hataları ayıklamak ve siteye gelen trafiği analiz etmektir. Nginx, kapıdan giren çıkan herkesi ve yaşanan tüm krizleri iki temel dosya üzerinden raporlar:

- **access.log (Giriş/Erişim Kayıtları):** Sunucuya gelen her bir isteğin satır satır kaydedildiği dosyadır. "Hangi IP adresi, saat kaçta, hangi sayfayı veya dosyayı istedi, yanıt olarak hangi HTTP kodunu aldı, tarayıcısı ve işletim sistemi neydi?" gibi istatistiksel bilgilerin tümü burada tutulur.

- **error.log (Hata Kayıtları):** Nginx'in çalışırken karşılaştığı yapısal sorunların ve en önemlisi arka plan uygulamasıyla yaşadığı iletişim kopukluklarının yazıldığı cankurtaran dosyasıdır. Örneğin; uygulama çöktüyse ve Nginx ona ulaşamıyorsa, ziyaretçiye "502 Bad Gateway" hatası gösterilir ve bunun teknik detayı anında bu dosyaya yazılır. Sorun çözerken ilk bakılacak yerdir.

### Log Yönetimi ve Özelleştirme

**Log Formatını Değiştirme:** http bloğu içinde özel log formatı oluşturulabilir. Vekilleri aşıp gelen "gerçek kullanıcı IP'sini" loglara yazdırmak bu şekilde mümkün olur.

**Gereksiz Logları Kapatma:** Bir web sitesinde yüzlerce resim, CSS ve font dosyası olabilir. Her bir resim yüklendiğinde bunun `access.log` dosyasına yazılması diski çok hızlı doldurur ve sunucuyu yorar. Nginx'te location blokları içine `access_log off`; komutu yazılarak, sadece statik dosyaların loglanması kolayca iptal edilebilir.

### Hız Sınırlandırma (Rate Limiting)

Belirli bir client'ın veya anahtarın belirli bir süre içinde gönderebileceği request oranını sınırlandırarak API'lerin, login endpoint'lerinin ve diğer kritik kaynakların aşırı kullanımını önlemeye yardımcı olur. Bot trafiği, brute-force denemeleri ve uygulama katmanındaki bazı DoS türlerine karşı faydalı olabilir; ancak tek başına genel amaçlı bir DDoS koruması değildir.

`limit_req`, rate limit aşıldığında isteği yapılandırmaya bağlı olarak geciktirebilir veya reddedebilir. Reddedilen istekler için Nginx'in varsayılan HTTP status kodu 503 Service Unavailable'dır. `limit_req_status` direktifi kullanılarak farklı bir status kodu, örneğin 429 Too Many Requests, yapılandırılabilir.

**Çalışma Mantığı (Leaky Bucket Algoritması):** Eğer bir IP adresi belirlenen limiti (örneğin saniyede 10 istek) aşarsa, Nginx fazla gelen istekleri arka plandaki asıl uygulamaya hiç iletmeden doğrudan reddeder. Kullanıcıya "503 Service Unavailable" (veya yapılandırmaya göre 429 Too Many Requests) hata kodu döndürülür.

**Kullanımı:** İlk olarak `http` bloğunda `limit_req_zone` direktifi ile IP adreslerinin takip edileceği bir RAM alanı (zone) ve saniyelik limit oluşturulur. Daha sonra, özellikle korunması gereken kritik sayfalarda (örneğin `/login` veya `/api`) ilgili `location` bloğunun içine `limit_req` komutu eklenerek kural devreye sokulur.

