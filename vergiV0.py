import requests as req
from bs4 import BeautifulSoup
import sys

def vergiBilgileriCekme(url):
    """
    Belirtilen URL'den vergi bilgilerini çeker.
    Parametreler:
    url (str): Vergi bilgilerinin bulunduğu web sayfasının URL'si.
    Dönüş Değeri:
    dict veya None: Vergi bilgilerini içeren bir sözlük döner. Başarısızlık durumunda None döner.
    """
    response = req.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        vergi_bilgileri = {}
        tablo = soup.find('table', class_='wikitable')

        for satir in tablo.find_all('tr')[1:]:
            hücreler = satir.find_all('td')
            if len(hücreler) >= 2:
                vergi_kodu = hücreler[0].text.strip()
                vergi_adi = hücreler[1].text.strip()
                vergi_bilgileri[vergi_kodu] = vergi_adi
        return vergi_bilgileri
    else:
        print("Hata! İstek başarısız oldu.")
        return None

def vergi_bilgilerini_yazdir(vergi_bilgileri, sayi=None):
    """
    Çekilen vergi bilgilerini ekrana yazdırır.
    Parametreler:
    vergi_bilgileri (dict): Vergi bilgilerini içeren sözlük.
    sayi (int veya None): Yazdırılacak vergi sayısı. None ise tüm veriler yazdırılır.
    """
    if vergi_bilgileri:
        print("Çekilen vergi bilgileri:")
        if sayi is None:
            for vergi_kodu, vergi_adi in vergi_bilgileri.items():
                print("Vergi Kodu:", vergi_kodu, "- Vergi Adı:", vergi_adi)
        else:
            sayac = 0
            for vergi_kodu, vergi_adi in vergi_bilgileri.items():
                print("Vergi Kodu:", vergi_kodu, "- Vergi Adı:", vergi_adi)
                sayac += 1
                if sayac >= sayi:
                    break
    else:
        print("Vergi bilgilerini çekme işlemi başarısız oldu.")

def vergi_kodu_ara(vergi_bilgileri, vergi_kodu):
    """
    Belirtilen vergi kodunu arar ve ekrana yazdırır.
    Parametreler:
    vergi_bilgileri (dict): Vergi bilgilerini içeren sözlük.
    vergi_kodu (str): Aranacak vergi kodu.
    """
    if vergi_kodu in vergi_bilgileri:
        print("Vergi Kodu:", vergi_kodu, "- Vergi Adı:", vergi_bilgileri[vergi_kodu])
    else:
        print("Belirtilen vergi kodu bulunamadı.")

if __name__ == "__main__":
    url = 'https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27deki_vergiler_listesi'
    vergi_bilgileri = vergiBilgileriCekme(url)

    if len(sys.argv) == 1:
        vergi_bilgilerini_yazdir(vergi_bilgileri)
    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            vergi_bilgilerini_yazdir(vergi_bilgileri, int(sys.argv[1]))
        else:
            vergi_kodu_ara(vergi_bilgileri, sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'ara':
            vergi_kodu_ara(vergi_bilgileri, sys.argv[2])
        elif sys.argv[1] == 'yazdir' and sys.argv[2].isdigit():
            vergi_bilgilerini_yazdir(vergi_bilgileri, int(sys.argv[2]))
        else:
            print("Hatalı kullanım. Lütfen doğru parametreleri girin.")
    else:
        print("Kullanım: python vergiV0.py [vergi_kodu] veya python vergiV0.py [sayi] veya python vergiV0.py ara [vergi_kodu] veya python vergiV0.py yazdir [sayi]")
