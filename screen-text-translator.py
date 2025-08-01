import pygetwindow as gw
import cv2
import numpy as np
import pytesseract
import deepl
import time
import mss
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QPen
import threading
import sys
import win32gui
import win32con
from PyQt5.QtGui import QColor

def pencereyi_one_getir(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

# DeepL API KEY
AUTH_KEY = "YOUR_DEEPL_API_KEY"
translator = deepl.Translator(AUTH_KEY)

# Tesseract yolunu belirt - Kendi kurulum yolunuzu yazın
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Yourname\Desktop\teseract\teseractOcr\tesseract.exe"

ocr_bbox = []
output_position = [0, 0]

# 📌 Tüm pencereleri listele
print("\nAçık Pencereler:\n")
pencereler = [w for w in gw.getAllWindows() if w.title.strip()]
for i, w in enumerate(pencereler):
    print(f"{i}: {w.title}")

# Alan seçim fonksiyonu (sadece seçilen pencerenin görüntüsünde seçim)
def alan_secimi(pencere, secim_tipi="OCR"):
    import cv2
    import numpy as np
    import mss

    left, top, right, bottom = pencere.left, pencere.top, pencere.right, pencere.bottom
    width = right - left
    height = bottom - top

    with mss.mss() as sct:
        mon = {"top": top, "left": left, "width": width, "height": height}
        ekran = np.array(sct.grab(mon))
        img_bgr = cv2.cvtColor(ekran, cv2.COLOR_BGRA2BGR)

    img_copy = img_bgr.copy()
    secim = []
    selecting = [False]
    start_point = [0, 0]
    end_point = [0, 0]

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            start_point[0], start_point[1] = x, y
            selecting[0] = True
        elif event == cv2.EVENT_MOUSEMOVE and selecting[0]:
            img_copy2 = img_bgr.copy()
            cv2.rectangle(img_copy2, (start_point[0], start_point[1]), (x, y), (0, 255, 0), 2)
            cv2.imshow(f"{secim_tipi} Alanı Seç", img_copy2)
        elif event == cv2.EVENT_LBUTTONUP:
            selecting[0] = False
            end_point[0], end_point[1] = x, y
            cv2.rectangle(img_bgr, (start_point[0], start_point[1]), (end_point[0], end_point[1]), (0, 255, 0), 2)
            cv2.imshow(f"{secim_tipi} Alanı Seç", img_bgr)
            secim.extend([min(start_point[0], end_point[0]), min(start_point[1], end_point[1]),
                         max(start_point[0], end_point[0]), max(start_point[1], end_point[1])])
            cv2.destroyWindow(f"{secim_tipi} Alanı Seç")

    cv2.imshow(f"{secim_tipi} Alanı Seç", img_bgr)
    cv2.setMouseCallback(f"{secim_tipi} Alanı Seç", mouse_callback)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Kullanıcı çıkış yaptı.")
            cv2.destroyAllWindows()
            exit()
        if not cv2.getWindowProperty(f"{secim_tipi} Alanı Seç", cv2.WND_PROP_VISIBLE):
            break
    cv2.destroyAllWindows()

    # Seçim koordinatlarını pencerenin gerçek ekran koordinatlarına dönüştür
    if secim:
        secim[0] += left
        secim[2] += left
        secim[1] += top
        secim[3] += top
    return secim

# Pencere seçimi sonrası:
secim = int(input("\nİzlemek istediğiniz pencerenin numarasını girin: "))
secilen = pencereler[secim]
pencereyi_one_getir(secilen._hWnd)

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen

class OverlaySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)
        self.start = None
        self.end = None
        self.selected_rect = None
        self.setCursor(Qt.CrossCursor)
        self.done = False

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.fillRect(self.rect(), QColor(100, 100, 100, 100))  # Yarı saydam gri arka plan
        if self.start and self.end:
            qp.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            rect = QRect(self.start, self.end)
            qp.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if self.start:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start:
            self.end = event.pos()
            self.selected_rect = QRect(self.start, self.end).normalized()
            self.done = True
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            print("Kullanıcı çıkış yaptı.")
            self.selected_rect = None
            self.done = True
            QApplication.quit()  # sys.exit(0) yerine
            self.close()


