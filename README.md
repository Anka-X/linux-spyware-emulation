# linux-spyware-emulation

**Disclaimer**  

*This repository contains a proof‑of‑concept script that captures screenshots and logs keystrokes on a Linux system. The code is provided **solely for educational purposes** and to demonstrate how a malicious actor might implement persistence and stealth on a target machine.  
Unauthorized use of this software on systems that you do not own or have explicit permission to test is **illegal** and may result in criminal prosecution.  
The author disclaims all liability for any damage or legal consequences that may arise from the misuse of this code.*


**Yasal Uyarı**  
*Bu depo, Linux sistemler üzerinde ekran görüntüsü alan ve tuş vuruşlarını kaydeden bir konsept kanıtlama (Proof-of-Concept) betiği içermektedir. Kod, **tamamen eğitim amaçlıdır** ve kötü niyetli bir aktörün hedef bir makinede kalıcılığı ve gizliliği nasıl uygulayabileceğini göstermek için sağlanmıştır.  
Sahibi olmadığınız veya test etmek için açık izniniz bulunmayan sistemler üzerinde bu yazılımın izinsiz kullanımı **yasadışıdır** ve cezai kovuşturmaya yol açabilir.  
Yazar, bu kodun kötüye kullanılmasından kaynaklanabilecek hiçbir zarardan veya yasal sonuçtan sorumluluk kabul etmez.*

---

## Genel Bakış

Betik aşağıdaki işlevleri gerçekleştirmektedir:

1. **Kalıcılık (Persistence)**  
   * Oturum açıldığında betiği başlatan kullanıcı düzeyinde bir systemd servisi (`gvfs-daemon.service`) kurar.  
   * Arka planda yardımcı yürütülebilir dosyayı (`gvfs-helper`) otomatik olarak başlatan bir bashrc diğer adı (alias) ekler.

2. **Gizlilik ve Kendini İmha (Stealth & Self‑Destruct)**  
   * Tüm kalıntıları (ikili dosyalar, servis dosyaları, kabuk geçmişi) silen ve servisi durdıran bir "bellek temizleme" rutini (`_burn_it_all`) kullanır.  
   * İşlemin hata ayıklandığını veya izlendiğini tespit ederse derhal sonlanır.

3. **Ekran Yakalama (Screen Capture)**  
   * `gnome‑screenshot` komutu veya `dbus‑send` aracılığıyla tam ekran görüntüsü alır.  
   * Görüntüyü RAM içinde saklar ve geçici dosyayı hemen siler.

4. **Tuş Kaydedici (Key‑Logger)**  
   * Her tuş vuruşunu kaydeden arka planda çalışan bir `pynput` dinleyicisi çalıştırır.  
   * Toplanan günlüğü periyodik olarak bir metin dosyası şeklinde gönderir.

5. **Komuta ve Kontrol (C2)**  
   * Yeni komutlar için Telegram botunu periyodik olarak sorgular (`/getUpdates`).  
   * Özel bir imha sinyali alınırsa, betik kendini imha etme rutinini tetikler.

6. **Telegram Üzerinden Veri Aktarımı (Telegram Delivery)**  
   * Ekran görüntülerini ve tuş vuruşu günlüklerini Telegram Bot API aracılığıyla belge olarak gönderir.  
   * Tüm hassas veriler (bot token, sohbet kimliği, sunucu) XOR ile şifrelenir ve çalışma zamanında çözülür.

---

## Ön Koşullar

* Python 3.8+  
* `python3-pynput`, `python3-pil`, `python3-xlib`  
* `gnome-screenshot` (veya `dbus-send` araçları)  
* Çalışan bir Telegram Botu ve verileri almak için bir sohbet kimliği (Chat ID)

---

## Kurulum / Kullanım

1. **Yer tutucuları düzenleyin** – Betik içerisindeki XOR şifreli değerleri değiştirin:

   ```python
   _T_X = bytearray(b"BURAYA_XORLU_TOKEN")
   _C_X = bytearray(b"BURAYA_XORLU_CHAT_ID")
   _H_X = bytearray(b"BURAYA_XORLU_HOST")
