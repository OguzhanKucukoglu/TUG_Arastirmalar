import sqlite3

# 1. Veritabanına Bağlan
conn = sqlite3.connect('proje.db')
cursor = conn.cursor()

# 2. Tabloyu Oluştur (Eğer yoksa)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        age INTEGER
    )
""")

# 3. Yeni Kullanıcı Ekleme (INSERT)
cursor.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)", 
    ("Ahmet", "ahmet@mail.com", 25)
)
conn.commit()

# 4. Veri Okuma (SELECT)
cursor.execute("SELECT * FROM users WHERE age > ?", (20,))
kullanicilar = cursor.fetchall()

# 5. Veriyi Ekrana Yazdırma
for kullanici in kullanicilar:
    print(f"{kullanici[1]} - Yaş: {kullanici[3]}")
