# TCP/IP Modeli

## İnternet Nasıl Çalışır? Protokol Nedir?

 İnternet: En temel haliyle "ağların ağıdır" (Network of networks). Dünyanın dört bir yanındaki bilgisayarların, sunucuların, yönlendiricilerin (router) ve kabloların (fiber optik, bakır vs.) birbirine bağlanarak oluşturduğu devasa bir iletişim altyapısıdır.

 Protokol: İki veya daha fazla cihazın birbiriyle nasıl iletişim kuracağını belirleyen kurallar bütünüdür. İki insanın anlaşabilmesi için aynı dili konuşması ve belirli dilbilgisi kurallarına uyması gerekir. Bilgisayarlar için bu "dil", protokollerdir (Örn: TCP, IP, HTTP).

## TCP/IP'nin Tarihçesi (ARPANET)

 1969 - ARPANET (Advanced Research Projects Agency Network): ABD Savunma Bakanlığı, nükleer bir saldırı durumunda bile iletişimin kopmayacağı, merkezi olmayan ve dayanıklı bir ağ kurmak istedi.

 Paket Anahtarlama (Packet Switching): ARPANET'in en büyük yeniliğiydi. Veriler tek ve kesintisiz bir hat üzerinden gitmek yerine, küçük "paketlere" bölünerek farklı yollardan hedefe ulaşıyor ve orada tekrar birleştiriliyordu.

 TCP/IP'nin Doğuşu: 1970'lerde Vint Cerf ve Bob Kahn, farklı ağların birbiriyle konuşabilmesini sağlayacak evrensel bir dil olan TCP/IP (Transmission Control Protocol/Internet Protocol) süitini geliştirdiler. 1983'te ARPANET tamamen TCP/IP'ye geçti ve modern internetin doğuşu olarak bu tarih kabul edilir.

## OSI vs. TCP/IP Modeli

 OSI, 1980'lerde ISO (Uluslararası Standartlar Örgütü) tarafından geliştirilen 7 katmanlı bir referans modelidir. Günümüzde internet doğrudan OSI'yi kullanmaz, ancak ağ mühendisleri sorunları çözerken veya sistemleri anlatırken her zaman OSI'yi referans alırlar.

 TCP/IP, OSI'den önce geliştirilmiş, daha pratik ve doğrudan internetin temelini oluşturan 4 katmanlı modeldir (Bazı kaynaklarda 5 katmanlı olarak da geçer ancak orijinal ABD Savunma Bakanlığı modelinde 4 katmandır).

| OSI Modeli (7 Katman) | TCP/IP Modeli (4 Katman) | Açıklama / Görev | Örnek Protokoller |
|:---:|:---:|:---|:---|
| 7. Application (Uygulama) | 4. Application (Uygulama) | Kullanıcının etkileşime girdiği yazılımlar (Tarayıcı, e-posta). | HTTP, HTTPS, SMTP, DNS |
| 6. Presentation (Sunum) | | Verinin şifrelenmesi ve formatlanması (JPEG, SSL). | SSL, TLS, JPEG |
| 5. Session (Oturum) | | İki cihaz arasındaki iletişimin başlatılması/kapatılması. | NetBIOS, RPC |
| 4. Transport (Taşıma) | 3. Transport (Taşıma) | Verinin uçtan uca güvenli/hızlı iletimi. Hata kontrolü. | TCP, UDP |
| 3. Network (Ağ) | 2. Internet (İnternet) | Mantıksal adresleme (IP) ve verinin en iyi yoldan yönlendirilmesi (Routing). | IPv4, IPv6, ICMP |
| 2. Data Link (Veri Bağlantısı) | 1. Network Access (Ağ Erişimi) | Fiziksel adresleme (MAC) ve ağ içi hata tespiti. | Ethernet, Wi-Fi, ARP |
| 1. Physical (Fiziksel) | | Verinin 1 ve 0'lar (elektrik, ışık) olarak kablolardan aktarımı. | Kablolar, Fiber, Hub'lar |

---

