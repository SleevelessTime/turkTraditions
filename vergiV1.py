import requests as req
import random
from bs4 import BeautifulSoup

def vergiBilgileriCekme(url):
    response = req.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        vergiBilgileri = {}
        tablo = soup.find('table', class_='wikitable')
        for satir in tablo.find_all('tr')[1:]:
            hücreler = satir.find_all('td')
            if len(hücreler) >= 2:
                vergiKodu = hücreler[0].text.strip()
                vergiAdi = hücreler[1].text.strip()
                vergiBilgileri[vergiKodu] = vergiAdi
        return vergiBilgileri
    else:
        print("Hata! İstek başarisiz oldu.")
        return None

def oyunBaslat(vergiBilgileri):
    dogruSayisi = 0
    yanlisSayisi = 0

    while True:
        vergiKodu = random.choice(list(vergiBilgileri.keys()))
        vergiAdi = vergiBilgileri[vergiKodu]

        print(f"Vergi adı: {vergiAdi}")
        kullaniciCevabi = input("Bu vergiye ait vergi kodu nedir? (Çıkmak için 'q' tuşlayın): ")

        if kullaniciCevabi.lower() == 'q':
            break

        if kullaniciCevabi == vergiKodu:
            print("Doğru!")
            dogruSayisi += 1
        else:
            print(f"Yanlış! Doğru cevap: {vergiKodu}")
            yanlisSayisi += 1

        print(f"Doğru Sayısı: {dogruSayisi}, Yanlış Sayısı: {yanlisSayisi}")

    print("Oyun bitti!")
    print(f"Toplam Doğru Sayısı: {dogruSayisi}, Toplam Yanlış Sayısı: {yanlisSayisi}")

url = 'https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27deki_vergiler_listesi'
vergiBilgileri = vergiBilgileriCekme(url)

if vergiBilgileri:
    print("Vergi bilgileri başarıyla çekildi. Oyun başlıyor!")
    oyunBaslat(vergiBilgileri)
else:
    print("Vergi bilgilerini çekme işlemi başarısız oldu.")
