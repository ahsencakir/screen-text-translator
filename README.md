# Gerçek Zamanlı Metin Çevirici - Real-Time Text Translator

Bu proje, herhangi bir uygulama ekranındaki metinleri gerçek zamanlı olarak OCR (Optical Character Recognition) ile okuyup DeepL API kullanarak Türkçe'ye çeviren bir masaüstü uygulamasıdır.

## 🎯 Özellikler

- **Pencere Seçimi**: Açık pencereler arasından istediğiniz uygulamayı seçebilirsiniz
- **Alan Seçimi**: OCR yapılacak alanı ve çevirinin gösterileceği yeri manuel olarak seçebilirsiniz
- **Gerçek Zamanlı OCR**: Seçilen alandaki metinleri sürekli olarak okur
- **Otomatik Çeviri**: İngilizce metinleri DeepL API ile Türkçe'ye çevirir
- **Overlay Görüntüleme**: Çevirileri uygulama üzerinde şeffaf bir kutu içinde gösterir
- **Akıllı Güncelleme**: Sadece metin değiştiğinde yeni çeviri yapar

## 📋 Gereksinimler

### Python Kütüphaneleri
```bash
pip install pygetwindow opencv-python pytesseract deepl pillow PyQt5 mss pywin32 numpy
```

### Harici Yazılımlar
1. **Tesseract OCR**: [Tesseract GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki) sayfasından Windows installer'ını indirip kurun
2. **DeepL API Key**: [DeepL API](https://www.deepl.com/pro-api) sayfasından ücretsiz hesap açıp API anahtarınızı alın

## 🛠️ Kurulum

### 1. Repository'yi klonlayın
```bash
git clone https://github.com/yourusername/screen-text-translate.git
cd screen-text-translate
```

### 2. Python kütüphanelerini kurun
```bash
pip install -r requirements.txt
```

### 3. Tesseract OCR'ı kurun
- [Tesseract Windows Installer](https://github.com/tesseract-ocr/tesseract) sayfasından indirin
- Kurulum sonrası Tesseract'ın kurulu olduğu yolu not edin (genellikle `C:\Program Files\Tesseract-OCR\tesseract.exe`)

### 4. Konfigürasyon
`screen-text-translator.py` dosyasını açın ve aşağıdaki satırları düzenleyin:

```python
# DeepL API KEY - Kendi API anahtarınızı buraya yazın
AUTH_KEY = "your-deepl-api-key-here"

# Tesseract yolunu belirt - Kendi kurulum yolunuzu yazın
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## 🚀 Kullanım

1. **Programı çalıştırın**:
   ```bash
   python screen-text-translator.py
   ```

2. **Pencere seçimi**:
   - Terminal'de açık pencereler listesi görünecek
   - İzlemek istediğiniz uygulamanın numarasını girin

3. **OCR alanı seçimi**:
   - Yeşil overlay açılacak
   - Uygulamadaki metin bölgesini fare ile çerçeveleyin
   - Sol tık basılı tutup sürükleyerek alan seçin

4. **Çeviri kutusu konumu**:
   - Çevirinin gösterileceği yeri seçin
   - Bu alan çeviri metninin görüneceği yer olacak

5. **Program kullanımda**:
   - Program otomatik olarak seçilen alandaki metinleri okuyacak
   - Çevirileri belirttiğiniz konumda gösterecek
   - Terminal'e `q` yazıp Enter'a basarak çıkabilirsiniz

## � Kullanım Alanları

Bu program çok çeşitli uygulamalarda kullanılabilir:

### 🎮 Oyunlar
- RPG oyunları (diyalog metinleri)
- Strateji oyunları (açıklamalar, görevler)
- Simülasyon oyunları (menüler, bilgi metinleri)

### 💼 İş Uygulamaları
- Yabancı dildeki yazılımların arayüzleri
- PDF görüntüleyicilerindeki metinler
- Web tarayıcısındaki sayfalar

### 📚 Eğitim ve Araştırma
- Akademik makaleler ve dökümanlar
- Yabancı dildeki eğitim materyalleri
- Video konferans uygulamalarındaki altyazılar

### 🌐 Genel Kullanım
- Herhangi bir masaüstü uygulamasındaki metin
- Ekran görüntülerindeki yazılar
- Çevrilemez uygulamalardaki arayüz metinleri

## ⚙️ Ayarlar

### OCR Hassasiyeti
Tesseract OCR'ın daha iyi çalışması için:
- Metnin net ve büyük olduğu alanları seçin
- Arka plan ile metin arasında yeterli kontrast olsun
- Mümkünse uygulamanın çözünürlüğünü artırın

### Çeviri Hızı
`screen-text-translator.py` dosyasında:
```python
ocr_timer.start(2000)  # 2000ms = 2 saniye
```
Bu değeri değiştirerek OCR sıklığını ayarlayabilirsiniz.

## 🔧 Sorun Giderme

### Tesseract bulunamıyor hatası
- Tesseract'ın doğru kurulduğundan emin olun
- Kod içindeki `pytesseract.pytesseract.tesseract_cmd` yolunu kontrol edin

### DeepL API hatası
- API anahtarının doğru olduğundan emin olun
- API kotanızı kontrol edin (ücretsiz hesapta aylık 500.000 karakter)

### OCR metin okumuyor
- Daha net ve kontrastlı metin alanları seçin
- Uygulama çözünürlüğünü artırın
- Farklı OCR dilleri deneyin (kod içinde `lang='eng'` parametresi)

## 🙏 Teşekkürler

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR motoru
- [DeepL](https://www.deepl.com/) - Çeviri API'si
- [PyQt5](https://pypi.org/project/PyQt5/) - GUI framework
- [OpenCV](https://opencv.org/) - Görüntü işleme
