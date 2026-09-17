from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite kullanarak yerel bir veritabanı dosyası (kutuphane.db) oluşturuyoruz
engine = create_engine('sqlite:///kutuphane.db', echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()