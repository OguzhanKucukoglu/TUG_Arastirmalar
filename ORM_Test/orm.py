from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# 1. Şema Tanımlaması (Model Katmanı)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)

engine = create_engine('sqlite:///proje_orm.db')

# EKSİK OLAN SATIR BURASI: Modelleri analiz edip veritabanında tabloları oluşturur
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# 2. Yeni Kullanıcı Ekleme (INSERT)
yeni_kullanici = User(name="Ahmet", email="ahmet@mail.com", age=25)
session.add(yeni_kullanici)
session.commit()

# 3. Veri Okuma ve Ekrana Yazdırma (SELECT)
kullanicilar = session.query(User).filter(User.age > 20).all()

for kullanici in kullanicilar:
    print(f"{kullanici.name} - Yaş: {kullanici.age}")
