# linux-spyware-emulation

> **LEGAL DISCLAIMER & ETHICAL NOTICE**
> This repository is created solely for educational purposes, Red Team operations, and adversarial simulation research. The techniques discussed simulate how Advanced Persistent Threats bypass endpoint defenses, maintain stealth, and exfiltrate data using native Linux binaries. Any malicious or unauthorized use is strictly prohibited.

> **YASAL UYARI VE ETİK BİLDİRİM**
> Bu depo, Kırmızı Takım operasyonları, saldırgan simülasyonu ve siber güvenlik araştırmaları amacıyla tamamen eğitim konsepti kapsamında hazırlanmıştır. İçerikte bahsedilen teknikler, Gelişmiş Sürekli Tehdit gruplarının uç nokta savunmalarını nasıl atlattığını ve sistemde nasıl sessizce barındığını anlamak üzere incelenmiştir. Kötü amaçlı kullanım kesinlikle reddedilmektedir.

## Proje Özeti
Bu proje, Linux tabanlı sistemlerde sızma sonrası aşamada kullanılan gelişmiş gizlenme, veri sızdırma ve adli bilişim atlatma tekniklerinin anatomisini incelemektedir. Operasyonel güvenlik kuralları gereği, sisteme dışarıdan üçüncü parti bağımlılıklar yüklemek yerine, işletim sisteminin halihazırda sunduğu yerleşik kütüphaneler ve sistem çağrıları kullanılarak savunma mekanizmalarının nasıl atlatıldığı kod seviyesinde analiz edilmiştir.

---

## Kırmızı Takım Operasyon Anatomisi

### 1. İşlem Adı Maskeleme
Sızma sonrası bir sistemde çalışan şüpheli betikler, sistem yöneticileri veya uç nokta tespit ve yanıt çözümleri tarafından anında tespit edilir. Bunu atlatmak için ctypes kütüphanesi tercih edilmiştir. 

Çalışma Mantığı: ctypes aracılığıyla doğrudan C seviyesindeki işletim sistemi arayüzlerine inilir ve libc.so.6 kütüphanesi üzerinden prctl sistem çağrısı tetiklenir. 

Amaç: Görev yöneticisindeki işlem adı, sistemde meşru olarak çalışan bir servis gibi değiştirilir. Diske derlenmiş zararlı bir ikili dosya bırakmadan, doğrudan bellek üzerinden manipülasyon yapılarak statik analiz araçları atlatılır.

### 2. Sıfır Disk İzi
Operasyon sırasında toplanan verilerin fiziksel diske yazılması, dosya bütünlük izleme ve antivirüs alarmlarını tetikler.

Çalışma Mantığı: Harici bir araç yüklemek yerine subprocess kütüphanesi kullanılarak işletim sisteminin varsayılan araçları arka planda sessizce tetiklenir. Çıktılar, fiziksel diski tamamen pas geçen ve doğrudan bellek üzerinde barındırılan /dev/shm dizinine yönlendirilir.

Amaç: Diske veri yazmadan hedeflenen verileri elde etmek ve disk tabanlı izleme araçlarına yakalanmamak.

### 3. Kaotik Veri Sızdırma
Komuta kontrol sunucusu ile iletişim kurarken popüler üçüncü parti araçların sisteme kurulması kurulum kayıtları bırakır.

Çalışma Mantığı: Sadece Python dilinin yerleşik socket ve ssl kütüphaneleri kullanılarak ağ paketleri manuel olarak inşa edilir. Ağ izleme cihazlarının periyodik sinyal gönderme tespit kurallarını kırmak için random ve time kütüphaneleri birleştirilir. 

Amaç: İletişim kesin zaman aralıklarıyla yapılmaz. Bekleme fonksiyonuna eklenen rastgele gecikmeler sayesinde, ağ trafiği makine tabanlı bir otomasyondan ziyade düzensiz bir insan davranışına benzetilir.

### 4. Adli Bilişim Atlatma
Operasyon bitiminde veya sistemden çıkış yapılması gerektiğinde standart silme komutlarını kullanmak, verilerin kolayca kurtarılabilmesine olanak tanır.

Çalışma Mantığı: Fiziksel silme aşamasında os kütüphanesi ile ardışık manipülasyonlar yapılır. Önce yeniden adlandırma işlemleriyle dosya isimleri sürekli değiştirilerek dosya sistemindeki düğüm takibi kırılır. Ardından dosya boyutunda rastgele veriler üretilip diske zorla yazılır. Aynı zamanda bellek içindeki şifreleme anahtarları çöp toplayıcı tetiklenerek bellekten silinir.

Amaç: Depolama birimlerinin aşınma dengeleme mekanizmalarını zorlayarak üzerine yazma işlemi gerçekleştirmek ve adli bilişim ekiplerinin veri kurtarma operasyonlarını imkansızlaştırmak.

---

## Mavi Takım: Tespit ve Savunma Stratejileri
Kırmızı Takım tarafından uygulanan bu gizlilik odaklı teknikler, proaktif bir siber güvenlik operasyon merkezi ortamında aşağıdaki kayıt kaynakları ve tespit kuralları ile yakalanabilir:

1. Sistem Çağrısı Anomalileri: İşlem isimlerine güvenilmemelidir. Linux denetim sistemi kullanılarak sistem çağrıları izlenmelidir. Standart süreçlerin aniden yetki yükseltip sistem servisleri başlatması güvenlik bilgi ve olay yönetimi platformu üzerinde korelasyona sokulmalıdır.

2. Geçici Bellek İzleme: /dev/shm dizini sistem çekirdek süreçleri içindir. Uç nokta güvenlik ajanları üzerinden bu dizin izlenmeli; aniden oluşturulup milisaniyeler içinde silinen gizli dosyalar kritik anomali olarak işaretlenmelidir.

3. Ağ Trafiği Analizi: Zaman manipülasyonu ile periyodik eşik değerleri aşılsa bile, ağ analizi araçları üzerinden şifreleme protokolü parmak izi analizi yapılmalıdır. Standart dışı kütüphanelerden başlatılan şifreli istekler tehdit istihbaratı veritabanları ile eşleştirilmelidir.

4. Aşırı Girdi Çıktı Yükü: Sistem izleme araçları kullanılarak, çok kısa zaman aralıklarında aynı dosya veya dizin üzerinde art arda gerçekleşen yeniden adlandırma ve yüksek hacimli üzerine yazma işlemleri şüpheli veri imhası olarak değerlendirilmelidir.
