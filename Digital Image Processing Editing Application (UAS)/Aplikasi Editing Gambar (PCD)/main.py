import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSlider, QAction, QToolBar, QMainWindow, QMenu
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from image_utils import tingkatkan_kontras, pertajam_gambar, noise, penyesuaiaan_kecerahan_dan_kontras

class Aplikasi_Image_Enhancement(QMainWindow):
    def __init__(self):
        super().__init__()

        # panggil metode initUI untuk mengatur user interface.
        self.initUI()

        # Untuk menyimpan gambar asli
        self.original_image = None  

    def initUI(self):
        """
        Inisialisasi Tampilan UI

        def initUI(self) -> fungsi yang mendefinisikan seluruh tampilan GUI seperti toolbar (tools), gambar, dll

        """
        # Membuat toolbar dengan nama tools
        self.toolbar = QToolBar("tools")
        # Meletakkan semua tooolbar di area atas
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        """
        Membuat Berbagai Tools

        > Tools Save File          ->  
        menambahkan icon pada tombol tools dan memanggil fungsi saveImage ketika ditekan

        > Tools Tambah Gambar      ->
        menambahkan icon pada tombol tools dan memanggil fungsi tambahGambar ketika ditekan

        > Tools Kontras            ->
        menambahkan icon pada tombol tools dan memanggil fungsi meningkatkanKontras ketika ditekan

        > Tools Ketajaman          ->
        menambahkan icon pada tombol tools dan memanggil fungsi mempertajamGambar ketika ditekan

        > Tools Pengurangan Noise  ->
        menambahkan icon pada tombol tools dan memanggil fungsi reduceNoise ketika ditekan

        > Tools Grayscale          ->
        menambahkan icon pada tombol tools dan memanggil fungsi ubahKeGrayscale ketika ditekan

        > Tools Negatif            ->
        menambahkan icon pada tombol tools dan memanggil fungsi ubahKeNegatif ketika ditekan

        > Tools Dominasi Merah           ->
        menambahkan icon pada tombol tools dan memanggil fungsi dominasiMerah ketika ditekan

        > Tools Referesh           ->
        menambahkan icon pada tombol tools dan memanggil fungsi resetToOriginal ketika ditekan

        """

        # Save File
        saveAction = QAction(QIcon("Resource/save.png"), "Save Image", self)
        saveAction.triggered.connect(self.saveImage)
        self.toolbar.addAction(saveAction)

        # Tambah Gambar
        tambah_gambar = QAction(QIcon("Resource/tambah gambar.png"), "Tambah Gambar", self)
        tambah_gambar.triggered.connect(self.tambahGambar)
        self.toolbar.addAction(tambah_gambar)

        # Kontras
        enhanceAction = QAction(QIcon("Resource/kontras.png"), "Tingkatkan Kontras", self)
        enhanceAction.triggered.connect(self.meningkatkanKontras)
        self.toolbar.addAction(enhanceAction)

        # Ketajaman
        tingkatkan_ketajaman = QAction(QIcon("Resource/ketajaman.png"), "Tingkatkan Ketajaman", self)
        tingkatkan_ketajaman.triggered.connect(self.mempertajamGambar)
        self.toolbar.addAction(tingkatkan_ketajaman)

        # Reduce Noise 
        noise = QAction(QIcon("Resource/Reduce Noise.png"), "Kurangi Noise", self)
        noise.triggered.connect(self.reduceNoise)      
        self.toolbar.addAction(noise)

        # Grayscale
        ubah_ke_grayscale = QAction(QIcon("Resource/hitam putih.png"), "Grayscale", self)
        ubah_ke_grayscale.triggered.connect(self.ubahKeGrayscale)
        self.toolbar.addAction(ubah_ke_grayscale)

        # Negatif
        ubah_ke_negatif = QAction(QIcon("Resource/negatif.png"), "Negatif", self)
        ubah_ke_negatif.triggered.connect(self.ubahKeNegatif)
        self.toolbar.addAction(ubah_ke_negatif)

        # Dominasi Merah
        dominanceAction = QAction(QIcon("Resource/RGB dan BGR.png"), "Dominasi Merah", self)
        dominanceAction.triggered.connect(self.dominasiMerah)
        self.toolbar.addAction(dominanceAction)

        # Reset to Original
        resetAction = QAction(QIcon("Resource/kembali.png"), "Kembali Ke Awal", self)
        resetAction.triggered.connect(self.resetToOriginal)
        self.toolbar.addAction(resetAction)

        """
        Pengaturan Simple Kecerahan Dan Kontras

        > Membuat pengaturan dalam bentuk slider horizontal untuk kecerahan dengan nama brightnessSlider. 
        > Menetapkan nilai awal slider ke 0, nilai minimum ke -100, dan nilai maximal ke 100 dengan interval 10.
        > dengan demikian gambar bisa lebih mudah diatur kecerahannya. 

        > Membuat pengaturan dalam bentuk slider horizontal untuk kontras dengan nama contrastSlider. 
        > Menetapkan nilai awal slider ke 0, nilai minimum ke -100, dan nilai maximal ke 100 dengan interval 10.
        > dengan demikian gambar bisa lebih mudah diatur kontras warnanya.
        """

        # kecerahan Slider
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setValue(0)
        self.brightnessSlider.setTickPosition(QSlider.TicksBelow)
        self.brightnessSlider.setTickInterval(10)
        self.brightnessSlider.valueChanged.connect(self.updateImage)

        # kontras Slider
        self.contrastSlider = QSlider(Qt.Horizontal)
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setValue(0)
        self.contrastSlider.setTickPosition(QSlider.TicksBelow)
        self.contrastSlider.setTickInterval(10)
        self.contrastSlider.valueChanged.connect(self.updateImage)

        """
        Buat bagian untuk menampilkan gambar yang di inputkan
        jika gamba tesebut belum di input maka memunculkan tulisan "tambahkan gambar"
        """
        self.imageLabel = QLabel("Tambahkan Gambar")
        self.imageLabel.setAlignment(Qt.AlignCenter)

        """ 
        mengatur tampilan Layout seperti :
        selinde untuk Pengaturan Simple Kecerahan Dan Kontras
        jendela aplikasi
        judul aplikasi
        dll
        """  
        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(QLabel("Kecerahan"))
        sliderLayout.addWidget(self.brightnessSlider)
        sliderLayout.addWidget(QLabel("Kontras"))
        sliderLayout.addWidget(self.contrastSlider)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.imageLabel)
        mainLayout.addLayout(sliderLayout)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        self.setWindowTitle('Aplikasi Image Enhancement')
        self.show()

    def tambahGambar(self):
        """
        
        Fungsi Input Gambar
        
        > Membuka path folder dan menginput file yang diinginkan
        > kondisi apakah file tersebut yang di pilih
        > membaca dan menyalin gambar dari file tadi dan menampilkannya
        """

        filePath, _ = QFileDialog.getOpenFileName(self, 'Open file', './', "Image files (*.jpg *.jpeg *.png)")
        if filePath:
            self.image = cv2.imread(filePath)
            
            # Simpan gambar asli (salinan dari file)
            self.original_image = self.image.copy()  
            self.displayImage(self.image)

    def displayImage(self, image):
        """
        Menampilkan Gambar
        
        Mengonversi gambar dari format BGR (default OpenCV) ke RGB (untuk PyQt).
        Membuat QImage dari gambar, Mengonversi QImage ke QPixmap, dan nampilin pada Label.

        NB : 
        > kenapa format awalnya harus BGR? karna OpenCV secara default menggunakan format warna BGR
        > kenapa harus dirubah ke RGB? karna PyQt memang menggunakan format warna RGB
        """
        qformat = QImage.Format_RGB888
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qimage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        pixmap = QPixmap.fromImage(qimage)
        self.imageLabel.setPixmap(pixmap)

    def meningkatkanKontras(self):
        """
        Fungsi Meningkatkan Kontras
        
        > Meningkatkan kontras gambar dengan Mengambil model "tingkatkan_kontras" yang ada di image_utils.py
        > Menampilkan gambar yang telah diproses 
        """
        self.image = tingkatkan_kontras(self.image)
        self.displayImage(self.image)


    def mempertajamGambar(self):
        """
        Fungsi Mempertajam Gambar
        
        > Mempertajam Gambar dengan Mengambil model "pertajam_gambar" yang ada di image_utils.py
        > Menampilkan gambar yang telah diproses 
        """
        self.image = pertajam_gambar(self.image)
        self.displayImage(self.image)

    def reduceNoise(self):
        """
        Fungsi Pengurangan Noise

        > mengurangi Noise pada Gambar dengan Mengambil model "noise" yang ada di image_utils.py
        > Menampilkan gambar yang telah diproses 
        """
        self.image = noise(self.image)
        self.displayImage(self.image)

    def ubahKeGrayscale(self):
        """
        Fungsi Ubah Gambar Ke Abu - Abu
        
        > Mengonversi gambar ke grayscale pada kode "cv2.COLOR_BGR2GRAY"
        > Mengembalikan ke format BGR untuk kompatibilitas dengan QImage (agar gambar bisa ditampilkan) 
        """
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)  
        self.displayImage(self.image)

    def resetToOriginal(self):
        """
        Fungsi Referesh Gambar
        
        > Mengembalikan Gambar ke awal dengan cara memanggil gambar aslinya : self.original_image.copy()
        > Menampilkan gambar yang telah diproses
        """
        self.image = self.original_image.copy()
        self.displayImage(self.image)

    def ubahKeNegatif(self):
        """
        Fungsi Merubah Ke Negatif
        
        > Mengubah Gambar ke bentuk negatif dengan Mengambil model "bitwise_not" yang ada di OpenCV
        > Menampilkan gambar yang telah diproses
        """
        self.image = cv2.bitwise_not(self.image)
        self.displayImage(self.image)

    def dominasiMerah(self):
        """
        Fungsi Mendominasi Warna Merah
        
        >  Memisahkan saluran warna B (Blue), G (Green), dan R (Red)
        > r += 50: Menambah nilai pada R (warna merah)
        > b -= 50: Mengurangi nilai pada B (warna biru)
        > gabungin kembali saluran warnanya
        > Menampilkan gambar yang telah diproses
        """
        b, g, r = cv2.split(self.image)
        # Tambahin warna merah
        r += 50  
        # Kurangi warna biru
        b -= 50  
        self.image = cv2.merge([b, g, r])
        self.displayImage(self.image)

    def updateImage(self):
        """
        Fungsi Update Gambar Dari Slinder Kecerahan Dan Kontras
        
        fungsi ini berguna untuk Mengambil nilai kecerahan dan kontras dari pengaturan slider,
        dan memperbarui gambar sesuai dengan nilai tersebut.

        > Mengambil nilai kecerahan dan kontras dari slider.
        > Mengaplikasikan penyesuaian kecerahan dan kontras pada gambar dengan 
          model penyesuaiaan_kecerahan_dan_kontras pada image_utils.py
        > Menampilkan gambar yang telah diproses
        """
        brightness = self.brightnessSlider.value()
        contrast = self.contrastSlider.value()

        self.image = penyesuaiaan_kecerahan_dan_kontras(self.original_image, brightness, contrast)
        self.displayImage(self.image)

    def saveImage(self):
        """
        Fungsi Menyimpan Gambar
        
        > Buka dialog file buat pilih dimana lokasi file akan disimpan
        > membuat kondisi apakah file path valid, jika iya dilanjut menyimpan gambar ke file yang dipilih.
        """
        filePath, _ = QFileDialog.getSaveFileName(self, 'Save file', './', "Image files (*.jpg *.jpeg *.png)")
        if filePath:
            cv2.imwrite(filePath, self.image)
            self.original_image = self.image.copy()

if __name__ == '__main__':
    # Membuat instance aplikasi
    app = QApplication(sys.argv)
    # Membuat instance dari kelas Aplikasi_Image_Enhancement
    ex = Aplikasi_Image_Enhancement()
    # Menjalankan loop event utama aplikasi dan keluar ketika aplikasi ditutup
    sys.exit(app.exec_())