def overlay_ile_alan_secimi(secim_tipi="Alan Seçimi"):
    app = QApplication.instance() or QApplication([])
    selector = OverlaySelector()
    selector.setWindowTitle(secim_tipi)
    selector.show()
    while not selector.done:
        app.processEvents()
    if selector.selected_rect:
        rect = selector.selected_rect
        x1, y1, x2, y2 = rect.left(), rect.top(), rect.right(), rect.bottom()
        return [x1, y1, x2, y2]
    else:
        sys.exit(0)

# --- Alan seçimi için overlay fonksiyonunu kullan ---
pencereyi_one_getir(secilen._hWnd)
print("🔳 Lütfen önce OCR yapılacak alanı seç (oyundaki metin bölgesi). Gerçek ekran üzerinde dikdörtgen çiz.")
ocr_bbox = overlay_ile_alan_secimi("OCR Alanı Seç")
print("OCR alanı:", ocr_bbox)

pencereyi_one_getir(secilen._hWnd)
print("💬 Şimdi çeviri kutusunun gösterileceği yeri seç. Gerçek ekran üzerinde bir nokta seç.")
output_box = overlay_ile_alan_secimi("Çeviri Kutusu Seç")
output_position = [output_box[0], output_box[1]]
print("Çeviri konumu:", output_position)

if not secilen:
    print("❌ Pencere bulunamadı.")
    exit()

print(f"\n✅ Seçilen pencere: {secilen.title}")

# 📌 Pencere koordinatlarını al
win_left = secilen.left
win_top = secilen.top

# ✅ PyQt5 ile çeviri kutusu
app = QApplication([])

import threading

def terminalden_cikis_kontrol():
    while True:
        komut = input()
        if komut.strip().lower() == 'q':
            print("Terminalden çıkış komutu alındı. Program sonlandırılıyor.")
            QApplication.quit()
            break

threading.Thread(target=terminalden_cikis_kontrol, daemon=True).start()

label = QLabel()
label.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
label.setStyleSheet("background-color: rgba(0, 0, 0, 160); color: white; font-size: 16pt; padding: 10px;")
width = output_box[2] - output_box[0]
height = output_box[3] - output_box[1]
label.setWordWrap(True)
label.setFixedSize(width, height)
label.setGeometry(output_box[0], output_box[1], width, height)
label.hide()

# 🔁 OCR ve çeviri işini yapan fonksiyon (QTimer ile)
onceki_metin = ""
def ceviri_yap():
    global onceki_metin
    # Seçilen pencere önde mi kontrol et
    if win32gui.GetForegroundWindow() != secilen._hWnd:
        label.hide()
        return
    x1, y1, x2, y2 = ocr_bbox
    mon = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
    with mss.mss() as sct:
        img = np.array(sct.grab(mon))
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGB))
        metin = pytesseract.image_to_string(img_pil, lang='eng').strip()

    if metin and metin != onceki_metin:
        onceki_metin = metin
        print("🔎 OCR:", metin)
        try:
            sonuc = translator.translate_text(metin, source_lang="EN", target_lang="TR")
            ceviri = sonuc.text
            print("🌍 Çeviri:", ceviri)
            label.setText(ceviri)
            label.show()
        except Exception as e:
            print("❌ Çeviri hatası:", e)

# QTimer ile periyodik olarak ceviri_yap fonksiyonunu çağır
ocr_timer = QTimer()
ocr_timer.timeout.connect(ceviri_yap)
ocr_timer.start(2000)  # 2 saniyede bir

sys.exit(app.exec_())