> Önemli Not: TCP/IP modelinin Uygulama katmanı, OSI modelindeki Uygulama, Sunum ve Oturum katmanlarının üçünün yaptığı işi tek başına üstlenir. Aynı şekilde TCP/IP'nin Ağ Erişimi katmanı, OSI'deki Veri Bağlantısı ve Fiziksel katmanları kapsar.

 ---

<p align="center">
  <img src="https://www.a1.digital/uploads/Images/KnowledgeHub/_1024x766_crop_center-center_82_line/Vergleich-des-TCP-IP-Modells-mit-dem-OSI-Modell.jpg.webp" alt="TCP/IP vs OSI">
</p>

### 1. Ağ Erişim Katmanı (Network Access Layer)

TCP/IP modelinin en alt katmanıdır. Bu katman, IP paketlerini alır ve onları ağın fiziksel yapısına (bakır kablo, fiber optik, radyo dalgaları) uygun sinyallere (0 ve 1'lere) dönüştürür.

Aynı zamanda yerel ağda (Local Area Network - LAN) verinin doğru cihaza ulaşmasından sorumludur.


#### 1.1 Fiziksel Bağlantılar ve MAC Adresleri

İki cihaz aynı odada veya aynı binada (aynı yerel ağda) iletişim kurarken IP adreslerini değil, MAC adreslerini kullanırlar.

- MAC Adresi (Media Access Control): Cihazın ağ kartına (NIC) üretim aşamasında fabrikada yazılan, dünya üzerinde eşi benzeri olmayan 48-bitlik fiziksel bir adrestir (Örn: 00:1A:2B:3C:4D:5E).

- IP vs. MAC Farkı: IP adresi posta kodu, MAC adresini ise TC Kimlik numarası gibi düşünülebilir. Modem veya ev değiştiğinde IP adresi değişir ama cihazının MAC adresi aynı kalır.

#### 1.2 Ethernet Çerçevesi (Frame) Yapısı

Veriler ağ üzerinden bütün bir dosya halinde değil, küçük parçalara bölünerek gönderilir. Ağ Erişim katmanında bu veri parçalarına Çerçeve (Frame) denir. Ethernet frame'i, bir mektup zarfı gibidir; içinde asıl veriyi taşır ve üzerine "Kimden kime" gideceği yazılır.

Bir Ethernet Frame'i temel olarak şu kısımlardan oluşur:

| Bölüm | Açıklama |
|---|---|
| Preamble (Öncül) | Alıcıya sinyal göndererek cihazları senkronize eder. |
| Hedef MAC Adresi | Verinin gideceği cihazın fiziksel adresi (6 Byte). |
| Kaynak MAC Adresi | Veriyi gönderen cihazın fiziksel adresi (6 Byte). |
| EtherType (Tür) | İçerideki verinin protokolünü söyler (Örn: Bu bir IPv4 paketidir). |
| Payload (Veri) | Asıl taşınan bilgi. Boyutu 46 ile 1500 Byte arası değişir. (IP paketi buradadır) |
| FCS - Frame Check Sequence (Çerçeve Kontrol Dizisi) | Hata kontrol alanıdır. Veri kabloda bozulmuş mu diye kontrol edilir. Bozulmuşsa veri çöpe atılır. |

#### 1.3 ARP (Address Resolution Protocol) Mantığı

Bilgisayar bir web sitesine veya yerel ağdaki başka bir cihaza veri göndermek istediğinde, onun IP adresini biliyor olabilir ancak aynı ağ (LAN) içinde veri iletimi için MAC adresine ihtiyacı vardır.

IP adresinden MAC adresini bulma işlemine ARP denir.

**ARP Nasıl Çalışır?**

Bilgisayar (IP:192.168.1.10) modeme (IP:192.168.1.1) bir paket gönderecek ama modemin MAC adresini bilmiyor.

1. İhtiyacın Belirlenmesi

    Kaynak cihaz, hedef IP adresine bir veri paketi göndermek üzere hazırlık yapar. Aynı alt ağda (subnet) bulunan bu hedefin MAC adresi, kaynak cihazın yerel ARP önbelleğinde (ARP Cache) bulunmamaktadır.

2. ARP Request (İstek) Yayını

    Kaynak cihaz bir ARP İstek çerçevesi oluşturur. Bu çerçevenin hedef MAC adresi alanı, tüm ağa yayın anlamına gelen FF:FF:FF:FF:FF:FF (Broadcast) olarak ayarlanır. İlgili veri paketi, ağ anahtarı (Switch) üzerinden ağdaki tüm cihazlara iletilir.

3. Ağdaki Cihazların Yanıtı

    Ağdaki tüm cihazlar Broadcast yayınını alır ve ARP paketinin içindeki hedef IP adresini kendi IP adresleriyle karşılaştırır. Eşleşme bulamayan cihazlar paketi işleme almaz ve düşürür (Drop).

4. ARP Yanıt (Reply) Paketi

    Hedef IP adresine sahip olan cihaz, ARP paketini doğrular. Kendi MAC adresini içeren bir ARP Yanıt paketi oluşturur. Bu paket, Broadcast yerine doğrudan işlemi başlatan kaynak cihazın MAC adresine özel (Unicast) olarak gönderilir.

5. ARP Önbelleğinin (Cache) Güncellenmesi

    Kaynak cihaz, ARP Yanıt paketini teslim alır. Gelen verideki IP ve MAC adresi eşleşmesini, belirli bir süre boyunca tekrar aynı işlemi yapmamak üzere kendi ARP tablosuna kaydeder ve asıl veri iletim işlemini başlatır.
---

### 2. İnternet Katmanı (Internet Layer)

Mantıksal adresleme (IP adresleri) ve verinin kaynak ağdan hedef ağa en uygun yoldan ulaştırılması (Yönlendirme - Routing) işlemlerinden sorumludur.

#### 2.1 IP (Internet Protocol) ve Yönlendirme (Routing)

IP, internet üzerindeki her cihaza benzersiz bir mantıksal kimlik (IP adresi) atayan temel protokoldür.

- Bağlantısız İletişim (Connectionless): IP protokolü, paketi gönderirken karşı tarafın hazır olup olmadığını kontrol etmez. Paketin ulaşıp ulaşmadığıyla da ilgilenmez (bu görev bir üst katman olan Taşıma Katmanı'ndaki TCP'ye aittir). IP'nin tek amacı, paketi doğru hedefe doğru yola çıkarmaktır.

- Yönlendirme (Routing): Veri paketinin hedef IP adresine ulaşmak için ağlar ve yönlendiriciler arasında izleyeceği en iyi yolun seçilmesidir.

- Yönlendiriciler (Routers): Ağları birbirine bağlayan ve paketleri hedeflerine ulaştırmak için "Yönlendirme Tabloları" (Routing Tables) kullanan cihazlardır. Gelen paketin üzerindeki hedef IP'ye bakar ve onu hedefe en yakın olan bir sonraki yönlendiriciye (Next Hop) iletirler.

#### 2.2 IPv4 ve IPv6 Arasındaki Farklar

İnternetin büyümesiyle birlikte IP adreslerinin tükenmesi sorunu ortaya çıkmıştır. Bu nedenle geleneksel IPv4 standardından, çok daha geniş bir adres alanına sahip olan IPv6 standardına geçiş yapılmaktadır.

<p align="center">
  <img src="https://ipwithease.com/wp-content/uploads/2017/02/IPv4-vs-IPv6-comparison-table.jpg" alt="IPv4 vs IPv6">
</p>

#### 2.3 ICMP (Internet Control Message Protocol)

IP protokolü veriyi taşır, ancak hata bildirimi veya kontrol mekanizmaları yoktur. İnternet Katmanı'nda bu eksikliği ICMP kapatır.  ICMP, veri taşımak için değil; ağdaki cihazların durumunu kontrol etmek, hataları bildirmek ve ağ teşhisi (Diagnostics) yapmak için kullanılır.

---

### 3. Taşıma Katmanı (Transport Layer)

Bu katman verinin uçtan uca, uygulamanın ihtiyacına göre ya güvenilir (TCP) ya da çok hızlı (UDP) bir şekilde iletilmesinden sorumludur.

#### 3.1 Port ve Soketler (Sockets)

- Port: Bilgisayarın ağa açılan kapılarıdır. 0 ile 65535 arasında numaralandırılırlar. (Örneğin; Web trafiği için 80 veya 443, E-posta için 25 gibi numaralar tahsis edilmiştir).

- Soket (Socket): IP adresi ve Port numarasının birleşimidir. (Örn: 192.168.1.10:443). İletişim aslında iki bilgisayar arasında değil, iki cihazdaki soketler arasında gerçekleşir.

#### 3.2 TCP (Transmission Control Protocol) vs UDP (User Datagram Protocol)

TCP, internetin "garantici" ve "güvenilir" kuryesidir. Verinin eksiksiz ve sırasıyla karşı tarafa ulaştığından emin olmak zorundadır. Web sitelerinde gezinirken (HTTP/HTTPS), dosya indirirken (FTP) veya mail gönderirken (SMTP) TCP kullanılır.

TCP'nin Temel Özellikleri:

- Güvenilirlik (Reliability): Gönderilen her veri paketi için karşı taraftan bir "Teslim Aldım (ACK)" onayı bekler.  

- Hata Telafisi: Eğer onay gelmezse, paketin yolda kaybolduğunu varsayar ve o paketi otomatik olarak tekrar gönderir.

- Akış Kontrolü (Flow Control): Alıcı cihazın veri işleme hızına göre gönderim hızını yavaşlatıp hızlandırabilir.

UDP ise TCP'nin tam zıttıdır; "hızlı ama sorumsuz"dur. Bağlantı kurmak için 3'lü el sıkışma ile vakit kaybetmez (Connectionless). Veriyi yollar ve karşıya ulaşıp ulaşmadığını, sırasının bozulup bozulmadığını kontrol etmez.

UDP Nerede Neden Kullanılır?

- Canlı Yayınlar ve Görüntülü Konuşmalar (Zoom, Skype): Görüntülü konuşurken 1 saniye önceki görüntü paketinin kaybolması sorun değildir. O paketin tekrar gönderilmesi beklenirse yayın donar ve senkron kayar. Bu yüzden birkaç piksel bozukluğu veya anlık ses kesintisi göze alınır ama yayın akmaya devam eder.

- Online Rekabetçi Oyunlar (CS:GO, Valorant vb.): Oyunda karakterinin anlık konumu saniyede onlarca kez sunucuya iletilir. Eğer eski bir konum paketi kaybolursa, TCP'nin bunu tekrar göndermesini beklemek "ping/lag" yaratır. UDP sayesinde en güncel veri sürekli akmaya devam eder.

- DNS Sorguları: Çok hızlı sonuç dönmesi gerektiği için UDP kullanır.

<p align="center">
  <img src="https://ipcisco.com/wp-content/uploads/2018/10/tcp-vs-udp-comparison-ipcisco.com_.png" alt="TCP vs UDP">
</p>

#### 3.3 3'lü El Sıkışma (3-Way Handshake)

TCP, veri göndermeden önce karşı tarafla resmi bir bağlantı kurmak zorundadır. İşlem şu adımlarla gerçekleşir:

1. SYN (Synchronize) İsteği:

    İstemci, Sunucuya "Seninle bağlantı kurmak istiyorum" anlamında bir SYN paketi gönderir.

2. SYN-ACK (Synchronize-Acknowledge) Yanıtı:

    Sunucu bu isteği alır, kabul eder ve istemciye "Bağlantı isteğini aldım ve kabul ediyorum, ben de hazırım" anlamında bir SYN-ACK paketi döndürür.

3. ACK (Acknowledge) Onayı:

    İstemci, sunucunun yanıtını aldığını onaylamak için son bir ACK paketi yollar. Bu adımdan sonra bağlantı (ESTABLISHED) kurulur ve asıl veri transferi başlar.

---

### 4. Uygulama Katmanı (Application Layer)

Uygulama katmanı, TCP/IP modelinin en üst katmanıdır. Doğrudan son kullanıcının etkileşime girdiği yazılımların (web tarayıcıları, e-posta istemcileri) ağ üzerinden iletişim kurmak için kullandığı kuralları (protokolleri) barındırır. Bu katman, verinin nasıl sunulacağını, şifreleneceğini ve yönetileceğini belirler.

#### 4.1 Günlük Kullanılan Servisler

Bir web sitesine girildiğinde veya bir e-posta gönderildiğinde arka planda birçok protokol eşzamanlı olarak çalışır. Tarayıcı bir adres çubuğuna girilen metni anlamlı bir ağ hedefine dönüştürmek, içeriği güvenli bir şekilde indirmek ve cihaza bir kimlik atamak için bu katmandaki servislere güvenir.

#### 4.2 DNS - Domain Name System 

Bilgisayarlar ve yönlendiriciler IP adresleri (örneğin 192.168.1.1 veya 142.250.184.46) üzerinden iletişim kurarken, insanların bu numaraları akılda tutması zordur. DNS, [www.google.com](https://www.google.com) gibi anlaşılır alan adlarını IP adreslerine dönüştüren sistemdir. Çoğunlukla Port 53 (UDP) üzerinden çalışır.


<p align="center">
  <img src="https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTun3A7zu42rvmul0i1rRBCBW1hsUgTmmEPJ-6biUda3Pa_KJ_p16EfoVavvCxw4dUZF_iksqzObiasCxI" alt="DNS Query">
</p>

**DNS Çözümleme Süreci (Hiyerarşik Yapı):**

1. Local DNS Cache: Tarayıcı önce hedefin IP adresini kendi belleğinde veya işletim sisteminde arar.

2. Recursive Resolver (Yerel DNS Sunucusu): Kayıt bulunamazsa, genellikle İnternet Servis Sağlayıcısının (ISP) sunduğu DNS sunucusuna sorulur.

3. Root Server (Kök Sunucu): Hedef bilinmiyorsa, kök sunucuya gidilir. Kök sunucu doğrudan IP'yi bilmez ancak .com, .net gibi uzantılardan sorumlu sunucuyu işaret eder.

4. TLD (Top-Level Domain) Server: .com sunucusu, hedefin hangi yetkili sunucuda (Authoritative Name Server) kayıtlı olduğunu söyler.

5. Authoritative Name Server: İlgili alan adının gerçek IP adresini barındıran son duraktır. IP adresi buradan alınıp kullanıcıya iletilir.


#### 4.3 HTTP/HTTPS: Web Trafiği

Web sayfalarının sunucudan istemciye (tarayıcıya) aktarılmasını sağlayan temel protokollerdir.

- HTTP (Hypertext Transfer Protocol): Metin, görsel, video gibi web içeriklerinin taşınmasını sağlar. Varsayılan olarak Port 80 (TCP) kullanır. Veriler düz metin (plain text) olarak iletildiği için aradaki ağ cihazları trafiği okuyabilir; bu nedenle günümüzde güvenli kabul edilmez.

- HTTPS (HTTP Secure): HTTP'nin güvenli versiyonudur. İletilen veriler TLS/SSL (Transport Layer Security / Secure Sockets Layer) kullanılarak şifrelenir. Kredi kartı bilgileri, şifreler gibi hassas verilerin çalınmasını veya değiştirilmesini engeller. Varsayılan olarak Port 443 (TCP) kullanır.

#### 4.4 Diğer Temel Uygulama Katmanı Protokolleri

| Protokol | Açılımı | Varsayılan Port | Temel İşlevi |
|---|---|---|---|
| DHCP | Dynamic Host Configuration Protocol | UDP 67/68 | Ağa bağlanan cihazlara otomatik olarak IP adresi, alt ağ maskesi, varsayılan ağ geçidi (default gateway) ve DNS sunucu adresi atar. "IP çakışması" sorunlarını engeller. |
| FTP | File Transfer Protocol | TCP 20/21 | İki bilgisayar veya bir sunucu ile istemci arasında dosya yükleme ve indirme işlemlerini yönetir. |
| SMTP | Simple Mail Transfer Protocol | TCP 25/587 | E-posta gönderimini sağlar. İstemciden e-posta sunucusuna veya sunucular arası mail transferinden sorumludur. (Not: Posta almak için POP3 veya IMAP kullanılır). |
| SSH | Secure Shell | TCP 22 | Ağ üzerindeki başka bir bilgisayara veya sunucuya komut satırı üzerinden güvenli (şifreli) ve uzaktan erişim sağlar. |


## IP Adresleme ve Subnetting (Alt Ağlara Bölme)

### IP Sınıfları

Geleneksel IPv4 adreslemesinde, IP adresleri kullanım amaçlarına ve ağ büyüklüklerine göre sınıflara ayrılmıştır. Bu sınıflar, bir ağın ne kadar cihaza (host) ev sahipliği yapabileceğini belirler. Toplamda 5 sınıf vardır, ancak günlük kullanımda ilk üçü (A, B, C) karşımıza çıkar.

| Sınıf | Başlangıç - Bitiş Aralığı | Varsayılan Alt Ağ Maskesi |Kullanım Alanı|
|:---:|:---:|:---:|---|
| A Sınıfı | 1.0.0.0 - 126.255.255.255 | 255.0.0.0 | Çok sayıda cihaz barındıran devasa ağlar (Milyonlarca host). |
| B Sınıfı | 128.0.0.0 - 191.255.255.255 | 255.255.0.0 | Orta ve büyük ölçekli şirket/üniversite ağları (On binlerce host). |
| C Sınıfı | 192.0.0.0 - 223.255.255.255 | 255.255.255.0 | Ev ağları ve küçük işletmeler (Maksimum 254 host). |
| D Sınıfı | 224.0.0.0 - 239.255.255.255 | Yok | Multicast (çoklu yayın) işlemleri için ayrılmıştır. |
| E Sınıfı | 240.0.0.0 - 255.255.255.255 | Yok | Bilimsel araştırmalar ve deneysel kullanımlar içindir. |
---
> Not: 127.0.0.0 - 127.255.255.255 aralığı Loopback (kendi kendine test) için ayrılmıştır. (Örn: 127.0.0.1 localhost'tur).


### Alt Ağ Maskesi (Subnet Mask) ve CIDR Notasyonu

Bir IP adresi tek başına cihazın hangi ağda olduğunu söyleyemez; bunun için Alt Ağ Maskesine (Subnet Mask) ihtiyaç vardır. Alt ağ maskesi, IP adresinin hangi kısmının ağı (Network ID), hangi kısmının cihazı (Host ID) temsil ettiğini belirler.

- Subnetting: Büyük bir ağı daha küçük, yönetilebilir alt ağlara bölme işlemidir. Bu sayede ağ trafiği (broadcast) azalır, güvenlik artar ve IP israfı önlenir.

- CIDR (Classless Inter-Domain Routing) Notasyonu: Alt ağ maskesini 255.255.255.0 şeklinde uzun uzun yazmak yerine, ağ bitlerinin sayısını belirten bir kısaltma kullanmaktır.

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQty_FcSlonlOrm6hp-UTGuQkiNxBwmbLD_f46L73teYpGUxHej6MsuQLE&s=10" alt="CIDR">
</p>

### Genel (Public) ve Özel (Private) IP'ler

İnternet üzerindeki her cihazın benzersiz bir IP adresi olması gerekse de, IPv4 adreslerinin sayısı (yaklaşık 4.3 milyar) tüm dünyaya yetecek kadar fazla değildir. Bu sorunu çözmek için IP adresleri ikiye ayrılmıştır:

1. Genel (Public) IP Adresleri: İnternet üzerinde yönlendirilebilir (routable) olan ve dünya çapında tamamen benzersiz IP adresleridir. Genellikle İnternet Servis Sağlayıcısı (ISP) tarafından modeme/yönlendiriciye atanır.

2. Özel (Private) IP Adresleri: Sadece yerel ağlarda (LAN) kullanılan, internete doğrudan çıkamayan adreslerdir. Farklı evlerde veya şirketlerde aynı özel IP adresleri tekrar tekrar kullanılabilir.

#### Özel IP Aralıkları (RFC 1918):

- A Sınıfı: 10.0.0.0 - 10.255.255.255

- B Sınıfı: 172.16.0.0 - 172.31.255.255

- C Sınıfı: 192.168.0.0 - 192.168.255.255

### NAT (Network Address Translation)

NAT, yerel ağdaki cihazların özel (Private) IP adreslerini, modemin veya yönlendiricinin sahip olduğu tek bir genel (Public) IP adresine dönüştüren işlemdir.

- İçerideki bir cihaz internete bir paket gönderdiğinde, yönlendirici paketin üzerindeki özel kaynak IP'sini siler ve kendi genel IP'sini yazar. Ayrıca hangi cihazın hangi isteği yaptığını bir NAT tablosuna (Port numaraları ile birlikte) kaydeder. İnternetten cevap geldiğinde, tabloya bakar ve veriyi içerideki doğru cihaza iletir (Buna daha spesifik olarak PAT - Port Address Translation denir).

- IPv4 adreslerinin çoktan tükenmiş olmasını engelleyen en büyük kurtarıcıdır. İçeride binlerce bilgisayar (özel IP) olabilir, ancak hepsi dış dünyaya tek bir genel IP üzerinden bağlanır.


### Pratik Ağ Araçları ve Sorun Giderme

#### Komut Satırı Araçları

İşletim sistemlerinin (Windows, Linux, macOS) içine yerleşik olarak gelen komutlar, ağ sorunlarını tespit etmek için ilk başvurulan araçlardır.

- Ping: Bir hedefe (IP adresi veya alan adı) ICMP (Internet Control Message Protocol) "Echo Request" (Yankı İsteği) paketleri gönderir ve karşıdan "Echo Reply" (Yankı Yanıtı) bekler.

    Karşıdaki cihazın açık ve ağda ulaşılabilir olup olmadığını test eder. Ayrıca paketlerin gidiş-dönüş süresini (ms cinsinden ping süresi) göstererek bağlantı kalitesi hakkında bilgi verir.

- Tracert (Windows) / Traceroute (Linux/macOS): Veri paketi hedefe ulaşana kadar hangi yönlendiricilerden (router) geçtiğini adım adım listeler.

    Hedefe giden yolda bağlantının tam olarak nerede koptuğunu veya yavaşladığını bulmayı sağlar.


- Netstat (Network Statistics): Cihazın tüm aktif ağ bağlantılarını, dinlenen (listening) portları ve bu bağlantıları kuran uygulamaları gösterir.

    Arka planda hangi uygulamanın internete bağlandığını görmek veya sisteme açık olan yetkisiz bir portu (örneğin bir zararlı yazılımı) tespit etmek için kullanılır.

- Ipconfig (Windows) / Ifconfig (Linux/macOS): Bilgisayarın mevcut ağ yapılandırmasını ekrana yazdırır.

    Cihazın aldığı IP adresini, alt ağ maskesini ve varsayılan ağ geçidini öğrenmeyi sağlar.


#### Veri Paketlerini İzlemek: Wireshark

Komut satırı araçları ağın genel durumu hakkında bilgi verir, ancak ağ kablosundan veya Wi-Fi üzerinden tam olarak hangi verilerin aktığını görmek için bir "Paket Analizörü" (Packet Sniffer) kullanmak gerekir. Bu alandaki endüstri standardı Wireshark'tır.

<p align="center">
  <img src="https://gdm-catalog-fmapi-prod.imgix.net/ProductScreenshot/f3212535-a4cf-4e53-bdb4-c6b5f24c36bc.png?auto=format&q=50" alt="Wireshark">
</p>

Wireshark, ağ kartını (NIC) "Promiscuous Mode" (Karışık Mod) adı verilen bir duruma geçirir. Bu moddayken ağ kartı, sadece kendisine gelen paketleri değil, ağda dolaşan ve görebildiği tüm veri paketlerini yakalar.

**Neler Yapılabilir?:**

- Bir web sitesine girerken gerçekleşen DNS sorgularını ve TCP'nin 3'lü el sıkışma (3-way handshake) sürecini adım adım gösterir.

- HTTP veya FTP gibi şifrelenmemiş protokoller üzerinden gönderilen verilerin içeriği düz metin olarak okunabilir.

- Ağda bir yavaşlama varsa, hangi bilgisayarın veya uygulamanın aşırı trafik yarattığını tespit edebilir.