import cv2
import numpy as np

def tingkatkan_kontras(image):
    """ 
    Meningkatkan kontras dengan CLAHE

    CLAHE (Contrast Limited Adaptive Histogram Equalization) adalah teknik peningkatan kontras gambar 
    yang dipakai untuk detail di area yang gelap atau terang.

    poin penting : 
    clipLimit=2.0        ->  nilai ambang batas untuk pembatasan kontras
    tileGridSize=(8, 8)  -> nentuin seberapa besar area yang diterapkan histogram equalization secara adaptif

    > ubah gambar dari BGR ke LAB
    > bentuk LAB punya karakteristik yang memisahkan informasi warna dan informasi kecerahan
    > ubah kembali ke bentuk BGR setelah selesai diproses
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = clahe.apply(l)
    enhanced_img = cv2.merge((l, a, b))
    return cv2.cvtColor(enhanced_img, cv2.COLOR_LAB2BGR)

def pertajam_gambar(image):
    """
    Peningkatan ketajaman dengan kernel sharpening

    > kernel convolution matrix untuk mempertajamkan pixel yang akan di filter dengan cv2.filter2D
    > Nilai di tengah "5" ningkatin nilai pixel pusat, nilai -1 mengurangi nilai pixel sekitarnya

    """
    kernel = np.array([[0, -1, 0], 
                       [-1, 5,-1], 
                       [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

def noise(image):
    # Reduksi noise dengan metode Bilateral Filter
    return cv2.bilateralFilter(image, 9, 75, 75)

def penyesuaiaan_kecerahan_dan_kontras(image, brightness=0, contrast=0):
    """
    Penyesuaian kecerahan dan kontras

    > alpha=1 + contrast/127.0  -> mengatur kontras
    > beta=brightness           -> mengatur kecerahan
    """
    img = cv2.convertScaleAbs(image, alpha=1 + contrast/127.0, beta=brightness)
    return img
