from database import engine, SessionLocal, Base
from models import Uye, Yazar, Kitap
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
import time

# Tabloları oluştur ve oturumu başlat
Base.metadata.create_all(bind=engine)
session = SessionLocal()

try:
    # 1. TEMEL VERİ EKLEME (Create)
    mevcut_yazar = session.query(Yazar).filter_by(ad_soyad="Ahmet Hamdi Tanpınar").first()

    if not mevcut_yazar:
        try:
            yeni_yazar = Yazar(ad_soyad="Ahmet Hamdi Tanpınar")
            kitap1 = Kitap(baslik="Saatleri Ayarlama Enstitüsü", yazar=yeni_yazar)
            kitap2 = Kitap(baslik="Huzur", yazar=yeni_yazar)
            
            session.add(yeni_yazar)
            session.add_all([kitap1, kitap2])
            
            # Veritabanına yaz
            session.commit()
            print("Yazar ve kitapları başarıyla eklendi!")
        except Exception as e:
            session.rollback() # Hata anında işlemleri geri al
            print(f"Bölüm 1'de kayıt sırasında hata oluştu: {e}")

    # 2. İSTATİSTİKLER (Aggregations & Group By)
    toplam_kitap = session.query(func.count(Kitap.id)).scalar()
    toplam_uye = session.query(func.count(Uye.id)).scalar()
    print(f"Kütüphane İstatistiği: {toplam_kitap} Kitap, {toplam_uye} Üye")

    yazar_istatistikleri = session.query(
        Yazar.ad_soyad, 
        func.count(Kitap.id).label('kitap_sayisi')
    ).join(Kitap).group_by(Yazar.id).all()

    print("\n--- Yazarların Kitap Sayıları ---")
    for yazar_adi, sayi in yazar_istatistikleri:
        print(f"{yazar_adi}: {sayi} kitap")

    en_aktif_uyeler = session.query(
        Uye.isim,
        func.count(Kitap.id).label('okunan_kitap')
    ).join(Uye.alinan_kitaplar).group_by(Uye.id).order_by(func.count(Kitap.id).desc()).all()

    print("\n--- En Çok Okuyan Üyeler ---")
    for uye_adi, okuma_sayisi in en_aktif_uyeler:
        print(f"{uye_adi}: {okuma_sayisi} kitap okumuş")

    # 3. EAGER LOADING (N+1 Çözümü)
    print("\n--- Eager Loading ile Hızlı Veri Çekimi ---")

    yazarlar_eager = session.execute(
        select(Yazar).options(joinedload(Yazar.kitaplar))
    ).unique().scalars().all()

    for yazar in yazarlar_eager:
        print(f"Yazar: {yazar.ad_soyad}, Kitap Sayısı: {len(yazar.kitaplar)}")

    # 4. BULK INSERT (Toplu Ekleme)
    print("\n--- Yeni Yazar ve Bulk Insert İşlemi ---")

    aranan_yazar = "Mine Urgan"
    hedef_yazar = session.query(Yazar).filter_by(ad_soyad=aranan_yazar).first()

    try:
        if not hedef_yazar:
            print(f"'{aranan_yazar}' bulunamadı. Yeni yazar olarak ekleniyor...")
            hedef_yazar = Yazar(ad_soyad=aranan_yazar)
            session.add(hedef_yazar)
            session.commit()

        # EĞER YAZARIN HİÇ KİTABI YOKSA EKLEME YAP
        if len(hedef_yazar.kitaplar) == 0:
            toplu_kitap_listesi = []
            for i in range(1, 1001):
                yeni_kitap = Kitap(
                    baslik=f"{aranan_yazar} - Toplu Eserler Cilt {i}", 
                    yazar_id=hedef_yazar.id, 
                    yayin_yili=2026
                )
                toplu_kitap_listesi.append(yeni_kitap)
                
            print(f"1000 kitap hafızada oluşturuldu, {aranan_yazar} adına veritabanına yazılıyor...")
            baslangic = time.time()
            
            session.bulk_save_objects(toplu_kitap_listesi)
            session.commit() # Toplu eklemeyi onayla
            
            bitis = time.time()
            print(f"İşlem tamamlandı! Geçen süre: {bitis - baslangic:.4f} saniye")
        else:
            print(f"{aranan_yazar} adına zaten {len(hedef_yazar.kitaplar)} kitap var, tekrar eklenmedi.")

    except Exception as e:
        session.rollback() # Toplu işlem sırasında hata olursa her şeyi geri al
        print(f"Toplu ekleme sırasında hata oluştu, işlem iptal edildi: {e}")

finally:
    # Kodun çalışması bittikten sonra veritabanı bağlantısını güvenle kapat
    session.close()