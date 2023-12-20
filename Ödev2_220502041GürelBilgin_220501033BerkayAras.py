class TIR:
    def __init__(self, gelis_zamani, plaka, ulke, ton_20_adet, ton_30_adet, yuk_miktari, maliyet):
        self.gelis_zamani = gelis_zamani
        self.plaka = plaka
        self.ulke = ulke
        self.ton_20_adet = ton_20_adet
        self.ton_30_adet = ton_30_adet
        self.yuk_miktari = yuk_miktari
        self.maliyet = maliyet

    def yuk_indir(self):
        if self.ton_20_adet > 0:
            print(
                f"{self.gelis_zamani} zamanında {self.plaka} plakalı TIR {self.ulke} ülkesine gitmek üzere {self.ton_20_adet} adet 20 tonluk yük indirdi")
            print(f"{self.plaka} yükü {self.ulke} gemisi gelene kadar istif alanında bekletiliyor")
            self.ton_20_adet = 0
        if self.ton_30_adet > 0:
            print(
                f"{self.gelis_zamani} zamanında {self.plaka} plakalı TIR {self.ulke} ülkesine gitmek üzere {self.ton_30_adet} adet 30 tonluk yük indirdi")
            print(f"{self.plaka} yükü {self.ulke} gemisi gelene kadar istif alanında bekletiliyor")
            self.ton_30_adet = 0


class Gemi:
    gemi_sayac = 0

    def __init__(self, gelis_zamani, ad, kapasite, gidecek_ulke):
        Gemi.gemi_sayac += 1
        self.gelis_zamani = gelis_zamani
        self.ad = ad
        self.kapasite = kapasite
        self.gidecek_ulke = gidecek_ulke
        self.numara = format(Gemi.gemi_sayac, '03d')

    def yuk_yukle(self, yuk_miktari):
        print(
            f"{self.gelis_zamani} zamanında {self.numara} numaralı gemiye {yuk_miktari} tonluk yük yüklendi. Gemi {self.gidecek_ulke} gitmek üzere bekliyor. Anlık yük: {self.kapasite} Harekete geçeceği yük: {self.kapasite + yuk_miktari}")
        self.kapasite += yuk_miktari


class Liman:
    def __init__(self):
        self.tir_listesi = []
        self.gemi_listesi = []
        self.istif_alani_1 = []
        self.istif_alani_2 = []
        self.vinc_sayisi = 20

    def tir_yukle(self, tir):
        self.tir_listesi.append(tir)

    def gemi_yukle(self, gemi):
        self.gemi_listesi.append(gemi)

    def yuk_indir(self):
        for tir in self.tir_listesi:
            tir.yuk_indir()

    def yuk_yukle(self):
        if self.vinc_sayisi > 0:
            gemi = sorted(self.gemi_listesi, key=lambda x: x.numara)[0]
            while gemi.kapasite < 95:
                if self.istif_alani_1:
                    yuk = self.istif_alani_1.pop(0)
                    gemi.yuk_yukle(yuk)
                    self.vinc_sayisi -= 1
                elif self.istif_alani_2:
                    yuk = self.istif_alani_2.pop(0)
                    gemi.yuk_yukle(yuk)
                    self.vinc_sayisi -= 1
                else:
                    break

    def kontrol(self):
        if len(self.istif_alani_1) >= 750 or len(self.istif_alani_2) >= 750:
            print("İstif alanı dolu!")
        else:
            print("İstif alanı boş.")

    def zaman_gecir(self):
        while True:
            self.yuk_indir()
            self.yuk_yukle()
            self.kontrol()
            # İstif alanları doluysa veya gemi bekliyorsa veya vinç işlemi yapılacaksa zamanı ilerlet
            if (len(self.istif_alani_1) >= 750 or len(
                    self.istif_alani_2) >= 750) or not self.gemi_listesi or self.vinc_sayisi < 20:
                continue
            else:
                break


# Liman oluşturma
liman = Liman()

# Olaylar.csv dosyasını okuma ve TIR nesnelerini oluşturma
with open('olaylar.csv', 'r', encoding='latin-1') as file:
    lines = file.readlines()

for line in lines[1:]:
    veri = line.strip().split(',')
    yeni_tir = TIR(int(veri[0]), veri[1], veri[2], int(veri[3]), int(veri[4]), int(veri[5]), int(veri[6]))
    liman.tir_yukle(yeni_tir)

# Gemiler.csv dosyasını okuma ve gemi nesnelerini oluşturma
with open('gemiler.csv', 'r', encoding='latin-1') as file:
    lines = file.readlines()

for line in lines[1:]:
    veri = line.strip().split(',')
    yeni_gemi = Gemi(int(veri[0]), veri[1], int(veri[2]), veri[3])
    liman.gemi_yukle(yeni_gemi)

# Simülasyonun çalıştırılması
liman.zaman_gecir()
