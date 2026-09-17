from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, validates
from database import Base  # database.py'den Base'i çekiyoruz

odunc_tablosu = Table('odunc_alma', Base.metadata,
    Column('uye_id', Integer, ForeignKey('uyeler.id')),
    Column('kitap_id', Integer, ForeignKey('kitaplar.id'))
)

class Yazar(Base):
    __tablename__ = 'yazarlar'
    id = Column(Integer, primary_key=True)
    ad_soyad = Column(String, nullable=False)
    kitaplar = relationship("Kitap", back_populates="yazar", cascade="all, delete-orphan")

    @validates('ad_soyad')
    def validate_ad_soyad(self, key, isim):
        if not isim or not isim.strip():
            raise ValueError("Yazar ismi boş bırakılamaz!")
        if len(isim) < 3:
            raise ValueError("Yazar ismi en az 3 karakter olmalıdır.")
        # Her kelimenin baş harfini otomatik büyüt (Örn: "mine urgan" -> "Mine Urgan")
        return isim.title()

class Kitap(Base):
    __tablename__ = 'kitaplar'
    id = Column(Integer, primary_key=True)
    baslik = Column(String, nullable=False)
    yazar_id = Column(Integer, ForeignKey('yazarlar.id'))
    yayin_yili = Column(Integer, nullable=True) 
    
    yazar = relationship("Yazar", back_populates="kitaplar")

class Uye(Base):
    __tablename__ = 'uyeler'
    id = Column(Integer, primary_key=True)
    isim = Column(String, nullable=False)
    alinan_kitaplar = relationship("Kitap", secondary=odunc_tablosu, backref="okuyan_uyeler")
